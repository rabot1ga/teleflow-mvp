import { useState } from 'react'
import { Card, StatCard, Button, PageHeader, Tabs, Badge } from '@/components/ui'
import { analyticsApi } from '@/services/analyticsApi'
import { useQuery } from '@tanstack/react-query'

function OverviewTab({ days }: { days: number }) {
  const { data: overview, isLoading } = useQuery({
    queryKey: ['analytics-overview', days],
    queryFn: () => analyticsApi.getOverview('550e8400-e29b-41d4-a716-446655440000', days).then(r => r.data.data),
  })

  if (isLoading) {
    return <div className="text-center text-muted py-6">Loading...</div>
  }

  return (
    <div className="d-flex flex-col gap-6">
      {/* Overview Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Articles Created"
          value={overview?.totals.articles_created || 0}
          icon="📰"
          trend={{ value: 12, isPositive: true }}
        />
        <StatCard
          title="Articles Published"
          value={overview?.totals.articles_published || 0}
          icon="📤"
          trend={{ value: 8, isPositive: true }}
        />
        <StatCard
          title="Funnel Entries"
          value={overview?.totals.funnel_entries || 0}
          icon="🎯"
          trend={{ value: 23, isPositive: true }}
        />
        <StatCard
          title="Messages Sent"
          value={overview?.totals.messages_delivered || 0}
          icon="✉️"
          trend={{ value: 15, isPositive: true }}
        />
      </div>

      {/* Charts placeholder */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <Card title="Activity Overview" className="lg:col-span-2">
          <div className="text-center text-muted py-8">
            <svg className="mx-auto mb-4" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <line x1="18" y1="20" x2="18" y2="10" />
              <line x1="12" y1="20" x2="12" y2="4" />
              <line x1="6" y1="20" x2="6" y2="14" />
            </svg>
            <p>Charts will be implemented here</p>
          </div>
        </Card>
        <Card title="Categories">
          <div className="text-center text-muted py-8">
            <p className="text-sm">Distribution chart</p>
          </div>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card title="Recent Activity">
        <ul className="list-none p-0 m-0">
          <li className="py-3 border-b d-flex justify-content-between">
            <div>
              <p className="m-0 font-medium">Article approved: "Breaking News"</p>
              <small className="text-muted">2 minutes ago</small>
            </div>
            <Badge variant="success">Content</Badge>
          </li>
          <li className="py-3 border-b d-flex justify-content-between">
            <div>
              <p className="m-0 font-medium">Broadcast completed: 1,234 sent</p>
              <small className="text-muted">15 minutes ago</small>
            </div>
            <Badge variant="primary">Funnel</Badge>
          </li>
          <li className="py-3 border-b d-flex justify-content-between">
            <div>
              <p className="m-0 font-medium">New user joined funnel</p>
              <small className="text-muted">1 hour ago</small>
            </div>
            <Badge variant="info">User</Badge>
          </li>
          <li className="py-3 d-flex justify-content-between">
            <div>
              <p className="m-0 font-medium">Parsing task completed: 500 users</p>
              <small className="text-muted">2 hours ago</small>
            </div>
            <Badge variant="warning">Promotion</Badge>
          </li>
        </ul>
      </Card>
    </div>
  )
}

function ContentTab({ days }: { days: number }) {
  const { data: contentStats } = useQuery({
    queryKey: ['analytics-content', days],
    queryFn: () => analyticsApi.getContentStats('550e8400-e29b-41d4-a716-446655440000', days).then(r => r.data.data),
  })

  return (
    <div className="d-flex flex-col gap-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card title="Content Performance">
          <div className="text-center text-muted py-8">
            <p>Performance chart will be here</p>
          </div>
        </Card>
        <Card title="Approval Rate">
          <div className="text-center py-8">
            <h1 className="text-4xl font-bold text-success m-0">
              {contentStats?.approval_rate?.toFixed(1) || 0}%
            </h1>
            <p className="text-muted mt-2">Average approval rate</p>
          </div>
        </Card>
      </div>
    </div>
  )
}

function FunnelsTab() {
  const funnelData = [
    { step: 'Entry', users: 2345 },
    { step: 'Step 1', users: 1876 },
    { step: 'Step 2', users: 1234 },
    { step: 'Step 3', users: 876 },
    { step: 'Complete', users: 543 },
  ]

  const conversionRate = ((funnelData[funnelData.length - 1].users / funnelData[0].users) * 100).toFixed(1)

  return (
    <div className="d-flex flex-col gap-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <Card title="Funnel Conversion" className="lg:col-span-2">
          <div className="text-center text-muted py-8">
            <p>Funnel chart will be here</p>
          </div>
        </Card>
        <Card title="Stats">
          <div className="text-center py-8">
            <h3 className="m-0 mb-4">Conversion Rate</h3>
            <h1 className="text-4xl font-bold text-primary m-0">
              {conversionRate}%
            </h1>
            <p className="text-muted mt-2">
              {funnelData[0].users} entries → {funnelData[funnelData.length - 1].users} completions
            </p>
          </div>
        </Card>
      </div>
    </div>
  )
}

function BroadcastsTab() {
  return (
    <Card title="Broadcast Performance">
      <div className="text-center text-muted py-8">
        <svg className="mx-auto mb-4" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M22 2L11 13" />
          <path d="M22 2L15 22L11 13L2 9L22 2Z" />
        </svg>
        <p className="text-lg font-medium">Broadcast statistics coming soon</p>
        <p className="text-sm">Delivery rates, open rates, click rates</p>
      </div>
    </Card>
  )
}

export function AnalyticsPage() {
  const [days, setDays] = useState(30)
  const [activeTab, setActiveTab] = useState<'overview' | 'content' | 'funnels' | 'broadcasts'>('overview')

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'content', label: 'Content' },
    { id: 'funnels', label: 'Funnels' },
    { id: 'broadcasts', label: 'Broadcasts' },
  ]

  return (
    <div>
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

      <Tabs tabs={tabs} activeTab={activeTab} onChange={(tab) => setActiveTab(tab as any)}>
        {activeTab === 'overview' && <OverviewTab days={days} />}
        {activeTab === 'content' && <ContentTab days={days} />}
        {activeTab === 'funnels' && <FunnelsTab />}
        {activeTab === 'broadcasts' && <BroadcastsTab />}
      </Tabs>
    </div>
  )
}
