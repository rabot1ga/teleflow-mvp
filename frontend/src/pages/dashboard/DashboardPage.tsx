import { useState } from 'react'
import { Card, StatCard, Button } from '@/components/ui'
import { useAuthStore } from '../../stores/authStore'
import './DashboardPage.css'

export function DashboardPage() {
  const { user } = useAuthStore()
  const [timeRange, setTimeRange] = useState('7d')

  const quickActions = [
    { icon: '📰', label: 'Add Source', action: () => console.log('Add Source') },
    { icon: '🎯', label: 'Create Funnel', action: () => console.log('Create Funnel') },
    { icon: '📤', label: 'New Broadcast', action: () => console.log('New Broadcast') },
    { icon: '⚙️', label: 'Settings', action: () => console.log('Settings') },
  ]

  const recentActivity = [
    { type: 'article', title: 'Article approved', time: '2 min ago', icon: '✅' },
    { type: 'broadcast', title: 'Broadcast completed', time: '15 min ago', icon: '📤' },
    { type: 'funnel', title: 'New funnel entry', time: '1 hour ago', icon: '🎯' },
    { type: 'user', title: 'User subscribed', time: '2 hours ago', icon: '👤' },
  ]

  const topSources = [
    { name: 'Habr RSS', articles: 42, status: 'active' },
    { name: 'TechCrunch', articles: 28, status: 'active' },
    { name: 'VC.ru', articles: 15, status: 'warning' },
  ]

  return (
    <div className="dashboard-page">
      {/* Header */}
      <div className="dashboard-page__header">
        <div className="dashboard-page__welcome">
          <h1 className="dashboard-page__title">
            Welcome back, {user?.first_name || 'User'}! 👋
          </h1>
          <p className="dashboard-page__subtitle">
            Here's what's happening with your Telegram operations today.
          </p>
        </div>
        <div className="dashboard-page__actions">
          <div className="dashboard-page__time-range">
            <button
              className={`dashboard-page__time-btn ${timeRange === '7d' ? 'active' : ''}`}
              onClick={() => setTimeRange('7d')}
            >
              7D
            </button>
            <button
              className={`dashboard-page__time-btn ${timeRange === '30d' ? 'active' : ''}`}
              onClick={() => setTimeRange('30d')}
            >
              30D
            </button>
            <button
              className={`dashboard-page__time-btn ${timeRange === '90d' ? 'active' : ''}`}
              onClick={() => setTimeRange('90d')}
            >
              90D
            </button>
          </div>
          <Button variant="primary" leftIcon="📥">
            Refresh Data
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="dashboard-page__stats">
        <StatCard
          title="Total Articles"
          value="1,234"
          trend={{ value: 12, isPositive: true }}
          icon="📰"
          color="purple"
        />
        <StatCard
          title="Active Sources"
          value="8"
          trend={{ value: 2, isPositive: true }}
          icon="📡"
          color="blue"
        />
        <StatCard
          title="Active Funnels"
          value="5"
          trend={{ value: -3, isPositive: false }}
          icon="🎯"
          color="orange"
        />
        <StatCard
          title="Subscribers"
          value="2,847"
          trend={{ value: 8, isPositive: true }}
          icon="👥"
          color="green"
        />
      </div>

      {/* Main Content Grid */}
      <div className="dashboard-page__grid">
        {/* Left Column */}
        <div className="dashboard-page__column dashboard-page__column--main">
          {/* Quick Actions */}
          <Card className="dashboard-page__card">
            <div className="dashboard-page__card-header">
              <h3 className="dashboard-page__card-title">Quick Actions</h3>
            </div>
            <div className="dashboard-page__quick-actions">
              {quickActions.map((action, index) => (
                <button
                  key={index}
                  className="dashboard-page__action-btn"
                  onClick={action.action}
                >
                  <span className="dashboard-page__action-icon">{action.icon}</span>
                  <span className="dashboard-page__action-label">{action.label}</span>
                </button>
              ))}
            </div>
          </Card>

          {/* Activity Chart Placeholder */}
          <Card className="dashboard-page__card dashboard-page__card--large">
            <div className="dashboard-page__card-header">
              <h3 className="dashboard-page__card-title">Activity Overview</h3>
              <div className="dashboard-page__card-actions">
                <Button variant="ghost" size="sm">View All</Button>
              </div>
            </div>
            <div className="dashboard-page__chart-placeholder">
              <div className="dashboard-page__chart-icon">📊</div>
              <p className="dashboard-page__chart-text">Interactive chart will be displayed here</p>
              <p className="dashboard-page__chart-subtext">Articles, funnels, and broadcasts over time</p>
            </div>
          </Card>
        </div>

        {/* Right Column */}
        <div className="dashboard-page__column dashboard-page__column--side">
          {/* Recent Activity */}
          <Card className="dashboard-page__card">
            <div className="dashboard-page__card-header">
              <h3 className="dashboard-page__card-title">Recent Activity</h3>
              <Button variant="ghost" size="sm">View All</Button>
            </div>
            <div className="dashboard-page__activity-list">
              {recentActivity.map((activity, index) => (
                <div key={index} className="dashboard-page__activity-item">
                  <span className="dashboard-page__activity-icon">{activity.icon}</span>
                  <div className="dashboard-page__activity-content">
                    <p className="dashboard-page__activity-title">{activity.title}</p>
                    <span className="dashboard-page__activity-time">{activity.time}</span>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Top Sources */}
          <Card className="dashboard-page__card">
            <div className="dashboard-page__card-header">
              <h3 className="dashboard-page__card-title">Top Sources</h3>
              <Button variant="ghost" size="sm">Manage</Button>
            </div>
            <div className="dashboard-page__sources-list">
              {topSources.map((source, index) => (
                <div key={index} className="dashboard-page__source-item">
                  <div className="dashboard-page__source-info">
                    <p className="dashboard-page__source-name">{source.name}</p>
                    <p className="dashboard-page__source-count">{source.articles} articles</p>
                  </div>
                  <span className={`dashboard-page__source-status dashboard-page__source-status--${source.status}`} />
                </div>
              ))}
            </div>
          </Card>

          {/* Performance Widget */}
          <Card className="dashboard-page__card dashboard-page__card--gradient">
            <div className="dashboard-page__performance">
              <div className="dashboard-page__performance-icon">🚀</div>
              <h4 className="dashboard-page__performance-title">Performance Great!</h4>
              <p className="dashboard-page__performance-text">
                Your content is performing 23% better than last week.
              </p>
              <Button variant="secondary" size="sm" fullWidth>
                View Analytics
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
