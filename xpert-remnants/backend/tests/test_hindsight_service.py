from app.services.hindsight_service import hindsight_service
from app.services.batch_processor import batch_processor
from app.core.config import settings

def test_hindsight_bank_creation():
    res = hindsight_service.create_or_get_bank(settings.HINDSIGHT_BANK_ID)
    assert res["status"] == "active"
    assert res["bank_id"] == settings.HINDSIGHT_BANK_ID

def test_hindsight_retain_and_recall():
    retain_res = hindsight_service.retain_memory(
        content="Incident INC-999: Kafka consumer rebalance lag caused 10-minute message delay.",
        context="Event Streaming in Payment Platform",
        metadata={"service": "kafka", "incident_id": "INC-999"},
        tags=["kafka", "incident"]
    )
    assert retain_res["status"] == "retained"
    assert "hindsight_memory_id" in retain_res

    # Recall
    recalled = hindsight_service.recall_memories("Kafka message delay rebalance")
    assert isinstance(recalled, list)
    assert len(recalled) > 0

def test_hindsight_reflect():
    reflect_res = hindsight_service.reflect("How did we previously resolve Kafka rebalance latency?")
    assert "reflection" in reflect_res
    assert reflect_res["bank_id"] == settings.HINDSIGHT_BANK_ID

def test_batch_processor():
    sample_memories = [
        {
            "id": 901,
            "problem": "Batch test problem 1",
            "context": "Context 1",
            "decision": "Decision 1",
            "reasoning": "Reasoning 1",
            "action_taken": "Action 1",
            "impact": "Impact 1",
            "lessons_learned": "Lesson 1",
            "memory_type": "decision",
            "status": "ACTIVE"
        },
        {
            "id": 902,
            "problem": "Batch test problem 2",
            "context": "Context 2",
            "decision": "Decision 2",
            "reasoning": "Reasoning 2",
            "action_taken": "Action 2",
            "impact": "Impact 2",
            "lessons_learned": "Lesson 2",
            "memory_type": "lesson",
            "status": "ACTIVE"
        }
    ]
    res = batch_processor.process_memories(sample_memories)
    assert res["total_submitted"] == 2
    assert res["retained_count"] == 2
    assert res["failed_count"] == 0
