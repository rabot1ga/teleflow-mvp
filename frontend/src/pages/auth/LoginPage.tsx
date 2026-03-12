import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import toast from 'react-hot-toast'
import { useAuthStore } from '../../stores/authStore'
import { Button, Input } from '@/components/ui'

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
})

type LoginForm = z.infer<typeof loginSchema>

export function LoginPage() {
  const navigate = useNavigate()
  const { login, isLoading } = useAuthStore()
  const [error, setError] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = async (data: LoginForm) => {
    try {
      setError(null)
      await login(data.email, data.password)
      toast.success('Welcome back!')
      navigate('/dashboard')
    } catch (err: any) {
      setError(err.message || 'Login failed')
      toast.error(err.message || 'Login failed')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="auth-form">
      {error && (
        <div className="auth-alert auth-alert--error">
          {error}
        </div>
      )}

      <div className="auth-form__field">
        <label htmlFor="email" className="auth-form__label">
          Email Address
        </label>
        <Input
          id="email"
          type="email"
          placeholder="you@example.com"
          error={errors.email?.message}
          {...register('email')}
        />
      </div>

      <div className="auth-form__field">
        <label htmlFor="password" className="auth-form__label">
          Password
        </label>
        <Input
          id="password"
          type="password"
          placeholder="••••••••"
          error={errors.password?.message}
          {...register('password')}
        />
      </div>

      <div className="auth-form__actions">
        <label className="auth-form__checkbox">
          <input type="checkbox" id="remember" />
          Remember me
        </label>
        <Link to="/forgot-password" className="auth-form__link">
          Forgot password?
        </Link>
      </div>

      <Button type="submit" variant="primary" size="lg" fullWidth isLoading={isLoading}>
        {isLoading ? 'Signing in...' : 'Sign In'}
      </Button>

      <div className="auth-form__divider">or continue with</div>

      <Button type="button" className="auth-form__telegram" fullWidth>
        <span>✈️</span> Sign in with Telegram
      </Button>

      <div className="auth-form__footer">
        Don't have an account?{' '}
        <Link to="/register" className="auth-form__link">
          Sign up
        </Link>
      </div>
    </form>
  )
}
