import { useState } from 'react'
import { Card, Button, Table, Badge, Modal, FormField, Input } from '@/components/ui'
import { contentApi, type Source, type Article } from '@/services/contentApi'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { z } from 'zod'
import './ContentPage.css'

const sourceSchema = z.object({
  project_id: z.string().uuid(),
  name: z.string().min(1, 'Name is required'),
  source_type: z.enum(['rss', 'json_api', 'scraper', 'telegram', 'webhook']),
  url: z.string().url('Invalid URL').optional().or(z.literal('')),
  fetch_interval_minutes: z.coerce.number().min(1).default(30),
})

type SourceForm = z.infer<typeof sourceSchema>

// Articles Tab Component
function ArticlesTab({ projectId }: { projectId: string }) {
  const { data: articles, isLoading } = useQuery({
    queryKey: ['articles', projectId],
    queryFn: async () => {
      const response = await contentApi.getArticles({ project_id: projectId, page: 1, per_page: 50 })
      const standardResponse = response.data
      if (standardResponse && typeof standardResponse === 'object' && 'data' in standardResponse) {
        const innerData = standardResponse.data
        if (innerData && typeof innerData === 'object' && 'items' in innerData) {
          return innerData.items || []
        }
        if (Array.isArray(innerData)) {
          return innerData
        }
      }
      return []
    },
  })

  const columns = [
    {
      key: 'title',
      title: 'Title',
      render: (item: Article) => (
        <div>
          <strong>{item.title}</strong>
          {item.summary && <small className="text-muted d-block mt-1">{item.summary}</small>}
        </div>
      ),
    },
    { key: 'category', title: 'Category', render: (item: Article) => item.category || '-' },
    {
      key: 'status',
      title: 'Status',
      render: (item: Article) => (
        <Badge variant={
          item.status === 'approved' ? 'success' :
          item.status === 'rejected' ? 'danger' :
          item.status === 'published' ? 'primary' : 'neutral'
        }>
          {item.status}
        </Badge>
      ),
    },
    { key: 'priority_score', title: 'Priority', render: (item: Article) => item.priority_score },
    {
      key: 'created_at',
      title: 'Created',
      render: (item: Article) => new Date(item.created_at).toLocaleDateString(),
    },
  ]

  return (
    <Card title={`Articles (${articles?.length || 0})`}>
      {isLoading ? (
        <div className="text-center py-5">Loading...</div>
      ) : articles && articles.length > 0 ? (
        <Table data={articles} columns={columns} />
      ) : (
        <div className="text-center text-muted py-5">
          <p>No articles yet</p>
          <small>Go to Sources tab and click "Fetch" to collect articles</small>
        </div>
      )}
    </Card>
  )
}

// Moderation Tab Component
function ModerationTab({ projectId }: { projectId: string }) {
  const queryClient = useQueryClient()

  const { data: queue, isLoading } = useQuery({
    queryKey: ['moderation-queue', projectId],
    queryFn: async () => {
      const response = await contentApi.getModerationQueue({ per_page: 50 })
      const standardResponse = response.data
      if (standardResponse && typeof standardResponse === 'object' && 'data' in standardResponse) {
        const innerData = standardResponse.data
        if (innerData && typeof innerData === 'object' && 'items' in innerData) {
          return innerData.items || []
        }
        if (Array.isArray(innerData)) {
          return innerData
        }
      }
      return []
    },
  })

  const approveMutation = useMutation({
    mutationFn: (id: string) => contentApi.approveArticle(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['moderation-queue', projectId] })
      queryClient.invalidateQueries({ queryKey: ['articles', projectId] })
      toast.success('Article approved!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error?.message || 'Failed to approve')
    },
  })

  const rejectMutation = useMutation({
    mutationFn: (id: string) => contentApi.rejectArticle(id, 'low_quality', ''),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['moderation-queue', projectId] })
      toast.success('Article rejected')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error?.message || 'Failed to reject')
    },
  })

  const columns = [
    {
      key: 'title',
      title: 'Title',
      render: (item: Article) => (
        <div>
          <strong>{item.title}</strong>
          <small className="text-muted d-block mt-1">
            Priority: {item.priority_score} | Quality: {(item.quality_score * 100).toFixed(0)}%
          </small>
        </div>
      ),
    },
    {
      key: 'actions',
      title: 'Actions',
      render: (item: Article) => (
        <div className="d-flex gap-2">
          <Button
            size="sm"
            variant="success"
            onClick={() => approveMutation.mutate(item.id)}
            disabled={approveMutation.isPending}
          >
            ✅ Approve
          </Button>
          <Button
            size="sm"
            variant="danger"
            onClick={() => rejectMutation.mutate(item.id)}
            disabled={rejectMutation.isPending}
          >
            ❌ Reject
          </Button>
        </div>
      ),
    },
  ]

  return (
    <Card title={`Moderation Queue (${queue?.length || 0})`}>
      {isLoading ? (
        <div className="text-center py-5">Loading...</div>
      ) : queue && queue.length > 0 ? (
        <Table data={queue} columns={columns} />
      ) : (
        <div className="text-center text-muted py-5">
          <p>🎉 No articles pending moderation!</p>
          <small>All articles have been reviewed</small>
        </div>
      )}
    </Card>
  )
}

