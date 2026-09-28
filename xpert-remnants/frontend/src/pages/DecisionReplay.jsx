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
  Layers,
  Sparkles,
  ChevronRight
} from 'lucide-react';
import { AppShell } from '../components/layout/AppShell';
import { Badge } from '../components/ui/Badge';
import { api } from '../services/api';
import './DecisionReplay.css';

function getStageIcon(stage) {
  const s = (stage || '').toLowerCase();
  if (s.includes('problem') || s.includes('alert')) return <AlertTriangle size={13} />;
  if (s.includes('investigation') || s.includes('option')) return <GitBranch size={13} />;
  if (s.includes('decision')) return <CheckCircle2 size={13} />;
  if (s.includes('action') || s.includes('rollout')) return <Layers size={13} />;
  if (s.includes('outcome') || s.includes('telemetry')) return <Sparkles size={13} />;
  if (s.includes('lesson') || s.includes('warning')) return <AlertTriangle size={13} />;
  return <Clock size={13} />;
}

function getStageVariantClass(stage) {
  const s = (stage || '').toLowerCase();
  if (s.includes('problem')) return 'stage-danger';
  if (s.includes('investigation') || s.includes('option')) return 'stage-info';
  if (s.includes('decision')) return 'stage-primary';
  if (s.includes('action')) return 'stage-neutral';
  if (s.includes('outcome')) return 'stage-success';
  if (s.includes('lesson') || s.includes('warning')) return 'stage-warning';
  return 'stage-primary';
}

function formatStepDescription(desc) {
  if (!desc) return null;
  if (desc.includes('|')) {
    const parts = desc.split('|').map((p) => p.trim());
    return (
      <div className="step-segments">
        {parts.map((part, i) => {
          const colonIdx = part.indexOf(':');
          if (colonIdx > -1) {
            const label = part.substring(0, colonIdx);
            const value = part.substring(colonIdx + 1).trim();
            const isWarning = label.toLowerCase().includes('warning') || label.toLowerCase().includes('reject');
            const isSuccess = label.toLowerCase().includes('actual') || label.toLowerCase().includes('selected');
            return (
              <div key={i} className="step-segment">
                <span className={`segment-label ${isWarning ? 'label-warning' : isSuccess ? 'label-success' : ''}`}>
                  {label}:
                </span>
                <span className="segment-value">{value}</span>
              </div>
            );
          }
          return <div key={i} className="step-segment">{part}</div>;
        })}
      </div>
    );
  }

  const colonIdx = desc.indexOf(':');
  if (colonIdx > -1 && colonIdx < 30) {
    const label = desc.substring(0, colonIdx);
    const value = desc.substring(colonIdx + 1).trim();
    const isWarning = label.toLowerCase().includes('warning');
    return (
      <div className="step-segments">
        <div className="step-segment">
          <span className={`segment-label ${isWarning ? 'label-warning' : ''}`}>{label}:</span>
          <span className="segment-value">{value}</span>
        </div>
      </div>
    );
  }

  return <p className="timeline-step-desc">{desc}</p>;
}

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
        setAllDecisions(decs || []);
      })
      .catch((err) => console.error('DecisionReplay load error:', err))
      .finally(() => setLoading(false));
  }, [decisionId]);

  return (
    <AppShell>
      <div className="replay-page-container">
        {/* Navigation / Switcher Bar */}
        <div className="replay-top-bar">
          <button className="back-link-btn" onClick={() => navigate('/knowledge')}>
            <ArrowLeft size={15} />
            <span>Back to Knowledge Library</span>
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
          <div className="replay-loading-state">
            <Clock size={28} className="loading-spin-icon" />
            <p>Reconstructing decision replay timeline...</p>
          </div>
        ) : !replayData ? (
          <div className="replay-empty-state">
            <AlertTriangle size={32} />
            <h3>Decision record not found</h3>
            <p>No historical decision matches ID {decisionId}.</p>
            <button className="back-link-btn" onClick={() => navigate('/knowledge')}>
              Return to Knowledge Library
            </button>
          </div>
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
                <span className="replay-id-badge">ID: DEC-{decisionId}</span>
              </div>

              <h1 className="replay-title">{replayData.title}</h1>

              <div className="replay-sub-meta">
                <span className="meta-item">
                  <Layers size={14} className="meta-icon" />
                  <span>System:</span>
                  <strong>{replayData.project_name}</strong>
                </span>
                <span className="meta-item">
                  <User size={14} className="meta-icon" />
                  <span>Primary Architect:</span>
                  <strong>{replayData.expert_name}</strong>
                </span>
              </div>
            </div>

            {/* Chronological Timeline */}
            <div className="timeline-container">
              {replayData.steps && replayData.steps.map((step, idx) => {
                const isLast = idx === replayData.steps.length - 1;
                const stageClass = getStageVariantClass(step.stage);

                return (
                  <div key={step.step_number} className="timeline-item">
                    {/* Node marker column */}
                    <div className="timeline-marker-column">
                      <div className="timeline-marker">
                        {step.step_number}
                      </div>
                      {!isLast && <div className="timeline-connector" />}
                    </div>

                    {/* Step Card Content */}
                    <div className="timeline-card">
                      <div className="timeline-card-header">
                        <span className={`timeline-stage-pill ${stageClass}`}>
                          {getStageIcon(step.stage)}
                          <span>{step.stage}</span>
                        </span>
                        <span className="timeline-timestamp">
                          <Calendar size={11} /> {step.timestamp}
                        </span>
                      </div>

                      <h3 className="timeline-step-title">{step.title}</h3>

                      <div className="timeline-step-body">
                        {formatStepDescription(step.description)}
                      </div>

                      {step.actor && (
                        <div className="timeline-step-footer">
                          <span className="step-actor">
                            <User size={12} />
                            <span>Logged by: <strong>{step.actor}</strong></span>
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
