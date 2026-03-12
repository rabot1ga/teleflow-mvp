import { useState } from 'react'
import { Card, StatCard, Button, SimpleAreaChart, SimpleBarChart, SimplePieChart, Breadcrumbs, PageHeader } from '@/components/ui'
import { analyticsApi } from '@/services/analyticsApi'
import { useQuery } from '@tanstack/react-query'

export function AnalyticsPage() {
  const [days, setDays] = useState(30)
  const [activeTab, setActiveTab] = useState<'overview' | 'content' | 'funnels' | 'broadcasts'>('overview')

  const { data: overview, isLoading } = useQuery({
    queryKey: ['analytics-overview', days],
    queryFn: () => analyticsApi.getOverview('550e8400-e29b-41d4-a716-446655440000', days).then(r => r.data.data),
  })

  const { data: contentStats } = useQuery({
    queryKey: ['analytics-content', days],
    queryFn: () => analyticsApi.getContentStats('550e8400-e29b-41d4-a716-446655440000', days).then(r => r.data.data),
  })

  // Mock data for charts (will be replaced with real API data)
  const activityData = [
    { date: 'Week 1', articles: 45, published: 32, funnel: 120 },
    { date: 'Week 2', articles: 52, published: 41, funnel: 145 },
    { date: 'Week 3', articles: 38, published: 29, funnel: 98 },
    { date: 'Week 4', articles: 65, published: 54, funnel: 187 },
  ]

  const categoryData = [
    { name: 'Technology', value: 35, color: '#0d6efd' },
    { name: 'Business', value: 25, color: '#198754' },
    { name: 'Science', value: 20, color: '#ffc107' },
    { name: 'Politics', value: 12, color: '#dc3545' },
    { name: 'Other', value: 8, color: '#6f42c1' },
  ]

  const funnelData = [
    { step: 'Entry', users: 2345 },
    { step: 'Step 1', users: 1876 },
    { step: 'Step 2', users: 1234 },
    { step: 'Step 3', users: 876 },
    { step: 'Complete', users: 543 },
  ]

  return (
    <div>
      <Breadcrumbs />
      <PageHeader
        title="Analytics"
        description="Comprehensive analytics and insights"
        action={
          <div className="d-flex gap-2">
            <Button
              variant={days === 7 ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setDays(7)}
            >
              7D
            </Button>
            <Button
              variant={days === 30 ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setDays(30)}
            >
              30D
            </Button>
            <Button
              variant={days === 90 ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setDays(90)}
            >
              90D
            </Button>
          </div>
        }
      />

      {/* Tabs */}
      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'content' ? 'active' : ''}`}
            onClick={() => setActiveTab('content')}
          >
            Content
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'funnels' ? 'active' : ''}`}
            onClick={() => setActiveTab('funnels')}
          >
            Funnels
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'broadcasts' ? 'active' : ''}`}
            onClick={() => setActiveTab('broadcasts')}
          >
            Broadcasts
          </button>
        </li>
      </ul>

      {isLoading ? (
        <div className="text-center py-5">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      ) : (
        <>
          {activeTab === 'overview' && (
            <>
              {/* Overview Stats */}
              <div className="row g-4 mb-4">
                <div className="col-md-3">
                  <StatCard
                    title="Articles Created"
                    value={overview?.totals.articles_created || 0}
                    icon="📰"
                    trend={{ value: 12, isPositive: true }}
                  />
                </div>
                <div className="col-md-3">
                  <StatCard
                    title="Articles Published"
                    value={overview?.totals.articles_published || 0}
                    icon="📤"
                    trend={{ value: 8, isPositive: true }}
                  />
                </div>
                <div className="col-md-3">
                  <StatCard
                    title="Funnel Entries"
                    value={overview?.totals.funnel_entries || 0}
                    icon="🎯"
                    trend={{ value: 23, isPositive: true }}
                  />
                </div>
                <div className="col-md-3">
                  <StatCard
                    title="Messages Sent"
                    value={overview?.totals.messages_delivered || 0}
                    icon="✉️"
                    trend={{ value: 15, isPositive: true }}
                  />
                </div>
              </div>

              {/* Activity Chart */}
              <div className="row g-4">
                <div className="col-md-8">
                  <Card title="Activity Overview">
                    <SimpleAreaChart
                      data={activityData}
                      xKey="date"
                      yKeys={[
                        { key: 'articles', color: '#0d6efd', name: 'Articles' },
                        { key: 'published', color: '#198754', name: 'Published' },
                        { key: 'funnel', color: '#ffc107', name: 'Funnel Entries' },
                      ]}
                      height={350}
                    />
                  </Card>
                </div>
                <div className="col-md-4">
                  <Card title="Categories Distribution">
                    <SimplePieChart
                      data={categoryData}
                      height={300}
                      showLegend
                    />
                  </Card>
                </div>
              </div>

              {/* Recent Activity */}
              <div className="mt-4">
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
            </>
          )}

          {activeTab === 'content' && (
            <div className="row g-4">
              <div className="col-md-12">
                <Card title="Content Performance">
                  <SimpleBarChart
                    data={contentStats?.daily || []}
                    xKey="date"
                    yKey="created"
                    height={350}
                    color="#0d6efd"
                  />
                </Card>
              </div>
              <div className="col-md-6">
                <Card title="Articles by Category">
                  <SimplePieChart
                    data={categoryData}
                    height={300}
                  />
                </Card>
              </div>
              <div className="col-md-6">
                <Card title="Approval Rate">
                  <div className="text-center py-5">
                    <h1 className="display-4 text-success">
                      {contentStats?.approval_rate?.toFixed(1) || 0}%
                    </h1>
                    <p className="text-muted">Average approval rate</p>
                  </div>
                </Card>
              </div>
            </div>
          )}

          {activeTab === 'funnels' && (
            <div className="row g-4">
              <div className="col-md-8">
                <Card title="Funnel Conversion">
                  <SimpleBarChart
                    data={funnelData}
                    xKey="step"
                    yKey="users"
                    height={350}
                    color="#198754"
                  />
                </Card>
              </div>
              <div className="col-md-4">
                <Card title="Funnel Stats">
                  <div className="text-center py-4">
                    <h3 className="mb-4">Conversion Rate</h3>
                    <h1 className="display-3 text-primary">
                      {((funnelData[funnelData.length - 1].users / funnelData[0].users) * 100).toFixed(1)}%
                    </h1>
                    <p className="text-muted mt-2">
                      {funnelData[0].users} entries → {funnelData[funnelData.length - 1].users} completions
                    </p>
                  </div>
                </Card>
              </div>
            </div>
          )}

          {activeTab === 'broadcasts' && (
            <div className="row g-4">
              <div className="col-md-12">
                <Card title="Broadcast Performance">
                  <div className="text-center text-muted py-5">
                    <span className="fs-1">📊</span>
                    <p className="mt-3">Broadcast statistics will be here</p>
                    <small>Delivery rates, open rates, click rates</small>
                  </div>
                </Card>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
