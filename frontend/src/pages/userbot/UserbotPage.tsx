import { useState } from 'react'
import { Card, StatCard, Button, Table, StatusBadge, Modal, FormField, Input } from '@/components/ui'
import { userbotApi, type UserbotAccount } from '@/services/userbotApi'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'

type AuthStep = 'phone' | 'code' | '2fa' | 'done'

export function UserbotPage() {
  const [showAddModal, setShowAddModal] = useState(false)
  const [authStep, setAuthStep] = useState<AuthStep>('phone')
  const [selectedAccount, setSelectedAccount] = useState<string | null>(null)
  const [authData, setAuthData] = useState({
    phone: '',
    code: '',
    password: '',
  })
  const queryClient = useQueryClient()

  const { data: accounts, isLoading } = useQuery({
    queryKey: ['userbot-accounts'],
    queryFn: () => userbotApi.getAccounts('550e8400-e29b-41d4-a716-446655440000').then(r => r.data.data),
  })

  const createMutation = useMutation({
    mutationFn: (data: { name: string }) => userbotApi.createAccount({ project_id: '550e8400-e29b-41d4-a716-446655440000', ...data }),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['userbot-accounts'] })
      setSelectedAccount(data.data.data.id)
      setAuthStep('phone')
      toast.success('Account created. Now authorize it.')
    },
  })

  const sendCodeMutation = useMutation({
    mutationFn: ({ accountId, phone }: { accountId: string; phone: string }) =>
      userbotApi.sendCode(accountId, phone),
    onSuccess: () => {
      setAuthStep('code')
      toast.success('Code sent to your Telegram')
    },
  })

  const verifyCodeMutation = useMutation({
    mutationFn: ({ accountId, code }: { accountId: string; code: string }) =>
      userbotApi.verifyCode(accountId, code),
    onSuccess: (data) => {
      if (data.data.data.needs_2fa) {
        setAuthStep('2fa')
      } else {
        setAuthStep('done')
        queryClient.invalidateQueries({ queryKey: ['userbot-accounts'] })
        toast.success('Authorized successfully!')
        setTimeout(() => {
          setShowAddModal(false)
          setAuthStep('phone')
        }, 1500)
      }
    },
  })

  const submit2FAMutation = useMutation({
    mutationFn: ({ accountId, password }: { accountId: string; password: string }) =>
      userbotApi.submit2FA(accountId, password),
    onSuccess: () => {
      setAuthStep('done')
      queryClient.invalidateQueries({ queryKey: ['userbot-accounts'] })
      toast.success('2FA verified! Account authorized.')
      setTimeout(() => {
        setShowAddModal(false)
        setAuthStep('phone')
      }, 1500)
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => userbotApi.deleteAccount(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['userbot-accounts'] })
      toast.success('Account deleted')
    },
  })

  const statusMap: Record<string, 'active' | 'pending' | 'failed'> = {
    'inactive': 'pending',
    'active': 'active',
    'banned': 'failed',
    'needs_auth': 'pending',
    'needs_2fa': 'pending',
  }

  const columns = [
    { key: 'name', title: 'Name' },
    { key: 'username', title: 'Username' },
    { key: 'phone_number', title: 'Phone' },
    {
      key: 'status',
      title: 'Status',
      render: (item: UserbotAccount) => (
        <StatusBadge status={statusMap[item.status] || 'pending'} />
      ),
    },
    {
      key: 'actions',
      title: 'Actions',
      render: (item: UserbotAccount) => (
        <div className="d-flex gap-2">
          {item.status === 'needs_auth' && (
            <Button 
              size="sm" 
              variant="primary" 
              onClick={() => {
                setSelectedAccount(item.id)
                setAuthStep('phone')
                setShowAddModal(true)
              }}
            >
              Authorize
            </Button>
          )}
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

  const handleCreateAccount = () => {
    const name = (document.getElementById('account-name') as HTMLInputElement)?.value
    if (name) {
      createMutation.mutate({ name })
    }
  }

  const handleSendCode = () => {
    if (selectedAccount && authData.phone) {
      sendCodeMutation.mutate({ accountId: selectedAccount, phone: authData.phone })
    }
  }

  const handleVerifyCode = () => {
    if (selectedAccount && authData.code) {
      verifyCodeMutation.mutate({ accountId: selectedAccount, code: authData.code })
    }
  }

  const handleSubmit2FA = () => {
    if (selectedAccount && authData.password) {
      submit2FAMutation.mutate({ accountId: selectedAccount, password: authData.password })
    }
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1 className="h2 mb-0">Userbot</h1>
        <Button onClick={() => { setShowAddModal(true); setAuthStep('phone'); setSelectedAccount(null) }}>
          + Add Account
        </Button>
      </div>

      {/* Stats */}
      <div className="row g-4 mb-4">
        <div className="col-md-3">
          <StatCard title="Total Accounts" value={accounts?.length || 0} icon="🤖" />
        </div>
        <div className="col-md-3">
          <StatCard title="Active" value={accounts?.filter((a: UserbotAccount) => a.status === 'active').length || 0} icon="✅" />
        </div>
        <div className="col-md-3">
          <StatCard title="Needs Auth" value={accounts?.filter((a: UserbotAccount) => a.status === 'needs_auth').length || 0} icon="⏳" />
        </div>
        <div className="col-md-3">
          <StatCard title="Warming" value={accounts?.filter((a: UserbotAccount) => a.is_warming_enabled).length || 0} icon="🔥" />
        </div>
      </div>

      {/* Accounts List */}
      <Card title="Accounts">
        {isLoading ? (
          <div className="text-center py-5">Loading...</div>
        ) : (
          <Table data={accounts || []} columns={columns} />
        )}
      </Card>

      {/* Add/Authorize Account Modal */}
      <Modal
        isOpen={showAddModal}
        onClose={() => { setShowAddModal(false); setAuthStep('phone') }}
        title={selectedAccount ? 'Authorize Account' : 'Add New Account'}
        size="md"
      >
        {!selectedAccount ? (
          <div>
            <FormField label="Account Name">
              <Input id="account-name" placeholder="My Userbot" />
            </FormField>
            <div className="alert alert-info small">
              After creating the account, you'll need to authorize it with your Telegram phone number.
            </div>
            <Button 
              className="w-100" 
              onClick={handleCreateAccount}
              disabled={createMutation.isPending}
            >
              {createMutation.isPending ? 'Creating...' : 'Create Account'}
            </Button>
          </div>
        ) : authStep === 'phone' ? (
          <div>
            <FormField label="Phone Number" required>
              <Input
                type="tel"
                placeholder="+1234567890"
                value={authData.phone}
                onChange={(e) => setAuthData({ ...authData, phone: e.target.value })}
              />
            </FormField>
            <div className="alert alert-info small">
              Enter your Telegram phone number with country code.
            </div>
            <Button 
              className="w-100" 
              onClick={handleSendCode}
              disabled={sendCodeMutation.isPending || !authData.phone}
            >
              {sendCodeMutation.isPending ? 'Sending...' : 'Send Code'}
            </Button>
          </div>
        ) : authStep === 'code' ? (
          <div>
            <FormField label="Verification Code" required>
              <Input
                type="text"
                placeholder="12345"
                value={authData.code}
                onChange={(e) => setAuthData({ ...authData, code: e.target.value })}
                maxLength={10}
              />
            </FormField>
            <div className="alert alert-info small">
              Enter the code you received from Telegram.
            </div>
            <Button 
              className="w-100" 
              onClick={handleVerifyCode}
              disabled={verifyCodeMutation.isPending || !authData.code}
            >
              {verifyCodeMutation.isPending ? 'Verifying...' : 'Verify Code'}
            </Button>
          </div>
        ) : authStep === '2fa' ? (
          <div>
            <FormField label="2FA Password" required>
              <Input
                type="password"
                placeholder="Your 2FA password"
                value={authData.password}
                onChange={(e) => setAuthData({ ...authData, password: e.target.value })}
              />
            </FormField>
            <div className="alert alert-warning small">
              Your Telegram account has two-factor authentication enabled.
            </div>
            <Button 
              className="w-100" 
              onClick={handleSubmit2FA}
              disabled={submit2FAMutation.isPending || !authData.password}
            >
              {submit2FAMutation.isPending ? 'Verifying...' : 'Verify 2FA'}
            </Button>
          </div>
        ) : (
          <div className="text-center py-4">
            <span className="fs-1">✅</span>
            <h4 className="mt-3">Authorization Successful!</h4>
            <p className="text-muted">Redirecting...</p>
          </div>
        )}
      </Modal>
    </div>
  )
}
