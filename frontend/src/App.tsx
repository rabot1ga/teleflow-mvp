import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'react-hot-toast'
import { useAuthStore } from './stores/authStore'

// Layouts
import { AuthLayout } from './components/layout/AuthLayout'
import { DashboardLayout } from './components/layout/DashboardLayout'

// Auth pages
import { LoginPage, RegisterPage, ForgotPasswordPage, ResetPasswordPage } from './pages/auth'

// Dashboard pages
import { DashboardPage } from './pages/dashboard'
import { ContentPage } from './pages/content'
import { PublishingPage, SettingsPage } from './pages/publishing'
import { FunnelsPage } from './pages/funnels'
import { UserbotPage } from './pages/userbot'
import { PromotionPage } from './pages/promotion'
import { AnalyticsPage } from './pages/analytics'

// Create query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

// Protected route component
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore()
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* Auth routes */}
          <Route element={<AuthLayout />}>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage />} />
            <Route path="/reset-password/:token" element={<ResetPasswordPage />} />
          </Route>

          {/* Protected routes */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <DashboardLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="content/*" element={<ContentPage />} />
            <Route path="publishing/*" element={<PublishingPage />} />
            <Route path="funnels/*" element={<FunnelsPage />} />
            <Route path="userbot/*" element={<UserbotPage />} />
            <Route path="promotion/*" element={<PromotionPage />} />
            <Route path="analytics/*" element={<AnalyticsPage />} />
            <Route path="settings/*" element={<SettingsPage />} />
          </Route>

          {/* 404 */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-right" />
    </QueryClientProvider>
  )
}

export default App
