import { useState } from 'react'
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'
import toast from 'react-hot-toast'

export function DashboardLayout() {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuthStore()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const handleLogout = () => {
    logout()
    toast.success('Logged out successfully')
    navigate('/login')
  }

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/content', label: 'Content', icon: '📰' },
    { path: '/publishing', label: 'Publishing', icon: '📤' },
    { path: '/funnels', label: 'Funnels', icon: '🎯' },
    { path: '/userbot', label: 'Userbot', icon: '🤖' },
    { path: '/promotion', label: 'Promotion', icon: '📈' },
    { path: '/analytics', label: 'Analytics', icon: '📉' },
    { path: '/settings', label: 'Settings', icon: '⚙️' },
  ]

  const isActive = (path: string) => {
    return location.pathname.startsWith(path)
  }

  return (
    <div className="d-flex" style={{ minHeight: '100vh' }}>
      {/* Sidebar */}
      <aside
        className={`bg-dark text-white transition-all ${
          sidebarOpen ? '' : 'collapsed'
        }`}
        style={{
          width: sidebarOpen ? '260px' : '70px',
          minHeight: '100vh',
          position: 'fixed',
          left: 0,
          top: 0,
          transition: 'width 0.3s ease',
          overflow: 'hidden',
        }}
      >
        {/* Logo */}
        <div
          className="p-3 border-bottom border-secondary d-flex align-items-center"
          style={{ height: '60px' }}
        >
          <span className="fs-4 fw-bold">🚀</span>
          {sidebarOpen && (
            <span className="ms-2 fs-5 fw-bold">TeleFlow</span>
          )}
        </div>

        {/* Navigation */}
        <nav className="p-2">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`d-flex align-items-center p-3 rounded mb-1 text-decoration-none ${
                isActive(item.path)
                  ? 'bg-primary text-white'
                  : 'text-white-50 hover:bg-secondary hover:text-white'
              }`}
              style={{ transition: 'all 0.2s' }}
            >
              <span className="fs-5">{item.icon}</span>
              {sidebarOpen && (
                <span className="ms-3">{item.label}</span>
              )}
            </Link>
          ))}
        </nav>

        {/* User info */}
        {sidebarOpen && (
          <div className="position-absolute bottom-0 w-100 p-3 border-top border-secondary">
            <div className="d-flex align-items-center">
              <div
                className="rounded-circle bg-primary d-flex align-items-center justify-content-center"
                style={{ width: '40px', height: '40px' }}
              >
                {user?.first_name?.[0]?.toUpperCase() || 'U'}
              </div>
              <div className="ms-3">
                <div className="fw-semibold small">
                  {user?.first_name} {user?.last_name}
                </div>
                <div className="text-white-50 small" style={{ fontSize: '12px' }}>
                  {user?.email}
                </div>
              </div>
            </div>
          </div>
        )}
      </aside>

      {/* Main content */}
      <div
        className="flex-grow-1"
        style={{ marginLeft: sidebarOpen ? '260px' : '70px', transition: 'margin-left 0.3s ease' }}
      >
        {/* Header */}
        <header
          className="bg-white shadow-sm d-flex align-items-center justify-content-between"
          style={{ height: '60px', position: 'sticky', top: 0, zIndex: 100 }}
        >
          <button
            className="btn btn-link text-dark p-3"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            ☰
          </button>

          <div className="d-flex align-items-center">
            {/* Notifications */}
            <button className="btn btn-link position-relative me-3">
              🔔
              <span
                className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                style={{ fontSize: '10px', padding: '2px 5px' }}
              >
                3
              </span>
            </button>

            {/* Logout */}
            <button className="btn btn-outline-danger btn-sm" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </header>

        {/* Page content */}
        <main className="p-4">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
