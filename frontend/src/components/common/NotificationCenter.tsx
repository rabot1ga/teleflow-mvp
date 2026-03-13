import { useState } from 'react'
import { useWebSocket } from '@/hooks/useWebSocket'
import { Badge } from '@/components/ui'
import './NotificationCenter.css'

interface Notification {
  id: string
  type: 'info' | 'success' | 'warning' | 'error'
  title: string
  message: string
  timestamp: string
  read: boolean
}

export function NotificationCenter() {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [isOpen, setIsOpen] = useState(false)

  // Listen for WebSocket notifications
  useWebSocket('notification', (message) => {
    const notification: Notification = {
      id: message.data.id || Date.now().toString(),
      type: message.data.type || 'info',
      title: message.data.title || 'Notification',
      message: message.data.message,
      timestamp: message.timestamp,
      read: false,
    }

    setNotifications(prev => [notification, ...prev.slice(0, 49)]) // Keep last 50
    setUnreadCount(prev => prev + 1)
  })

  // Listen for article events
  useWebSocket('article_approved', (message) => {
    const notification: Notification = {
      id: message.data.article_id,
      type: 'success',
      title: 'Article Approved',
      message: `Article "${message.data.title}" has been approved`,
      timestamp: message.timestamp,
      read: false,
    }

    setNotifications(prev => [notification, ...prev.slice(0, 49)])
    setUnreadCount(prev => prev + 1)
  })

  // Listen for broadcast events
  useWebSocket('broadcast_completed', (message) => {
    const notification: Notification = {
      id: message.data.broadcast_id,
      type: 'success',
      title: 'Broadcast Completed',
      message: `Broadcast sent to ${message.data.delivered_count} recipients`,
      timestamp: message.timestamp,
      read: false,
    }

    setNotifications(prev => [notification, ...prev.slice(0, 49)])
    setUnreadCount(prev => prev + 1)
  })

  const markAsRead = (id: string) => {
    setNotifications(prev =>
      prev.map(n => n.id === id ? { ...n, read: true } : n)
    )
    setUnreadCount(prev => Math.max(0, prev - 1))
  }

  const markAllAsRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })))
    setUnreadCount(0)
  }

  const clearAll = () => {
    setNotifications([])
    setUnreadCount(0)
  }

  const getBadgeVariant = (type: Notification['type']) => {
    switch (type) {
      case 'success': return 'success'
      case 'warning': return 'warning'
      case 'error': return 'danger'
      default: return 'info'
    }
  }

  const getIcon = (type: Notification['type']) => {
    switch (type) {
      case 'success': return '✅'
      case 'warning': return '⚠️'
      case 'error': return '❌'
      default: return 'ℹ️'
    }
  }

  return (
    <div className="notification-center">
      <button
        className="notification-center__trigger"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Notifications"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
          <path d="M13.73 21a2 2 0 0 1-3.46 0" />
        </svg>
        {unreadCount > 0 && (
          <Badge variant="danger" size="sm" className="notification-center__badge">
            {unreadCount > 99 ? '99+' : unreadCount}
          </Badge>
        )}
      </button>

      {isOpen && (
        <div className="notification-center__dropdown">
          <div className="notification-center__header">
            <h3>Notifications</h3>
            <div className="notification-center__actions">
              <button onClick={markAllAsRead} className="notification-center__action">
                Mark all read
              </button>
              <button onClick={clearAll} className="notification-center__action">
                Clear all
              </button>
            </div>
          </div>

          <div className="notification-center__list">
            {notifications.length === 0 ? (
              <div className="notification-center__empty">
                <p>No notifications</p>
              </div>
            ) : (
              notifications.map(notification => (
                <div
                  key={notification.id}
                  className={`notification-center__item ${!notification.read ? 'notification-center__item--unread' : ''}`}
                  onClick={() => markAsRead(notification.id)}
                >
                  <span className="notification-center__icon">{getIcon(notification.type)}</span>
                  <div className="notification-center__content">
                    <div className="notification-center__title">
                      <Badge variant={getBadgeVariant(notification.type)} size="sm">
                        {notification.type}
                      </Badge>
                      <span>{notification.title}</span>
                    </div>
                    <p className="notification-center__message">{notification.message}</p>
                    <span className="notification-center__time">
                      {new Date(notification.timestamp).toLocaleString()}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  )
}
