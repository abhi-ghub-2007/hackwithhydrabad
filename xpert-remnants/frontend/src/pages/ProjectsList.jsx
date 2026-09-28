import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FolderGit2, ArrowRight, ShieldCheck, Activity, Layers } from 'lucide-react';
import { AppShell } from '../components/layout/AppShell';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { api } from '../services/api';
import './ProjectsList.css';

export function ProjectsList() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getProjects()
      .then((data) => setProjects(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <AppShell>
      <div className="projects-page-container">
        <div className="page-header">
          <div>
            <h1 className="page-title">
              <FolderGit2 className="page-icon" size={24} />
              Enterprise Projects
            </h1>
            <p className="page-subtitle">
              Mission-critical systems across Northstar Technologies India with preserved architectural decisions.
            </p>
          </div>
        </div>

        {loading ? (
          <div className="loading-state">Loading projects...</div>
        ) : (
          <div className="projects-grid">
            {projects.map((p) => (
              <div
                key={p.id}
                className="project-card"
                onClick={() => navigate(`/projects/${p.id}`)}
              >
                <div className="project-card-header">
                  <Badge variant={p.criticality === 'CRITICAL' ? 'warning' : 'primary'}>
                    {p.criticality}
                  </Badge>
                  <span className="domain-tag">{p.domain}</span>
                </div>

                <h3 className="project-name">{p.name}</h3>
                <p className="project-desc">{p.description}</p>
                <p className="project-context">{p.business_context}</p>

                <div className="project-card-footer">
                  <span className="explore-btn">
                    Explore Decisions & Map <ArrowRight size={13} />
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </AppShell>
  );
}
