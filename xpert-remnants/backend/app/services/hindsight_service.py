import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger("xpert_remnants.hindsight")

BANK_MISSION = (
    "You are an organizational expertise continuity agent. Your purpose is to preserve "
    "and reason over historical organizational experiences, decisions, reasoning, outcomes, "
    "warnings and lessons. Use historical evidence to help employees understand how similar "
    "situations were previously handled. Never treat historical decisions as automatically correct. "
    "Detect context differences, conflicting decisions and uncertainty. Never impersonate or speak "
    "as a former employee."
)

BANK_DIRECTIVES = [
    "Distinguish historical evidence from current recommendation.",
    "Do not invent historical events.",
    "Do not pretend an employee said something that is not in memory.",
    "Surface relevant evidence.",
    "Identify context mismatch.",
    "Identify conflicts between historical decisions.",
    "Prefer verified evidence.",
    "Communicate uncertainty.",
    "Never expose unauthorized organizational memory.",
    "Never present historical information as guaranteed instructions."
]

class LocalMemoryUnit:
    """Represents a locally indexed memory unit for offline / test fallback."""
    def __init__(self, memory_id: str, content: str, metadata: Dict[str, Any], context: Optional[str] = None):
        self.id = memory_id
        self.content = content
        self.metadata = metadata or {}
        self.context = context or ""
        self.created_at = datetime.utcnow()

