import { Card, Button } from '@/components/ui'
import toast from 'react-hot-toast'

export function PublishingPage() {
  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1 className="h2 mb-0">Publishing</h1>
        <Button onClick={() => toast.success('Create Target')}>+ Add Target</Button>
      </div>

      <div className="row g-4">
        <div className="col-md-6">
          <Card title="Targets">
            <div className="text-center text-muted py-5">
              <span className="fs-1">📤</span>
              <p className="mt-3">Telegram channels and groups</p>
            </div>
          </Card>
        </div>
        <div className="col-md-6">
          <Card title="Templates">
            <div className="text-center text-muted py-5">
              <span className="fs-1">📝</span>
              <p className="mt-3">Message templates</p>
            </div>
          </Card>
        </div>
      </div>

      <div className="mt-4">
        <Card title="Publish Calendar">
          <div className="text-center text-muted py-5">
            <p>Calendar view for scheduled publications</p>
          </div>
        </Card>
      </div>
    </div>
  )
}

export function SettingsPage() {
  return (
    <div>
      <h1 className="h2 mb-4">Settings</h1>

      <div className="row g-4">
        <div className="col-md-6">
          <Card title="Profile Settings">
            <form>
              <div className="mb-3">
                <label className="form-label">Email</label>
                <input type="email" className="form-control" defaultValue="test@example.com" />
              </div>
              <div className="mb-3">
                <label className="form-label">First Name</label>
                <input type="text" className="form-control" defaultValue="Test" />
              </div>
              <div className="mb-3">
                <label className="form-label">Last Name</label>
                <input type="text" className="form-control" defaultValue="User" />
              </div>
              <Button type="button" onClick={() => toast.success('Settings saved')}>
                Save Changes
              </Button>
            </form>
          </Card>
        </div>
        <div className="col-md-6">
          <Card title="Project Settings">
            <div className="text-center text-muted py-5">
              <p>Project configuration</p>
              <small>Members, API keys, notifications</small>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
