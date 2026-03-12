import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button, FormField, Input } from '@/components/ui'
import toast from 'react-hot-toast'

export function ResetPasswordPage() {
  const navigate = useNavigate()
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsLoading(true)
    
    // TODO: Implement password reset API call
    toast.success('Password reset successfully!')
    navigate('/login')
  }

  return (
    <div className="card shadow" style={{ maxWidth: '400px', width: '100%' }}>
      <div className="card-body p-4">
        <h1 className="h3 mb-4 text-center">Reset Password</h1>
        <form onSubmit={handleSubmit}>
          <FormField label="New Password" required>
            <Input type="password" placeholder="••••••••" required minLength={8} />
          </FormField>
          <FormField label="Confirm Password" required>
            <Input type="password" placeholder="••••••••" required minLength={8} />
          </FormField>
          <Button type="submit" className="w-100" disabled={isLoading}>
            {isLoading ? 'Resetting...' : 'Reset Password'}
          </Button>
        </form>
      </div>
    </div>
  )
}
