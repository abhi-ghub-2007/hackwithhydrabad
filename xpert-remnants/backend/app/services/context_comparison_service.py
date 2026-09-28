import re
from typing import Dict, Any, List, Tuple

class ContextComparisonService:
    """
    Compares current situational context from the user query with historical
    experiences stored in organizational memory (Section 29 & 30).
    Identifies 'same', 'different', and 'unknown' across critical operational dimensions.
    """

    @staticmethod
    def extract_context(query: str, hint: str = None) -> Dict[str, Any]:
        """
        Extracts operational entities from the current user query.
        """
        full_text = f"{query} {hint or ''}".lower()
        extracted = {
            "service": "General Backend Service",
            "environment": "production" if "prod" in full_text or "live" in full_text else "unknown",
            "symptom": "unknown",
            "trigger": "unknown",
            "technology": "unknown",
            "scale": "unknown"
        }

        # Service detection
        if "payment" in full_text:
            extracted["service"] = "Payment API / Gateway"
        elif "gateway" in full_text or "routing" in full_text:
            extracted["service"] = "API Gateway"
        elif "auth" in full_text or "login" in full_text or "token" in full_text:
            extracted["service"] = "Customer Identity Platform"
        elif "billing" in full_text or "ledger" in full_text:
            extracted["service"] = "Billing & Ledger Platform"
        elif "kafka" in full_text or "stream" in full_text:
            extracted["service"] = "Event Streaming Pipeline"

        # Symptom detection
        if "latency" in full_text or "slow" in full_text or "spike" in full_text:
            extracted["symptom"] = "Latency degradation / P99 spike"
        elif "timeout" in full_text or "504" in full_text or "502" in full_text:
            extracted["symptom"] = "Connection timeouts / Gateway errors"
        elif "oom" in full_text or "memory" in full_text or "crash" in full_text:
            extracted["symptom"] = "Out of memory crash / saturation"
        elif "lock" in full_text or "deadlock" in full_text:
            extracted["symptom"] = "Database table locking / contention"

        # Trigger detection
        if "traffic" in full_text or "spike" in full_text or "sale" in full_text or "surge" in full_text:
            extracted["trigger"] = "High-concurrency traffic surge"
        elif "deploy" in full_text or "release" in full_text or "migration" in full_text:
            extracted["trigger"] = "Recent deployment or schema migration"

        # Technology detection
        if "postgres" in full_text or "db" in full_text or "database" in full_text or "pool" in full_text:
            extracted["technology"] = "PostgreSQL"
        elif "redis" in full_text or "cache" in full_text:
            extracted["technology"] = "Redis"
        elif "kafka" in full_text:
            extracted["technology"] = "Kafka"
        elif "k8s" in full_text or "kubernetes" in full_text or "pod" in full_text:
            extracted["technology"] = "Kubernetes"

        return extracted

    @classmethod
    def compare_contexts(
        cls,
        current_ctx: Dict[str, Any],
        historical_mem: Dict[str, Any]
    ) -> Tuple[List[str], List[str]]:
        """
        Compares current operational context against a historical memory record.
        Returns:
            why_relevant: List of reasons why this past experience applies.
            context_differences: Material differences between current situation and historical case.
        """
        why_relevant = []
        context_differences = []

        hist_content = (historical_mem.get("problem", "") + " " +
                        historical_mem.get("context", "") + " " +
                        historical_mem.get("decision", "")).lower()

        # Check Service relevance
        if "payment" in current_ctx.get("service", "").lower() and "payment" in hist_content:
            why_relevant.append("Same critical domain: Payment Gateway checkout authorization path.")
        elif current_ctx.get("service") != "General Backend Service" and current_ctx.get("service", "").lower() in hist_content:
            why_relevant.append(f"Matching service domain: {current_ctx.get('service')}.")

        # Check Symptom
        if "latency" in current_ctx.get("symptom", "").lower() and ("latency" in hist_content or "spike" in hist_content):
            why_relevant.append("Identical performance symptom: Latency degradation during active customer requests.")

        # Check Trigger
        if "traffic" in current_ctx.get("trigger", "").lower() and ("traffic" in hist_content or "sale" in hist_content or "surge" in hist_content):
            why_relevant.append("Similar external load condition: High-throughput surge / peak traffic event.")

        # Check Technology
        if current_ctx.get("technology") == "PostgreSQL" and ("postgres" in hist_content or "pool" in hist_content or "database" in hist_content):
            why_relevant.append("Shared infrastructure layer: PostgreSQL connection pooling & database session allocation.")

        # Detect Material Context Differences
        if "max_connections" in hist_content:
            context_differences.append(
                "Database max_connections headroom must be validated: Historical resolution succeeded because database CPU was below 30% and connection ceiling had not been breached."
            )

        if "pgbouncer" in hist_content or "billing" in hist_content:
            context_differences.append(
                "Topology difference: If transaction-level pooling (PgBouncer) is already present, local instance pool expansion will have no effect."
            )
        else:
            context_differences.append(
                "Current service scale and database replica configuration may differ from historical baseline of 8 payment service pods."
            )

        if not why_relevant:
            why_relevant.append("Historical case shares comparable infrastructure scalability patterns.")

        return why_relevant, context_differences

context_comparison_service = ContextComparisonService()
