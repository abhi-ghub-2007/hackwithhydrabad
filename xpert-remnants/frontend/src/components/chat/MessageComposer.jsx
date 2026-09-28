import React, { useState, useRef, useEffect } from 'react';
import { ArrowUp, Loader2 } from 'lucide-react';
import './MessageComposer.css';

export function MessageComposer({
  onSendMessage,
  externalText = '',
  setExternalText,
  isLoading = false,
  activeExpert = null
}) {
  const [text, setText] = useState('');
  const textareaRef = useRef(null);

  // Sync external prompt clicks (e.g. suggestion pills) with textarea
  useEffect(() => {
    if (externalText) {
      setText(externalText);
      if (setExternalText) setExternalText('');
      if (textareaRef.current) {
        textareaRef.current.focus();
      }
    }
  }, [externalText, setExternalText]);

  // Auto-resize textarea height as content changes
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const newHeight = Math.min(textareaRef.current.scrollHeight, 180);
      textareaRef.current.style.height = `${newHeight}px`;
    }
  }, [text]);

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (text.trim() && !isLoading) {
      const query = text.trim();
      onSendMessage(query);
      setText('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
        textareaRef.current.focus();
      }
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const placeholderText = activeExpert?.id
    ? `Ask about ${activeExpert.name}'s decisions, warnings, or code history...`
    : `Ask about your organization's history...`;

  const canSubmit = text.trim().length > 0 && !isLoading;

  return (
    <div className="composer-container">
      <div className="composer-inner">
        <form onSubmit={handleSubmit} className="composer-pill-box">
          <textarea
            ref={textareaRef}
            rows={1}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholderText}
            className="composer-textarea"
            disabled={isLoading}
            aria-label="Ask about organizational memory"
          />

          <button
            type="submit"
            disabled={!canSubmit}
            className={`composer-send-btn ${canSubmit ? 'active' : ''}`}
            aria-label="Send message"
            title="Send message (Enter)"
          >
            {isLoading ? (
              <Loader2 size={16} className="send-spinner" />
            ) : (
              <ArrowUp size={16} className="send-arrow-icon" strokeWidth={2.5} />
            )}
          </button>
        </form>

        <div className="composer-footer-note">
          XPERT REMNANTS preserves institutional knowledge from verified historical records.
        </div>
      </div>
    </div>
  );
}
