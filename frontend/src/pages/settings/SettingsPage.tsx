import { useState } from 'react'
import { Card, Button, Input, FormField, Switch, Tabs, Badge, Avatar, Modal, Select, Textarea } from '@/components/ui'
import { useAuthStore } from '@/stores/authStore'
import toast from 'react-hot-toast'
import { z } from 'zod'
import './SettingsPage.css'

// Schema для валидации профиля
const profileSchema = z.object({
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  email: z.string().email('Invalid email'),
  telegram_username: z.string().optional(),
})

// Schema для смены пароля
const passwordSchema = z.object({
  current_password: z.string().min(6, 'Minimum 6 characters'),
  new_password: z.string().min(8, 'Minimum 8 characters'),
  confirm_password: z.string(),
}).refine((data) => data.new_password === data.confirm_password, {
  message: "Passwords don't match",
  path: ['confirm_password'],
})

// Mock данные для members
const mockMembers = [
  { id: '1', name: 'John Doe', email: 'john@example.com', role: 'admin', status: 'active', avatar: '' },
  { id: '2', name: 'Jane Smith', email: 'jane@example.com', role: 'editor', status: 'active', avatar: '' },
  { id: '3', name: 'Bob Wilson', email: 'bob@example.com', role: 'viewer', status: 'pending', avatar: '' },
]

const roleOptions = [
  { value: 'admin', label: 'Admin' },
  { value: 'editor', label: 'Editor' },
  { value: 'viewer', label: 'Viewer' },
]

