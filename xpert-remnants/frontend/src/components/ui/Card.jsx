import React from 'react';
import './Card.css';

export function Card({ children, className = '', onClick, hoverable = false, ...props }) {
  return (
    <div
      className={`card ${hoverable ? 'card-hoverable' : ''} ${className}`}
      onClick={onClick}
      {...props}
    >
      {children}
    </div>
  );
}
