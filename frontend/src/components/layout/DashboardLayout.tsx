import { useState, useCallback, useEffect } from 'react'
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'
import toast from 'react-hot-toast'
import './DashboardLayout.css'

interface NavItem {
  path: string
  label: string
  icon: React.ReactNode
  category: string
}

const NavIcons = {
  dashboard: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="3" y="3" width="7" height="7" rx="1" />
      <rect x="14" y="3" width="7" height="7" rx="1" />
      <rect x="3" y="14" width="7" height="7" rx="1" />
      <rect x="14" y="14" width="7" height="7" rx="1" />
    </svg>
  ),
  content: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14,2 14,8 20,8" />
      <line x1="16" y1="13" x2="8" y2="13" />
      <line x1="16" y1="17" x2="8" y2="17" />
    </svg>
  ),
  publishing: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <polyline points="22,12 18,12 15,21 9,3 6,12 2,12" />
    </svg>
  ),
  funnels: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <polygon points="22,3 2,3 10,12.46 10,19 14,21 14,12.46" />
    </svg>
  ),
  userbot: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
      <circle cx="12" cy="7" r="4" />
    </svg>
  ),
  promotion: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <polyline points="23,6 13.5,15.5 8.5,10.5 1,18" />
      <polyline points="17,6 23,6 23,12" />
    </svg>
  ),
  analytics: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <line x1="18" y1="20" x2="18" y2="10" />
      <line x1="12" y1="20" x2="12" y2="4" />
      <line x1="6" y1="20" x2="6" y2="14" />
    </svg>
  ),
  settings: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
    </svg>
  ),
}

export function DashboardLayout() {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuthStore()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const [isMobile, setIsMobile] = useState(false)

  // Handle window resize for responsive sidebar
  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth <= 1024
      setIsMobile(mobile)
      if (mobile) {
        setSidebarOpen(false)
      }
    }

    // Initial check
    handleResize()

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  // Handle logout
  const handleLogout = useCallback(() => {
    logout()
    toast.success('Logged out successfully')
    navigate('/login')
  }, [logout, navigate])

  // Toggle sidebar
  const toggleSidebar = useCallback(() => {
    setSidebarOpen(prev => !prev)
  }, [])

  // Close sidebar on mobile when clicking a link
  const handleNavClick = useCallback(() => {
    if (isMobile) {
      setSidebarOpen(false)
    }
  }, [isMobile])

  // Close sidebar when clicking overlay
  const handleOverlayClick = useCallback(() => {
    setSidebarOpen(false)
  }, [])

  const navItems: NavItem[] = [
    { path: '/dashboard', label: 'Dashboard', icon: NavIcons.dashboard, category: 'main' },
    { path: '/content', label: 'Content', icon: NavIcons.content, category: 'operations' },
    { path: '/publishing', label: 'Publishing', icon: NavIcons.publishing, category: 'operations' },
    { path: '/funnels', label: 'Funnels', icon: NavIcons.funnels, category: 'growth' },
    { path: '/userbot', label: 'Userbot', icon: NavIcons.userbot, category: 'growth' },
    { path: '/promotion', label: 'Promotion', icon: NavIcons.promotion, category: 'growth' },
    { path: '/analytics', label: 'Analytics', icon: NavIcons.analytics, category: 'insights' },
    { path: '/settings', label: 'Settings', icon: NavIcons.settings, category: 'settings' },
  ]

  const isActive = useCallback((path: string) => location.pathname.startsWith(path), [location.pathname])

  const groupedNavItems = navItems.reduce((acc, item) => {
    if (!acc[item.category]) {
      acc[item.category] = []
    }
    acc[item.category].push(item)
    return acc
  }, {} as Record<string, NavItem[]>)

  return (
    <div className="dashboard-layout">
      {/* Mobile Overlay - shows when sidebar is open on mobile */}
      {isMobile && sidebarOpen && (
        <div className="sidebar-overlay" onClick={handleOverlayClick} />
      )}
      
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'sidebar--open' : 'sidebar--collapsed'}`}>
        {/* Logo */}
        <div className="sidebar__header">
          <Link to="/dashboard" className="sidebar__logo" onClick={handleNavClick}>
            <div className="sidebar__logo-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
              </svg>
            </div>
            {sidebarOpen && <span className="sidebar__logo-text">TeleFlow</span>}
          </Link>
          <button
            className="sidebar__toggle"
            onClick={toggleSidebar}
            aria-label={sidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
            type="button"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="15,18 9,12 15,6" />
            </svg>
          </button>
        </div>

        {/* Navigation */}
        <nav className="sidebar__nav">
          {Object.entries(groupedNavItems).map(([category, items]) => (
            <div key={category} className="sidebar__group">
              {sidebarOpen && (
                <div className="sidebar__group-title">{category.charAt(0).toUpperCase() + category.slice(1)}</div>
              )}
              {items.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`sidebar__link ${isActive(item.path) ? 'sidebar__link--active' : ''}`}
                  onClick={handleNavClick}
                  title={!sidebarOpen ? item.label : undefined}
                >
                  <span className="sidebar__link-icon">{item.icon}</span>
                  {sidebarOpen && <span className="sidebar__link-label">{item.label}</span>}
                </Link>
              ))}
            </div>
          ))}
        </nav>

        {/* User */}
        <div className="sidebar__footer">
          <div className="sidebar__user">
            <div className="sidebar__user-avatar">
              {user?.first_name?.charAt(0) || user?.email?.charAt(0) || 'U'}
            </div>
            {sidebarOpen && (
              <div className="sidebar__user-info">
                <div className="sidebar__user-name">
                  {user?.first_name || 'User'} {user?.last_name || ''}
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
              className="main-header__toggle"
              onClick={toggleSidebar}
              aria-label="Toggle menu"
              type="button"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="3" y1="12" x2="21" y2="12" />
                <line x1="3" y1="6" x2="21" y2="6" />
                <line x1="3" y1="18" x2="21" y2="18" />
              </svg>
            </button>
            <h1 className="main-header__title">
              {navItems.find((item) => isActive(item.path))?.label || 'Dashboard'}
            </h1>
          </div>

          <div className="main-header__right">
            {/* User Menu */}
            <div className="user-menu">
              <button
                className="user-menu__trigger"
                onClick={() => setUserMenuOpen(!userMenuOpen)}
                aria-label="User menu"
                type="button"
              >
                <div className="user-menu__avatar">
                  {user?.first_name?.charAt(0) || user?.email?.charAt(0) || 'U'}
                </div>
              </button>

              {userMenuOpen && (
                <div className="user-menu__dropdown">
                  <div className="user-menu__header">
                    <div className="user-menu__name">
                      {user?.first_name || 'User'} {user?.last_name || ''}
                    </div>
                    <div className="user-menu__email">{user?.email}</div>
                  </div>
                  <div className="user-menu__divider" />
                  <Link to="/settings" className="user-menu__item" onClick={() => setUserMenuOpen(false)}>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="user-menu__item-icon">
                      <circle cx="12" cy="12" r="3" />
                      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
                    </svg>
                    Settings
                  </Link>
                  <button className="user-menu__item user-menu__item--danger" onClick={handleLogout}>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="user-menu__item-icon">
                      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                      <polyline points="16,17 21,12 16,7" />
                      <line x1="21" y1="12" x2="9" y2="12" />
                    </svg>
                    Logout
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
    </div>
  )
}
