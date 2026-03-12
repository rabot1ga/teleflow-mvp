import { Card, StatCard, Breadcrumbs, PageHeader } from '@/components/ui'

export function DashboardPage() {
  return (
    <div>
      <Breadcrumbs />
      <PageHeader
        title="Dashboard"
        description="Overview of your TeleFlow platform activity"
      />
      
      {/* Stats Cards */}
      <div className="row g-4 mb-4">
        <div className="col-md-3">
          <StatCard
            title="Articles"
            value="1,234"
            icon="📰"
            trend={{ value: 12, isPositive: true }}
          />
        </div>
        
        <div className="col-md-3">
          <StatCard
            title="Published"
            value="856"
            icon="📤"
            trend={{ value: 8, isPositive: true }}
          />
        </div>
        
        <div className="col-md-3">
          <StatCard
            title="Funnel Entries"
            value="2,345"
            icon="🎯"
            trend={{ value: 23, isPositive: true }}
          />
        </div>
        
        <div className="col-md-3">
          <StatCard
            title="Messages Sent"
            value="12,456"
            icon="✉️"
            trend={{ value: 15, isPositive: true }}
          />
        </div>
      </div>

      {/* Charts and Activity */}
      <div className="row g-4">
        <div className="col-md-8">
          <Card title="Activity Overview">
            <div className="text-center text-muted py-5" style={{ minHeight: '300px' }}>
              <div className="mb-3">
                <span className="fs-1">📊</span>
              </div>
              <p className="mb-1">Chart will be rendered here</p>
              <small className="text-muted">Using Recharts library</small>
              <div className="mt-4">
                <div className="bg-light rounded" style={{ height: '200px' }} />
              </div>
            </div>
          </Card>
        </div>
        
        <div className="col-md-4">
          <Card title="Recent Activity">
            <ul className="list-unstyled mb-0">
              <li className="py-3 border-bottom">
                <div className="d-flex justify-content-between">
                  <div>
                    <p className="mb-1">Article approved: "Breaking News"</p>
                    <small className="text-muted">2 minutes ago</small>
                  </div>
                  <span className="badge bg-success">Content</span>
                </div>
              </li>
              <li className="py-3 border-bottom">
                <div className="d-flex justify-content-between">
                  <div>
                    <p className="mb-1">Broadcast completed: 1,234 sent</p>
                    <small className="text-muted">15 minutes ago</small>
                  </div>
                  <span className="badge bg-primary">Funnel</span>
                </div>
              </li>
              <li className="py-3 border-bottom">
                <div className="d-flex justify-content-between">
                  <div>
                    <p className="mb-1">New user joined funnel</p>
                    <small className="text-muted">1 hour ago</small>
                  </div>
                  <span className="badge bg-info">User</span>
                </div>
              </li>
              <li className="py-3">
                <div className="d-flex justify-content-between">
                  <div>
                    <p className="mb-1">Parsing task completed: 500 users</p>
                    <small className="text-muted">2 hours ago</small>
                  </div>
                  <span className="badge bg-warning">Promotion</span>
                </div>
              </li>
            </ul>
          </Card>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="row g-4 mt-4">
        <div className="col-12">
          <Card title="Quick Actions">
            <div className="d-flex gap-3 flex-wrap">
              <button className="btn btn-primary">
                <span className="me-2">➕</span>
                Add Source
              </button>
              <button className="btn btn-success">
                <span className="me-2">🎯</span>
                Create Funnel
              </button>
              <button className="btn btn-info text-white">
                <span className="me-2">📤</span>
                New Broadcast
              </button>
              <button className="btn btn-warning">
                <span className="me-2">📋</span>
                Parse Users
              </button>
              <button className="btn btn-secondary">
                <span className="me-2">🤖</span>
                Add Userbot
              </button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
