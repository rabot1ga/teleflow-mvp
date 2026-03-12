import { useState } from 'react'
import { Outlet, Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'
import toast from 'react-hot-toast'
import './AuthLayout.css'

export function AuthLayout() {
  const navigate = useNavigate()
  const { isAuthenticated, logout } = useAuthStore()

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  return (
    <div className="auth-page">
      {/* Animated Background */}
      <div className="auth-bg">
        <div className="auth-bg__gradient auth-bg__gradient--1"></div>
        <div className="auth-bg__gradient auth-bg__gradient--2"></div>
        <div className="auth-bg__gradient auth-bg__gradient--3"></div>
        <div className="auth-bg__overlay"></div>
      </div>

      {/* Content */}
      <div className="auth-container">
        <div className="auth-card">
          <div className="auth-card__header">
            <div className="auth-card__logo">
              <div className="auth-card__logo-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                </svg>
              </div>
              <span className="auth-card__logo-text">TeleFlow</span>
            </div>
            <p className="auth-card__subtitle">
              Manage your Telegram channels with ease
            </p>
          </div>
          <Outlet />
        </div>
      </div>
    </div>
  )
}
