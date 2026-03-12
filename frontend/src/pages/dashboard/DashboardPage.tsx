import { Card } from '@/components/ui'

export function DashboardPage() {
  return (
    <div>
      <div className="mb-4">
        <h1 className="h2 mb-1">Dashboard</h1>
        <p className="text-muted">Overview of your TeleFlow platform activity</p>
      </div>

      {/* Stats Grid */}
      <div className="d-flex flex-wrap gap-4 mb-4">
        {/* Articles Card */}
        <Card title="Articles" style={{ flex: '1 1 250px' }}>
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h2 className="h3 mb-0">1,234</h2>
              <small className="text-muted">Total articles</small>
            </div>
            <span className="fs-1">📰</span>
          </div>
          <div className="mt-3">
            <span className="badge bg-success">↑ 12%</span>
            <small className="text-muted ms-2">from last month</small>
          </div>
        </Card>

        {/* Sources Card */}
        <Card title="Sources" style={{ flex: '1 1 250px' }}>
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h2 className="h3 mb-0">8</h2>
              <small className="text-muted">Active sources</small>
            </div>
            <span className="fs-1">📡</span>
          </div>
          <div className="mt-3">
            <span className="badge bg-success">↑ 2</span>
            <small className="text-muted ms-2">new this week</small>
          </div>
        </Card>

        {/* Funnels Card */}
        <Card title="Funnels" style={{ flex: '1 1 250px' }}>
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h2 className="h3 mb-0">5</h2>
              <small className="text-muted">Active funnels</small>
            </div>
            <span className="fs-1">🎯</span>
          </div>
          <div className="mt-3">
            <span className="badge bg-secondary">No change</span>
            <small className="text-muted ms-2">stable</small>
          </div>
        </Card>

        {/* Subscribers Card */}
        <Card title="Subscribers" style={{ flex: '1 1 250px' }}>
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h2 className="h3 mb-0">2,847</h2>
              <small className="text-muted">Total subscribers</small>
            </div>
            <span className="fs-1">👥</span>
          </div>
          <div className="mt-3">
            <span className="badge bg-success">↑ 8%</span>
            <small className="text-muted ms-2">from last month</small>
          </div>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card title="Quick Actions">
        <div className="d-flex flex-wrap gap-3">
          <button className="btn btn-primary">📰 Add Source</button>
          <button className="btn btn-primary">🎯 Create Funnel</button>
          <button className="btn btn-primary">📤 New Broadcast</button>
          <button className="btn btn-outline-secondary">⚙️ Settings</button>
        </div>
      </Card>

      {/* Recent Activity */}
      <Card title="Recent Activity" className="mt-4">
        <div className="text-center text-muted py-5">
          <p className="mb-2">No recent activity</p>
          <small>Start by adding a content source</small>
        </div>
      </Card>
    </div>
  )
}
