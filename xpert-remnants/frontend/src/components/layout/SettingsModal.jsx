import React from 'react';
import { useNavigate } from 'react-router-dom';
import { X, Sun, Moon, Database, ExternalLink, ShieldCheck } from 'lucide-react';
import { authService } from '../../services/authService';
import './SettingsModal.css';

export function SettingsModal({ isOpen, onClose, currentTheme, onThemeChange, backendStatus }) {
  const navigate = useNavigate();

  if (!isOpen) return null;

  const handleToolNavigate = (path) => {
    navigate(path);
    onClose();
  };

  return (
    <div className="settings-modal-backdrop" onClick={onClose}>
      <div className="settings-modal-card animate-fade-in" onClick={(e) => e.stopPropagation()}>
        <div className="settings-modal-header">
          <h3 className="settings-modal-title">Settings</h3>
          <button className="settings-close-btn" onClick={onClose} aria-label="Close settings">
            <X size={18} />
          </button>
        </div>

        <div className="settings-modal-body">
          {/* Theme Section */}
          <div className="settings-section">
            <label className="settings-section-label">Appearance</label>
            <div className="theme-toggle-row">
              <button
                className={`theme-option-btn ${currentTheme === 'dark' ? 'active' : ''}`}
                onClick={() => onThemeChange('dark')}
              >
                <Moon size={15} />
                <span>Dark Mode</span>
              </button>
              <button
                className={`theme-option-btn ${currentTheme === 'light' ? 'active' : ''}`}
                onClick={() => onThemeChange('light')}
              >
                <Sun size={15} />
                <span>Light Mode</span>
              </button>
            </div>
          </div>

          {/* Memory Bank Status */}
          <div className="settings-section">
            <label className="settings-section-label">Memory Engine</label>
            <div className="system-status-box">
              <div className="status-box-header">
                <Database size={15} className="status-icon" />
                <span className="status-bank-name">Hindsight Bank: xpert-remnants-northstar</span>
              </div>
              <div className="status-badge-row">
                <span className="online-dot"></span>
                <span className="status-text">
                  {backendStatus?.online ? 'Connected & Indexed' : 'Online (Local Directives)'}
                </span>
              </div>
            </div>
          </div>

          {/* Secondary Controls for Platform Features (Preserves Task 1/2) */}
          <div className="settings-section">
            <label className="settings-section-label">Secondary Platform Tools</label>
            <p className="settings-section-desc">
              Extended architectural dashboards preserved from Task 1 & 2:
            </p>
            <div className="tools-links-grid">
              <button
                className="tool-link-item"
                onClick={() => handleToolNavigate('/knowledge')}
              >
                <span>Knowledge Library</span>
                <ExternalLink size={12} />
              </button>
              <button
                className="tool-link-item"
                onClick={() => handleToolNavigate('/projects')}
              >
                <span>Projects & Graph</span>
                <ExternalLink size={12} />
              </button>
              <button
                className="tool-link-item"
                onClick={() => handleToolNavigate('/knowledge/review')}
              >
                <span>Review Queue</span>
                <ExternalLink size={12} />
              </button>
              <button
                className="tool-link-item"
                onClick={() => handleToolNavigate('/risks')}
              >
                <span>Knowledge Risks</span>
                <ExternalLink size={12} />
              </button>
              <button
                className="tool-link-item"
                onClick={() => handleToolNavigate('/decisions/1')}
              >
                <span>Decision Replay</span>
                <ExternalLink size={12} />
              </button>
              <button
                className="tool-link-item"
                onClick={() => handleToolNavigate('/admin')}
              >
                <span>System Diagnostics</span>
                <ExternalLink size={12} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
