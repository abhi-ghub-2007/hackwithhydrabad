import React, { useState, useRef, useEffect } from 'react';
import { ArrowUp, Loader2, Sparkles, Building2 } from 'lucide-react';
import './MessageComposer.css';

export function MessageComposer({
  onSendMessage,
  externalText = '',
  setExternalText,
  isLoading = false,
  activeExpert = null,
  activeProject = null
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

  const handlePromptClick = (promptText) => {
    if (!isLoading) {
      onSendMessage(promptText);
    }
  };

  // Section 47 contextual prompts
  const getContextualPrompts = () => {
    if (activeExpert?.id) {
      return [
        "What did this expert work on?",
        "What problems did they solve?",
        "What would they check first?",
        "What mistakes should we avoid?",
        "What lessons did they leave?"
      ];
    } else if (activeProject?.id) {
      return [
        "What are the current architectural risks?",
        "What decisions are active?",
        "What problems were encountered before?",
        "What should the team be careful about?",
        "We are stuck on a compatibility issue. What should we check?"
      ];
    } else {
      return [
        "Which database is used?",
        "Why did we switch?",
        "List all experts",
        "Active experts?",
        "Which is better, hidden coupling or explicit interfaces?"
      ];
    }
  };

  const prompts = getContextualPrompts();

  const placeholderText = activeExpert?.id
    ? `Ask about ${activeExpert.name}'s decisions, warnings, or code history...`
    : (activeProject?.id
        ? `Ask about ${activeProject.name}'s architecture, decisions, or incidents...`
        : `Ask about your organization's history...`);

  const canSubmit = text.trim().length > 0 && !isLoading;

  const breadcrumbContext = `Microsoft / ${activeProject ? activeProject.name : 'All Projects'} / ${activeExpert?.id ? activeExpert.name : 'All Experts'}`;

  return (
    <div className="composer-container">
      <div className="composer-inner">
        {/* Section 46 Context Breadcrumb Header */}
        <div className="composer-context-bar">
          <Building2 size={12} className="composer-context-icon" />
          <span className="composer-context-text">{breadcrumbContext}</span>
        </div>

        {/* Section 47 Contextual Ready-Made Prompts */}
        <div className="composer-prompts-row">
          <div className="prompts-scroll-container">
            <span className="prompts-sparkle-label"><Sparkles size={11} /> Suggested:</span>
            {prompts.map((p, idx) => (
              <button
                key={idx}
                type="button"
                className="context-prompt-pill"
                onClick={() => handlePromptClick(p)}
                disabled={isLoading}
              >
                {p}
              </button>
            ))}
          </div>
        </div>

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