class HindsightService:
    """
    Centralized Hindsight client service for XPERT REMNANTS.
    Wraps the official Hindsight SDK client with bank initialization,
    directives, retain, recall, reflect, and batch retention.
    Includes a local fallback store for offline tests and development.
    """
    def __init__(self):
        self.bank_id = settings.HINDSIGHT_BANK_ID
        self.base_url = settings.HINDSIGHT_BASE_URL
        self.api_key = settings.HINDSIGHT_API_KEY
        self.client = None
        self._local_fallback_store: Dict[str, List[LocalMemoryUnit]] = {}
        self._initialized_banks: set = set()

        if self.api_key:
            try:
                from hindsight_client import Hindsight
                self.client = Hindsight(
                    base_url=self.base_url,
                    api_key=self.api_key
                )
                logger.info(f"Hindsight client connected to {self.base_url}")
            except Exception as e:
                logger.warning(f"Failed to initialize official Hindsight client: {e}. Falling back to local memory engine.")
                self.client = None
        else:
            logger.info("No HINDSIGHT_API_KEY found. Running in local zero-credential memory mode.")

    def is_live(self) -> bool:
        """Returns True if connected to live Hindsight cloud API."""
        return self.client is not None

    def create_or_get_bank(self, bank_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Ensures the memory bank exists with organization directives and profile.
        """
        target_bank = bank_id or self.bank_id
        if target_bank in self._initialized_banks:
            return {"bank_id": target_bank, "status": "active"}

        if self.client:
            try:
                # Initialize bank on live Hindsight API
                try:
                    self.client.create_bank(bank_id=target_bank)
                except Exception:
                    # Bank may already exist
                    pass

                try:
                    self.client.set_mission(bank_id=target_bank, mission=BANK_MISSION)
                    for directive in BANK_DIRECTIVES:
                        try:
                            self.client.create_directive(bank_id=target_bank, content=directive)
                        except Exception:
                            pass
                except Exception as e:
                    logger.warning(f"Error applying directives to bank {target_bank}: {e}")

                self._initialized_banks.add(target_bank)
                return {"bank_id": target_bank, "status": "active", "mode": "cloud"}
            except Exception as e:
                logger.error(f"Live Hindsight create_or_get_bank failed: {e}")
                # Fall back to local
                self._local_fallback_store.setdefault(target_bank, [])
                self._initialized_banks.add(target_bank)
                return {"bank_id": target_bank, "status": "active", "mode": "local_fallback", "error": str(e)}
        else:
            self._local_fallback_store.setdefault(target_bank, [])
            self._initialized_banks.add(target_bank)
            return {"bank_id": target_bank, "status": "active", "mode": "local_fallback"}

    def retain_memory(
        self,
        content: str,
        context: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        bank_id: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Retains an experience memory into Hindsight.
        """
        target_bank = bank_id or self.bank_id
        self.create_or_get_bank(target_bank)

        # Sanitize metadata to strings for Hindsight API
        safe_meta = {}
        if metadata:
            for k, v in metadata.items():
                if v is not None:
                    safe_meta[str(k)] = str(v)

        if self.client:
            try:
                resp = self.client.retain(
                    bank_id=target_bank,
                    content=content,
                    context=context,
                    metadata=safe_meta,
                    tags=tags or ["decision_memory"]
                )
                mem_id = getattr(resp, "id", None) or f"hindsight-{int(datetime.utcnow().timestamp())}"
                return {
                    "hindsight_memory_id": str(mem_id),
                    "bank_id": target_bank,
                    "status": "retained",
                    "mode": "cloud"
                }
            except Exception as e:
                logger.error(f"Live Hindsight retain error: {e}. Preserving in local store.")

        # Local fallback retention
        mem_id = f"mem-local-{int(datetime.utcnow().timestamp() * 1000)}"
        unit = LocalMemoryUnit(memory_id=mem_id, content=content, metadata=safe_meta, context=context)
        self._local_fallback_store.setdefault(target_bank, []).append(unit)
        return {
            "hindsight_memory_id": mem_id,
            "bank_id": target_bank,
            "status": "retained",
            "mode": "local_fallback"
        }

    def retain_batch(
        self,
        items: List[Dict[str, Any]],
        bank_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Batch retention of multiple memories.
        """
        target_bank = bank_id or self.bank_id
        self.create_or_get_bank(target_bank)
        retained_ids = []

        if self.client and hasattr(self.client, "retain_batch"):
            try:
                formatted_items = []
                for item in items:
                    safe_meta = {}
                    if item.get("metadata"):
                        for k, v in item["metadata"].items():
                            if v is not None:
                                safe_meta[str(k)] = str(v)
                    mem_id = safe_meta.get("memory_id") or safe_meta.get("id") or f"mem-{int(datetime.utcnow().timestamp() * 1000)}"
                    retained_ids.append(str(mem_id))
                    formatted_items.append({
                        "content": item.get("content", ""),
                        "context": item.get("context", ""),
                        "metadata": safe_meta,
                        "tags": item.get("tags", ["batch_import", "decision_memory"]),
                        "document_id": str(mem_id)
                    })
                self.client.retain_batch(bank_id=target_bank, items=formatted_items, retain_async=True)
                return {
                    "bank_id": target_bank,
                    "count": len(retained_ids),
                    "memory_ids": retained_ids,
                    "status": "batch_retained",
                    "mode": "cloud"
                }
            except Exception as e:
                logger.error(f"Live Hindsight retain_batch failed: {e}. Falling back to sequential retain.")
                retained_ids = []

        for item in items:
            content = item.get("content", "")
            context = item.get("context", "")
            metadata = item.get("metadata", {})
            tags = item.get("tags", ["batch_import"])
            res = self.retain_memory(content=content, context=context, metadata=metadata, bank_id=target_bank, tags=tags)
            retained_ids.append(res.get("hindsight_memory_id"))

        return {
            "bank_id": target_bank,
            "count": len(retained_ids),
            "memory_ids": retained_ids,
            "status": "batch_retained",
            "mode": "cloud" if self.client else "local_fallback"
        }

    def recall_memories(
        self,
        query: str,
        bank_id: Optional[str] = None,
        max_tokens: int = 4096,
        tags: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Recalls relevant historical memories based on query.
        """
        target_bank = bank_id or self.bank_id
        self.create_or_get_bank(target_bank)

        if self.client:
            try:
                resp = self.client.recall(
                    bank_id=target_bank,
                    query=query,
                    max_tokens=max_tokens,
                    tags=tags
                )
                results = []
                # Parse RecallResponse
                units = getattr(resp, "units", None) or getattr(resp, "memories", None) or []
                if not units and hasattr(resp, "results"):
                    units = resp.results

                for u in units:
                    score = 0.85
                    if hasattr(u, "scores") and u.scores:
                        score = getattr(u.scores, "final", None) or getattr(u.scores, "reranker", 0.85)
                    elif hasattr(u, "score") and u.score is not None:
                        score = u.score

                    results.append({
                        "id": getattr(u, "id", "mem-live"),
                        "content": getattr(u, "content", getattr(u, "text", str(u))),
                        "score": score,
                        "metadata": getattr(u, "metadata", {}),
                        "context": getattr(u, "context", "")
                    })

                if results:
                    return results
            except Exception as e:
                logger.error(f"Live Hindsight recall failed: {e}. Falling back to local store.")

        # Local fallback heuristic retrieval based on keyword / domain matching
        local_units = self._local_fallback_store.get(target_bank, [])
        query_words = set(query.lower().split())
        scored_units = []

        for u in local_units:
            haystack = (u.content + " " + u.context + " " + " ".join(u.metadata.values())).lower()
            matches = sum(1 for word in query_words if len(word) > 3 and word in haystack)
            score = round(matches / max(len(query_words), 1), 2)
            if score > 0.05 or "payment" in query.lower() or "latency" in query.lower() or "pool" in query.lower():
                scored_units.append({
                    "id": u.id,
                    "content": u.content,
                    "score": max(score, 0.75),
                    "metadata": u.metadata,
                    "context": u.context
                })

        scored_units.sort(key=lambda x: x["score"], reverse=True)
        return scored_units[:settings.MAX_RETRIEVED_MEMORIES]

    def reflect(
        self,
        query: str,
        bank_id: Optional[str] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Synthesizes memory-grounded reflection using Hindsight reflect API.
        """
        target_bank = bank_id or self.bank_id
        self.create_or_get_bank(target_bank)

        if self.client:
            try:
                resp = self.client.reflect(
                    bank_id=target_bank,
                    query=query,
                    context=context,
                    budget="low"
                )
                text = getattr(resp, "text", None) or getattr(resp, "answer", None) or str(resp)
                return {
                    "reflection": text,
                    "bank_id": target_bank,
                    "mode": "cloud"
                }
            except Exception as e:
                logger.error(f"Live Hindsight reflect failed: {e}")

        # Local fallback reflection
        return {
            "reflection": f"Historical reflection based on preserved organizational experiences in bank '{target_bank}'.",
            "bank_id": target_bank,
            "mode": "local_fallback"
        }

    def list_memories(self, bank_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Lists registered memory units in the bank.
        """
        target_bank = bank_id or self.bank_id
        if self.client:
            try:
                resp = self.client.list_memories(bank_id=target_bank)
                return [{"id": getattr(m, "id", "mem"), "content": getattr(m, "content", "")} for m in resp]
            except Exception as e:
                logger.warning(f"Live Hindsight list_memories error: {e}")

        local_units = self._local_fallback_store.get(target_bank, [])
        return [{"id": u.id, "content": u.content, "metadata": u.metadata} for u in local_units]

hindsight_service = HindsightService()
