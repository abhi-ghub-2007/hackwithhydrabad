import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  FolderGit2,
  ArrowLeft,
  GitBranch,
  AlertTriangle,
  Layers,
  ArrowRight,
  Share2,
  Users,
  MessageSquare,
  Cpu,
  ShieldAlert
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
  const [modules, setModules] = useState([]);
  const [experts, setExperts] = useState([]);
  const [decisions, setDecisions] = useState([]);
  const [risks, setRisks] = useState([]);
  const [mapData, setMapData] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      api.getProject(id),
      api.getProjectModules(id).catch(() => []),
      api.getExperts({ projectId: id }).catch(() => []),
      api.getDecisions({ projectId: id }).catch(() => []),
      api.getProjectRisks(id).catch(() => []),
      api.getProjectMap(id).catch(() => null)
    ])
      .then(([prj, mods, exps, decs, rks, kMap]) => {
        setProject(prj);
        setModules(mods || []);
        setExperts(exps || []);
        setDecisions(decs || []);
        setRisks(rks || []);
        setMapData(kMap);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, [id]);

  const handleStartChatWithProject = () => {
    navigate('/', { state: { projectId: project?.id } });
  };

  const handleStartChatWithExpert = (expert) => {
    navigate('/', { state: { projectId: project?.id, expertId: expert?.id } });
  };

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
                <span className="domain-chip">Organization: Microsoft</span>
              </div>

              <div className="project-title-row">
                <h1 className="project-detail-title">{project.name}</h1>
                <Button variant="primary" size="sm" onClick={handleStartChatWithProject}>
                  <MessageSquare size={14} /> Chat with {project.name} Knowledge
                </Button>
              </div>

              <p className="project-detail-desc">{project.description}</p>
              <div className="project-detail-context">
                <strong>Business Context:</strong> {project.business_context}
              </div>
            </div>

            {/* Navigation Tabs (Section 46) */}
            <div className="project-tabs-nav">
              <button
                className={`project-tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
                onClick={() => setActiveTab('overview')}
              >
                Overview & Graph
              </button>
              <button
                className={`project-tab-btn ${activeTab === 'modules' ? 'active' : ''}`}
                onClick={() => setActiveTab('modules')}
              >
                <Cpu size={14} /> Modules ({modules.length})
              </button>
              <button
                className={`project-tab-btn ${activeTab === 'experts' ? 'active' : ''}`}
                onClick={() => setActiveTab('experts')}
              >
                <Users size={14} /> Preserved Experts ({experts.length})
              </button>
              <button
                className={`project-tab-btn ${activeTab === 'decisions' ? 'active' : ''}`}
                onClick={() => setActiveTab('decisions')}
              >
                <GitBranch size={14} /> Decisions ({decisions.length})
              </button>
              <button
                className={`project-tab-btn ${activeTab === 'risks' ? 'active' : ''}`}
                onClick={() => setActiveTab('risks')}
              >
                <ShieldAlert size={14} /> Risks ({risks.length})
              </button>
            </div>

            {/* TAB: Overview & Graph */}
            {activeTab === 'overview' && (
              <>
                {mapData && mapData.nodes?.length > 0 && (
                  <div className="knowledge-map-panel">
                    <div className="panel-title">
                      <Share2 size={16} /> Knowledge Graph Map
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

                <div className="stats-grid">
                  <div className="stat-card">
                    <div className="stat-number">{modules.length}</div>
                    <div className="stat-label">Architectural Modules</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-number">{experts.length}</div>
                    <div className="stat-label">Preserved Experts</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-number">{decisions.length}</div>
                    <div className="stat-label">Historical Decisions</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-number">{risks.length}</div>
                    <div className="stat-label">Active Vulnerabilities</div>
                  </div>
                </div>
              </>
            )}

            {/* TAB: Modules (Section 44 & 45) */}
            {activeTab === 'modules' && (
              <div className="modules-grid-section">
                <h2>Major Architectural Modules & Components</h2>
                <div className="modules-grid">
                  {modules.map((m) => (
                    <div key={m.id} className="module-detail-card">
                      <div className="module-card-header">
                        <Cpu size={16} className="module-icon" />
                        <h4 className="module-name">{m.name}</h4>
                      </div>
                      <p className="module-desc">{m.description}</p>
                      <div className="module-tech-badge">
                        <span>Tech:</span> <code>{m.technology || 'Core C++ / TypeScript'}</code>
                      </div>
                      {m.risks && (
                        <div className="module-risks">
                          <AlertTriangle size={12} className="risk-icon" />
                          <span>Known Constraint: {m.risks}</span>
                        </div>
                      )}
                    </div>
                  ))}
                  {modules.length === 0 && (
                    <div className="empty-substate">No modules registered yet for this project.</div>
                  )}
                </div>
              </div>
            )}

            {/* TAB: Experts (Section 37 & 46) */}
            {activeTab === 'experts' && (
              <div className="experts-grid-section">
                <h2>Preserved Senior Engineers & Departed Experts</h2>
                <div className="experts-grid">
                  {experts.map((exp) => (
                    <div key={exp.id} className="expert-detail-card">
                      <div className="expert-card-top">
                        <div className="expert-avatar-box">
                          <Users size={16} />
                        </div>
                        <div>
                          <h4 className="expert-name">{exp.person?.full_name || `Expert #${exp.id}`}</h4>
                          <span className="expert-role">{exp.role}</span>
                        </div>
                        <Badge variant="secondary" className="status-badge">
                          {exp.status || 'DEPARTED'}
                        </Badge>
                      </div>
                      <p className="expert-bio">{exp.biography || exp.expertise || 'Senior contributor on core architecture.'}</p>
                      <div className="expert-card-footer">
                        <button
                          className="expert-chat-btn"
                          onClick={() => handleStartChatWithExpert(exp)}
                        >
                          <MessageSquare size={13} /> Chat with Preserved Knowledge
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* TAB: Decisions */}
            {activeTab === 'decisions' && (
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
                  {decisions.length === 0 && (
                    <div className="empty-substate">No decisions logged for this project.</div>
                  )}
                </div>
              </div>
            )}

            {/* TAB: Risks */}
            {activeTab === 'risks' && (
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
                  {risks.length === 0 && (
                    <div className="empty-substate">No unresolved critical knowledge risks detected.</div>
                  )}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </AppShell>
  );
}
