import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import toast from 'react-hot-toast'
import { useAuthStore } from '../../stores/authStore'

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
    <div className="card shadow" style={{ maxWidth: '400px', width: '100%' }}>
      <div className="card-body p-4">
        <div className="text-center mb-4">
          <h1 className="h3 mb-2">🚀 TeleFlow</h1>
          <p className="text-muted">Sign in to your account</p>
        </div>

        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="mb-3">
            <label htmlFor="email" className="form-label">
              Email
            </label>
            <input
              type="email"
              className={`form-control ${errors.email ? 'is-invalid' : ''}`}
              id="email"
              {...register('email')}
              placeholder="you@example.com"
            />
            {errors.email && (
              <div className="invalid-feedback">{errors.email.message}</div>
            )}
          </div>

          <div className="mb-3">
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <input
              type="password"
              className={`form-control ${errors.password ? 'is-invalid' : ''}`}
              id="password"
              {...register('password')}
              placeholder="••••••••"
            />
            {errors.password && (
              <div className="invalid-feedback">{errors.password.message}</div>
            )}
          </div>

          <div className="d-flex justify-content-between align-items-center mb-3">
            <div className="form-check">
              <input
                type="checkbox"
                className="form-check-input"
                id="remember"
              />
              <label className="form-check-label" htmlFor="remember">
                Remember me
              </label>
            </div>
            <Link to="/forgot-password" className="text-decoration-none small">
              Forgot password?
            </Link>
          </div>

          <button
            type="submit"
            className="btn btn-primary w-100 mb-3"
            disabled={isLoading}
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>

          <div className="text-center">
            <button type="button" className="btn btn-outline-secondary w-100 mb-3">
              <span className="me-2">✈️</span> Sign in with Telegram
            </button>
          </div>

          <div className="text-center">
            <span className="text-muted">Don't have an account?</span>{' '}
            <Link to="/register" className="text-decoration-none">
              Sign up
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}
