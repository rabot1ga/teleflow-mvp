import { useState } from 'react'
import { Card, StatCard, Button, Table, StatusBadge, Modal, Select } from '@/components/ui'
import { promotionApi, type PromotionTask } from '@/services/promotionApi'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'

export function PromotionPage() {
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

  const statusMap: Record<string, 'pending' | 'running' | 'completed' | 'failed'> = {
    'pending': 'pending',
    'running': 'running',
    'completed': 'completed',
    'failed': 'failed',
    'cancelled': 'failed',
  }

  const taskTypeOptions = [
    { value: 'parse', label: 'Parse Users' },
    { value: 'invite', label: 'Invite Users' },
    { value: 'masslook', label: 'Masslook' },
    { value: 'comment', label: 'Comment' },
  ]

  const columns = [
    { key: 'name', title: 'Name' },
    { key: 'task_type', title: 'Type' },
    {
      key: 'status',
      title: 'Status',
      render: (item: PromotionTask) => (
        <StatusBadge status={statusMap[item.status] || 'pending'} />
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

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1 className="h2 mb-0">Promotion</h1>
        <Button onClick={() => setShowCreateModal(true)}>+ Create Task</Button>
      </div>

      {/* Stats */}
      <div className="row g-4 mb-4">
        <div className="col-md-3">
          <StatCard title="Total Tasks" value={tasks?.length || 0} icon="📋" />
        </div>
        <div className="col-md-3">
          <StatCard title="Running" value={tasks?.filter((t: PromotionTask) => t.status === 'running').length || 0} icon="🔄" />
        </div>
        <div className="col-md-3">
          <StatCard title="Completed" value={tasks?.filter((t: PromotionTask) => t.status === 'completed').length || 0} icon="✅" />
        </div>
        <div className="col-md-3">
          <StatCard title="Total Success" value={tasks?.reduce((sum: number, t: PromotionTask) => sum + t.success_count, 0) || 0} icon="🎉" />
        </div>
      </div>

      {/* Filter */}
      <div className="mb-3">
        <select
          className="form-select w-auto"
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
        >
          <option value="">All Types</option>
          <option value="parse">Parse</option>
          <option value="invite">Invite</option>
          <option value="masslook">Masslook</option>
          <option value="comment">Comment</option>
        </select>
      </div>

      {/* Tasks List */}
      <Card title="Tasks">
        {isLoading ? (
          <div className="text-center py-5">Loading...</div>
        ) : (
          <Table data={tasks || []} columns={columns} />
        )}
      </Card>

      {/* Create Task Modal */}
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
        <div className="mb-3">
          <label className="form-label">Task Type</label>
          <Select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            options={taskTypeOptions}
          />
        </div>

        <div className="alert alert-info">
          <strong>{selectedType === 'parse' && 'Parse users from a Telegram channel'}</strong>
          <strong>{selectedType === 'invite' && 'Invite parsed users to your channel'}</strong>
          <strong>{selectedType === 'masslook' && 'View stories from target users'}</strong>
          <strong>{selectedType === 'comment' && 'Post comments on channel posts'}</strong>
        </div>

        <div className="text-center text-muted py-4">
          <p>Configuration form for <strong>{selectedType}</strong> task</p>
          <small>Full wizard will be implemented here</small>
        </div>
      </Modal>
    </div>
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