// ===== Profile Tab =====
function ProfileTab() {
  const { user } = useAuthStore()
  const [isLoading, setIsLoading] = useState(false)
  const [showPasswordModal, setShowPasswordModal] = useState(false)
  const [telegramConnected, setTelegramConnected] = useState(false)

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    
    const formData = new FormData(e.currentTarget as HTMLFormElement)
    const data = {
      first_name: formData.get('first_name') as string,
      last_name: formData.get('last_name') as string,
      email: formData.get('email') as string,
      telegram_username: formData.get('telegram_username') as string,
    }

    try {
      const validated = profileSchema.parse(data)
      console.log('Profile data:', validated)
      toast.success('Profile updated successfully')
    } catch (error: any) {
      if (error.errors) {
        error.errors.forEach((err: any) => toast.error(err.message))
      }
    } finally {
      setIsLoading(false)
    }
  }

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault()
    
    const formData = new FormData(e.currentTarget as HTMLFormElement)
    const data = {
      current_password: formData.get('current_password') as string,
      new_password: formData.get('new_password') as string,
      confirm_password: formData.get('confirm_password') as string,
    }

    try {
      const validated = passwordSchema.parse(data)
      console.log('Password change:', validated)
      toast.success('Password changed successfully')
      setShowPasswordModal(false)
    } catch (error: any) {
      if (error.errors) {
        error.errors.forEach((err: any) => toast.error(err.message))
      }
    }
  }

  const handleConnectTelegram = () => {
    setTelegramConnected(!telegramConnected)
    toast.success(telegramConnected ? 'Telegram disconnected' : 'Telegram connected')
  }

  return (
    <div className="settings-profile">
      <div className="row g-4">
        {/* Profile Info */}
        <div className="col-md-6">
          <Card title="Profile Information">
            <div className="d-flex align-items-center gap-4 mb-4">
              <Avatar name={`${user?.first_name || 'User'} ${user?.last_name || ''}`} size="xl" />
              <div>
                <Button variant="outline" size="sm" className="me-2">
                  Change Avatar
                </Button>
                <Button variant="ghost" size="sm">
                  Remove
                </Button>
              </div>
            </div>

            <form onSubmit={handleSaveProfile}>
              <div className="row g-3">
                <div className="col-6">
                  <FormField label="First Name" required>
                    <Input
                      name="first_name"
                      defaultValue={user?.first_name || ''}
                      placeholder="John"
                      required
                    />
                  </FormField>
                </div>
                <div className="col-6">
                  <FormField label="Last Name" required>
                    <Input
                      name="last_name"
                      defaultValue={user?.last_name || ''}
                      placeholder="Doe"
                      required
                    />
                  </FormField>
                </div>
                <div className="col-12">
                  <FormField label="Email" required>
                    <Input
                      name="email"
                      type="email"
                      defaultValue={user?.email || ''}
                      placeholder="john@example.com"
                      required
                    />
                  </FormField>
                </div>
                <div className="col-12">
                  <FormField label="Telegram Username">
                    <Input
                      name="telegram_username"
                      defaultValue={telegramConnected ? '@johndoe' : ''}
                      placeholder="@username"
                      disabled={!telegramConnected}
                    />
                  </FormField>
                </div>
              </div>

              <div className="d-flex gap-2 mt-4">
                <Button type="submit" variant="primary" isLoading={isLoading}>
                  Save Changes
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setShowPasswordModal(true)}
                >
                  Change Password
                </Button>
              </div>
            </form>
          </Card>
        </div>

        {/* Integrations */}
        <div className="col-md-6">
          <Card title="Integrations">
            <div className="d-flex flex-col gap-4">
              {/* Telegram */}
              <div className="settings-integration-item">
                <div className="d-flex align-items-center gap-3">
                  <div className="settings-integration-icon telegram">
                    <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.2-.08-.06-.19-.04-.27-.02-.11.02-1.93 1.23-5.46 3.62-.51.35-.98.52-1.4.51-.46-.01-1.35-.26-2.01-.48-.81-.27-1.44-.42-1.38-.88.03-.24.37-.49 1.03-.74 4.04-1.76 6.74-2.92 8.09-3.48 3.85-1.6 4.64-1.89 5.17-1.9.11 0 .37.03.54.17.14.12.18.28.2.45-.02.07-.02.13-.03.26z"/>
                    </svg>
                  </div>
                  <div className="flex-grow-1">
                    <h4 className="m-0 fs-6">Telegram</h4>
                    <p className="text-muted small m-0">
                      {telegramConnected ? 'Connected to @johndoe' : 'Connect your Telegram account'}
                    </p>
                  </div>
                  <Switch
                    checked={telegramConnected}
                    onChange={handleConnectTelegram}
                    label={telegramConnected ? 'On' : 'Off'}
                  />
                </div>
              </div>

              {/* Slack */}
              <div className="settings-integration-item">
                <div className="d-flex align-items-center gap-3">
                  <div className="settings-integration-icon slack">
                    <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
                      <path d="M5.042 15.165a2.528 2.528 0 0 1-2.52 2.523A2.528 2.528 0 0 1 0 15.165a2.527 2.527 0 0 1 2.522-2.52h2.52v2.52zM6.313 15.165a2.527 2.527 0 0 1 2.521-2.52 2.527 2.527 0 0 1 2.521 2.52v6.313A2.528 2.528 0 0 1 8.834 24a2.528 2.528 0 0 1-2.521-2.522v-6.313zM8.834 5.042a2.528 2.528 0 0 1-2.521-2.52A2.528 2.528 0 0 1 8.834 0a2.528 2.528 0 0 1 2.521 2.522v2.52H8.834zM8.834 6.313a2.528 2.528 0 0 1 2.521 2.521 2.528 2.528 0 0 1-2.521 2.521H2.522A2.528 2.528 0 0 1 0 8.834a2.528 2.528 0 0 1 2.522-2.521h6.312zM18.956 8.834a2.528 2.528 0 0 1 2.522-2.521A2.528 2.528 0 0 1 24 8.834a2.528 2.528 0 0 1-2.522 2.521h-2.522V8.834zM17.688 8.834a2.528 2.528 0 0 1-2.522 2.521 2.527 2.527 0 0 1-2.521-2.521V2.522A2.527 2.527 0 0 1 15.166 0a2.528 2.528 0 0 1 2.522 2.522v6.312zM15.166 18.956a2.528 2.528 0 0 1 2.522 2.522A2.528 2.528 0 0 1 15.166 24a2.527 2.527 0 0 1-2.521-2.522v-2.52h2.521zM15.166 17.688a2.527 2.527 0 0 1-2.521-2.522 2.527 2.527 0 0 1 2.521-2.521h6.312A2.527 2.527 0 0 1 24 15.166a2.528 2.528 0 0 1-2.522 2.522h-6.312z"/>
                    </svg>
                  </div>
                  <div className="flex-grow-1">
                    <h4 className="m-0 fs-6">Slack</h4>
                    <p className="text-muted small m-0">Connect Slack workspace</p>
                  </div>
                  <Button variant="outline" size="sm">Connect</Button>
                </div>
              </div>

              {/* Google Calendar */}
              <div className="settings-integration-item">
                <div className="d-flex align-items-center gap-3">
                  <div className="settings-integration-icon google">
                    <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
                      <path d="M21.35 11.1h-9.17v2.73h6.51c-.33 3.81-3.5 5.44-6.5 5.44C8.36 19.27 5 16.25 5 12c0-4.1 3.2-7.27 7.2-7.27 3.09 0 4.9 1.97 4.9 1.97L19 4.72S14.86 2 12.2 2C6.73 2 2 6.73 2 12s4.73 10 10 10c5.09 0 8.55-3.59 8.55-8.74 0-.6-.06-1.06-.13-1.56z"/>
                    </svg>
                  </div>
                  <div className="flex-grow-1">
                    <h4 className="m-0 fs-6">Google Calendar</h4>
                    <p className="text-muted small m-0">Sync publication schedule</p>
                  </div>
                  <Button variant="outline" size="sm">Connect</Button>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Change Password Modal */}
      <Modal
        isOpen={showPasswordModal}
        onClose={() => setShowPasswordModal(false)}
        title="Change Password"
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowPasswordModal(false)}>
              Cancel
            </Button>
            <Button
              variant="primary"
              type="submit"
              form="change-password-form"
            >
              Change Password
            </Button>
          </>
        }
      >
        <form id="change-password-form" onSubmit={handleChangePassword}>
          <FormField label="Current Password" required>
            <Input name="current_password" type="password" required />
          </FormField>
          <FormField label="New Password" required>
            <Input name="new_password" type="password" required />
          </FormField>
          <FormField label="Confirm Password" required>
            <Input name="confirm_password" type="password" required />
          </FormField>
        </form>
      </Modal>
    </div>
  )
}

