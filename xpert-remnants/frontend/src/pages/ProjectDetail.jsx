import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  FolderGit2,
  ArrowLeft,
  GitBranch,
  AlertTriangle,
  Layers,
  ArrowRight,
  Share2
} from 'lucide-react';
import { AppShell } from '../components/layout/AppShell';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { api } from '../services/api';
import './ProjectDetail.css';

export function ProjectDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [project, setProject] = useState(null);
  const [decisions, setDecisions] = useState([]);
  const [risks, setRisks] = useState([]);
  const [mapData, setMapData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      api.getProject(id),
      api.getDecisions({ projectId: id }),
      api.getProjectRisks(id),
      api.getProjectMap(id)
    ])
      .then(([prj, decs, rks, kMap]) => {
        setProject(prj);
        setDecisions(decs);
        setRisks(rks);
        setMapData(kMap);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, [id]);

  return (
    <AppShell>
      <div className="project-detail-container">
        <button className="back-link-btn" onClick={() => navigate('/projects')}>
          <ArrowLeft size={14} /> Back to Projects
        </button>

        {loading ? (
          <div className="loading-state">Loading project knowledge details...</div>
        ) : !project ? (
          <div className="empty-state">Project not found.</div>
        ) : (
          <>
            {/* Project Header */}
            <div className="project-detail-header">
              <div className="header-meta">
                <Badge variant={project.criticality === 'CRITICAL' ? 'warning' : 'primary'}>
                  {project.criticality}
                </Badge>
                <span className="domain-chip">{project.domain}</span>
              </div>

              <h1 className="project-detail-title">{project.name}</h1>
              <p className="project-detail-desc">{project.description}</p>
              <div className="project-detail-context">
                <strong>Business Context:</strong> {project.business_context}
              </div>
            </div>

            {/* Knowledge Map Visualization (Section 40) */}
            {mapData && mapData.nodes?.length > 0 && (
              <div className="knowledge-map-panel">
                <div className="panel-title">
                  <Share2 size={16} /> Knowledge Graph Map (Section 40)
                </div>
                <div className="nodes-cloud">
                  {mapData.nodes.map((node) => (
                    <div key={node.id} className={`map-node node-${node.type}`}>
                      <span className="node-type-label">{node.type}</span>
                      <span className="node-label">{node.label}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Project Knowledge Risks */}
            {risks.length > 0 && (
              <div className="project-risks-section">
                <h2>Knowledge Vulnerabilities in this System</h2>
                <div className="risks-compact-list">
                  {risks.map((r) => (
                    <div key={r.id} className="risk-compact-card">
                      <div className="risk-compact-header">
                        <Badge variant="warning">{r.risk_level} RISK</Badge>
                        <span className="expert-name">Expert: {r.expert_name}</span>
                      </div>
                      <h4 className="risk-compact-title">{r.topic}</h4>
                      <p className="risk-compact-action">{r.action_required}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Preserved Decisions in this Project */}
            <div className="project-decisions-section">
              <h2>Preserved Architectural Decisions</h2>
              <div className="decisions-list">
                {decisions.map((d) => (
                  <div
                    key={d.id}
                    className="decision-row-card"
                    onClick={() => navigate(`/decisions/${d.id}`)}
                  >
                    <div className="decision-row-info">
                      <GitBranch size={16} className="branch-icon" />
                      <div>
                        <h4 className="decision-row-title">{d.title}</h4>
                        <p className="decision-row-problem">{d.problem}</p>
                      </div>
                    </div>
                    <div className="decision-row-action">
                      <span className="replay-link">
                        Replay Timeline <ArrowRight size={13} />
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </AppShell>
  );
}
