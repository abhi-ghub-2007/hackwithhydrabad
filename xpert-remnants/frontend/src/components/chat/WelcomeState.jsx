import React from 'react';
import './WelcomeState.css';

export function WelcomeState({ onSelectPrompt, activeExpert }) {
  const suggestions = [
    'Why did Raj choose Kafka?',
    'What mistakes did Raj warn about?',
    'Show similar historical cases'
  ];

  const expertName = activeExpert?.name && activeExpert.id ? activeExpert.name : null;

  return (
    <div className="welcome-container animate-fade-in">
      <div className="welcome-content">
        <div className="welcome-header">
          <h1 className="welcome-app-name">XPERT REMNANTS</h1>
          <h2 className="welcome-tagline">
            Preserve the knowledge<br />
            experts leave behind.
          </h2>
          <p className="welcome-description">
            {expertName
              ? `Ask about decisions, failures, reasoning and lessons from ${expertName}.`
              : 'Ask about decisions, failures, reasoning and lessons.'}
          </p>
        </div>

        <div className="welcome-suggestions-wrapper">
          <span className="suggestions-label">Try asking:</span>
          <div className="welcome-suggestions">
            {suggestions.map((text, idx) => (
              <button
                key={idx}
                className="suggestion-btn"
                onClick={() => onSelectPrompt && onSelectPrompt(text)}
              >
                <span>{text}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
