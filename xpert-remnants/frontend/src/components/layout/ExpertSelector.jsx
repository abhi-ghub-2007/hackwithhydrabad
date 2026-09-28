import React, { useState, useEffect, useRef } from 'react';
import { ChevronDown, Search, Check, Users, UserCheck, FolderGit2, Building2 } from 'lucide-react';
import { api } from '../../services/api';
import { expertService, ALL_KNOWLEDGE_SCOPE } from '../../services/expertService';
import './ExpertSelector.css';

export function ExpertSelector({ activeExpert, onSelectExpert, activeProject, onSelectProject }) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [experts, setExperts] = useState([]);
  const [projects, setProjects] = useState([]);
  const dropdownRef = useRef(null);

  useEffect(() => {
    expertService.getExperts().then(setExperts).catch(console.error);
    api.getProjects({ canonicalOnly: true }).then(setProjects).catch(console.error);
  }, []);

  // Close on outside click
  useEffect(() => {
    function handleClickOutside(e) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    }
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const handleSelectExpert = (expert) => {
    if (onSelectExpert) onSelectExpert(expert);
    if (expert?.projectId && onSelectProject) {
      const p = projects.find((prj) => prj.id === expert.projectId);
      if (p) onSelectProject(p);
    }
    setIsOpen(false);
    setSearchQuery('');
  };

  const handleSelectProject = (project) => {
    if (onSelectProject) onSelectProject(project);
    if (activeExpert?.projectId && activeExpert.projectId !== project?.id) {
      if (onSelectExpert) onSelectExpert(ALL_KNOWLEDGE_SCOPE);
    }
  };

  const handleSelectAll = () => {
    if (onSelectProject) onSelectProject(null);
    if (onSelectExpert) onSelectExpert(ALL_KNOWLEDGE_SCOPE);
    setIsOpen(false);
    setSearchQuery('');
  };

  // Breadcrumb text for button
  const orgName = 'Microsoft';
  const projName = activeProject ? activeProject.name : null;
  const expName = activeExpert?.id ? activeExpert.name : null;

  let labelText = `${orgName}`;
  if (projName && expName) {
    labelText = `${orgName} / ${projName} / ${expName}`;
  } else if (projName) {
    labelText = `${orgName} / ${projName} / All Experts`;
  } else if (expName) {
    labelText = `${orgName} / ${expName}`;
  } else {
    labelText = `${orgName} / All Projects / All Knowledge`;
  }

  // Filter experts based on activeProject & search query
  const relevantExperts = activeProject
    ? experts.filter((e) => e.projectId === activeProject.id)
    : experts;
  const filteredExperts = expertService.filterExperts(relevantExperts, searchQuery);

  return (
    <div className="expert-selector-container" ref={dropdownRef}>
      <button
        className={`expert-selector-btn ${isOpen ? 'active' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
      >
        <Building2 size={13} className="org-icon-pill" />
        <span className="selector-current-name">{labelText}</span>
        <ChevronDown size={14} className="selector-chevron" />
      </button>

      {isOpen && (
        <div className="expert-dropdown-menu animate-fade-in hierarchy-menu">
          {/* Top Hierarchy Context Card */}
          <div className="hierarchy-breadcrumb-header">
            <span className="breadcrumb-org"><Building2 size={12} /> Microsoft</span>
            <span className="breadcrumb-sep">/</span>
            <span className="breadcrumb-proj">{activeProject ? activeProject.name : 'All Projects'}</span>
            <span className="breadcrumb-sep">/</span>
            <span className="breadcrumb-exp">{activeExpert?.id ? activeExpert.name : 'All Experts'}</span>
          </div>

          {/* Canonical 5 Projects Quick Selector */}
          <div className="project-chips-container">
            <button
              className={`project-chip ${!activeProject ? 'selected' : ''}`}
              onClick={handleSelectAll}
            >
              All Projects
            </button>
            {projects.map((p) => (
              <button
                key={p.id}
                className={`project-chip ${activeProject?.id === p.id ? 'selected' : ''}`}
                onClick={() => handleSelectProject(p)}
              >
                <FolderGit2 size={11} />
                <span>{p.name}</span>
              </button>
            ))}
          </div>

          <div className="dropdown-search-wrapper">
            <Search size={14} className="dropdown-search-icon" />
            <input
              type="text"
              className="dropdown-search-input"
              placeholder={activeProject ? `Search ${activeProject.name} experts...` : 'Search all Microsoft experts...'}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              autoFocus
            />
          </div>

          <div className="dropdown-list">
            {/* Option: All Knowledge */}
            <button
              className={`dropdown-item ${!activeExpert?.id ? 'selected' : ''}`}
              onClick={() => handleSelectExpert(ALL_KNOWLEDGE_SCOPE)}
            >
              <div className="item-icon-box">
                <Users size={14} />
              </div>
              <div className="item-info">
                <span className="item-name">{activeProject ? `All ${activeProject.name} Knowledge` : 'All Microsoft Knowledge'}</span>
                <span className="item-role">{activeProject ? `Preserved experience across ${activeProject.name}` : 'Company-wide historical memory'}</span>
              </div>
              {!activeExpert?.id && <Check size={14} className="item-check" />}
            </button>

            <div className="dropdown-divider" />
            <div className="dropdown-section-title">
              {activeProject ? `${activeProject.name.toUpperCase()} PRESERVED EXPERTS (10)` : 'MICROSOFT EXPERTS (50)'}
            </div>

            {filteredExperts.map((exp) => {
              const isSelected = activeExpert?.id === exp.id;
              return (
                <button
                  key={exp.id}
                  className={`dropdown-item ${isSelected ? 'selected' : ''}`}
                  onClick={() => handleSelectExpert(exp)}
                >
                  <div className="item-icon-box">
                    <UserCheck size={14} />
                  </div>
                  <div className="item-info">
                    <span className="item-name">{exp.name}</span>
                    <span className="item-role">{exp.role}</span>
                  </div>
                  {isSelected && <Check size={14} className="item-check" />}
                </button>
              );
            })}

            {filteredExperts.length === 0 && (
              <div className="dropdown-empty-state">No matching experts found</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
