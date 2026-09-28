import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Menu, Sun, Moon, User } from 'lucide-react';
import { Sidebar } from './Sidebar';
import { ExpertSelector } from './ExpertSelector';
import { SettingsModal } from './SettingsModal';
import { authService } from '../../services/authService';
import { chatService } from '../../services/chatService';
import './AppShell.css';

export function AppShell({
  chats: propChats,
  activeChatId: propActiveChatId,
  onSelectChat: propOnSelectChat,
  onNewChat: propOnNewChat,
  onDeleteChat: propOnDeleteChat,
  activeExpert,
  onSelectExpert,
  activeProject,
  onSelectProject,
  backendStatus = { online: true, loading: false },
  children
}) {
  const navigate = useNavigate();
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [theme, setTheme] = useState(() => authService.initTheme());
  const [storedChats, setStoredChats] = useState(() => chatService.getStoredChats());

  useEffect(() => {
    authService.initTheme();
  }, []);

  // Synchronize stored chats when not provided via props (e.g. on secondary pages)
  useEffect(() => {
    if (propChats !== undefined) return;
    const unsubscribe = chatService.subscribeToChats((updated) => {
      setStoredChats(updated);
    });
    return unsubscribe;
  }, [propChats]);

  const effectiveChats = propChats !== undefined ? propChats : storedChats;
  const effectiveActiveChatId = propActiveChatId !== undefined ? propActiveChatId : chatService.getActiveChatId();

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
    if (propOnNewChat) {
      propOnNewChat();
    } else {
      chatService.setActiveChatId(null);
    }
    navigate('/');
  };

  const handleSelectChat = (chatId) => {
    if (propOnSelectChat) {
      propOnSelectChat(chatId);
    } else {
      chatService.setActiveChatId(chatId);
      navigate(`/?chatId=${chatId}`);
    }
  };

  const handleDeleteChat = (chatId) => {
    if (propOnDeleteChat) {
      propOnDeleteChat(chatId);
    } else {
      chatService.deleteChat(chatId);
    }
  };

  return (
    <div className="app-shell">
      {/* Minimal Left Sidebar */}
      <Sidebar
        chats={effectiveChats}
        activeChatId={effectiveActiveChatId}
        onSelectChat={handleSelectChat}
        onNewChat={handleNew}
        onDeleteChat={handleDeleteChat}
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
              activeProject={activeProject}
              onSelectProject={onSelectProject}
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
