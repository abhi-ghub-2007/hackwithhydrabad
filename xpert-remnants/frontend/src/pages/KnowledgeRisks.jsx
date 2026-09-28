import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  AlertTriangle,
  ShieldAlert,
  UserX,
  FileText,
  CheckCircle,
  ArrowRight,
  TrendingDown,
  Activity
} from 'lucide-react';
import { AppShell } from '../components/layout/AppShell';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { api } from '../services/api';
import './KnowledgeRisks.css';

export function KnowledgeRisks() {
  const navigate = useNavigate();
  const [risks, setRisks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getRisks()
      .then((data) => setRisks(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  const highRisksCount = risks.filter((r) => r.risk_level === 'HIGH').length;

  return (
    <AppShell>
      <div className="risks-page-container">
        <div className="page-header">
          <div>
            <h1 className="page-title">
              <AlertTriangle className="page-icon" size={24} />
              Organizational Knowledge Risks Engine
            </h1>
            <p className="page-subtitle">
              Calculates institutional vulnerability based on single-expert concentration, low documentation coverage, and unverified critical systems (Section 36 & Scene 2–3).
            </p>
          </div>
          <div className="header-actions">
            <Button
              variant="primary"
              size="md"
              onClick={() => navigate('/knowledge/handoff')}
            >
              Initiate Expert Handoff
            </Button>
          </div>
        </div>

        {/* Metrics Banner */}
        <div className="risks-metrics-grid">
          <div className="metric-card metric-critical">
            <div className="metric-header">
              <span className="metric-title">Critical Knowledge Risks</span>
              <ShieldAlert size={18} className="metric-icon" />
            </div>
            <div className="metric-value">{highRisksCount}</div>
            <div className="metric-desc">Single-expert dependencies with departed architects</div>
          </div>

          <div className="metric-card">
            <div className="metric-header">
              <span className="metric-title">Primary Risk Factor</span>
              <UserX size={18} className="metric-icon" />
            </div>
            <div className="metric-value">Arjun Mehta</div>
            <div className="metric-desc">23 historical decisions (11 incompletely documented)</div>
          </div>

          <div className="metric-card">
            <div className="metric-header">
              <span className="metric-title">Avg Documentation Coverage</span>
              <FileText size={18} className="metric-icon" />
            </div>
            <div className="metric-value">38%</div>
            <div className="metric-desc">Across mission-critical payment services</div>
          </div>
        </div>

        {/* Risk Cards */}
        <div className="risks-list-header">
          <h2>Active Systemic Vulnerabilities</h2>
        </div>

        {loading ? (
          <div className="loading-state">Analyzing knowledge dependencies...</div>
        ) : risks.length === 0 ? (
          <div className="empty-state">No critical knowledge risks identified.</div>
        ) : (
          <div className="risks-cards-grid">
            {risks.map((risk) => (
              <div key={risk.id} className="risk-card">
                <div className="risk-card-header">
                  <div className="risk-badge-row">
                    <Badge variant={risk.risk_level === 'HIGH' ? 'warning' : 'neutral'}>
                      {risk.risk_level} RISK
                    </Badge>
                    <Badge variant="neutral">Criticality: {risk.criticality}</Badge>
                  </div>
                  <span className="project-tag">{risk.project_name}</span>
                </div>

                <h3 className="risk-topic-title">{risk.topic}</h3>

                <div className="risk-expert-row">
                  <span className="risk-label">Primary Expert:</span>
                  <strong>{risk.expert_name}</strong>
                  <span className="former-employee-badge">(Former Employee)</span>
                </div>

                {/* Progress Indicators */}
                <div className="risk-metrics-bars">
                  <div className="metric-bar-group">
                    <div className="metric-bar-label">
                      <span>Documentation Coverage</span>
                      <span>{Math.round(risk.documentation_coverage * 100)}%</span>
                    </div>
                    <div className="progress-track">
                      <div
                        className="progress-fill warning-fill"
                        style={{ width: `${risk.documentation_coverage * 100}%` }}
                      />
                    </div>
                  </div>

                  <div className="metric-bar-group">
                    <div className="metric-bar-label">
                      <span>Verification Level</span>
                      <span>{Math.round(risk.verification_level * 100)}%</span>
                    </div>
                    <div className="progress-track">
                      <div
                        className="progress-fill primary-fill"
                        style={{ width: `${risk.verification_level * 100}%` }}
                      />
                    </div>
                  </div>
                </div>

                <div className="risk-action-box">
                  <span className="action-box-title">Required Action:</span>
                  <p>{risk.action_required}</p>
                </div>

                <div className="risk-card-footer">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => navigate('/knowledge/handoff')}
                  >
                    Conduct Handoff <ArrowRight size={13} />
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
