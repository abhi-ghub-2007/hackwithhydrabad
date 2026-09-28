import React from 'react';
import { Plus, MessageSquare, Settings, X, Sparkles } from 'lucide-react';
import './Sidebar.css';

export function Sidebar({
  chats = [],
  activeChatId,
  onSelectChat,
  onNewChat,
  isOpen,
  onClose,
  onOpenSettings
}) {
  return (
    <>
      {/* Mobile drawer backdrop */}
      {isOpen && (
        <div className="sidebar-backdrop mobile-only" onClick={onClose} aria-hidden="true" />
      )}

      <aside className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
        {/* Top: Brand Header */}
        <div className="sidebar-top">
          <div className="sidebar-brand">
            <span className="brand-title">XPERT REMNANTS</span>
            <button className="mobile-only sidebar-close-btn" onClick={onClose} aria-label="Close menu">
              <X size={18} />
            </button>
          </div>

          {/* Action: + New Chat */}
          <button
            className="new-chat-btn"
            onClick={() => {
              if (onNewChat) onNewChat();
              if (onClose) onClose();
            }}
          >
            <Plus size={16} className="new-chat-icon" />
            <span>New Chat</span>
          </button>
        </div>

        {/* Middle: Recent Chats List (Scrollable) */}
        <div className="sidebar-recent-section">
          <div className="recent-header">Recent</div>
          <div className="recent-divider" />

          <div className="recent-chats-list">
            {chats.map((chat) => {
              const isActive = activeChatId === chat.id;
              return (
                <button
                  key={chat.id}
                  onClick={() => {
                    if (onSelectChat) onSelectChat(chat.id);
                    if (onClose) onClose();
                  }}
                  className={`recent-chat-item ${isActive ? 'active' : ''}`}
                  title={chat.title}
                >
                  <MessageSquare size={14} className="chat-item-icon" />
                  <span className="chat-item-title">{chat.title}</span>
                </button>
              );
            })}

            {chats.length === 0 && (
              <div className="recent-empty">No recent conversations</div>
            )}
          </div>
        </div>

        {/* Bottom: Settings */}
        <div className="sidebar-bottom">
          <div className="recent-divider" />
          <button
            className="sidebar-settings-btn"
            onClick={() => {
              if (onOpenSettings) onOpenSettings();
              if (onClose) onClose();
            }}
          >
            <Settings size={16} className="settings-icon" />
            <span>Settings</span>
          </button>
        </div>
      </aside>
    </>
  );
}
