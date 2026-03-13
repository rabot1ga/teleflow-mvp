import { createBrowserRouter, Navigate } from 'react-router-dom'
import { AuthLayout } from '../../components/layout/AuthLayout'
import { DashboardLayout } from '../../components/layout/DashboardLayout'
import { ProtectedRoute, GuestRoute } from './guards'
import { ROUTES } from '../../constants/routes'

// Auth pages
import { LoginPage } from '../../pages/auth/LoginPage'
import { RegisterPage } from '../../pages/auth/RegisterPage'
import { ForgotPasswordPage } from '../../pages/auth/ForgotPasswordPage'
import { ResetPasswordPage } from '../../pages/auth/ResetPasswordPage'

// Dashboard pages
import { DashboardPage } from '../../pages/dashboard/DashboardPage'
import { ContentPage } from '../../pages/content/ContentPage'
import { PublishingPage } from '../../pages/publishing/PublishingPage'
import { FunnelsPage } from '../../pages/funnels/FunnelsPage'
import { UserbotPage } from '../../pages/userbot/UserbotPage'
import { PromotionPage } from '../../pages/promotion/PromotionPage'
import { AnalyticsPage } from '../../pages/analytics/AnalyticsPage'
import { SettingsPage } from '../../pages/settings/SettingsPage'

export const router = createBrowserRouter([
  // Auth routes (guest only)
  {
    path: '',
    element: (
      <GuestRoute>
        <AuthLayout />
      </GuestRoute>
    ),
    children: [
      {
        path: '',
        element: <Navigate to={ROUTES.LOGIN} replace />,
      },
      {
        path: ROUTES.LOGIN,
        element: <LoginPage />,
      },
      {
        path: ROUTES.REGISTER,
        element: <RegisterPage />,
      },
      {
        path: ROUTES.FORGOT_PASSWORD,
        element: <ForgotPasswordPage />,
      },
      {
        path: `${ROUTES.RESET_PASSWORD}/:token`,
        element: <ResetPasswordPage />,
      },
    ],
  },
  // Protected routes
  {
    path: '',
    element: (
      <ProtectedRoute>
        <DashboardLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        path: ROUTES.DASHBOARD,
        element: <DashboardPage />,
      },
      {
        path: `${ROUTES.CONTENT}/*`,
        element: <ContentPage />,
      },
      {
        path: `${ROUTES.PUBLISHING}/*`,
        element: <PublishingPage />,
      },
      {
        path: `${ROUTES.FUNNELS}/*`,
        element: <FunnelsPage />,
      },
      {
        path: `${ROUTES.USERBOT}/*`,
        element: <UserbotPage />,
      },
      {
        path: `${ROUTES.PROMOTION}/*`,
        element: <PromotionPage />,
      },
      {
        path: `${ROUTES.ANALYTICS}/*`,
        element: <AnalyticsPage />,
      },
      {
        path: `${ROUTES.SETTINGS}/*`,
        element: <SettingsPage />,
      },
    ],
  },
  // 404
  {
    path: '*',
    element: <Navigate to={ROUTES.LOGIN} replace />,
  },
])
