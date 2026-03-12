import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import toast from 'react-hot-toast'
import { useAuthStore } from '../../stores/authStore'

const registerSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
  firstName: z.string().min(1, 'First name is required'),
  lastName: z.string().min(1, 'Last name is required'),
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
})

type RegisterForm = z.infer<typeof registerSchema>

export function RegisterPage() {
  const navigate = useNavigate()
  const { register: registerUser, isLoading } = useAuthStore()
  const [error, setError] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema),
  })

  const onSubmit = async (data: RegisterForm) => {
    try {
      setError(null)
      await registerUser(data.email, data.password, data.firstName, data.lastName)
      toast.success('Account created successfully!')
      navigate('/dashboard')
    } catch (err: any) {
      setError(err.message || 'Registration failed')
      toast.error(err.message || 'Registration failed')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="auth-form">
      {error && (
        <div className="auth-alert auth-alert--error">
          {error}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--tf-spacing-4)' }}>
        <div className="auth-form__field">
          <label htmlFor="firstName" className="auth-form__label">
            First Name
          </label>
          <input
            type="text"
            className={`auth-form__input ${errors.firstName ? 'auth-form__input--error' : ''}`}
            id="firstName"
            {...register('firstName')}
            placeholder="John"
          />
          {errors.firstName && (
            <div className="auth-form__error">{errors.firstName.message}</div>
          )}
        </div>

        <div className="auth-form__field">
          <label htmlFor="lastName" className="auth-form__label">
            Last Name
          </label>
          <input
            type="text"
            className={`auth-form__input ${errors.lastName ? 'auth-form__input--error' : ''}`}
            id="lastName"
            {...register('lastName')}
            placeholder="Doe"
          />
          {errors.lastName && (
            <div className="auth-form__error">{errors.lastName.message}</div>
          )}
        </div>
      </div>

      <div className="auth-form__field">
        <label htmlFor="email" className="auth-form__label">
          Email Address
        </label>
        <input
          type="email"
          className={`auth-form__input ${errors.email ? 'auth-form__input--error' : ''}`}
          id="email"
          {...register('email')}
          placeholder="you@example.com"
        />
        {errors.email && (
          <div className="auth-form__error">{errors.email.message}</div>
        )}
      </div>

      <div className="auth-form__field">
        <label htmlFor="password" className="auth-form__label">
          Password
        </label>
        <input
          type="password"
          className={`auth-form__input ${errors.password ? 'auth-form__input--error' : ''}`}
          id="password"
          {...register('password')}
          placeholder="••••••••"
        />
        {errors.password && (
          <div className="auth-form__error">{errors.password.message}</div>
        )}
      </div>

      <div className="auth-form__field">
        <label htmlFor="confirmPassword" className="auth-form__label">
          Confirm Password
        </label>
        <input
          type="password"
          className={`auth-form__input ${errors.confirmPassword ? 'auth-form__input--error' : ''}`}
          id="confirmPassword"
          {...register('confirmPassword')}
          placeholder="••••••••"
        />
        {errors.confirmPassword && (
          <div className="auth-form__error">{errors.confirmPassword.message}</div>
        )}
      </div>

      <button
        type="submit"
        className="auth-form__submit"
        disabled={isLoading}
      >
        {isLoading ? 'Creating account...' : 'Create Account'}
      </button>

      <div className="auth-form__footer">
        Already have an account?{' '}
        <Link to="/login" className="auth-form__link">
          Sign in
        </Link>
      </div>
    </form>
  )
}
