import { useState } from 'react'
import { Outlet, Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'
import toast from 'react-hot-toast'
import './AuthLayout.css'

export function AuthLayout() {
  const navigate = useNavigate()
  const { isAuthenticated, logout } = useAuthStore()

  // If already authenticated, redirect to dashboard
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  return (
    <div className="auth-layout">
      <div className="auth-layout__bg">
        <div className="auth-layout__gradient"></div>
      </div>
      <div className="auth-layout__container">
        <div className="auth-layout__card">
          <div className="auth-layout__header">
            <div className="auth-layout__logo">
              <span className="auth-layout__logo-icon">⚡</span>
              <span className="auth-layout__logo-text">TeleFlow</span>
            </div>
            <p className="auth-layout__subtitle">
              Modular platform for Telegram channels
            </p>
          </div>
          <Outlet />
        </div>
        <div className="auth-layout__footer">
          <p className="text-muted">
            © 2026 TeleFlow Platform. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  )
}
