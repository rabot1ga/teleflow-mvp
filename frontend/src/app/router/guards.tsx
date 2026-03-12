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
  const { isAuthenticated } = useAuthStore()

  if (!isAuthenticated) {
    return <Navigate to={ROUTES.LOGIN} replace />
  }

  return <>{children}</>
}

/**
 * Guest route - redirects to dashboard if already authenticated
 */
export function GuestRoute({ children }: GuestRouteProps) {
  const { isAuthenticated } = useAuthStore()

  if (isAuthenticated) {
    return <Navigate to={ROUTES.DASHBOARD} replace />
  }

  return <>{children}</>
}
