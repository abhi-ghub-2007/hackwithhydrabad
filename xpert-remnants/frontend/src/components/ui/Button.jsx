import React from 'react';
import './Button.css';

export function Button({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  icon: Icon, 
  className = '', 
  disabled = false, 
  onClick,
  type = 'button',
  ...props 
}) {
  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      className={`btn btn-${variant} btn-${size} ${className}`}
      {...props}
    >
      {Icon && <Icon className="btn-icon" size={size === 'sm' ? 16 : 18} />}
      {children && <span className="btn-label">{children}</span>}
    </button>
  );
}
