import { Outlet, Navigate } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'

export function AuthLayout() {
  const { isAuthenticated } = useAuthStore()
  
  // If already authenticated, redirect to dashboard
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }
  
  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center bg-light">
      <Outlet />
    </div>
  )
}
