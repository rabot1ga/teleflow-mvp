import { Card, StatCard, PageHeader, Button } from '@/components/ui'
import './DashboardPage.css'

export function DashboardPage() {
  return (
    <div className="dashboard-page">
      <PageHeader
        title="Dashboard"
        description="Overview of your TeleFlow platform activity"
        action={
          <Button variant="primary" size="md">
            📊 Refresh
          </Button>
        }
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
          <Button variant="primary" leftIcon="📰">
            Add Source
          </Button>
          <Button variant="primary" leftIcon="🎯">
            Create Funnel
          </Button>
          <Button variant="primary" leftIcon="📤">
            New Broadcast
          </Button>
          <Button variant="outline" leftIcon="⚙️">
            Settings
          </Button>
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