// ===== Project Tab =====
function ProjectTab() {
  const [isLoading, setIsLoading] = useState(false)

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    toast.success('Project settings saved')
    setIsLoading(false)
  }

  return (
    <div className="settings-project">
      <Card title="Project Settings">
        <form onSubmit={handleSave}>
          <div className="row g-3">
            <div className="col-6">
              <FormField label="Project Name" required>
                <Input name="name" defaultValue="My Project" required />
              </FormField>
            </div>
            <div className="col-6">
              <FormField label="Project Slug" required>
                <Input name="slug" defaultValue="my-project" required />
              </FormField>
            </div>
            <div className="col-6">
              <FormField label="Timezone" required>
                <Select
                  name="timezone"
                  defaultValue="UTC"
                  options={[
                    { value: 'UTC', label: 'UTC' },
                    { value: 'Europe/Moscow', label: 'Moscow (UTC+3)' },
                    { value: 'Europe/London', label: 'London (UTC+0)' },
                    { value: 'America/New_York', label: 'New York (UTC-5)' },
                    { value: 'Asia/Tokyo', label: 'Tokyo (UTC+9)' },
                  ]}
                  required
                />
              </FormField>
            </div>
            <div className="col-6">
              <FormField label="Language" required>
                <Select
                  name="language"
                  defaultValue="en"
                  options={[
                    { value: 'en', label: 'English' },
                    { value: 'ru', label: 'Russian' },
                    { value: 'es', label: 'Spanish' },
                  ]}
                  required
                />
              </FormField>
            </div>
            <div className="col-12">
              <FormField label="Description">
                <Textarea
                  name="description"
                  placeholder="Project description..."
                  rows={4}
                />
              </FormField>
            </div>
          </div>

          <div className="d-flex gap-2 mt-4">
            <Button type="submit" variant="primary" isLoading={isLoading}>
              Save Changes
            </Button>
            <Button type="button" variant="danger" onClick={() => toast.error('Delete project not implemented')}>
              Delete Project
            </Button>
          </div>
        </form>
      </Card>
    </div>
  )
}

