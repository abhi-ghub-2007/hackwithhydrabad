import React from 'react';
import { Menu, Plus, Cpu } from 'lucide-react';
import { appConfig } from '../../config/appConfig';
import './MobileNavigation.css';

export function MobileNavigation({ onToggleSidebar, onNewChat }) {
  return (
    <header className="mobile-header mobile-only">
      <button className="icon-btn" onClick={onToggleSidebar} aria-label="Open menu">
        <Menu size={22} />
      </button>

      <div className="mobile-header-brand">
        <Cpu size={18} className="mobile-brand-icon" />
        <span className="mobile-brand-title">{appConfig.appName}</span>
      </div>

      <button className="icon-btn" onClick={onNewChat} aria-label="New chat">
        <Plus size={22} />
      </button>
    </header>
  );
}
