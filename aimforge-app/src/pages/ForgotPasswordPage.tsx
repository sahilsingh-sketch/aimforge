import React, { useState } from 'react';
import type { MouseEvent } from 'react';
import { Link } from 'react-router-dom';
import { AuthLayout } from '../components/AuthLayout';
import { api } from '../services/api';

export function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

  const handleMouseMove = (e: MouseEvent<HTMLDivElement>) => {
    const panel = e.currentTarget;
    const card = document.getElementById('card');
    if (!card) return;
    const r = panel.getBoundingClientRect();
    const px = (e.clientX - r.left) / r.width - 0.5;
    const py = (e.clientY - r.top) / r.height - 0.5;
    requestAnimationFrame(() => {
      card.style.transform = `rotateY(${px * 4}deg) rotateX(${-py * 4}deg)`;
    });
  };

  const handleMouseLeave = () => {
    const card = document.getElementById('card');
    if (card) {
      card.style.transform = 'rotateY(0deg) rotateX(0deg)';
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage(null);
    try {
      const response = await api.post(`/auth/forgot-password?email=${encodeURIComponent(email)}`);
      setMessage({ type: 'success', text: response.data.message });
    } catch (err: any) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'An error occurred. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthLayout>
      <div 
        className="auth-panel" 
        onMouseMove={handleMouseMove} 
        onMouseLeave={handleMouseLeave}
        style={{ padding: 0 }}
      >
        <div className="auth-card" id="card">
          <div className="auth-badge">
            <svg viewBox="0 0 24 24" fill="none">
              <rect x="5" y="11" width="14" height="9" rx="2" stroke="currentColor" strokeWidth="1.6" />
              <path d="M8 11V8a4 4 0 018 0v3" stroke="currentColor" strokeWidth="1.6" />
            </svg>
            Account recovery
          </div>

          <h2 className="auth-welcome">Reset password</h2>
          <p className="auth-welcome-sub">Enter your email and we'll send you a recovery link.</p>

          {message && (
            <div style={{ color: message.type === 'error' ? 'var(--accent)' : 'var(--accent-light)', marginBottom: '16px', fontSize: '13px' }}>
              {message.text}
            </div>
          )}

          <form id="forgotForm" onSubmit={handleSubmit}>
            <div className="auth-field">
              <div className="field-head"><span className="field-label">Email address</span></div>
              <div className="input-wrap">
                <svg className="leading" viewBox="0 0 24 24" fill="none">
                  <path d="M4 6h16v12H4z" stroke="currentColor" strokeWidth="1.6" />
                  <path d="M4 7l8 6 8-6" stroke="currentColor" strokeWidth="1.6" />
                </svg>
                <input 
                  type="email" 
                  placeholder="you@example.com" 
                  required 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>

            <button type="submit" className={`auth-btn-primary ${isLoading ? 'is-loading' : ''}`} style={{ marginTop: '20px' }} id="submitBtn" disabled={isLoading}>
              <span className="auth-spinner"></span>
              <span className="btn-label">Send recovery link</span>
              <svg className="btn-arrow" viewBox="0 0 24 24" fill="none">
                <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>
          </form>

          <p className="signup-note" style={{ marginTop: '28px' }}>Remember your password? <Link to="/login">Sign in</Link></p>
        </div>
      </div>
    </AuthLayout>
  );
}
