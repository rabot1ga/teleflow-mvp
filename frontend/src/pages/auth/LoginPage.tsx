import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import toast from 'react-hot-toast'
import { useAuthStore } from '../../stores/authStore'
import { Button, Input } from '@/components/ui'
import './AuthForm.css'

const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(6, 'Min 6 characters'),
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
          <span className="auth-alert__icon">⚠️</span>
          {error}
        </div>
      )}

      <div className="auth-form__group">
        <label className="auth-form__label" htmlFor="email">
          Email
        </label>
        <Input
          id="email"
          type="email"
          placeholder="you@example.com"
          error={!!errors.email?.message}
          errorText={errors.email?.message}
          {...register('email')}
        />
      </div>

      <div className="auth-form__group">
        <div className="auth-form__label-row">
          <label className="auth-form__label" htmlFor="password">
            Password
          </label>
          <Link to="/forgot-password" className="auth-form__link">
            Forgot?
          </Link>
        </div>
        <Input
          id="password"
          type="password"
          placeholder="••••••••"
          error={!!errors.password?.message}
          errorText={errors.password?.message}
          {...register('password')}
        />
      </div>

      <div className="auth-form__checkbox-group">
        <label className="auth-form__checkbox">
          <input type="checkbox" id="remember" />
          <span>Remember me for 30 days</span>
        </label>
      </div>

      <Button 
        type="submit" 
        variant="primary" 
        size="lg" 
        fullWidth 
        isLoading={isLoading}
        className="auth-form__submit"
      >
        {isLoading ? (
          <>
            <span className="auth-form__spinner"></span>
            Signing in...
          </>
        ) : (
          'Sign In'
        )}
      </Button>

      <div className="auth-form__divider">
        <span>or continue with</span>
      </div>

      <Button 
        type="button" 
        variant="outline" 
        size="lg" 
        fullWidth
        className="auth-form__telegram"
      >
        <svg className="auth-form__telegram-icon" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.16.16-.295.295-.605.295l.213-3.054 5.56-5.022c.242-.213-.054-.334-.373-.121l-6.869 4.326-2.96-.924c-.64-.203-.658-.64.135-.954l11.566-4.458c.538-.196 1.006.128.832.941z"/>
        </svg>
        Sign in with Telegram
      </Button>

      <p className="auth-form__footer">
        Don't have an account?{' '}
        <Link to="/register" className="auth-form__link auth-form__link--bold">
          Sign up
        </Link>
      </p>
    </form>
  )
}
