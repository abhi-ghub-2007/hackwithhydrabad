import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { PlusCircle, FileText, CheckCircle2, AlertTriangle, ArrowRight, Sparkles } from 'lucide-react';
import { AppShell } from '../components/layout/AppShell';
import { Button } from '../components/ui/Button';
import { api } from '../services/api';
import './CaptureMemory.css';

export function CaptureMemory() {
  const navigate = useNavigate();
  const [mode, setMode] = useState('manual'); // 'manual' or 'document'
  const [projects, setProjects] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  // Manual form state
  const [manualForm, setManualForm] = useState({
    problem: '',
    context: '',
    options_considered: '',
    decision: '',
    reasoning: '',
    action_taken: '',
    impact: '',
    lessons_learned: '',
    project_id: '',
    memory_type: 'decision',
    status: 'ACTIVE'
  });

  // Document extraction form state
  const [docForm, setDocForm] = useState({
    title: '',
    content: '',
    project_id: '',
    file_type: 'POSTMORTEM'
  });

  useEffect(() => {
    api.getProjects()
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setProjects(data);
          setManualForm((prev) => ({ ...prev, project_id: data[0].id.toString() }));
          setDocForm((prev) => ({ ...prev, project_id: data[0].id.toString() }));
        }
      })
      .catch((err) => console.error('Failed to load projects:', err));
  }, []);

  const handleManualSubmit = async (e) => {
    e.preventDefault();
    if (!manualForm.problem || !manualForm.decision || !manualForm.reasoning) {
      setErrorMessage('Please fill in Problem, Decision, and Reasoning.');
      return;
    }

    setIsSubmitting(true);
    setErrorMessage('');
    try {
      const payload = {
        ...manualForm,
        organization_id: 1,
        project_id: manualForm.project_id ? Number(manualForm.project_id) : 1
      };
      const res = await api.createMemory(payload);
      setSuccessMessage(`Memory successfully captured and retained in Hindsight (ID: MEM-${res.id})!`);
      setTimeout(() => navigate('/knowledge'), 1500);
    } catch (err) {
      setErrorMessage(err.message || 'Failed to capture memory');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDocSubmit = async (e) => {
    e.preventDefault();
    if (!docForm.title || !docForm.content) {
      setErrorMessage('Please enter a Document Title and Content.');
      return;
    }

    setIsSubmitting(true);
    setErrorMessage('');
    try {
      const payload = {
        title: docForm.title,
        content: docForm.content,
        project_id: docForm.project_id ? Number(docForm.project_id) : 1,
        file_type: docForm.file_type
      };
      const res = await api.extractDocument(payload);
      setSuccessMessage(
        'Document analyzed! Memories extracted in DRAFT status. Human review is required before activation.'
      );
      setTimeout(() => navigate('/knowledge/review'), 1500);
    } catch (err) {
      setErrorMessage(err.message || 'Failed to extract document');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AppShell>
      <div className="capture-page-container">
        <div className="page-header">
          <div>
            <h1 className="page-title">
              <PlusCircle className="page-icon" size={24} />
              Capture Organizational Memory
            </h1>
            <p className="page-subtitle">
              Preserve critical architectural decisions, reasoning, failed attempts, and operational gotchas before knowledge is lost.
            </p>
          </div>
        </div>

        {/* Mode Toggle */}
        <div className="mode-toggle-card">
          <button
            className={`mode-btn ${mode === 'manual' ? 'active' : ''}`}
            onClick={() => setMode('manual')}
          >
            <PlusCircle size={16} /> Structured Experience Capture
          </button>
          <button
            className={`mode-btn ${mode === 'document' ? 'active' : ''}`}
            onClick={() => setMode('document')}
          >
            <FileText size={16} /> AI Document Ingestion & Extraction
          </button>
        </div>

        {successMessage && (
          <div className="alert-box success-alert">
            <CheckCircle2 size={16} /> {successMessage}
          </div>
        )}

        {errorMessage && (
          <div className="alert-box error-alert">
            <AlertTriangle size={16} /> {errorMessage}
          </div>
        )}

        {mode === 'manual' ? (
          <form className="capture-form" onSubmit={handleManualSubmit}>
            <div className="form-grid">
              <div className="form-group full-width">
                <label className="form-label">Problem / Operational Degradation *</label>
                <textarea
                  rows={2}
                  className="form-textarea"
                  placeholder="Describe the operational challenge, incident, or design dilemma..."
                  value={manualForm.problem}
                  onChange={(e) => setManualForm({ ...manualForm, problem: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Project Scope</label>
                <select
                  className="form-select"
                  value={manualForm.project_id}
                  onChange={(e) => setManualForm({ ...manualForm, project_id: e.target.value })}
                >
                  {projects.map((p) => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Memory Category</label>
                <select
                  className="form-select"
                  value={manualForm.memory_type}
                  onChange={(e) => setManualForm({ ...manualForm, memory_type: e.target.value })}
                >
                  <option value="decision">Decision</option>
                  <option value="warning">Warning / Gotcha</option>
                  <option value="lesson">Lesson Learned</option>
                  <option value="tradeoff">Technical Trade-off</option>
                  <option value="incident">Incident Resolution</option>
                </select>
              </div>

              <div className="form-group full-width">
                <label className="form-label">Options Considered & Rejected Approaches</label>
                <textarea
                  rows={2}
                  className="form-textarea"
                  placeholder="What other paths were evaluated? Why were they rejected?..."
                  value={manualForm.options_considered}
                  onChange={(e) => setManualForm({ ...manualForm, options_considered: e.target.value })}
                />
              </div>

              <div className="form-group full-width">
                <label className="form-label">Decision Selected *</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="What specific architectural or configuration action was executed?..."
                  value={manualForm.decision}
                  onChange={(e) => setManualForm({ ...manualForm, decision: e.target.value })}
                  required
                />
              </div>

              <div className="form-group full-width">
                <label className="form-label">Deep Reasoning & Trade-offs *</label>
                <textarea
                  rows={3}
                  className="form-textarea"
                  placeholder="Why was this specific option chosen over alternatives? What trade-offs were accepted?..."
                  value={manualForm.reasoning}
                  onChange={(e) => setManualForm({ ...manualForm, reasoning: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Measured Impact & Realized Outcome</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g. Reduced P99 latency by 68% without downtime"
                  value={manualForm.impact}
                  onChange={(e) => setManualForm({ ...manualForm, impact: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Vital Warning / Advice for Successors</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g. WARNING: Only apply when DB max_connections permits..."
                  value={manualForm.lessons_learned}
                  onChange={(e) => setManualForm({ ...manualForm, lessons_learned: e.target.value })}
                />
              </div>
            </div>

            <div className="form-footer">
              <Button
                variant="primary"
                size="md"
                type="submit"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Retaining to Hindsight...' : 'Preserve into Memory'}
              </Button>
            </div>
          </form>
        ) : (
          <form className="capture-form" onSubmit={handleDocSubmit}>
            <div className="doc-instruction-box">
              <Sparkles size={16} className="sparkle-icon" />
              <span>
                Upload or paste postmortems, ADRs, or incident notes. The LLM extraction pipeline will extract structured rationale into <strong>DRAFT</strong> status for human approval.
              </span>
            </div>

            <div className="form-grid">
              <div className="form-group">
                <label className="form-label">Document Title *</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g. Postmortem: Payment Gateway Outage Q3"
                  value={docForm.title}
                  onChange={(e) => setDocForm({ ...docForm, title: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Document Type</label>
                <select
                  className="form-select"
                  value={docForm.file_type}
                  onChange={(e) => setDocForm({ ...docForm, file_type: e.target.value })}
                >
                  <option value="POSTMORTEM">Incident Postmortem</option>
                  <option value="ADR">Architecture Decision Record (ADR)</option>
                  <option value="RUNBOOK">Operational Runbook</option>
                  <option value="TECHNICAL_NOTE">Technical Architecture Note</option>
                </select>
              </div>

              <div className="form-group full-width">
                <label className="form-label">Document Content *</label>
                <textarea
                  rows={8}
                  className="form-textarea"
                  placeholder="Paste complete incident review, discussion notes, or architectural rationale here..."
                  value={docForm.content}
                  onChange={(e) => setDocForm({ ...docForm, content: e.target.value })}
                  required
                />
              </div>
            </div>

            <div className="form-footer">
              <Button
                variant="primary"
                size="md"
                type="submit"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Extracting Memory Rationale...' : 'Extract & Queue for Review'}
              </Button>
            </div>
          </form>
        )}
      </div>
    </AppShell>
  );
}
