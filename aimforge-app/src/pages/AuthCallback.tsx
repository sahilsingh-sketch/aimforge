import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../services/supabaseClient';
import { api } from '../services/api';
import { useAuthStore } from '../store/useAuthStore';

export function AuthCallback() {
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const { checkAuth } = useAuthStore();

  useEffect(() => {
    const processCallback = async () => {
      try {
        // Supabase JS handles the hash parsing automatically in the browser.
        // We just need to wait for the session.
        const { data: { session }, error: sessionError } = await supabase.auth.getSession();
        
        if (sessionError) throw sessionError;
        if (!session) throw new Error("No active session found.");
        
        // Send the Supabase token to our backend to generate our custom JWT cookie
        // and sync the user profile.
        await api.post('/auth/google', {
          access_token: session.access_token
        });
        
        // Check auth using our normal endpoint to update Zustand state
        await checkAuth();
        
        // Redirect to dashboard on success
        navigate('/dashboard', { replace: true });
        
      } catch (err: any) {
        console.error("Auth callback error:", err);
        setError(err.message || "Failed to authenticate. Please try again.");
        setTimeout(() => navigate('/login', { replace: true }), 3000);
      }
    };

    processCallback();
  }, [navigate, checkAuth]);

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: '#08080B', color: 'white' }}>
      {error ? (
        <div style={{ textAlign: 'center' }}>
          <div style={{ color: 'var(--accent)', marginBottom: '16px' }}>{error}</div>
          <p style={{ color: '#8B8B93', fontSize: '14px' }}>Redirecting to login...</p>
        </div>
      ) : (
        <>
          <div style={{ width: '32px', height: '32px', borderRadius: '50%', border: '2px solid rgba(255,93,31,0.3)', borderTopColor: '#FF5D1F', animation: 'spin .7s linear infinite', marginBottom: '16px' }} />
          <div>Completing authentication...</div>
        </>
      )}
    </div>
  );
}
