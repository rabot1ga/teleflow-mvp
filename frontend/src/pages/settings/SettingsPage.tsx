import { Card, Button } from '@/components/ui'
import toast from 'react-hot-toast'

export function SettingsPage() {
  return (
    <div>
      <h1 className="h2 mb-4">Settings</h1>

      <div className="row g-4">
        <div className="col-md-6">
          <Card title="Profile Settings">
            <form onSubmit={(e) => { e.preventDefault(); toast.success('Settings saved') }}>
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
              <Button type="submit" onClick={() => toast.success('Settings saved')}>
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