export function ContentPage() {
  const [activeTab, setActiveTab] = useState<'sources' | 'articles' | 'moderation'>('sources')
  const [showAddModal, setShowAddModal] = useState(false)
  const [editingSource, setEditingSource] = useState<Source | null>(null)
  const [selectedSourceType, setSelectedSourceType] = useState<'rss' | 'telegram' | 'json_api' | 'scraper'>('rss')
  const [telegramUsername, setTelegramUsername] = useState('')
  const queryClient = useQueryClient()
  
  // Get project_id from localStorage or use user ID as fallback
  const authStorage = localStorage.getItem('auth-storage')
  let projectId = '9ca1f5a6-6b41-4090-b366-9ac87200c6ec' // Default test project ID

  if (authStorage) {
    const user = JSON.parse(authStorage).state?.user
    // Try to get project from user.projects array
    if (user?.projects?.length > 0) {
      projectId = user.projects[0].id
    } else if (user?.id) {
      // Fallback: use user ID as project ID
      projectId = user.id
    }
  }

  console.log('🔑 Project ID:', projectId)
  console.log('📦 Auth storage:', authStorage ? JSON.parse(authStorage).state?.user : 'Not logged in')

  const { data: sources, isLoading } = useQuery({
    queryKey: ['sources', projectId],
    queryFn: async () => {
      const response = await contentApi.getSources(projectId)
      const standardResponse = response.data

      if (standardResponse && typeof standardResponse === 'object' && 'data' in standardResponse) {
        const innerData = standardResponse.data
        if (innerData && typeof innerData === 'object' && 'items' in innerData) {
          return innerData.items || []
        }
        if (Array.isArray(innerData)) {
          return innerData
        }
      }
      return []
    },
    staleTime: 0, // Always refetch
    enabled: !!projectId, // Only run if projectId is defined
  })

  const createMutation = useMutation({
    mutationFn: async (data: SourceForm) => {
      console.log('📝 Creating source with data:', data)
      console.log('🔑 Using project_id:', projectId)
      
      const validated = sourceSchema.parse(data)
      const response = await contentApi.createSource(validated)
      console.log('✅ API response:', response.data)
      return response.data
    },
    onSuccess: async (data) => {
      console.log('✅ Source created:', data)
      setShowAddModal(false)
      toast.success('Source created')

      // Invalidate queries to trigger refetch
      queryClient.invalidateQueries({ queryKey: ['sources', projectId] })
    },
    onError: (error: any) => {
      console.error('❌ Create error:', error)
      console.error('❌ Error response:', error.response?.data)
      console.error('❌ Error status:', error.response?.status)
      console.error('❌ Error headers:', error.response?.headers)
      
      let errorMessage = 'Failed to create source'
      
      // Try to get error message from different response formats
      const errorData = error.response?.data
      if (errorData) {
        if (typeof errorData === 'string') {
          errorMessage = errorData
        } else if (errorData.error?.message) {
          errorMessage = errorData.error.message
        } else if (errorData.detail) {
          errorMessage = Array.isArray(errorData.detail) 
            ? errorData.detail.map((d: any) => d.msg || d.message).join('; ')
            : errorData.detail
        } else if (errorData.message) {
          errorMessage = errorData.message
        }
      }
      
      toast.error(errorMessage)
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => contentApi.deleteSource(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sources', projectId] })
      toast.success('Source deleted')
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Source> }) =>
      contentApi.updateSource(id, data),
    onSuccess: () => {
      setEditingSource(null)
      queryClient.invalidateQueries({ queryKey: ['sources', projectId] })
      toast.success('Source updated')
    },
    onError: (error: any) => {
      console.error('❌ Update error:', error)
      console.error('❌ Error response:', error.response?.data)
      
      let errorMessage = 'Failed to update source'
      
      // Try to get error message from different response formats
      const errorData = error.response?.data
      if (errorData) {
        // Format 1: { error: { message, details } }
        if (errorData.error?.message) {
          errorMessage = errorData.error.message
          if (errorData.error.details && Array.isArray(errorData.error.details)) {
            errorMessage = errorData.error.details
              .map((d: any) => `${d.field || d.loc?.join('.')}: ${d.message || d.msg}`)
              .join('; ')
          }
        }
        // Format 2: { detail: [...] } (Pydantic standard)
        else if (errorData.detail) {
          const detail = errorData.detail
          if (Array.isArray(detail)) {
            errorMessage = detail.map((d: any) => `${d.loc?.join('.') || d.field}: ${d.msg || d.message}`).join('; ')
          } else {
            errorMessage = detail
          }
        }
      }
      
      toast.error(errorMessage)
    },
  })

  const fetchMutation = useMutation({
    mutationFn: (id: string) => contentApi.fetchSource(id),
    onSuccess: (response) => {
      console.log('✅ Fetch response:', response)
      toast.success('✅ Fetch started! Articles will appear in ~30 seconds')
    },
    onError: (error: any) => {
      console.error('❌ Fetch error:', error)
      console.error('❌ Error response:', error.response?.data)
      
      let errorMessage = 'Failed to fetch source'
      const errorData = error.response?.data
      
      if (errorData) {
        if (errorData.error?.message) {
          errorMessage = errorData.error.message
        } else if (errorData.detail) {
          errorMessage = errorData.detail
        }
      }
      
      // Special handling for SSL errors
      if (errorMessage.includes('SSL') || errorMessage.includes('certificate')) {
        errorMessage = 'SSL certificate error. Try using HTTP instead of HTTPS or check the URL.'
      }
      
      toast.error(errorMessage)
    },
  })

  const columns = [
    { key: 'name', title: 'Name' },
    { key: 'source_type', title: 'Type' },
    { key: 'fetch_interval_minutes', title: 'Interval (min)' },
    {
      key: 'actions',
      title: 'Actions',
      render: (item: Source) => (
        <div className="d-flex gap-2">
          <Button 
            size="sm" 
            variant="primary" 
            onClick={() => fetchMutation.mutate(item.id)}
            title="Fetch now"
          >
            🔄 Fetch
          </Button>
          <Button 
            size="sm" 
            variant="outline" 
            onClick={() => setEditingSource(item)}
          >
            ✏️ Edit
          </Button>
          <Button 
            size="sm" 
            variant="danger" 
            onClick={() => deleteMutation.mutate(item.id)}
          >
            🗑️ Delete
          </Button>
        </div>
      ),
    },
  ]

  return (
    <div className="content-page">
      {/* Header */}
      <div className="content-page__header">
        <h1 className="content-page__title">Content</h1>
        <Button onClick={() => setShowAddModal(true)} size="sm">
          + Add Source
        </Button>
      </div>

      {/* Tabs */}
      <div className="tf-tabs">
        <div className="tf-tabs__list">
          <button
            className={`tf-tabs__tab ${activeTab === 'sources' ? 'tf-tabs__tab--active' : ''}`}
            onClick={() => setActiveTab('sources')}
            type="button"
          >
            Sources
          </button>
          <button
            className={`tf-tabs__tab ${activeTab === 'articles' ? 'tf-tabs__tab--active' : ''}`}
            onClick={() => setActiveTab('articles')}
            type="button"
          >
            Articles
          </button>
          <button
            className={`tf-tabs__tab ${activeTab === 'moderation' ? 'tf-tabs__tab--active' : ''}`}
            onClick={() => setActiveTab('moderation')}
            type="button"
          >
            Moderation
          </button>
        </div>
      </div>

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
        <ArticlesTab projectId={projectId} />
      )}

      {activeTab === 'moderation' && (
        <ModerationTab projectId={projectId} />
      )}

      {/* Add Source Modal */}
      <Modal
        isOpen={showAddModal}
        onClose={() => {
          setShowAddModal(false)
          createMutation.reset()
          setSelectedSourceType('rss')
          setTelegramUsername('')
        }}
        title="Add New Source"
        size="lg"
        footer={
          <>
            <Button
              variant="secondary"
              onClick={() => setShowAddModal(false)}
              disabled={createMutation.isPending}
            >
              Cancel
            </Button>
            <Button
              variant="primary"
              type="submit"
              form="add-source-form"
              disabled={createMutation.isPending}
            >
              {createMutation.isPending ? 'Creating...' : 'Create'}
            </Button>
          </>
        }
      >
        {createMutation.isError && (
          <div className="alert alert-danger mb-3">
            {createMutation.error instanceof Error
              ? createMutation.error.message
              : 'Failed to create source'}
          </div>
        )}
        
        {/* Source Type Quick Select */}
        <div className="mb-4">
          <label className="form-label">Source Type</label>
          <div className="d-flex gap-2 flex-wrap">
            <Button
              variant={selectedSourceType === 'rss' ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setSelectedSourceType('rss')}
            >
              📰 RSS Feed
            </Button>
            <Button
              variant={selectedSourceType === 'json_api' ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setSelectedSourceType('json_api')}
            >
              🔌 JSON API
            </Button>
            <Button
              variant={selectedSourceType === 'telegram' ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setSelectedSourceType('telegram')}
            >
              ✈️ Telegram
            </Button>
            <Button
              variant={selectedSourceType === 'scraper' ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setSelectedSourceType('scraper')}
            >
              🕸️ Web Scraper
            </Button>
          </div>
        </div>

        <form
          id="add-source-form"
          onSubmit={(e) => {
            e.preventDefault()
            const formData = new FormData(e.currentTarget)
            let url = formData.get('url') as string
            
            // Auto-generate URL based on source type
            if (selectedSourceType === 'telegram' && telegramUsername) {
              // For Telegram channels via userbot
              url = `https://t.me/${telegramUsername.replace(/^@/, '')}`
            }
            
            createMutation.mutate({
              project_id: projectId,
              name: formData.get('name') as string,
              source_type: selectedSourceType,
              url: url || undefined,
              fetch_interval_minutes: Number(formData.get('fetch_interval_minutes')),
            })
          }}
        >
          <FormField label="Name" required>
            <Input
              name="name"
              placeholder={
                selectedSourceType === 'rss' ? 'My RSS Feed' :
                selectedSourceType === 'telegram' ? 'Telegram Channel' :
                'JSON API Source'
              }
              required
            />
          </FormField>

          {/* Telegram Username Input */}
          {selectedSourceType === 'telegram' && (
            <FormField label="Telegram Channel Username" required>
              <Input 
                name="telegram_username"
                value={telegramUsername}
                onChange={(e) => setTelegramUsername(e.target.value)}
                placeholder="@durov" 
              />
              <small className="text-muted">
                Enter channel username (e.g., @durov or durov)
              </small>
            </FormField>
          )}

          {/* Custom URL Input (for RSS and JSON API) */}
          {(selectedSourceType === 'rss' || selectedSourceType === 'json_api') && (
            <FormField label="URL" required={selectedSourceType === 'rss'}>
              <Input 
                name="url" 
                type="url" 
                placeholder={
                  selectedSourceType === 'rss' 
                    ? 'https://example.com/rss' 
                    : 'https://api.example.com/articles'
                } 
              />
            </FormField>
          )}

          <FormField label="Fetch Interval (minutes)">
            <Input name="fetch_interval_minutes" type="number" defaultValue="30" min="5" max="1440" />
            <small className="text-muted">Must be between 5 and 1440 minutes</small>
          </FormField>
        </form>
      </Modal>

      {/* Edit Source Modal */}
      {editingSource && (
        <Modal
          isOpen={!!editingSource}
          onClose={() => {
            setEditingSource(null)
            updateMutation.reset()
          }}
          title="Edit Source"
          footer={
            <>
              <Button
                variant="secondary"
                onClick={() => setEditingSource(null)}
                disabled={updateMutation.isPending}
              >
                Cancel
              </Button>
              <Button
                variant="primary"
                type="submit"
                form="edit-source-form"
                disabled={updateMutation.isPending}
              >
                {updateMutation.isPending ? 'Saving...' : 'Save Changes'}
              </Button>
            </>
          }
        >
          {updateMutation.isError && (
            <div className="alert alert-danger mb-3">
              {updateMutation.error instanceof Error
                ? updateMutation.error.message
                : 'Failed to update source'}
            </div>
          )}
          <form
            id="edit-source-form"
            onSubmit={(e) => {
              e.preventDefault()
              const formData = new FormData(e.currentTarget)
              const fetchInterval = Number(formData.get('fetch_interval_minutes'))
              const url = formData.get('url') as string
              
              const data: Partial<Source> = {
                name: formData.get('name') as string,
                url: url || undefined,  // Send undefined if empty
                fetch_interval_minutes: isNaN(fetchInterval) ? undefined : fetchInterval,
                is_active: formData.get('is_active') === 'on',
              }
              console.log('📝 Updating source:', editingSource.id, data)
              updateMutation.mutate({
                id: editingSource.id,
                data,
              })
            }}
          >
            <FormField label="Name" required>
              <Input name="name" defaultValue={editingSource.name} required />
            </FormField>

            <FormField label="URL">
              <Input name="url" type="url" defaultValue={editingSource.url || ''} />
            </FormField>

            <FormField label="Fetch Interval (minutes)">
              <Input
                name="fetch_interval_minutes"
                type="number"
                defaultValue={editingSource.fetch_interval_minutes}
                min="5"
                max="1440"
              />
              <small className="text-muted">Must be between 5 and 1440 minutes</small>
            </FormField>

            <FormField label="Active">
              <div className="form-check">
                <input
                  className="form-check-input"
                  type="checkbox"
                  name="is_active"
                  id="is_active"
                  defaultChecked={editingSource.is_active}
                />
                <label className="form-check-label" htmlFor="is_active">
                  Source is active
                </label>
              </div>
            </FormField>
          </form>
        </Modal>
      )}
    </div>
  )
}
