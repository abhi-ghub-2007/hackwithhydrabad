import React, { useState } from 'react';
import { Plus, MessageSquare, Settings, X, Trash2 } from 'lucide-react';
import { DeleteChatModal } from './DeleteChatModal';
import './Sidebar.css';

export function Sidebar({
  chats = [],
  activeChatId,
  onSelectChat,
  onNewChat,
  onDeleteChat,
  isOpen,
  onClose,
  onOpenSettings
}) {
  const [chatToDelete, setChatToDelete] = useState(null);

  const handleConfirmDelete = (chatId) => {
    if (onDeleteChat) {
      onDeleteChat(chatId);
    }
    setChatToDelete(null);
  };

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
                <div
                  key={chat.id}
                  className={`recent-chat-item-wrapper ${isActive ? 'active' : ''}`}
                >
                  <button
                    type="button"
                    onClick={() => {
                      if (onSelectChat) onSelectChat(chat.id);
                      if (onClose) onClose();
                    }}
                    className="recent-chat-item-btn"
                    title={chat.title}
                  >
                    <MessageSquare size={14} className="chat-item-icon" />
                    <span className="chat-item-title">{chat.title}</span>
                  </button>

                  <button
                    type="button"
                    className="chat-item-delete-btn"
                    onClick={(e) => {
                      e.stopPropagation();
                      setChatToDelete(chat);
                    }}
                    title="Delete chat"
                    aria-label={`Delete chat ${chat.title}`}
                  >
                    <Trash2 size={13} />
                  </button>
                </div>
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

      {/* ChatGPT-style Delete Confirmation Modal */}
      <DeleteChatModal
        isOpen={Boolean(chatToDelete)}
        chat={chatToDelete}
        onConfirm={handleConfirmDelete}
        onClose={() => setChatToDelete(null)}
      />
    </>
  );
}
