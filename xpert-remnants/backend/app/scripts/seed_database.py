import random
import datetime
from sqlalchemy.orm import Session
from app.db.database import Base, engine, SessionLocal
from app.models.models import (
    Organization, User, Person, Expert, Project, Technology,
    DecisionMemory, Decision, Incident, Meeting, Document, KnowledgeRisk, AuditLog, MemoryRelationship,
    Lesson, Feedback
)
from app.scripts.dataset_config import PROFILES, CURRENT_CONFIG

INDIAN_LOCATIONS = ["Pune Hub", "Bengaluru", "Mumbai", "Hyderabad Hub", "Chennai", "Delhi NCR", "Kochi", "Ahmedabad"]
DEPARTMENTS = ["Payments & Core Ledger", "Platform Architecture", "Cloud Infrastructure", "Core Identity", "Data Engineering", "Cybersecurity"]

ENTERPRISE_PROJECTS = [
    {
        "name": "Payment Platform Modernization",
        "domain": "Payments",
        "description": "High-throughput payment gateway processing 5,000 TPS across APAC checkout channels.",
        "business_context": "Core checkout processing authorizing credit/debit, UPI, netbanking, and tokenized cards.",
        "criticality": "CRITICAL",
    },
    {
        "name": "API Gateway & Service Mesh",
        "domain": "Platform",
        "description": "Enterprise API routing, rate limiting, and mTLS security mesh connecting 140+ internal services.",
        "business_context": "Single ingress entry point for all mobile & web client traffic across enterprise products.",
        "criticality": "HIGH",
    },
    {
        "name": "Fraud Detection Platform",
        "domain": "Security & Risk",
        "description": "Real-time behavioral ML risk scoring evaluating card transactions within 40ms SLA.",
        "business_context": "Stops account takeovers and fraudulent transactions before banking ledger settlement.",
        "criticality": "CRITICAL",
    },
    {
        "name": "Customer Identity Platform",
        "domain": "Identity",
        "description": "Centralized OAuth2 / OIDC authentication service supporting 45M enterprise accounts.",
        "business_context": "Federated identity, single sign-on, and role-based access control across corporate ecosystem.",
        "criticality": "HIGH",
    },
    {
        "name": "Observability & Telemetry Platform",
        "domain": "Platform",
        "description": "Unified OpenTelemetry, Prometheus, and Grafana tracing platform processing 250M spans/day.",
        "business_context": "Central monitoring and automated incident detection across all production workloads.",
        "criticality": "HIGH",
    },
    {
        "name": "Billing & Ledger Platform",
        "domain": "Payments",
        "description": "Double-entry financial accounting ledger maintaining ACID transaction consistency.",
        "business_context": "Handles merchant settlements, invoicing, tax calculations, and compliance audits.",
        "criticality": "CRITICAL",
    },
    {
        "name": "Data Warehouse Modernization",
        "domain": "Data",
        "description": "Real-time streaming pipeline replicating OLTP PostgreSQL data to analytical data lake.",
        "business_context": "Powers daily business intelligence, risk analytics, and executive KPI reporting.",
        "criticality": "MEDIUM",
    },
    {
        "name": "Developer Platform & CI/CD",
        "domain": "Platform",
        "description": "Internal developer portal, automated Kubernetes rollout pipelines, and preview environments.",
        "business_context": "Accelerates time-to-market for 250+ software engineers across 12 product squads.",
        "criticality": "MEDIUM",
    },
]

TECHS = [
    ("PostgreSQL", "Database", "Relational Database Engine v15 with connection pooler"),
    ("Redis", "In-Memory Cache", "Cluster Caching System v7 with volatile-lru"),
    ("Kafka", "Event Streaming", "Distributed Event Streaming v3.4 for payment logs"),
    ("Kubernetes", "Container Orchestration", "Microservices Cluster Management with HPA"),
    ("FastAPI", "Web Framework", "Python High-Performance Asynchronous REST API"),
    ("React", "Frontend", "User Interface Library v19"),
    ("Docker", "Containerization", "Production Distroless Container Images"),
    ("Prometheus", "Monitoring", "Time-Series Metrics Collector and Alertmanager"),
    ("Grafana", "Observability", "Dashboard Metrics Visualizer & SLO Dashboards"),
    ("OpenTelemetry", "Distributed Tracing", "APM Tracing Framework with Jaeger collector"),
    ("PgBouncer", "Database Proxy", "Connection Pooler for PostgreSQL master & replicas"),
    ("Envoy", "Service Proxy", "High-performance edge and service proxy for API routing"),
]