// ===== Members Tab =====
function MembersTab() {
  const [members, setMembers] = useState(mockMembers)
  const [showInviteModal, setShowInviteModal] = useState(false)

  const handleRemoveMember = (id: string) => {
    setMembers(members.filter(m => m.id !== id))
    toast.success('Member removed')
  }

  const handleInviteMember = (e: React.FormEvent) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget as HTMLFormElement)
    const newMember = {
      id: String(Date.now()),
      name: formData.get('name') as string,
      email: formData.get('email') as string,
      role: formData.get('role') as string,
      status: 'pending',
      avatar: '',
    }
    setMembers([...members, newMember])
    setShowInviteModal(false)
    toast.success(`Invitation sent to ${newMember.email}`)
  }

  const getRoleBadgeVariant = (role: string) => {
    switch (role) {
      case 'admin': return 'danger'
      case 'editor': return 'primary'
      case 'viewer': return 'neutral'
      default: return 'neutral'
    }
  }

  return (
    <div className="settings-members">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h3 className="h5 mb-1">Team Members</h3>
          <p className="text-muted small m-0">Manage who has access to this project</p>
        </div>
        <Button onClick={() => setShowInviteModal(true)}>
          + Invite Member
        </Button>
      </div>

      <Card noPadding>
        <div className="table-responsive">
          <table className="tf-table">
            <thead>
              <tr>
                <th>Member</th>
                <th>Role</th>
                <th>Status</th>
                <th>Joined</th>
                <th className="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              {members.map((member) => (
                <tr key={member.id}>
                  <td>
                    <div className="d-flex align-items-center gap-3">
                      <Avatar name={member.name} size="sm" />
                      <div>
                        <div className="fw-medium">{member.name}</div>
                        <div className="text-muted small">{member.email}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <Badge variant={getRoleBadgeVariant(member.role)}>
                      {member.role}
                    </Badge>
                  </td>
                  <td>
                    <Badge variant={member.status === 'active' ? 'success' : 'warning'}>
                      {member.status}
                    </Badge>
                  </td>
                  <td className="text-muted">Jan 15, 2026</td>
                  <td className="text-end">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleRemoveMember(member.id)}
                    >
                      Remove
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Invite Modal */}
      <Modal
        isOpen={showInviteModal}
        onClose={() => setShowInviteModal(false)}
        title="Invite Team Member"
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowInviteModal(false)}>
              Cancel
            </Button>
            <Button
              variant="primary"
              type="submit"
              form="invite-member-form"
            >
              Send Invitation
            </Button>
          </>
        }
      >
        <form id="invite-member-form" onSubmit={handleInviteMember}>
          <FormField label="Name" required>
            <Input name="name" placeholder="John Doe" required />
          </FormField>
          <FormField label="Email" required>
            <Input name="email" type="email" placeholder="john@example.com" required />
          </FormField>
          <FormField label="Role" required>
            <Select
              name="role"
              options={roleOptions}
              defaultValue="viewer"
              required
            />
          </FormField>
          <div className="alert alert-info small mb-0">
            Invited members will receive an email with instructions to join the project.
          </div>
        </form>
      </Modal>
    </div>
  )
}

