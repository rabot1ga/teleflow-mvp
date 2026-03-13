import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'
import './AuthLayout.css'

export function AuthLayout() {
  const { isAuthenticated } = useAuthStore()

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  return (
    <div className="auth-layout">
      {/* Animated Background */}
      <div className="auth-layout__bg">
        <div className="auth-layout__gradient auth-layout__gradient--1" />
        <div className="auth-layout__gradient auth-layout__gradient--2" />
        <div className="auth-layout__gradient auth-layout__gradient--3" />
        <div className="auth-layout__grid-overlay" />
      </div>

      {/* Floating Shapes */}
      <div className="auth-layout__shapes">
        <div className="auth-layout__shape auth-layout__shape--1" />
        <div className="auth-layout__shape auth-layout__shape--2" />
        <div className="auth-layout__shape auth-layout__shape--3" />
      </div>

      {/* Content */}
      <div className="auth-layout__container">
        {/* Logo Section */}
        <div className="auth-layout__logo-section">
          <div className="auth-layout__logo">
            <div className="auth-layout__logo-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
              </svg>
            </div>
            <span className="auth-layout__logo-text">TeleFlow</span>
          </div>
          <p className="auth-layout__tagline">
            Manage your Telegram operations with ease
          </p>
        </div>

        {/* Card */}
        <div className="auth-layout__card">
          <div className="auth-layout__content">
            <Outlet />
          </div>
        </div>

        {/* Footer */}
        <div className="auth-layout__footer">
          <p className="auth-layout__copyright">
            © 2026 TeleFlow Platform. All rights reserved.
          </p>
          <div className="auth-layout__links">
            <a href="#" className="auth-layout__link">Privacy</a>
            <a href="#" className="auth-layout__link">Terms</a>
            <a href="#" className="auth-layout__link">Support</a>
          </div>
        </div>
      </div>
    </div>
  )
}
