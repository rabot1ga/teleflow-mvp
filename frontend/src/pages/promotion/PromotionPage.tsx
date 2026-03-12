import { useState } from 'react'
import { Card, StatCard, Button, Table, Badge, Modal, Select, PageHeader, Tabs } from '@/components/ui'
import { promotionApi, type PromotionTask } from '@/services/promotionApi'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'

function TasksTab() {
  const [filterType, setFilterType] = useState<string>('')
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [selectedType, setSelectedType] = useState<string>('parse')
  const queryClient = useQueryClient()

  const { data: tasks, isLoading } = useQuery({
    queryKey: ['promotion-tasks'],
    queryFn: () => promotionApi.getTasks('550e8400-e29b-41d4-a716-446655440000', { task_type: filterType }).then(r => r.data.data),
  })

  const startMutation = useMutation({
    mutationFn: (id: string) => promotionApi.startTask(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['promotion-tasks'] })
      toast.success('Task started')
    },
  })

  const createMutation = useMutation({
    mutationFn: (data: Partial<PromotionTask>) => promotionApi.createTask(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['promotion-tasks'] })
      setShowCreateModal(false)
      toast.success('Task created')
    },
  })

  const statusMap: Record<string, 'success' | 'warning' | 'danger' | 'neutral'> = {
    'pending': 'neutral',
    'running': 'warning',
    'completed': 'success',
    'failed': 'danger',
    'cancelled': 'danger',
  }

  const columns = [
    { key: 'name', title: 'Name' },
    { key: 'task_type', title: 'Type' },
    {
      key: 'status',
      title: 'Status',
      render: (item: PromotionTask) => (
        <Badge variant={statusMap[item.status] || 'neutral'}>
          {item.status}
        </Badge>
      ),
    },
    { key: 'success_count', title: 'Success' },
    { key: 'failed_count', title: 'Failed' },
    {
      key: 'actions',
      title: 'Actions',
      render: (item: PromotionTask) => (
        <div className="d-flex gap-2">
          {item.status === 'pending' && (
            <Button
              size="sm"
              variant="success"
              onClick={() => startMutation.mutate(item.id)}
              disabled={startMutation.isPending}
            >
              {startMutation.isPending ? '...' : 'Start'}
            </Button>
          )}
          <Button size="sm" variant="outline" onClick={() => toast.success('View results')}>
            Results
          </Button>
        </div>
      ),
    },
  ]

  const taskTypeOptions = [
    { value: '', label: 'All Types' },
    { value: 'parse', label: 'Parse' },
    { value: 'invite', label: 'Invite' },
    { value: 'masslook', label: 'Masslook' },
    { value: 'comment', label: 'Comment' },
  ]

  return (
    <>
      <div className="d-flex justify-content-between items-center mb-4">
        <div>
          <Select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            options={taskTypeOptions}
          />
        </div>
        <Button onClick={() => setShowCreateModal(true)}>+ Create Task</Button>
      </div>

      <Card>
        {isLoading ? (
          <div className="text-center text-muted py-6">Loading...</div>
        ) : (
          <Table data={tasks || []} columns={columns} />
        )}
      </Card>

      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="Create Promotion Task"
        size="lg"
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowCreateModal(false)}>
              Cancel
            </Button>
            <Button variant="primary" onClick={() => handleCreateTask()}>
              Create
            </Button>
          </>
        }
      >
        <div className="mb-4">
          <label className="tf-select__label">Task Type</label>
          <Select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            options={[
              { value: 'parse', label: 'Parse Users' },
              { value: 'invite', label: 'Invite Users' },
              { value: 'masslook', label: 'Masslook' },
              { value: 'comment', label: 'Comment' },
            ]}
          />
        </div>

        <div className="bg-primary bg-opacity-10 border border-primary rounded p-4 mb-4">
          <p className="font-semibold m-0">
            {selectedType === 'parse' && '📊 Parse users from a Telegram channel'}
            {selectedType === 'invite' && '👥 Invite parsed users to your channel'}
            {selectedType === 'masslook' && '👀 View stories from target users'}
            {selectedType === 'comment' && '💬 Post comments on channel posts'}
          </p>
        </div>

        <div className="text-center text-muted py-6">
          <p>Configuration form for <strong>{selectedType}</strong> task</p>
          <small>Full wizard will be implemented here</small>
        </div>
      </Modal>
    </>
  )

  function handleCreateTask() {
    createMutation.mutate({
      project_id: '550e8400-e29b-41d4-a716-446655440000',
      name: `${selectedType.charAt(0).toUpperCase() + selectedType.slice(1)} Task`,
      task_type: selectedType as PromotionTask['task_type'],
      status: 'pending',
      config: {},
    })
  }
}

function StatsTab() {
  return (
    <div className="text-center text-muted py-8">
      <svg className="mx-auto mb-4" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
        <line x1="18" y1="20" x2="18" y2="10" />
        <line x1="12" y1="20" x2="12" y2="4" />
        <line x1="6" y1="20" x2="6" y2="14" />
      </svg>
      <p className="text-lg font-medium">Promotion statistics coming soon</p>
      <p className="text-sm">Detailed analytics for all promotion activities</p>
    </div>
  )
}

export function PromotionPage() {
  const [activeTab, setActiveTab] = useState<'tasks' | 'stats'>('tasks')

  const tabs = [
    { id: 'tasks', label: 'Tasks' },
    { id: 'stats', label: 'Statistics' },
  ]

  return (
    <div>
      <PageHeader
        title="Promotion"
        description="Parse, invite, and engage with Telegram users"
      />

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard title="Total Tasks" value="12" icon="📋" />
        <StatCard title="Running" value="2" icon="🔄" />
        <StatCard title="Completed" value="8" icon="✅" />
        <StatCard title="Total Success" value="1,234" icon="🎉" />
      </div>

      <Tabs tabs={tabs} activeTab={activeTab} onChange={(tab) => setActiveTab(tab as any)}>
        {activeTab === 'tasks' && <TasksTab />}
        {activeTab === 'stats' && <StatsTab />}
      </Tabs>
    </div>
  )
}
