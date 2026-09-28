import React, { useState, useEffect, useRef } from 'react';
import { ChevronDown, Search, Check, Users, UserCheck } from 'lucide-react';
import { expertService, ALL_KNOWLEDGE_SCOPE } from '../../services/expertService';
import './ExpertSelector.css';

export function ExpertSelector({ activeExpert, onSelectExpert }) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [experts, setExperts] = useState([]);
  const dropdownRef = useRef(null);

  useEffect(() => {
    expertService.getExperts().then(setExperts).catch(console.error);
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

  const filteredExperts = expertService.filterExperts(experts, searchQuery);

  const handleSelect = (expert) => {
    onSelectExpert(expert);
    setIsOpen(false);
    setSearchQuery('');
  };

  const isAllKnowledge = !activeExpert || activeExpert.id === null;

  return (
    <div className="expert-selector-container" ref={dropdownRef}>
      <button
        className={`expert-selector-btn ${isOpen ? 'active' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
      >
        <span className="selector-label">Talking about:</span>
        <span className="selector-current-name">
          {isAllKnowledge ? 'All organizational knowledge' : activeExpert.name}
        </span>
        <ChevronDown size={14} className="selector-chevron" />
      </button>

      {isOpen && (
        <div className="expert-dropdown-menu animate-fade-in">
          <div className="dropdown-search-wrapper">
            <Search size={14} className="dropdown-search-icon" />
            <input
              type="text"
              className="dropdown-search-input"
              placeholder="Search experts..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              autoFocus
            />
          </div>

          <div className="dropdown-list">
            {/* Option: All organizational knowledge */}
            <button
              className={`dropdown-item ${isAllKnowledge ? 'selected' : ''}`}
              onClick={() => handleSelect(ALL_KNOWLEDGE_SCOPE)}
            >
              <div className="item-icon-box">
                <Users size={14} />
              </div>
              <div className="item-info">
                <span className="item-name">All organizational knowledge</span>
                <span className="item-role">Company-wide Historical Memory</span>
              </div>
              {isAllKnowledge && <Check size={14} className="item-check" />}
            </button>

            <div className="dropdown-divider" />
            <div className="dropdown-section-title">DEPARTED & ACTIVE EXPERTS</div>

            {filteredExperts.map((exp) => {
              const isSelected = activeExpert?.id === exp.id;
              return (
                <button
                  key={exp.id}
                  className={`dropdown-item ${isSelected ? 'selected' : ''}`}
                  onClick={() => handleSelect(exp)}
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
