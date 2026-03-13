import { Navigate } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'
import { ROUTES } from '../../constants/routes'

interface ProtectedRouteProps {
  children: React.ReactNode
}

interface GuestRouteProps {
  children: React.ReactNode
}

/**
 * Protected route - redirects to login if not authenticated
 */
export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, user } = useAuthStore()

  console.log('[ProtectedRoute] isAuthenticated:', isAuthenticated, 'user:', user)

  if (!isAuthenticated) {
    console.log('[ProtectedRoute] Redirecting to login')
    return <Navigate to={ROUTES.LOGIN} replace />
  }

  console.log('[ProtectedRoute] Rendering children')
  return <>{children}</>
}

/**
 * Guest route - redirects to dashboard if already authenticated
 */
export function GuestRoute({ children }: GuestRouteProps) {
  const { isAuthenticated, user } = useAuthStore()

  console.log('[GuestRoute] isAuthenticated:', isAuthenticated, 'user:', user)

  if (isAuthenticated) {
    console.log('[GuestRoute] Redirecting to dashboard')
    return <Navigate to={ROUTES.DASHBOARD} replace />
  }

  console.log('[GuestRoute] Rendering children')
  return <>{children}</>
}