def seed_database(profile_name="DEV", force=False):
    config = PROFILES.get(profile_name.upper(), CURRENT_CONFIG)
    print(f"[Seed] Initializing database schema with profile: {profile_name} (target {config['MEMORIES']} memories)...")
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        org = db.query(Organization).filter(Organization.slug == "northstar-india").first()
        if org and not force:
            existing_count = db.query(DecisionMemory).count()
            print(f"[Seed] Database already contains {existing_count} memories for Northstar Technologies India.")
            return {"status": "already_seeded", "memories_count": existing_count, "organization": org.name}

        if org and force:
            print("[Seed] Force re-seed: cleaning existing records...")
            # Clean up existing records in dependency order
            db.query(Feedback).delete()
            db.query(Lesson).delete()
            db.query(MemoryRelationship).delete()
            db.query(DecisionMemory).delete()
            db.query(Decision).delete()
            db.query(Incident).delete()
            db.query(Meeting).delete()
            db.query(Document).delete()
            db.query(KnowledgeRisk).delete()
            db.query(Expert).delete()
            db.query(Person).delete()
            db.query(Project).delete()
            db.query(Organization).delete()
            db.commit()

        print("[Seed] Creating Organization: Northstar Technologies India...")
        org = Organization(
            name="Northstar Technologies India",
            slug="northstar-india",
            domain="northstar.co.in"
        )
        db.add(org)
        db.flush()

        # Seed realistic Indian People & Experts
        people_data = [
            ("Arjun Mehta", "arjun.mehta@northstar.co.in", "Pune Hub", "Principal Software Architect",
             "Payments & Platform Architecture", 12,
             "Distributed Systems, PostgreSQL Performance Tuning, High-Throughput Payment Gateways, Connection Pool Topology",
             "Lead architect for 8 years at Northstar. Designed the core Payment API, DB pooling rules, and high-concurrency safeguards.",
             "2016-04-01", "2024-08-31", "FORMER_EMPLOYEE"),

            ("Priya Sharma", "priya.sharma@northstar.co.in", "Bengaluru", "Senior Platform Engineer",
             "Cloud Infrastructure & Kubernetes", 7,
             "Kubernetes, Service Mesh, Kafka Event Streaming, Envoy Gateway",
             "Core infrastructure engineer overseeing cloud migrations and cluster auto-scaling policies.",
             "2019-06-15", None, "ACTIVE"),

            ("Vikram Rao", "vikram.rao@northstar.co.in", "Hyderabad Hub", "Principal Security Architect",
             "Cybersecurity & Identity", 11,
             "mTLS, OAuth2/OIDC, Zero-Trust Architecture, Secret Management, PCI-DSS Compliance",
             "Architected enterprise identity federation and PCI-DSS compliant vault boundaries.",
             "2017-02-10", "2024-01-15", "FORMER_EMPLOYEE"),

            ("Ananya Iyer", "ananya.iyer@northstar.co.in", "Mumbai", "Staff Data Engineer",
             "Data Platform & Analytics", 9,
             "Kafka Partitioning, Change Data Capture (Debezium), Spark Streaming, PostgreSQL CDC",
             "Engineered transactional streaming pipelines from OLTP databases to real-time analytics lake.",
             "2018-09-01", None, "ACTIVE"),

            ("Rohan Sen", "rohan.sen@northstar.co.in", "Delhi NCR", "Lead Payment Systems Architect",
             "Payments & Core Ledger", 10,
             "Double-Entry Accounting, ACID Ledgers, UPI Settlement, Distributed Lock Management",
             "Specialist in reconciliation engines and zero-loss financial transaction topology.",
             "2017-11-01", None, "ACTIVE"),
        ]

        created_experts = []
        for name, email, loc, title, dept, exp_yrs, skills, bio, j_date, l_date, status in people_data:
            p = Person(full_name=name, email=email, location=loc, title=title)
            db.add(p)
            db.flush()

            exp = Expert(
                person_id=p.id,
                organization_id=org.id,
                role=title,
                department=dept,
                years_of_experience=exp_yrs,
                expertise=skills,
                biography=bio,
                joining_date=j_date,
                leaving_date=l_date,
                status=status
            )
            db.add(exp)
            db.flush()
            created_experts.append(exp)

        expert_arjun = created_experts[0]
        expert_priya = created_experts[1]
        expert_vikram = created_experts[2]
        expert_ananya = created_experts[3]
        expert_rohan = created_experts[4]

        # Seed Projects
        created_projects = []
        for p_info in ENTERPRISE_PROJECTS:
            prj = Project(
                organization_id=org.id,
                name=p_info["name"],
                domain=p_info["domain"],
                description=p_info["description"],
                business_context=p_info["business_context"],
                status="ACTIVE",
                criticality=p_info["criticality"]
            )
            db.add(prj)
            db.flush()
            created_projects.append(prj)

        prj_payments = created_projects[0]
        prj_gateway = created_projects[1]
        prj_fraud = created_projects[2]
        prj_identity = created_projects[3]
        prj_telemetry = created_projects[4]
        prj_billing = created_projects[5]

        # Seed Technologies
        tech_objs = []
        for name, category, desc in TECHS:
            t = db.query(Technology).filter(Technology.name == name).first()
            if not t:
                t = Technology(name=name, category=category, description=desc)
                db.add(t)
                db.flush()
            tech_objs.append(t)

        # -------------------------------------------------------------
        # 1. CANONICAL SCENARIO 1 (The Core Demo Narrative: INC-1842 & DEC-219)
        # -------------------------------------------------------------
        curated_memory_1 = DecisionMemory(
            organization_id=org.id,
            project_id=prj_payments.id,
            expert_id=expert_arjun.id,
            problem="During a production traffic surge (4,500 TPS during Diwali Flash Sale), Payment API p99 latency spiked from 45ms to 1800ms due to database connection pool saturation.",
            context="Payment Gateway running on 8 service instances hitting primary PostgreSQL DB cluster. Max database connections limit was set to 500, with app pool size set to only 50.",
            options_considered="Option 1: Scale application instances from 8 to 24 (Rejected: Would exhaust DB port handles without relieving connection waiting queue). Option 2: Increase DB connection pool size from 50 to 100 per instance with 3000ms acquire timeout. Option 3: Aggressive query batching and read caching in Redis.",
            decision="Increased PostgreSQL database connection pool from 50 to 100 per service instance, and configured connection timeout to 3000ms with keepalive monitoring.",
            reasoning="Telemetry confirmed active queries were queueing for connection allocation while PostgreSQL CPU was only at 28%. Scaling app pods would have aggravated connection limits, whereas expanding the pool matched existing database headroom.",
            action_taken="Deployed updated pool configuration across payment pods via zero-downtime rolling restart and added Prometheus connection wait-time metrics.",
            impact="Reduced Payment API p99 latency by 68% (from 1800ms down to 120ms) without downtime.",
            lessons_learned="WARNING: Connection pool expansion works only when DB max_connections permits. If max_connections is already > 300, pool expansion causes DB thrashing; query optimization and redis caching must be prioritized instead.",
            memory_type="decision",
            status="ACTIVE",
            source_type="INCIDENT",
            source_id="INC-1842",
            occurred_at="2023-11-14",
            verification_status="VERIFIED",
            outcome_score=0.92,
            hindsight_memory_id="mem-inc-1842-dec-219"
        )
        db.add(curated_memory_1)
        db.flush()

        dec_1 = Decision(
            project_id=prj_payments.id,
            expert_id=expert_arjun.id,
            title="DEC-219: Database Connection Pool Scaling for Flash Sales",
            problem="Payment API latency spike during traffic surge",
            decision="Expand DB pool from 50 to 100 and add pool timeout safeguards",
            reasoning="Active connection starvation identified in telemetry while DB CPU remained low",
            alternatives="Horizontal app pod scaling, aggressive Redis caching",
            selected_option="Database Pool Expansion to 100 connections per pod",
            rejected_options="Pod scaling (would exceed max_connections limit without solving pool wait queue)",
            risks="Higher memory footprint on PostgreSQL master node",
            expected_outcome="Sub-200ms p99 latency",
            actual_outcome="68% reduction in latency (down to 120ms)",
            decision_date="2023-11-14"
        )
        db.add(dec_1)

        inc_1 = Incident(
            project_id=prj_payments.id,
            title="INC-1842: Payment Gateway Connection Saturation Outage",
            description="P99 latency degradation across APAC payment checkout during Q3 Flash Sale",
            severity="CRITICAL",
            root_cause="DB pool connection starvation under 4,500 TPS load with application instances waiting on connection checkout",
            impact="5.2% checkout drop-off rate for 22 minutes",
            detection_method="Grafana P99 latency alert > 1000ms",
            resolution="Executed DEC-219 connection pool expansion",
            prevention="Established mandatory pool sizing baseline prior to major sales",
            incident_date="2023-11-14",
            expert_involved="Arjun Mehta"
        )
        db.add(inc_1)

        # -------------------------------------------------------------
        # 2. CONFLICTING SCENARIO 2 (Section 32: Historical Conflict Detection)
        # -------------------------------------------------------------
        curated_memory_2 = DecisionMemory(
            organization_id=org.id,
            project_id=prj_billing.id,
            expert_id=expert_rohan.id,
            problem="Billing Platform DB connection pool expansion caused severe PostgreSQL CPU spike (98%) and transaction timeouts.",
            context="Billing Ledger processing reconciliation batches. Max connections on database cluster was already at 480/500.",
            options_considered="Option 1: Repeat DEC-219 and increase pool from 100 to 150. Option 2: Deploy PgBouncer external transaction pooler and Redis query cache.",
            decision="REJECTED pool expansion. Deployed PgBouncer transaction-mode connection pooler and capped client connections to 40 per instance.",
            reasoning="Historical DEC-219 succeeded only because DB max_connections had headroom. When max_connections approaches physical limits, expanding the pool causes OS process context thrashing in PostgreSQL. External transaction pooling is required.",
            action_taken="Installed PgBouncer in front of Ledger PostgreSQL cluster and reduced application pool sizes.",
            impact="Reduced DB CPU from 98% down to 34%, eliminated transaction timeouts, and maintained ACID integrity.",
            lessons_learned="CRITICAL CONFLICT WARNING: Do not apply DEC-219 connection pool expansion when total pool allocations across all services exceed 70% of postgres max_connections. Always verify max_connections headroom before increasing application-side pools.",
            memory_type="tradeoff",
            status="ACTIVE",
            source_type="INCIDENT_POSTMORTEM",
            source_id="INC-2041",
            occurred_at="2024-03-22",
            verification_status="VERIFIED",
            outcome_score=0.95,
            hindsight_memory_id="mem-inc-2041-dec-288"
        )
        db.add(curated_memory_2)
        db.flush()

        dec_2 = Decision(
            project_id=prj_billing.id,
            expert_id=expert_rohan.id,
            title="DEC-288: Rejection of Connection Pool Expansion in Favor of PgBouncer",
            problem="Ledger database CPU thrashing under connection pool expansion attempt",
            decision="Reject local pool enlargement; install PgBouncer transaction pooler",
            reasoning="Exceeded connection threshold caused kernel context switching overhead",
            alternatives="Expanding pool to 150 (rejected: caused DB thrashing in staging test)",
            selected_option="PgBouncer transaction-level pooling",
            rejected_options="Local application pool expansion (DEC-219 pattern inapplicable here)",
            risks="Prepared statements require named transaction session handling",
            expected_outcome="Stable sub-50% database CPU under reconciliation load",
            actual_outcome="Database CPU stabilized at 34%, zero timeouts",
            decision_date="2024-03-22"
        )
        db.add(dec_2)

        # Link relationship: DEC-288 contradicts/refines DEC-219
        rel_conflict = MemoryRelationship(
            source_memory_id=curated_memory_2.id,
            target_memory_id=curated_memory_1.id,
            relationship_type="contradicts"
        )
        db.add(rel_conflict)

        # -------------------------------------------------------------
        # 3. KNOWLEDGE RISKS (Section 36)
        # -------------------------------------------------------------
        risks_data = [
            (prj_payments.id, expert_arjun.id,
             "PostgreSQL Database Connection Saturation & Failover Topology", "HIGH", "CRITICAL",
             0.35, 0.50, expert_priya.id,
             "Conduct expert handoff interview regarding payment DB failover SOPs. 23 decisions tied to Arjun with low documentation."),

            (prj_gateway.id, expert_arjun.id,
             "Envoy Service Mesh Rate Limiting & Zero-Trust Token Ingress", "HIGH", "HIGH",
             0.40, 0.45, expert_priya.id,
             "Document custom Envoy Lua rate-limiting filters and fallback token verification routes."),

            (prj_identity.id, expert_vikram.id,
             "OAuth2 / OIDC Token Vault Boundary & Key Rotation Procedures", "HIGH", "CRITICAL",
             0.28, 0.40, expert_rohan.id,
             "Vikram has left the company; only 4 of 18 key rotation decisions are documented. Urgent handoff required."),

            (prj_fraud.id, expert_ananya.id,
             "Real-Time Feature Store CDC Lag Recovery Under Kafka Rebalance", "MEDIUM", "HIGH",
             0.55, 0.65, expert_priya.id,
             "Review partition rebalance consumer group backpressure handling."),
        ]

        for p_id, exp_id, topic, r_lvl, crit, doc_cov, ver_lvl, bk_id, action in risks_data:
            rk = KnowledgeRisk(
                project_id=p_id,
                expert_id=exp_id,
                topic=topic,
                risk_level=r_lvl,
                criticality=crit,
                documentation_coverage=doc_cov,
                verification_level=ver_lvl,
                backup_expert_id=bk_id,
                action_required=action
            )
            db.add(rk)

        # -------------------------------------------------------------
        # 4. CANONICAL LESSONS & MEETINGS
        # -------------------------------------------------------------
        lesson_1 = Lesson(
            project_id=prj_payments.id,
            expert_id=expert_arjun.id,
            memory_id=curated_memory_1.id,
            title="Database Connection Pool Expansion Safety Checklist",
            takeaway="Always compare active query wait queues vs database CPU. If CPU is low and queries are waiting on pool acquisition, expand pool. If CPU is high, pool expansion makes degradation worse.",
            category="DATABASE_RELIABILITY"
        )
        db.add(lesson_1)

        meeting_1 = Meeting(
            project_id=prj_payments.id,
            title="Post-Incident Review: INC-1842 Flash Sale Saturation",
            date="2023-11-16",
            meeting_type="Incident Review",
            participants="Arjun Mehta, Priya Sharma, Rohan Sen, VP Engineering",
            discussion_summary="Analyzed 22-minute latency degradation during flash sale. Confirmed DEC-219 mitigated issue. Established 80-connection baseline rule.",
            decisions_made="Adopted DEC-219 pool expansion across all APAC payment microservices.",
            action_items="Add automated alerting when connection pool acquisition wait time exceeds 250ms.",
            outcomes="Approved DEC-219 as standard runbook SOP for sales events."
        )
        db.add(meeting_1)

        # -------------------------------------------------------------
        # 5. BULK REALISTIC MEMORIES TO REACH PROFILE COUNT
        # -------------------------------------------------------------
        target_count = config["MEMORIES"] - 2
        bulk_topics = [
            ("Kafka Partitioning Strategy", "Event streaming lag during bulk settlement processing",
             "Increased partition count from 12 to 48 and tuned batch.size to 64KB",
             "Reduced processing lag from 42 minutes to under 3 minutes", "decision", "PERF-201"),

            ("Redis Cache Eviction Policy", "Redis cluster OOM error under heavy customer session storage",
             "Separated session cache from read-through cache and enabled volatile-lru eviction",
             "Prevented session store crashes and dropped memory consumption by 44%", "decision", "DEC-118"),

            ("Zero-Downtime DB Migration", "Schema migration caused 5-minute table lock on payment ledger table",
             "Implemented expand-contract migration pattern with background column backfill batching",
             "Zero customer downtime achieved during multi-million row schema alter", "lesson", "DEC-142"),

            ("API Gateway Token-Bucket Throttling", "Third-party bot scraping degraded API gateway responsiveness",
             "Deployed token-bucket rate limiter at Envoy proxy layer with IP and API key fingerprinting",
             "Mitigated 99.4% of unauthorized automated scraping within 60 seconds", "incident", "INC-1205"),

            ("PostgreSQL VACUUM Optimization", "Autovacuum failed to keep up with high-frequency payment insert/update cycle causing table bloat",
             "Tuned autovacuum_vacuum_cost_limit to 1000 and lowered autovacuum_vacuum_scale_factor to 0.05",
             "Table bloat reduced by 62% and sequential scan latencies dropped by 3.5x", "warning", "PERF-330"),

            ("Idempotency Key Cache Expiry", "Duplicate charge requests during network timeout retries from payment partner",
             "Enforced mandatory 24-hour distributed Redis lock with SHA256 idempotency key hash check",
             "Completely eliminated duplicate charges across 15M transactions", "decision", "DEC-094"),

            ("Circuit Breaker Timeout Tuning", "Cascading timeouts when third-party banking SMS gateway suffered brownout",
             "Configured Resilience4j circuit breaker with 500ms timeout and automatic fallback to WhatsApp/Push",
             "Prevented payment service thread exhaustion during external vendor outages", "tradeoff", "DEC-312"),
        ]

        print(f"[Seed] Generating {target_count} interconnected enterprise memory records...")
        batch = []
        for i in range(target_count):
            title_stem, prob, dec, imp, m_type, s_id = random.choice(bulk_topics)
            chosen_proj = random.choice(created_projects)
            chosen_exp = random.choice(created_experts)

            mem = DecisionMemory(
                organization_id=org.id,
                project_id=chosen_proj.id,
                expert_id=chosen_exp.id,
                problem=f"{prob} in {chosen_proj.name} (Instance #{i+1})",
                context=f"High-concurrency enterprise scenario #{i+1} in {chosen_proj.domain} domain.",
                options_considered="Option A (Local Quick Fix) vs Option B (Architectural Refactor with Telemetry Verification).",
                decision=f"{dec} (Refined for scenario #{i+1})",
                reasoning=f"Evaluated telemetry and risk tradeoffs. Historical data showed approach minimized downtime in {chosen_proj.name}.",
                action_taken="Applied configuration updates, performed canary deployment, and monitored p99 metrics.",
                impact=f"{imp} in production verification.",
                lessons_learned="Verify telemetry baselines before deploying configuration changes to mission-critical infrastructure.",
                memory_type=m_type,
                status="ACTIVE",
                source_type="HISTORICAL_ARCHIVE",
                source_id=f"{s_id}-{i+1}",
                occurred_at=f"202{random.randint(2, 4)}-0{random.randint(1, 9)}-{random.randint(10, 28)}",
                verification_status="VERIFIED" if i % 10 != 0 else "REVIEW_REQUIRED",
                outcome_score=round(random.uniform(0.72, 0.98), 2),
                hindsight_memory_id=f"mem-auto-seed-{i+1}"
            )
            batch.append(mem)

            if len(batch) >= 500:
                db.bulk_save_objects(batch)
                db.commit()
                batch = []

        if batch:
            db.bulk_save_objects(batch)
            db.commit()

        total_mems = db.query(DecisionMemory).count()
        print(f"[Seed] Successfully completed seed! Total memories in DB: {total_mems}")
        return {
            "status": "success",
            "profile": profile_name,
            "memories_count": total_mems,
            "experts_count": len(created_experts),
            "projects_count": len(created_projects)
        }

    except Exception as e:
        db.rollback()
        print(f"[Seed Error] Failed to seed database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database(profile_name="DEV", force=True)
