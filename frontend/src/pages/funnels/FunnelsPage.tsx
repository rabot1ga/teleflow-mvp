import { useState } from 'react'
import { Card, StatCard, Button, Table, StatusBadge, Modal, FormField, Input, Select } from '@/components/ui'
import { funnelsApi, type Funnel } from '@/services/funnelsApi'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'

export function FunnelsPage() {
  const [showCreateModal, setShowCreateModal] = useState(false)
  const queryClient = useQueryClient()

  const { data: funnels, isLoading } = useQuery({
    queryKey: ['funnels'],
    queryFn: () => funnelsApi.getFunnels('550e8400-e29b-41d4-a716-446655440000').then(r => r.data.data),
  })

  const createMutation = useMutation({
    mutationFn: (data: { name: string; trigger_type: 'command' | 'keyword' | 'subscription'; trigger_value?: string }) => funnelsApi.createFunnel(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['funnels'] })
      setShowCreateModal(false)
      toast.success('Funnel created')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => funnelsApi.deleteFunnel(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['funnels'] })
      toast.success('Funnel deleted')
    },
  })

  const columns = [
    { key: 'name', title: 'Name' },
    { key: 'trigger_type', title: 'Trigger' },
    {
      key: 'is_active',
      title: 'Status',
      render: (item: Funnel) => (
        <StatusBadge status={item.is_active ? 'active' : 'pending'} />
      ),
    },
    {
      key: 'actions',
      title: 'Actions',
      render: (item: Funnel) => (
        <div className="d-flex gap-2">
          <Button size="sm" variant="outline" onClick={() => toast.success(`Edit ${item.name}`)}>
            Edit
          </Button>
          <Button size="sm" variant="danger" onClick={() => deleteMutation.mutate(item.id)}>
            Delete
          </Button>
        </div>
      ),
    },
  ]

  const triggerTypeOptions = [
    { value: 'command', label: 'Command (/start)' },
    { value: 'keyword', label: 'Keyword' },
    { value: 'subscription', label: 'Subscription' },
  ]

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1 className="h2 mb-0">Funnels</h1>
        <Button onClick={() => setShowCreateModal(true)}>+ Create Funnel</Button>
      </div>

      {/* Stats */}
      <div className="row g-4 mb-4">
        <div className="col-md-4">
          <StatCard title="Total Funnels" value={funnels?.length || 0} icon="🎯" />
        </div>
        <div className="col-md-4">
          <StatCard title="Active Funnels" value={funnels?.filter((f: Funnel) => f.is_active).length || 0} icon="✅" />
        </div>
        <div className="col-md-4">
          <StatCard title="Total Entries" value="1,234" icon="👥" trend={{ value: 23, isPositive: true }} />
        </div>
      </div>

      {/* Funnels List */}
      <Card title="Funnels">
        {isLoading ? (
          <div className="text-center py-5">Loading...</div>
        ) : (
          <Table data={funnels || []} columns={columns} />
        )}
      </Card>

      {/* Create Funnel Modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="Create New Funnel"
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowCreateModal(false)}>
              Cancel
            </Button>
            <Button 
              variant="primary" 
              onClick={() => document.getElementById('create-funnel-form')?.click()}
            >
              Create
            </Button>
          </>
        }
      >
        <form
          id="create-funnel-form"
          onSubmit={(e) => {
            e.preventDefault()
            const formData = new FormData(e.currentTarget)
            createMutation.mutate({
              name: formData.get('name') as string,
              trigger_type: formData.get('trigger_type') as 'command' | 'keyword' | 'subscription',
              trigger_value: formData.get('trigger_value') as string,
            })
          }}
        >
          <FormField label="Funnel Name" required>
            <Input name="name" placeholder="Welcome Funnel" required />
          </FormField>
          
          <FormField label="Trigger Type" required>
            <Select 
              name="trigger_type" 
              options={triggerTypeOptions}
              defaultValue="command"
              required
            />
          </FormField>
          
          <FormField label="Trigger Value">
            <Input name="trigger_value" placeholder="/start or keyword" />
          </FormField>
          
          <div className="alert alert-info small mb-0">
            <strong>Tip:</strong> You can configure funnel steps after creation.
          </div>
        </form>
      </Modal>
    </div>
  )
}
