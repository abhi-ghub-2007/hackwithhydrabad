import React, { useState } from 'react';
import { ChevronRight, ChevronDown, ThumbsUp, ThumbsDown, Check } from 'lucide-react';
import { chatService } from '../../services/chatService';
import './Message.css';

// Simple lightweight markdown parser for clean bullet points and bold text
function formatMessageContent(text) {
  if (!text) return null;

  const lines = text.split('\n');
  const elements = [];
  let currentBullets = [];

  const flushBullets = (key) => {
    if (currentBullets.length > 0) {
      elements.push(
        <ul key={`ul-${key}`} className="message-bullet-list">
          {currentBullets.map((b, i) => (
            <li key={i} dangerouslySetInnerHTML={{ __html: parseInlineStyles(b) }} />
          ))}
        </ul>
      );
      currentBullets = [];
    }
  };

  lines.forEach((line, index) => {
    const trimmed = line.trim();
    if (!trimmed) {
      flushBullets(index);
      return;
    }

    if (trimmed.startsWith('•') || trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      const bulletContent = trimmed.replace(/^[•\-\*]\s*/, '');
      currentBullets.push(bulletContent);
    } else {
      flushBullets(index);
      elements.push(
        <p
          key={`p-${index}`}
          className="message-paragraph"
          dangerouslySetInnerHTML={{ __html: parseInlineStyles(line) }}
        />
      );
    }
  });

  flushBullets('final');
  return elements;
}

function parseInlineStyles(str) {
  return str
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>');
}

export function Message({ message, onRetry }) {
  const isUser = message.sender === 'user';
  const isThinking = message.isThinking;
  const isError = message.isError;
  const [showSources, setShowSources] = useState(false);
  const [feedbackState, setFeedbackState] = useState(null); // 'helpful' | 'not_helpful'

  const sources = message.sources || [];
  const evidenceCount = message.evidenceCount || sources.length;

  const handleFeedback = async (type) => {
    try {
      setFeedbackState(type);
      await chatService.submitFeedback(
        message.originalQuery || message.text,
        type === 'helpful' ? 'HELPFUL' : 'NOT_HELPFUL',
        null,
        message.decisionMemoryId
      );
    } catch (err) {
      console.error('Feedback failed:', err);
    }
  };

  return (
    <div className={`message-item ${isUser ? 'message-user' : 'message-assistant'}`}>
      <div className="message-inner">
        {/* Author Header */}
        <div className="message-header">
          <span className="message-sender-name">
            {isUser ? 'You' : 'XPERT REMNANTS'}
          </span>
          {message.timestamp && (
            <span className="message-timestamp">{message.timestamp}</span>
          )}
        </div>

        {/* Message Body */}
        <div className="message-body">
          {isThinking ? (
            <div className="thinking-indicator">
              <span className="thinking-text">XPERT REMNANTS is thinking</span>
              <span className="typing-dots">
                <span className="dot"></span>
                <span className="dot"></span>
                <span className="dot"></span>
              </span>
            </div>
          ) : isError ? (
            <div className="error-indicator">
              <p className="error-title">Something went wrong.</p>
              <p className="error-sub">Please try again.</p>
              {onRetry && (
                <button className="retry-btn" onClick={onRetry}>
                  Retry question
                </button>
              )}
            </div>
          ) : (
            <div className="message-text-content">
              {formatMessageContent(message.text)}
            </div>
          )}
        </div>

        {/* Minimal Expandable Evidence Section (Section 6) */}
        {!isUser && !isThinking && !isError && sources.length > 0 && (
          <div className="evidence-section">
            <div className="evidence-toggle-row">
              <span className="evidence-summary-text">
                Based on {evidenceCount} historical record{evidenceCount !== 1 ? 's' : ''}
              </span>
              <button
                className="sources-toggle-btn"
                onClick={() => setShowSources(!showSources)}
                aria-expanded={showSources}
              >
                {showSources ? (
                  <>
                    <ChevronDown size={14} className="toggle-icon" />
                    <span>Hide sources</span>
                  </>
                ) : (
                  <>
                    <ChevronRight size={14} className="toggle-icon" />
                    <span>View sources</span>
                  </>
                )}
              </button>

              {/* Feedback action */}
              <div className="message-feedback-group">
                {feedbackState ? (
                  <span className="feedback-confirmed">
                    <Check size={12} /> Recorded
                  </span>
                ) : (
                  <>
                    <button
                      className="feedback-btn"
                      onClick={() => handleFeedback('helpful')}
                      title="Helpful"
                      aria-label="Helpful"
                    >
                      <ThumbsUp size={13} />
                    </button>
                    <button
                      className="feedback-btn"
                      onClick={() => handleFeedback('not_helpful')}
                      title="Not helpful"
                      aria-label="Not helpful"
                    >
                      <ThumbsDown size={13} />
                    </button>
                  </>
                )}
              </div>
            </div>

            {showSources && (
              <div className="sources-dropdown animate-fade-in">
                <div className="sources-heading">Sources</div>
                <div className="sources-list">
                  {sources.map((src, i) => (
                    <div key={i} className="source-row-item">
                      <span className="source-id-badge">{src.id}</span>
                      <span className="source-title-text">{src.title}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
