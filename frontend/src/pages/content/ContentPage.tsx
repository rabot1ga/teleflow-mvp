import { useState } from 'react'
import { Card, Button, Table, Badge, Modal, FormField, Input, Select } from '@/components/ui'
import { contentApi, type Source } from '@/services/contentApi'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { z } from 'zod'

const sourceSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  source_type: z.enum(['rss', 'json_api', 'scraper', 'telegram', 'webhook']),
  url: z.string().url('Invalid URL').optional().or(z.literal('')),
  fetch_interval_minutes: z.coerce.number().min(1).default(30),
})

type SourceForm = z.infer<typeof sourceSchema>

export function ContentPage() {
  const [activeTab, setActiveTab] = useState<'sources' | 'articles' | 'moderation'>('sources')
  const [showAddModal, setShowAddModal] = useState(false)
  const queryClient = useQueryClient()

  const { data: sources, isLoading } = useQuery({
    queryKey: ['sources'],
    queryFn: () => contentApi.getSources('550e8400-e29b-41d4-a716-446655440000').then(r => r.data.data),
  })

  const createMutation = useMutation({
    mutationFn: (data: SourceForm) => contentApi.createSource(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sources'] })
      setShowAddModal(false)
      toast.success('Source created')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => contentApi.deleteSource(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sources'] })
      toast.success('Source deleted')
    },
  })

  const fetchMutation = useMutation({
    mutationFn: (id: string) => contentApi.fetchSource(id),
    onSuccess: () => {
      toast.success('Fetch started')
    },
  })

  const columns = [
    { key: 'name', title: 'Name' },
    { key: 'source_type', title: 'Type' },
    { key: 'fetch_interval_minutes', title: 'Interval (min)' },
    {
      key: 'is_active',
      title: 'Status',
      render: (item: Source) => (
        <Badge variant={item.is_active ? 'success' : 'secondary'}>
          {item.is_active ? 'Active' : 'Inactive'}
        </Badge>
      ),
    },
    {
      key: 'actions',
      title: 'Actions',
      render: (item: Source) => (
        <div className="d-flex gap-2">
          <Button size="sm" variant="primary" onClick={() => fetchMutation.mutate(item.id)}>
          </Button>
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

  const sourceTypeOptions = [
    { value: 'rss', label: 'RSS Feed' },
    { value: 'json_api', label: 'JSON API' },
    { value: 'scraper', label: 'Web Scraper' },
    { value: 'telegram', label: 'Telegram Channel' },
    { value: 'webhook', label: 'Webhook' },
  ]

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1 className="h2 mb-0">Content</h1>
        <Button onClick={() => setShowAddModal(true)}>+ Add Source</Button>
      </div>

      {/* Tabs */}
      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'sources' ? 'active' : ''}`}
            onClick={() => setActiveTab('sources')}
          >
            Sources
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'articles' ? 'active' : ''}`}
            onClick={() => setActiveTab('articles')}
          >
            Articles
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'moderation' ? 'active' : ''}`}
            onClick={() => setActiveTab('moderation')}
          >
            Moderation
          </button>
        </li>
      </ul>

      {/* Content */}
      {activeTab === 'sources' && (
        <Card title="Sources">
          {isLoading ? (
            <div className="text-center py-5">Loading...</div>
          ) : (
            <Table data={sources || []} columns={columns} />
          )}
        </Card>
      )}

      {activeTab === 'articles' && (
        <Card title="Articles">
          <div className="text-center text-muted py-5">
            <p>Articles list will be here</p>
            <small>With filters, search, and AI actions</small>
          </div>
        </Card>
      )}

      {activeTab === 'moderation' && (
        <Card title="Moderation Queue">
          <div className="text-center text-muted py-5">
            <p>Moderation queue will be here</p>
            <small>With approve/reject actions</small>
          </div>
        </Card>
      )}

      {/* Add Source Modal */}
      <Modal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        title="Add New Source"
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowAddModal(false)}>
              Cancel
            </Button>
            <Button 
              variant="primary" 
              onClick={() => document.getElementById('add-source-form')?.click()}
            >
              Create
            </Button>
          </>
        }
      >
        <form
          id="add-source-form"
          onSubmit={(e) => {
            e.preventDefault()
            const formData = new FormData(e.currentTarget)
            createMutation.mutate({
              name: formData.get('name') as string,
              source_type: formData.get('source_type') as SourceForm['source_type'],
              url: formData.get('url') as string,
              fetch_interval_minutes: Number(formData.get('fetch_interval_minutes')),
            })
          }}
        >
          <FormField label="Name" required>
            <Input name="name" placeholder="My RSS Feed" required />
          </FormField>
          
          <FormField label="Source Type" required>
            <Select 
              name="source_type" 
              options={sourceTypeOptions}
              defaultValue="rss"
              required
            />
          </FormField>
          
          <FormField label="URL">
            <Input name="url" type="url" placeholder="https://example.com/rss" />
          </FormField>
          
          <FormField label="Fetch Interval (minutes)">
            <Input name="fetch_interval_minutes" type="number" defaultValue="30" min="1" />
          </FormField>
        </form>
      </Modal>
    </div>
  )
}
