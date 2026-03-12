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
      {/* Background */}
      <div className="auth-layout__bg">
        <div className="auth-layout__gradient auth-layout__gradient--1" />
        <div className="auth-layout__gradient auth-layout__gradient--2" />
        <div className="auth-layout__gradient auth-layout__gradient--3" />
        <div className="auth-layout__overlay" />
      </div>

      {/* Content */}
      <div className="auth-layout__container">
        <div className="auth-layout__card">
          <div className="auth-layout__header">
            <div className="auth-layout__logo">
              <div className="auth-layout__logo-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
                </svg>
              </div>
              <span className="auth-layout__logo-text">TeleFlow</span>
            </div>
            <p className="auth-layout__subtitle">
              Manage your Telegram operations with ease
            </p>
          </div>
          <div className="auth-layout__content">
            <Outlet />
          </div>
        </div>
      </div>
    </div>
  )
}
