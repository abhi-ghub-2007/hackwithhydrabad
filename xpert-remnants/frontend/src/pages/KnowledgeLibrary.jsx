import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BookOpen,
  Search,
  Filter,
  CheckCircle2,
  AlertTriangle,
  History,
  Layers,
  ArrowRight,
  GitBranch,
  Sparkles
} from 'lucide-react';
import { AppShell } from '../components/layout/AppShell';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { api } from '../services/api';
import './KnowledgeLibrary.css';

export function KnowledgeLibrary() {
  const navigate = useNavigate();
  const [memories, setMemories] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [projectFilter, setProjectFilter] = useState('');

  useEffect(() => {
    fetchData();
  }, [typeFilter, statusFilter, projectFilter]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [mems, projs] = await Promise.all([
        api.getMemories({
          type: typeFilter || undefined,
          status: statusFilter || undefined,
          projectId: projectFilter || undefined,
          limit: 100
        }),
        api.getProjects()
      ]);
      setMemories(mems);
      setProjects(projs);
    } catch (err) {
      console.error('Failed to load memories:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredMemories = memories.filter((m) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return (
      m.problem.toLowerCase().includes(q) ||
      m.decision.toLowerCase().includes(q) ||
      (m.reasoning && m.reasoning.toLowerCase().includes(q)) ||
      (m.lessons_learned && m.lessons_learned.toLowerCase().includes(q))
    );
  });

  return (
    <AppShell>
      <div className="knowledge-page-container">
        {/* Header */}
        <div className="page-header">
          <div>
            <h1 className="page-title">
              <BookOpen className="page-icon" size={24} />
              Organizational Knowledge Library
            </h1>
            <p className="page-subtitle">
              Preserved decision reasoning, rejected alternatives, warnings, and postmortems from Northstar Architects.
            </p>
          </div>
          <div className="header-actions">
            <Button
              variant="primary"
              size="md"
              onClick={() => navigate('/knowledge/capture')}
            >
              + Capture Memory
            </Button>
          </div>
        </div>

        {/* Filter Controls Bar */}
        <div className="filter-bar">
          <div className="search-box">
            <Search size={16} className="search-icon" />
            <input
              type="text"
              placeholder="Search problems, decisions, lessons, or warnings..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="search-input"
            />
          </div>

          <div className="dropdown-filters">
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="filter-select"
            >
              <option value="">All Memory Types</option>
              <option value="decision">Decisions</option>
              <option value="warning">Warnings</option>
              <option value="lesson">Lessons</option>
              <option value="tradeoff">Trade-offs</option>
              <option value="incident">Incidents</option>
            </select>

            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="filter-select"
            >
              <option value="">All Statuses</option>
              <option value="ACTIVE">Active (Verified)</option>
              <option value="DRAFT">Draft (AI Extracted)</option>
              <option value="REVIEW_REQUIRED">Review Required</option>
              <option value="UPDATED">Updated with Feedback</option>
            </select>

            <select
              value={projectFilter}
              onChange={(e) => setProjectFilter(e.target.value)}
              className="filter-select"
            >
              <option value="">All Projects</option>
              {projects.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Memories Count Stat */}
        <div className="results-meta">
          <span>
            Showing <strong>{filteredMemories.length}</strong> preserved memories
          </span>
          <span className="hindsight-sync-notice">
            <Sparkles size={13} /> Synchronized with Hindsight Bank: xpert-remnants-northstar
          </span>
        </div>

        {/* Memory Cards Grid */}
        {loading ? (
          <div className="loading-state">Loading organizational memory records...</div>
        ) : filteredMemories.length === 0 ? (
          <div className="empty-state">
            <AlertTriangle size={32} className="empty-icon" />
            <p>No memories match your search criteria.</p>
          </div>
        ) : (
          <div className="memories-grid">
            {filteredMemories.map((mem) => (
              <div key={mem.id} className="memory-card">
                <div className="memory-card-header">
                  <div className="memory-badges">
                    <Badge variant={mem.memory_type === 'warning' ? 'warning' : 'primary'}>
                      {mem.memory_type}
                    </Badge>
                    <Badge variant={mem.status === 'ACTIVE' ? 'success' : 'neutral'}>
                      {mem.status}
                    </Badge>
                    {mem.source_id && <span className="source-chip">{mem.source_id}</span>}
                  </div>
                  <span className="outcome-score">
                    Score: {Math.round((mem.outcome_score || 0.9) * 100)}%
                  </span>
                </div>

                <div className="memory-card-body">
                  <h3 className="memory-problem-title">{mem.problem}</h3>

                  <div className="memory-section">
                    <span className="section-heading">Decision & Action:</span>
                    <p className="section-body">{mem.decision}</p>
                  </div>

                  {mem.reasoning && (
                    <div className="memory-section">
                      <span className="section-heading">Architectural Reasoning:</span>
                      <p className="section-body">{mem.reasoning}</p>
                    </div>
                  )}

                  {mem.impact && (
                    <div className="memory-impact-box">
                      <CheckCircle2 size={13} className="impact-icon" />
                      <span>{mem.impact}</span>
                    </div>
                  )}

                  {mem.lessons_learned && (
                    <div className="memory-lesson-box">
                      <span className="lesson-tag">Preserved Lesson:</span>
                      <span>{mem.lessons_learned}</span>
                    </div>
                  )}
                </div>

                <div className="memory-card-footer">
                  <span className="memory-id-tag">ID: MEM-{mem.id}</span>
                  <button
                    className="replay-link-btn"
                    onClick={() => navigate(`/decisions/1`)}
                  >
                    View Replay Timeline <ArrowRight size={13} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </AppShell>
  );
}
