import { useState } from 'react'
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'
import toast from 'react-hot-toast'
import './DashboardLayout.css'

export function DashboardLayout() {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuthStore()
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [userMenuOpen, setUserMenuOpen] = useState(false)

  const handleLogout = () => {
    logout()
    toast.success('Logged out successfully')
    navigate('/login')
  }

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊', category: 'main' },
    { path: '/content', label: 'Content', icon: '📰', category: 'content' },
    { path: '/publishing', label: 'Publishing', icon: '📤', category: 'content' },
    { path: '/funnels', label: 'Funnels', icon: '🎯', category: 'growth' },
    { path: '/userbot', label: 'Userbot', icon: '🤖', category: 'growth' },
    { path: '/promotion', label: 'Promotion', icon: '📈', category: 'growth' },
    { path: '/analytics', label: 'Analytics', icon: '📉', category: 'analytics' },
    { path: '/settings', label: 'Settings', icon: '⚙️', category: 'settings' },
  ]

  const isActive = (path: string) => location.pathname.startsWith(path)

  const groupedNavItems = navItems.reduce((acc, item) => {
    if (!acc[item.category]) {
      acc[item.category] = []
    }
    acc[item.category].push(item)
    return acc
  }, {} as Record<string, typeof navItems>)

  return (
    <div className="dashboard-layout">
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'sidebar--open' : 'sidebar--collapsed'}`}>
        {/* Logo */}
        <div className="sidebar__header">
          <Link to="/dashboard" className="sidebar__logo">
            <span className="sidebar__logo-icon">⚡</span>
            {sidebarOpen && <span className="sidebar__logo-text">TeleFlow</span>}
          </Link>
          <button
            className="sidebar__toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label={sidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
          >
            {sidebarOpen ? '◀' : '▶'}
          </button>
        </div>

        {/* Navigation */}
        <nav className="sidebar__nav">
          {Object.entries(groupedNavItems).map(([category, items]) => (
            <div key={category} className="sidebar__nav-group">
              {sidebarOpen && (
                <div className="sidebar__nav-category">
                  {category.charAt(0).toUpperCase() + category.slice(1)}
                </div>
              )}
              {items.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`sidebar__nav-item ${isActive(item.path) ? 'sidebar__nav-item--active' : ''}`}
                  title={!sidebarOpen ? item.label : undefined}
                >
                  <span className="sidebar__nav-icon">{item.icon}</span>
                  {sidebarOpen && <span className="sidebar__nav-label">{item.label}</span>}
                </Link>
              ))}
            </div>
          ))}
        </nav>

        {/* Footer */}
        <div className="sidebar__footer">
          <div className="sidebar__user-info">
            <div className="sidebar__user-avatar">
              {user?.first_name?.charAt(0) || 'U'}
            </div>
            {sidebarOpen && (
              <div className="sidebar__user-details">
                <div className="sidebar__user-name">
                  {user?.first_name} {user?.last_name}
                </div>
                <div className="sidebar__user-email">{user?.email}</div>
              </div>
            )}
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className={`main-content ${sidebarOpen ? 'main-content--expanded' : 'main-content--collapsed'}`}>
        {/* Header */}
        <header className="main-header">
          <div className="main-header__left">
            <button
              className="main-header__menu-toggle"
              onClick={() => setSidebarOpen(!sidebarOpen)}
              aria-label="Toggle menu"
            >
              ☰
            </button>
            <h1 className="main-header__title">
              {navItems.find(item => isActive(item.path))?.label || 'Dashboard'}
            </h1>
          </div>

          <div className="main-header__right">
            {/* User Menu */}
            <div className="user-menu">
              <button
                className="user-menu__trigger"
                onClick={() => setUserMenuOpen(!userMenuOpen)}
              >
                <div className="user-menu__avatar">
                  {user?.first_name?.charAt(0) || 'U'}
                </div>
              </button>

              {userMenuOpen && (
                <div className="user-menu__dropdown">
                  <div className="user-menu__header">
                    <div className="user-menu__name">
                      {user?.first_name} {user?.last_name}
                    </div>
                    <div className="user-menu__email">{user?.email}</div>
                  </div>
                  <div className="user-menu__divider" />
                  <Link to="/settings" className="user-menu__item">
                    ⚙️ Settings
                  </Link>
                  <button className="user-menu__item user-menu__item--danger" onClick={handleLogout}>
                    🚪 Logout
                  </button>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="page-content">
          <Outlet />
        </main>
      </div>

      {/* Backdrop for mobile */}
      {sidebarOpen && (
        <div
          className="sidebar-backdrop"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  )
}
