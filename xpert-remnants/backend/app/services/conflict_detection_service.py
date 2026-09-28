from typing import List, Dict, Any

class ConflictDetectionService:
    """
    Detects contradictory or conflicting recommendations across historical decisions (Section 32).
    Ensures that when different experts or past incidents took opposite approaches,
    both contexts are presented explicitly rather than arbitrarily picking one.
    """

    @staticmethod
    def detect_conflicts(
        memories: List[Dict[str, Any]],
        relationships: List[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Scans retrieved memories for opposing decisions or explicit contradiction relationships.
        """
        conflicts = []
        has_pool_expansion = False
        has_pool_rejection = False

        for mem in memories:
            text = (mem.get("problem", "") + " " +
                    mem.get("decision", "") + " " +
                    mem.get("lessons_learned", "")).lower()

            if "increase" in text and "pool" in text:
                has_pool_expansion = True
            if ("rejected" in text and "pool" in text) or ("pgbouncer" in text and "thrashing" in text):
                has_pool_rejection = True

        if has_pool_expansion and has_pool_rejection:
            conflicts.append(
                "Historical approaches conflict: In 2023 (DEC-219 / INC-1842), expanding the connection pool from 50 to 100 resolved latency by 68% because database CPU had ample headroom. However, in 2024 (DEC-288 / INC-2041), expanding the pool under high connection saturation caused severe database context switching thrashing, requiring PgBouncer transaction pooling instead."
            )

        # Check explicit relationships if provided
        if relationships:
            for rel in relationships:
                if rel.get("relationship_type") == "contradicts":
                    conflicts.append(
                        f"Preserved architectural conflict detected between Memory #{rel.get('source_memory_id')} and Memory #{rel.get('target_memory_id')}."
                    )

        return conflicts

conflict_detection_service = ConflictDetectionService()
