import { useState } from 'react'
import { Card, Button, Table, Modal, FormField, Input, Textarea, PageHeader, Tabs } from '@/components/ui'
import { publishingApi, type Target, type Template } from '@/services/publishingApi'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'

function TargetsTab() {
  const queryClient = useQueryClient()
  const [showModal, setShowModal] = useState(false)

  const { data: targets, isLoading } = useQuery({
    queryKey: ['publishing-targets'],
    queryFn: () => publishingApi.getTargets('550e8400-e29b-41d4-a716-446655440000').then(r => r.data.data),
  })

  const createMutation = useMutation({
    mutationFn: (data: { name: string; chat_id: string; type: 'channel' | 'group' }) =>
      publishingApi.createTarget({ project_id: '550e8400-e29b-41d4-a716-446655440000', ...data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['publishing-targets'] })
      setShowModal(false)
      toast.success('Target created')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => publishingApi.deleteTarget(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['publishing-targets'] })
      toast.success('Target deleted')
    },
  })

  const columns = [
    { key: 'name', title: 'Name' },
    { key: 'chat_id', title: 'Chat ID' },
    { key: 'type', title: 'Type' },
    {
      key: 'actions',
      title: 'Actions',
      render: (item: Target) => (
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

  return (
    <>
      <div className="d-flex justify-content-between items-center mb-4">
        <h2 className="text-lg font-semibold m-0">Targets</h2>
        <Button onClick={() => setShowModal(true)}>+ Add Target</Button>
      </div>

      <Card>
        {isLoading ? (
          <div className="text-center text-muted py-6">Loading...</div>
        ) : (
          <Table data={targets || []} columns={columns} />
        )}
      </Card>

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title="Add New Target"
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowModal(false)}>
              Cancel
            </Button>
            <Button
              variant="primary"
              onClick={() => {
                const name = (document.getElementById('target-name') as HTMLInputElement)?.value
                const chatId = (document.getElementById('target-chat-id') as HTMLInputElement)?.value
                const type = (document.getElementById('target-type') as HTMLSelectElement)?.value as 'channel' | 'group'
                if (name && chatId) {
                  createMutation.mutate({ name, chat_id: chatId, type })
                }
              }}
            >
              Create
            </Button>
          </>
        }
      >
        <FormField label="Name" required>
          <Input id="target-name" placeholder="My Channel" />
        </FormField>
        <FormField label="Chat ID" required>
          <Input id="target-chat-id" placeholder="@username or -100123456789" />
        </FormField>
        <FormField label="Type" required>
          <select id="target-type" className="tf-select">
            <option value="channel">Channel</option>
            <option value="group">Group</option>
          </select>
        </FormField>
      </Modal>
    </>
  )
}

