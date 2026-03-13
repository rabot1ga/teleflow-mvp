import { useState } from 'react'
import { Card, Button, Table, Modal, FormField, Input, Textarea, PageHeader, Tabs, Badge } from '@/components/ui'
import { publishingApi, type Target, type Template } from '@/services/publishingApi'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import './PublishingPage.css'

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
  const [currentDate, setCurrentDate] = useState(new Date())
  const [selectedDate, setSelectedDate] = useState<Date | null>(null)

  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear()
    const month = date.getMonth()
    const firstDay = new Date(year, month, 1)
    const lastDay = new Date(year, month + 1, 0)
    const daysInMonth = lastDay.getDate()
    const startingDay = firstDay.getDay()
    
    return { daysInMonth, startingDay, year, month }
  }

  const { daysInMonth, startingDay, year, month } = getDaysInMonth(currentDate)
  
  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ]

  const prevMonth = () => {
    setCurrentDate(new Date(year, month - 1, 1))
  }

  const nextMonth = () => {
    setCurrentDate(new Date(year, month + 1, 1))
  }

  const today = new Date()
  const isToday = (day: number) => {
    return day === today.getDate() && month === today.getMonth() && year === today.getFullYear()
  }

  const isSelected = (day: number) => {
    if (!selectedDate) return false
    return day === selectedDate.getDate() && month === selectedDate.getMonth() && year === selectedDate.getFullYear()
  }

  // Mock publications for demo
  const publications = [
    { day: 5, title: 'Article: Tech News', time: '10:00' },
    { day: 12, title: 'Broadcast: Weekly Digest', time: '14:00' },
    { day: 20, title: 'Article: AI Update', time: '09:00' },
  ]

  const hasPublication = (day: number) => publications.find(p => p.day === day)

  return (
    <div className="publishing-calendar">
      <Card>
        {/* Calendar Header */}
        <div className="calendar-header mb-4">
          <button className="calendar-nav-btn" onClick={prevMonth}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="15,18 9,12 15,6" />
            </svg>
          </button>
          <h3 className="calendar-title">
            {monthNames[month]} {year}
          </h3>
          <button className="calendar-nav-btn" onClick={nextMonth}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="9,18 15,12 9,6" />
            </svg>
          </button>
          <Button variant="outline" size="sm" className="ms-auto" onClick={() => setCurrentDate(new Date())}>
            Today
          </Button>
        </div>

        {/* Calendar Grid */}
        <div className="calendar-grid">
          {/* Weekday Headers */}
          {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
            <div key={day} className="calendar-weekday-header">{day}</div>
          ))}

          {/* Empty cells for days before month starts */}
          {Array.from({ length: startingDay }).map((_, i) => (
            <div key={`empty-${i}`} className="calendar-day calendar-day--empty" />
          ))}

          {/* Days of the month */}
          {Array.from({ length: daysInMonth }).map((_, i) => {
            const day = i + 1
            const pub = hasPublication(day)
            return (
              <div
                key={day}
                className={`calendar-day ${isToday(day) ? 'calendar-day--today' : ''} ${isSelected(day) ? 'calendar-day--selected' : ''}`}
                onClick={() => setSelectedDate(new Date(year, month, day))}
              >
                <div className="calendar-day-number">{day}</div>
                {pub && (
                  <div className="calendar-day-publication">
                    <div className="calendar-day-publication-dot" />
                    <span className="calendar-day-publication-title">{pub.title}</span>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </Card>

      {/* Selected Day Details */}
      {selectedDate && (
        <Card title={`Publications on ${selectedDate.toLocaleDateString()}`} className="mt-4">
          <div className="text-center text-muted py-4">
            <p>No publications scheduled for this day</p>
            <Button variant="primary" size="sm" className="mt-2" onClick={() => toast.success('Create publication')}>
              + Schedule Publication
            </Button>
          </div>
        </Card>
      )}

      {/* Upcoming Publications */}
      <Card title="Upcoming Publications" className="mt-4">
        <div className="d-flex flex-col gap-3">
          {publications.map((pub, index) => (
            <div key={index} className="calendar-upcoming-item">
              <div className="calendar-upcoming-day">{monthNames[month]} {pub.day}</div>
              <div className="calendar-upcoming-info">
                <div className="calendar-upcoming-title">{pub.title}</div>
                <div className="calendar-upcoming-time">{pub.time}</div>
              </div>
              <Badge variant="primary">Scheduled</Badge>
            </div>
          ))}
        </div>
      </Card>
    </div>
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
