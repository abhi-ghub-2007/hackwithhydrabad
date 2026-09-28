import React, { useRef, useEffect } from 'react';
import { Message } from './Message';
import './ConversationView.css';

export function ConversationView({ messages }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="conversation-viewport">
      <div className="conversation-messages">
        {messages.map((msg) => (
          <Message key={msg.id} message={msg} />
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