function TemplatesTab() {
  const queryClient = useQueryClient()
  const [showModal, setShowModal] = useState(false)

  const { data: templates, isLoading } = useQuery({
    queryKey: ['publishing-templates'],
    queryFn: () => publishingApi.getTemplates('550e8400-e29b-41d4-a716-446655440000').then(r => r.data.data),
  })

  const createMutation = useMutation({
    mutationFn: (data: { name: string; content: string }) =>
      publishingApi.createTemplate({ project_id: '550e8400-e29b-41d4-a716-446655440000', ...data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['publishing-templates'] })
      setShowModal(false)
      toast.success('Template created')
    },
  })

  const columns = [
    { key: 'name', title: 'Name' },
    {
      key: 'content',
      title: 'Content',
      render: (item: Template) => (
        <div className="text-secondary text-sm" style={{ maxWidth: '400px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {item.content}
        </div>
      ),
    },
    {
      key: 'actions',
      title: 'Actions',
      render: (item: Template) => (
        <div className="d-flex gap-2">
          <Button size="sm" variant="outline" onClick={() => toast.success(`Edit ${item.name}`)}>
            Edit
          </Button>
          <Button size="sm" variant="danger" onClick={() => publishingApi.deleteTemplate(item.id).then(() => {
            queryClient.invalidateQueries({ queryKey: ['publishing-templates'] })
            toast.success('Template deleted')
          })}>
            Delete
          </Button>
        </div>
      ),
    },
  ]

  return (
    <>
      <div className="d-flex justify-content-between items-center mb-4">
        <h2 className="text-lg font-semibold m-0">Templates</h2>
        <Button onClick={() => setShowModal(true)}>+ Create Template</Button>
      </div>

      <Card>
        {isLoading ? (
          <div className="text-center text-muted py-6">Loading...</div>
        ) : (
          <Table data={templates || []} columns={columns} />
        )}
      </Card>

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title="Create Template"
        size="lg"
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowModal(false)}>
              Cancel
            </Button>
            <Button
              variant="primary"
              onClick={() => {
                const name = (document.getElementById('template-name') as HTMLInputElement)?.value
                const content = (document.getElementById('template-content') as HTMLTextAreaElement)?.value
                if (name && content) {
                  createMutation.mutate({ name, content })
                }
              }}
            >
              Create
            </Button>
          </>
        }
      >
        <FormField label="Name" required>
          <Input id="template-name" placeholder="Default Template" />
        </FormField>
        <FormField label="Content" required>
          <Textarea
            id="template-content"
            placeholder={`{{title}}\n\n{{content}}\n\n#{{tags}}`}
            rows={8}
          />
        </FormField>
        <div className="text-secondary text-sm mt-2">
          <strong>Available variables:</strong> {'{{title}}'}, {'{{content}}'}, {'{{source}}'}, {'{{tags}}'}, {'{{url}}'}
        </div>
      </Modal>
    </>
  )
}

function CalendarTab() {
  return (
    <Card title="Publish Calendar">
      <div className="text-center text-muted py-8">
        <svg className="mx-auto mb-4" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <rect x="3" y="4" width="18" height="18" rx="2" />
          <line x1="16" y1="2" x2="16" y2="6" />
          <line x1="8" y1="2" x2="8" y2="6" />
          <line x1="3" y1="10" x2="21" y2="10" />
        </svg>
        <p className="text-lg font-medium">Calendar view coming soon</p>
        <p className="text-sm">Schedule and manage your publications visually</p>
      </div>
    </Card>
  )
}

export function PublishingPage() {
  const [activeTab, setActiveTab] = useState<'targets' | 'templates' | 'calendar'>('targets')

  const tabs = [
    { id: 'targets', label: 'Targets' },
    { id: 'templates', label: 'Templates' },
    { id: 'calendar', label: 'Calendar' },
  ]

  return (
    <div>
      <PageHeader
        title="Publishing"
        description="Manage Telegram channels and message templates"
      />

      <Tabs tabs={tabs} activeTab={activeTab} onChange={(tab) => setActiveTab(tab as any)}>
        {activeTab === 'targets' && <TargetsTab />}
        {activeTab === 'templates' && <TemplatesTab />}
        {activeTab === 'calendar' && <CalendarTab />}
      </Tabs>
    </div>
  )
}

export function SettingsPage() {

  const handleSaveProfile = () => {
    toast.success('Profile settings saved')
  }

  return (
    <div>
      <PageHeader
        title="Settings"
        description="Manage your account and project settings"
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card title="Profile Settings">
          <form onSubmit={(e) => { e.preventDefault(); handleSaveProfile() }}>
            <div className="d-flex flex-col gap-4">
              <FormField label="Email">
                <Input type="email" defaultValue="test@example.com" />
              </FormField>
              <FormField label="First Name">
                <Input type="text" defaultValue="Test" />
              </FormField>
              <FormField label="Last Name">
                <Input type="text" defaultValue="User" />
              </FormField>
              <Button type="submit" variant="primary">
                Save Changes
              </Button>
            </div>
          </form>
        </Card>

        <Card title="Project Settings">
          <div className="text-center text-muted py-8">
            <svg className="mx-auto mb-4" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <line x1="3" y1="9" x2="21" y2="9" />
              <line x1="9" y1="21" x2="9" y2="9" />
            </svg>
            <p className="text-lg font-medium">Project configuration</p>
            <p className="text-sm">Members, API keys, notifications</p>
          </div>
        </Card>
      </div>
    </div>
  )
}
