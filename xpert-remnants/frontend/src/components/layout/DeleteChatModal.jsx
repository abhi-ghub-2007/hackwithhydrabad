import React, { useEffect, useRef } from 'react';
import { Trash2, X, AlertTriangle } from 'lucide-react';
import './DeleteChatModal.css';

export function DeleteChatModal({ isOpen, chat, onConfirm, onClose }) {
  const cancelBtnRef = useRef(null);

  useEffect(() => {
    if (!isOpen) return;

    // Focus cancel button by default for safety
    if (cancelBtnRef.current) {
      cancelBtnRef.current.focus();
    }

    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen || !chat) return null;

  return (
    <div
      className="delete-modal-backdrop"
      onClick={onClose}
      aria-hidden="true"
    >
      <div
        className="delete-modal-card animate-scale-in"
        role="dialog"
        aria-modal="true"
        aria-labelledby="delete-chat-title"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="delete-modal-header">
          <div className="delete-modal-icon-badge">
            <Trash2 size={18} className="delete-badge-icon" />
          </div>
          <button
            className="delete-close-btn"
            onClick={onClose}
            aria-label="Close dialog"
          >
            <X size={18} />
          </button>
        </div>

        <div className="delete-modal-body">
          <h3 id="delete-chat-title" className="delete-modal-title">
            Delete chat?
          </h3>
          <p className="delete-modal-description">
            This will delete <strong className="delete-chat-name">"{chat.title}"</strong>.
          </p>
          <p className="delete-modal-subtext">
            This action cannot be undone.
          </p>
        </div>

        <div className="delete-modal-footer">
          <button
            ref={cancelBtnRef}
            type="button"
            className="delete-btn-cancel"
            onClick={onClose}
          >
            Cancel
          </button>
          <button
            type="button"
            className="delete-btn-confirm"
            onClick={() => onConfirm(chat.id)}
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}
