import React, { useState } from 'react';
import type { MouseEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AuthLayout } from '../components/AuthLayout';
import { useAuthStore } from '../store/useAuthStore';

export function SignupPage() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  
  const { signup, isLoading, error } = useAuthStore();
  const navigate = useNavigate();

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
    document.body.classList.add('is-locking');
    try {
      await signup({ email, username, password });
      setTimeout(() => {
        document.body.classList.remove('is-locking');
        navigate('/dashboard');
      }, 700);
    } catch (err) {
      document.body.classList.remove('is-locking');
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
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round" />
            </svg>
            Join the elite
          </div>

          <h2 className="auth-welcome">Create your account</h2>
          <p className="auth-welcome-sub">Start improving your gameplay today.</p>

          {error && <div style={{ color: 'var(--accent)', marginBottom: '16px', fontSize: '13px' }}>{error}</div>}

          <form id="signupForm" onSubmit={handleSubmit}>
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

            <div className="auth-field">
              <div className="field-head"><span className="field-label">Username (Optional)</span></div>
              <div className="input-wrap">
                <svg className="leading" viewBox="0 0 24 24" fill="none">
                  <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"/>
                  <circle cx="12" cy="7" r="4" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <input 
                  type="text" 
                  placeholder="AimGod99" 
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
            </div>

            <div className="auth-field">
              <div className="field-head">
                <span className="field-label">Password</span>
              </div>
              <div className="input-wrap">
                <svg className="leading" viewBox="0 0 24 24" fill="none">
                  <rect x="5" y="11" width="14" height="9" rx="2" stroke="currentColor" strokeWidth="1.6" />
                  <path d="M8 11V8a4 4 0 018 0v3" stroke="currentColor" strokeWidth="1.6" />
                </svg>
                <input 
                  type={showPassword ? 'text' : 'password'} 
                  placeholder="Create a strong password" 
                  id="pwInput" 
                  required 
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button type="button" className="toggle-vis" onClick={() => setShowPassword(!showPassword)} aria-label="Show password">
                  <svg viewBox="0 0 24 24" fill="none" id="eyeIcon">
                    {showPassword ? (
                      <>
                        <path d="M3 3l18 18" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
                        <path d="M9.9 5.1A10.4 10.4 0 0112 5c6.4 0 10 7 10 7a17.7 17.7 0 01-3.2 4.2M6.6 6.6C4 8.3 2 12 2 12s3.6 7 10 7c1.4 0 2.7-.25 3.85-.7M9.9 14.1a3 3 0 004.2-4.2" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
                      </>
                    ) : (
                      <>
                        <path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7z" stroke="currentColor" strokeWidth="1.6" />
                        <circle cx="12" cy="12" r="2.8" stroke="currentColor" strokeWidth="1.6" />
                      </>
                    )}
                  </svg>
                </button>
              </div>
            </div>

            <button type="submit" className={`auth-btn-primary ${isLoading ? 'is-loading' : ''}`} style={{ marginTop: '20px' }} id="submitBtn" disabled={isLoading}>
              <span className="auth-spinner"></span>
              <span className="btn-label">Create account</span>
              <svg className="btn-arrow" viewBox="0 0 24 24" fill="none">
                <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>
          </form>

          <div className="auth-divider"><span>OR CONTINUE WITH</span></div>

          <div className="oauth-row">
            <button className="btn-oauth" type="button">
              <svg viewBox="0 0 24 24" fill="none">
                <rect x="3" y="3" width="7" height="7" rx="1.5" stroke="currentColor" strokeWidth="1.6" />
                <rect x="14" y="3" width="7" height="7" rx="1.5" stroke="currentColor" strokeWidth="1.6" />
                <rect x="3" y="14" width="7" height="7" rx="1.5" stroke="currentColor" strokeWidth="1.6" />
                <rect x="14" y="14" width="7" height="7" rx="1.5" stroke="currentColor" strokeWidth="1.6" />
              </svg>
              Gaming ID
            </button>
            <button className="btn-oauth" type="button">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M21 12.2c0-.7-.06-1.4-.18-2H12v3.8h5c-.22 1.2-.9 2.2-1.9 2.9v2.4h3.1c1.8-1.7 2.8-4.1 2.8-7.1z" fill="#8B8B93" />
                <path d="M12 21c2.6 0 4.8-.9 6.2-2.4l-3.1-2.4c-.85.6-1.95.95-3.1.95-2.4 0-4.4-1.6-5.1-3.8H3.7v2.5C5.1 18.8 8.3 21 12 21z" fill="#8B8B93" />
                <path d="M6.9 13.35A5.4 5.4 0 016.6 12c0-.5.1-.95.3-1.35V8.15H3.7A9 9 0 003 12c0 1.45.35 2.8.97 4l3.93-2.65z" fill="#8B8B93" />
                <path d="M12 6.9c1.4 0 2.7.5 3.7 1.45l2.75-2.75C16.8 3.9 14.6 3 12 3 8.3 3 5.1 5.2 3.7 8.15l3.2 2.5C7.6 8.5 9.6 6.9 12 6.9z" fill="#8B8B93" />
              </svg>
              Google
            </button>
          </div>

          <p className="signup-note">Already have an account? <Link to="/login">Sign in</Link></p>
        </div>
      </div>
    </AuthLayout>
  );
}
