import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Menu, Sun, Moon, User } from 'lucide-react';
import { Sidebar } from './Sidebar';
import { ExpertSelector } from './ExpertSelector';
import { SettingsModal } from './SettingsModal';
import { authService } from '../../services/authService';
import './AppShell.css';

export function AppShell({
  chats = [],
  activeChatId = null,
  onSelectChat,
  onNewChat,
  activeExpert,
  onSelectExpert,
  backendStatus = { online: true, loading: false },
  children
}) {
  const navigate = useNavigate();
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [theme, setTheme] = useState(() => authService.initTheme());

  useEffect(() => {
    authService.initTheme();
  }, []);

  const handleToggleTheme = () => {
    const nextTheme = theme === 'dark' ? 'light' : 'dark';
    authService.setTheme(nextTheme);
    setTheme(nextTheme);
  };

  const handleThemeChange = (newTheme) => {
    authService.setTheme(newTheme);
    setTheme(newTheme);
  };

  const handleNew = () => {
    if (onNewChat) onNewChat();
    navigate('/');
  };

  return (
    <div className="app-shell">
      {/* Minimal Left Sidebar */}
      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        onSelectChat={onSelectChat}
        onNewChat={handleNew}
        isOpen={isMobileSidebarOpen}
        onClose={() => setIsMobileSidebarOpen(false)}
        onOpenSettings={() => setIsSettingsOpen(true)}
      />

      {/* Main Viewport */}
      <main className="main-viewport">
        {/* Top Minimal Header */}
        <header className="app-header">
          <div className="header-left">
            <button
              className="mobile-toggle-btn mobile-only"
              onClick={() => setIsMobileSidebarOpen(true)}
              aria-label="Open menu"
            >
              <Menu size={20} />
            </button>
            <div className="mobile-brand mobile-only">XPERT REMNANTS</div>
          </div>

          <div className="header-center">
            <ExpertSelector
              activeExpert={activeExpert}
              onSelectExpert={onSelectExpert}
            />
          </div>

          <div className="header-right">
            <button
              className="theme-toggle-btn"
              onClick={handleToggleTheme}
              title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? <Sun size={17} /> : <Moon size={17} />}
            </button>

            <div className="user-profile-badge" title="Signed in as Engineer">
              <span className="user-avatar-dot">○</span>
              <span className="user-name-text desktop-only">User</span>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className="main-content-area">
          {children}
        </div>
      </main>

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        currentTheme={theme}
        onThemeChange={handleThemeChange}
        backendStatus={backendStatus}
      />
    </div>
  );
}
