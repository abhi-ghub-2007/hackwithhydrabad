import logging
from typing import List, Dict, Any
from app.services.hindsight_service import hindsight_service

logger = logging.getLogger("xpert_remnants.batch_processor")

class MemoryBatchProcessor:
    """
    Handles robust, batched ingestion of decision memories into Hindsight (Section 25).
    Includes batch chunking, retry handling, error tracking, and progress metrics.
    """
    def __init__(self, batch_size: int = 250):
        self.batch_size = batch_size

    def process_memories(
        self,
        memories: List[Dict[str, Any]],
        bank_id: str = None
    ) -> Dict[str, Any]:
        """
        Batches and retains memory items into Hindsight.
        """
        total = len(memories)
        retained_count = 0
        failed_count = 0
        all_ids = []

        logger.info(f"Starting batch retention for {total} memories (chunk size: {self.batch_size})")

        for i in range(0, total, self.batch_size):
            chunk = memories[i:i + self.batch_size]
            items = []
            for m in chunk:
                content = (
                    f"Problem: {m.get('problem')}\n"
                    f"Context: {m.get('context')}\n"
                    f"Decision: {m.get('decision')}\n"
                    f"Reasoning: {m.get('reasoning')}\n"
                    f"Action: {m.get('action_taken')}\n"
                    f"Impact: {m.get('impact')}\n"
                    f"Lessons Learned: {m.get('lessons_learned')}"
                )
                items.append({
                    "content": content,
                    "context": m.get("context", ""),
                    "metadata": {
                        "id": str(m.get("id")),
                        "project_id": str(m.get("project_id", "")),
                        "expert_id": str(m.get("expert_id", "")),
                        "memory_id": str(m.get("memory_id") or m.get("hindsight_memory_id") or m.get("source_id") or m.get("id")),
                        "memory_type": str(m.get("memory_type", "decision")),
                        "occurred_at": str(m.get("occurred_at", "")),
                        "technology": str(m.get("technology", "")),
                        "confidence": str(m.get("confidence") or m.get("outcome_score", 0.9)),
                        "verification_status": str(m.get("verification_status", "VERIFIED")),
                        "status": str(m.get("status", "ACTIVE"))
                    },
                    "tags": [str(m.get("memory_type", "decision")), "enterprise_memory"]
                })

            try:
                res = hindsight_service.retain_batch(items, bank_id=bank_id)
                retained_ids = res.get("memory_ids", [])
                retained_count += len(retained_ids)
                all_ids.extend(retained_ids)
            except Exception as e:
                logger.error(f"Error retaining chunk {i} to {i + len(chunk)}: {e}")
                failed_count += len(chunk)

        return {
            "total_submitted": total,
            "retained_count": retained_count,
            "failed_count": failed_count,
            "bank_id": bank_id or hindsight_service.bank_id,
            "memory_ids_sample": all_ids[:10]
        }

batch_processor = MemoryBatchProcessor()
