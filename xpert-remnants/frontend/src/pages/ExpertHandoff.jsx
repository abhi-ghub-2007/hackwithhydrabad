import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  UserCheck,
  CheckCircle2,
  AlertTriangle,
  Sparkles,
  ArrowRight,
  ShieldAlert,
  Send
} from 'lucide-react';
import { AppShell } from '../components/layout/AppShell';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { api } from '../services/api';
import './ExpertHandoff.css';

export function ExpertHandoff() {
  const navigate = useNavigate();
  const [experts, setExperts] = useState([]);
  const [projects, setProjects] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [resultData, setResultData] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const [form, setForm] = useState({
    expert_id: '1',
    project_id: '1',
    deep_systems: '',
    recurring_problems: '',
    critical_decisions: '',
    sop_exceptions: '',
    vital_warnings: '',
    past_failures: '',
    hidden_dependencies: '',
    successor_lessons: ''
  });

  useEffect(() => {
    Promise.all([api.getExperts(), api.getProjects()])
      .then(([exps, projs]) => {
        if (exps?.length > 0) setExperts(exps);
        if (projs?.length > 0) setProjects(projs);
      })
      .catch((err) => console.error(err));
  }, []);

  // Demo auto-fill convenience (Scene 4 of Demo Narrative)
  const handlePreFillDemo = () => {
    setForm({
      expert_id: '1',
      project_id: '1',
      deep_systems: 'Payment authorization gateway, PostgreSQL master-replica topology, HikariCP connection pooler, and APAC merchant routing mesh.',
      recurring_problems: 'P99 latency degradation during Diwali & Q3 flash sales; database connection pool exhaustion before CPU reaches 30%.',
      critical_decisions: 'Enlarged application connection pool from 50 to 100 with acquire timeout of 3000ms (DEC-219). Verified with Grafana telemetry.',
      sop_exceptions: 'The standard cloud horizontal autoscaling SOP fails in payment checkout because spinning up more pods without pool tuning exhausts database port handles.',
      vital_warnings: 'CRITICAL: Never increase local connection pool beyond 100 per instance if postgres max_connections > 350. When capacity is tight, PgBouncer transaction pooling is mandatory.',
      past_failures: 'Attempted to autoscale application pods from 8 to 24 during a traffic spike; crashed the primary database connection listener completely.',
      hidden_dependencies: 'The connection timeout must be strictly matched to the third-party bank webhook timeout (3000ms), otherwise hung threads deadlock the pool.',
      successor_lessons: 'Always verify active query waiting queues vs CPU before restarting services. Telemetry first, action second.'
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.deep_systems || !form.critical_decisions || !form.vital_warnings) {
      setErrorMessage('Please fill in Systems, Critical Decisions, and Vital Warnings.');
      return;
    }

    setIsSubmitting(true);
    setErrorMessage('');
    try {
      const payload = {
        expert_id: Number(form.expert_id),
        project_id: Number(form.project_id),
        deep_systems: form.deep_systems,
        recurring_problems: form.recurring_problems,
        critical_decisions: form.critical_decisions,
        sop_exceptions: form.sop_exceptions,
        vital_warnings: form.vital_warnings,
        past_failures: form.past_failures,
        hidden_dependencies: form.hidden_dependencies,
        successor_lessons: form.successor_lessons
      };

      const res = await api.submitHandoff(payload);
      setResultData(res);
    } catch (err) {
      setErrorMessage(err.message || 'Failed to submit expert handoff');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AppShell>
      <div className="handoff-page-container">
        <div className="page-header">
          <div>
            <h1 className="page-title">
              <UserCheck className="page-icon" size={24} />
              Expert Knowledge Handoff Interview
            </h1>
            <p className="page-subtitle">
              Guided 8-question institutional knowledge preservation (Section 35 & Scene 4). Transforms experience into structured, verified Hindsight memories before key engineers depart.
            </p>
          </div>
          <div className="header-actions">
            <button
              type="button"
              className="demo-prefill-btn"
              onClick={handlePreFillDemo}
            >
              <Sparkles size={14} /> Auto-Fill Arjun Mehta Handoff (Demo Scene 4)
            </button>
          </div>
        </div>

        {resultData && (
          <div className="handoff-success-card">
            <div className="success-header">
              <CheckCircle2 size={24} className="success-check-icon" />
              <div>
                <h3>Knowledge Handoff Successfully Preserved!</h3>
                <p>
                  Created <strong>{resultData.created_memories_count}</strong> verified DecisionMemory records and retained them into Hindsight bank <strong>xpert-remnants-northstar</strong>.
                </p>
              </div>
            </div>
            <div className="success-actions">
              <Button variant="primary" size="sm" onClick={() => navigate('/')}>
                Test Recall in Decision Chat <ArrowRight size={14} />
              </Button>
              <Button variant="ghost" size="sm" onClick={() => navigate('/knowledge')}>
                Browse in Knowledge Library
              </Button>
            </div>
          </div>
        )}

        {errorMessage && (
          <div className="alert-box error-alert">
            <AlertTriangle size={16} /> {errorMessage}
          </div>
        )}

        <form className="handoff-form" onSubmit={handleSubmit}>
          <div className="scope-selection-bar">
            <div className="scope-field">
              <label>Departing Expert:</label>
              <select
                value={form.expert_id}
                onChange={(e) => setForm({ ...form, expert_id: e.target.value })}
                className="scope-select"
              >
                {experts.map((exp) => (
                  <option key={exp.id} value={exp.id}>
                    {exp.person?.full_name || `Expert #${exp.id}`} ({exp.role})
                  </option>
                ))}
              </select>
            </div>

            <div className="scope-field">
              <label>System / Project Area:</label>
              <select
                value={form.project_id}
                onChange={(e) => setForm({ ...form, project_id: e.target.value })}
                className="scope-select"
              >
                {projects.map((p) => (
                  <option key={p.id} value={p.id}>{p.name}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="questions-grid">
            {/* Q1: Systems */}
            <div className="question-card">
              <div className="question-num">1</div>
              <div className="question-content">
                <label className="question-label">Core Systems & Architecture</label>
                <span className="question-hint">What systems did you understand deeply that others may find opaque?</span>
                <textarea
                  rows={3}
                  className="question-textarea"
                  placeholder="e.g. Payment authorization gateway, connection pool topology, UPI settlement loop..."
                  value={form.deep_systems}
                  onChange={(e) => setForm({ ...form, deep_systems: e.target.value })}
                  required
                />
              </div>
            </div>

            {/* Q2: Recurring Problems */}
            <div className="question-card">
              <div className="question-num">2</div>
              <div className="question-content">
                <label className="question-label">Recurring Operational Problems</label>
                <span className="question-hint">Which issues or performance degradations happened repeatedly under production load?</span>
                <textarea
                  rows={3}
                  className="question-textarea"
                  placeholder="e.g. P99 latency spikes during flash sales, DB pool starvation..."
                  value={form.recurring_problems}
                  onChange={(e) => setForm({ ...form, recurring_problems: e.target.value })}
                />
              </div>
            </div>

            {/* Q3: Decisions */}
            <div className="question-card">
              <div className="question-num">3</div>
              <div className="question-content">
                <label className="question-label">Critical Decisions & Hard-Won Choices</label>
                <span className="question-hint">Which architectural decisions required significant trial and error?</span>
                <textarea
                  rows={3}
                  className="question-textarea"
                  placeholder="e.g. Tuned HikariCP pool to 100 with acquire timeout instead of autoscaling pods..."
                  value={form.critical_decisions}
                  onChange={(e) => setForm({ ...form, critical_decisions: e.target.value })}
                  required
                />
              </div>
            </div>

            {/* Q4: SOP Exceptions */}
            <div className="question-card">
              <div className="question-num">4</div>
              <div className="question-content">
                <label className="question-label">SOP Exceptions & Runbook Reality</label>
                <span className="question-hint">Which standard operating procedures fail or cause damage in real-world emergencies?</span>
                <textarea
                  rows={3}
                  className="question-textarea"
                  placeholder="e.g. Standard horizontal scaling SOP crashes PostgreSQL port listeners..."
                  value={form.sop_exceptions}
                  onChange={(e) => setForm({ ...form, sop_exceptions: e.target.value })}
                />
              </div>
            </div>

            {/* Q5: Warnings */}
            <div className="question-card highlight-card">
              <div className="question-num highlight-num">5</div>
              <div className="question-content">
                <label className="question-label highlight-label">Vital Warnings & Gotchas</label>
                <span className="question-hint">What should a successor NEVER do when touching this system?</span>
                <textarea
                  rows={3}
                  className="question-textarea"
                  placeholder="e.g. WARNING: Never increase pool size beyond 100 without PgBouncer..."
                  value={form.vital_warnings}
                  onChange={(e) => setForm({ ...form, vital_warnings: e.target.value })}
                  required
                />
              </div>
            </div>

            {/* Q6: Past Failures */}
            <div className="question-card">
              <div className="question-num">6</div>
              <div className="question-content">
                <label className="question-label">Past Failures & Dead Ends</label>
                <span className="question-hint">What approaches did you try in the past that failed miserably?</span>
                <textarea
                  rows={3}
                  className="question-textarea"
                  placeholder="e.g. Tried autoscaling pods from 8 to 24; caused database port exhaustion outage..."
                  value={form.past_failures}
                  onChange={(e) => setForm({ ...form, past_failures: e.target.value })}
                />
              </div>
            </div>

            {/* Q7: Hidden Dependencies */}
            <div className="question-card">
              <div className="question-num">7</div>
              <div className="question-content">
                <label className="question-label">Hidden Dependencies & Latent Assumptions</label>
                <span className="question-hint">What undocumented configurations or timeouts must be aligned?</span>
                <textarea
                  rows={3}
                  className="question-textarea"
                  placeholder="e.g. Connection pool timeout must match payment gateway 3000ms SLA..."
                  value={form.hidden_dependencies}
                  onChange={(e) => setForm({ ...form, hidden_dependencies: e.target.value })}
                />
              </div>
            </div>

            {/* Q8: Lessons */}
            <div className="question-card">
              <div className="question-num">8</div>
              <div className="question-content">
                <label className="question-label">Successor Lessons & Wisdom</label>
                <span className="question-hint">What single piece of advice would you give someone taking on this on-call duty tomorrow?</span>
                <textarea
                  rows={3}
                  className="question-textarea"
                  placeholder="e.g. Always check connection wait queue telemetry before blaming CPU..."
                  value={form.successor_lessons}
                  onChange={(e) => setForm({ ...form, successor_lessons: e.target.value })}
                />
              </div>
            </div>
          </div>

          <div className="form-submit-footer">
            <Button
              type="submit"
              variant="primary"
              size="lg"
              disabled={isSubmitting}
              icon={Send}
            >
              {isSubmitting ? 'Preserving to Hindsight...' : 'Complete Expert Handoff'}
            </Button>
          </div>
        </form>
      </div>
    </AppShell>
  );
}
