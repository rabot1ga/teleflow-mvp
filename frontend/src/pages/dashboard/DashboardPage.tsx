import { Card, StatCard, PageHeader } from '@/components/ui'
import './DashboardPage.css'

export function DashboardPage() {
  return (
    <div className="dashboard-page">
      <PageHeader
        title="Dashboard"
        description="Overview of your TeleFlow platform activity"
      />

      {/* Stats Grid */}
      <div className="stats-grid">
        <StatCard
          title="Total Articles"
          value="1,234"
          icon="📰"
          trend={{ value: 12, isPositive: true }}
        />
        <StatCard
          title="Active Sources"
          value="8"
          icon="📡"
          trend={{ value: 2, isPositive: true }}
        />
        <StatCard
          title="Active Funnels"
          value="5"
          icon="🎯"
        />
        <StatCard
          title="Subscribers"
          value="2,847"
          icon="👥"
          trend={{ value: 8, isPositive: true }}
        />
      </div>

      {/* Quick Actions */}
      <Card title="Quick Actions" className="mt-6">
        <div className="quick-actions">
          <button className="btn btn-primary">
            <span className="btn-icon">📰</span>
            Add Source
          </button>
          <button className="btn btn-primary">
            <span className="btn-icon">🎯</span>
            Create Funnel
          </button>
          <button className="btn btn-primary">
            <span className="btn-icon">📤</span>
            New Broadcast
          </button>
          <button className="btn btn-outline">
            <span className="btn-icon">⚙️</span>
            Settings
          </button>
        </div>
      </Card>

      {/* Recent Activity */}
      <Card title="Recent Activity" className="mt-6">
        <div className="empty-state">
          <div className="empty-state__icon">📭</div>
          <h3 className="empty-state__title">No recent activity</h3>
          <p className="empty-state__text">
            Start by adding a content source to see activity here
          </p>
        </div>
      </Card>

      {/* Content Overview */}
      <div className="grid-2 mt-6">
        <Card title="Content Performance">
          <div className="empty-state empty-state--small">
            <div className="empty-state__icon">📈</div>
            <p className="text-muted">Analytics coming soon</p>
          </div>
        </Card>
        <Card title="Top Sources">
          <div className="empty-state empty-state--small">
            <div className="empty-state__icon">🔥</div>
            <p className="text-muted">Top sources coming soon</p>
          </div>
        </Card>
      </div>
    </div>
  )
}
