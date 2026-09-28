import React, { useState, useEffect } from 'react';
import {
  CheckSquare,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Sparkles,
  Layers,
  ArrowRight,
  ShieldCheck
} from 'lucide-react';
import { AppShell } from '../components/layout/AppShell';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { api } from '../services/api';
import './ReviewQueue.css';

export function ReviewQueue() {
  const [draftMemories, setDraftMemories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionNotice, setActionNotice] = useState('');

  useEffect(() => {
    fetchDrafts();
  }, []);

  const fetchDrafts = async () => {
    setLoading(true);
    try {
      const [drafts, reviewReq] = await Promise.all([
        api.getMemories({ status: 'DRAFT', limit: 50 }),
        api.getMemories({ status: 'REVIEW_REQUIRED', limit: 50 })
      ]);
      setDraftMemories([...drafts, ...reviewReq]);
    } catch (err) {
      console.error('Failed to load review queue:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (id) => {
    try {
      const res = await api.approveMemory(id);
      setActionNotice(`Memory MEM-${id} approved and retained into Hindsight! (Memory ID: ${res.hindsight_memory_id})`);
      setDraftMemories((prev) => prev.filter((m) => m.id !== id));
    } catch (err) {
      console.error('Approval failed:', err);
      setActionNotice(`Approval failed: ${err.message}`);
    }
  };

  const handleReject = async (id) => {
    try {
      await api.updateMemoryStatus(id, 'ARCHIVED');
      setActionNotice(`Memory MEM-${id} rejected and archived.`);
      setDraftMemories((prev) => prev.filter((m) => m.id !== id));
    } catch (err) {
      console.error('Rejection failed:', err);
    }
  };

  return (
    <AppShell>
      <div className="review-page-container">
        <div className="page-header">
          <div>
            <h1 className="page-title">
              <CheckSquare className="page-icon" size={24} />
              Memory Verification & Review Queue
            </h1>
            <p className="page-subtitle">
              Human-in-the-loop review queue (Section 23 & 58). AI-extracted memories remain in <strong>DRAFT</strong> until explicitly verified by engineering leads before entering Hindsight persistent memory.
            </p>
          </div>
        </div>

        {actionNotice && (
          <div className="review-action-notice">
            <CheckCircle2 size={16} /> {actionNotice}
          </div>
        )}

        <div className="queue-meta">
          <span>Pending Human Review: <strong>{draftMemories.length}</strong></span>
          <span className="policy-badge">
            <ShieldCheck size={14} /> Zero Auto-Approval Security Policy Enforced
          </span>
        </div>

        {loading ? (
          <div className="loading-state">Loading pending memories...</div>
        ) : draftMemories.length === 0 ? (
          <div className="empty-queue-card">
            <CheckCircle2 size={36} className="empty-check-icon" />
            <h3>Review Queue is Clear!</h3>
            <p>All AI-extracted and handoff memories have been reviewed and verified into persistent organizational memory.</p>
          </div>
        ) : (
          <div className="review-cards-list">
            {draftMemories.map((mem) => (
              <div key={mem.id} className="review-card">
                <div className="review-card-header">
                  <div className="header-tags">
                    <Badge variant="warning">AI Extracted Experience</Badge>
                    <Badge variant="neutral">Status: {mem.status}</Badge>
                    {mem.source_id && <span className="source-tag">{mem.source_id}</span>}
                  </div>
                  <span className="memory-id">ID: MEM-{mem.id}</span>
                </div>

                <div className="review-card-body">
                  <div className="review-field">
                    <span className="field-label">Problem / Operational Scenario:</span>
                    <p className="field-content">{mem.problem}</p>
                  </div>

                  <div className="review-field">
                    <span className="field-label">Extracted Decision & Action:</span>
                    <p className="field-content">{mem.decision}</p>
                  </div>

                  <div className="review-field">
                    <span className="field-label">Reasoning & Trade-offs:</span>
                    <p className="field-content">{mem.reasoning}</p>
                  </div>

                  {mem.options_considered && (
                    <div className="review-field">
                      <span className="field-label">Rejected Approaches / Alternatives:</span>
                      <p className="field-content rejected-text">{mem.options_considered}</p>
                    </div>
                  )}

                  {mem.impact && (
                    <div className="review-field">
                      <span className="field-label">Observed Impact / Outcome:</span>
                      <p className="field-content outcome-text">{mem.impact}</p>
                    </div>
                  )}
                </div>

                <div className="review-card-actions">
                  <button
                    className="action-btn reject-btn"
                    onClick={() => handleReject(mem.id)}
                  >
                    <XCircle size={15} /> Reject & Archive
                  </button>

                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => handleApprove(mem.id)}
                    icon={CheckCircle2}
                  >
                    Approve & Retain to Hindsight
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </AppShell>
  );
}
