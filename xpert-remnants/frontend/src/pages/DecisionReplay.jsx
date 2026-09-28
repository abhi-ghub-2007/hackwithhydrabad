import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Clock,
  GitBranch,
  AlertTriangle,
  CheckCircle2,
  Calendar,
  User,
  ArrowLeft,
  ChevronRight,
  Layers,
  Sparkles
} from 'lucide-react';
import { AppShell } from '../components/layout/AppShell';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { api } from '../services/api';
import './DecisionReplay.css';

export function DecisionReplay() {
  const { id } = useParams();
  const navigate = useNavigate();
  const decisionId = id || '1';

  const [replayData, setReplayData] = useState(null);
  const [allDecisions, setAllDecisions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      api.getDecisionReplay(decisionId),
      api.getDecisions()
    ])
      .then(([replay, decs]) => {
        setReplayData(replay);
        setAllDecisions(decs);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, [decisionId]);

  return (
    <AppShell>
      <div className="replay-page-container">
        {/* Navigation / Switcher Bar */}
        <div className="replay-top-bar">
          <button className="back-link-btn" onClick={() => navigate('/knowledge')}>
            <ArrowLeft size={14} /> Back to Knowledge Library
          </button>

          <div className="decision-switcher">
            <span className="switcher-label">Select Replay:</span>
            <select
              className="decision-select"
              value={decisionId}
              onChange={(e) => navigate(`/decisions/${e.target.value}`)}
            >
              {allDecisions.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.title}
                </option>
              ))}
            </select>
          </div>
        </div>

        {loading ? (
          <div className="loading-state">Reconstructing decision replay timeline...</div>
        ) : !replayData ? (
          <div className="empty-state">Decision replay record not found.</div>
        ) : (
          <>
            {/* Header */}
            <div className="replay-header-card">
              <div className="header-meta">
                <Badge variant="primary">
                  <Clock size={12} /> Decision Replay Timeline (Section 39)
                </Badge>
                <span className="date-badge">
                  <Calendar size={13} /> {replayData.decision_date || 'Historical Record'}
                </span>
              </div>

              <h1 className="replay-title">{replayData.title}</h1>

              <div className="replay-sub-meta">
                <span className="meta-item">
                  <Layers size={14} /> System: <strong>{replayData.project_name}</strong>
                </span>
                <span className="meta-item">
                  <User size={14} /> Primary Architect: <strong>{replayData.expert_name}</strong>
                </span>
              </div>
            </div>

            {/* Chronological Timeline */}
            <div className="timeline-container">
              {replayData.steps.map((step, idx) => {
                const isLast = idx === replayData.steps.length - 1;
                return (
                  <div key={step.step_number} className="timeline-item">
                    {/* Node marker */}
                    <div className="timeline-marker-column">
                      <div className={`timeline-marker marker-${step.step_number}`}>
                        {step.step_number}
                      </div>
                      {!isLast && <div className="timeline-connector" />}
                    </div>

                    {/* Step Card Content */}
                    <div className="timeline-card">
                      <div className="timeline-card-header">
                        <span className="timeline-stage-tag">{step.stage}</span>
                        <span className="timeline-timestamp">{step.timestamp}</span>
                      </div>

                      <h3 className="timeline-step-title">{step.title}</h3>
                      <p className="timeline-step-desc">{step.description}</p>

                      {step.actor && (
                        <div className="timeline-step-footer">
                          <span className="step-actor">
                            <User size={12} /> Actor: {step.actor}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </>
        )}
      </div>
    </AppShell>
  );
}
