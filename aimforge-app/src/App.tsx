import { BrowserRouter as Router, Routes, Route, useLocation, Navigate } from "react-router-dom";
import React, { useEffect } from "react";
import LandingPage from "./pages/LandingPage";
import HistoryPage from "./pages/HistoryPage";
import TrainingPlanPage from "./pages/TrainingPlanPage";
import AiCoachPage from "./pages/AiCoachPage";
import ProfilePage from "./pages/ProfilePage";
import UploadPage from "./pages/UploadPage";
import ProcessingPage from "./pages/ProcessingPage";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { AppLayout } from "./components/AppLayout";
import UploadManager from "./components/UploadManager";
import AnalysisPage from "./pages/AnalysisPage";

import { LoginPage } from "./pages/LoginPage";
import { SignupPage } from "./pages/SignupPage";
import { ForgotPasswordPage } from "./pages/ForgotPasswordPage";
import { useAuthStore } from "./store/useAuthStore";

import { AuthCallback } from "./pages/AuthCallback";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuthStore();
  
  if (isLoading) {
    return (
      <div style={{height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#08080B'}}>
        <div style={{width: '24px', height: '24px', borderRadius: '50%', border: '2px solid rgba(255,93,31,0.3)', borderTopColor: '#FF5D1F', animation: 'spin .7s linear infinite'}} />
      </div>
    );
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
}

function AppContent() {
  const location = useLocation();
  const isAuthOrLanding = ["/", "/login", "/signup", "/forgot-password", "/dashboard", "/auth/callback"].includes(location.pathname);
  
  const { checkAuth } = useAuthStore();
  
  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  return (
    <>
      {!isAuthOrLanding && <UploadManager />}
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/auth/callback" element={<AuthCallback />} />
        <Route path="/dashboard" element={<ProtectedRoute><LandingPage /></ProtectedRoute>} />
        
        {/* Protected Routes */}
        <Route element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/processing" element={<ProcessingPage />} />
          <Route path="/analysis/:jobId" element={<AnalysisPage />} />
          <Route path="/analysis" element={<AnalysisPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/training" element={<TrainingPlanPage />} />
          <Route path="/coach" element={<AiCoachPage />} />
          <Route path="/profile" element={<ProfilePage />} />
        </Route>
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <ErrorBoundary>
      <Router>
        <AppContent />
      </Router>
    </ErrorBoundary>
  );
}