// ===== Roles Tab =====
function RolesTab() {
  const [permissions, setPermissions] = useState({
    'articles.read': true,
    'articles.create': true,
    'articles.edit': false,
    'articles.delete': false,
    'articles.moderate': false,
    'publishing.read': true,
    'publishing.create': false,
    'publishing.execute': false,
    'funnels.read': true,
    'funnels.create': false,
    'funnels.manage': false,
    'analytics.read': true,
    'settings.read': false,
    'settings.manage': false,
    'members.read': false,
    'members.invite': false,
    'members.remove': false,
  })

  const permissionGroups = [
    {
      name: 'Articles',
      permissions: [
        { key: 'articles.read', label: 'Read articles' },
        { key: 'articles.create', label: 'Create articles' },
        { key: 'articles.edit', label: 'Edit articles' },
        { key: 'articles.delete', label: 'Delete articles' },
        { key: 'articles.moderate', label: 'Moderate articles' },
      ],
    },
    {
      name: 'Publishing',
      permissions: [
        { key: 'publishing.read', label: 'View publishing' },
        { key: 'publishing.create', label: 'Create publications' },
        { key: 'publishing.execute', label: 'Execute publications' },
      ],
    },
    {
      name: 'Funnels',
      permissions: [
        { key: 'funnels.read', label: 'View funnels' },
        { key: 'funnels.create', label: 'Create funnels' },
        { key: 'funnels.manage', label: 'Manage funnels' },
      ],
    },
    {
      name: 'Analytics',
      permissions: [
        { key: 'analytics.read', label: 'View analytics' },
      ],
    },
    {
      name: 'Settings',
      permissions: [
        { key: 'settings.read', label: 'View settings' },
        { key: 'settings.manage', label: 'Manage settings' },
        { key: 'members.read', label: 'View members' },
        { key: 'members.invite', label: 'Invite members' },
        { key: 'members.remove', label: 'Remove members' },
      ],
    },
  ]

  const togglePermission = (key: string) => {
    setPermissions(prev => ({ ...prev, [key]: !prev[key as keyof typeof prev] }))
  }

  const handleSave = () => {
    console.log('Permissions:', permissions)
    toast.success('Role permissions saved')
  }

  return (
    <div className="settings-roles">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h3 className="h5 mb-1">Role Permissions</h3>
          <p className="text-muted small m-0">Configure what each role can do</p>
        </div>
        <Button onClick={handleSave}>
          Save Changes
        </Button>
      </div>

      <div className="row g-4">
        {permissionGroups.map((group) => (
          <div className="col-md-6" key={group.name}>
            <Card title={group.name}>
              <div className="d-flex flex-col gap-3">
                {group.permissions.map((perm) => (
                  <div
                    key={perm.key}
                    className="d-flex justify-content-between align-items-center"
                  >
                    <span className="text-sm">{perm.label}</span>
                    <Switch
                      checked={permissions[perm.key as keyof typeof permissions]}
                      onChange={() => togglePermission(perm.key)}
                      size="sm"
                    />
                  </div>
                ))}
              </div>
            </Card>
          </div>
        ))}
      </div>
    </div>
  )
}

// ===== Main Settings Page =====
export function SettingsPage() {
  const [activeTab, setActiveTab] = useState<'profile' | 'project' | 'members' | 'roles'>('profile')

  const tabs = [
    { id: 'profile', label: 'Profile' },
    { id: 'project', label: 'Project' },
    { id: 'members', label: 'Members' },
    { id: 'roles', label: 'Roles' },
  ]

  return (
    <div className="settings-page">
      <h1 className="h2 mb-4">Settings</h1>

      <Tabs tabs={tabs} activeTab={activeTab} onChange={(tab) => setActiveTab(tab as any)}>
        {activeTab === 'profile' && <ProfileTab />}
        {activeTab === 'project' && <ProjectTab />}
        {activeTab === 'members' && <MembersTab />}
        {activeTab === 'roles' && <RolesTab />}
      </Tabs>
    </div>
  )
}
