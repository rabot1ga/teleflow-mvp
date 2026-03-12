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
  terms: z.boolean().refine(val => val === true, 'You must accept the terms'),
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
    <div className="card shadow" style={{ maxWidth: '500px', width: '100%' }}>
      <div className="card-body p-4">
        <div className="text-center mb-4">
          <h1 className="h3 mb-2">🚀 TeleFlow</h1>
          <p className="text-muted">Create your account</p>
        </div>

        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="row">
            <div className="col-md-6 mb-3">
              <label htmlFor="firstName" className="form-label">
                First Name
              </label>
              <input
                type="text"
                className={`form-control ${errors.firstName ? 'is-invalid' : ''}`}
                id="firstName"
                {...register('firstName')}
                placeholder="John"
              />
              {errors.firstName && (
                <div className="invalid-feedback">{errors.firstName.message}</div>
              )}
            </div>

            <div className="col-md-6 mb-3">
              <label htmlFor="lastName" className="form-label">
                Last Name
              </label>
              <input
                type="text"
                className={`form-control ${errors.lastName ? 'is-invalid' : ''}`}
                id="lastName"
                {...register('lastName')}
                placeholder="Doe"
              />
              {errors.lastName && (
                <div className="invalid-feedback">{errors.lastName.message}</div>
              )}
            </div>
          </div>

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

          <div className="mb-3">
            <label htmlFor="confirmPassword" className="form-label">
              Confirm Password
            </label>
            <input
              type="password"
              className={`form-control ${errors.confirmPassword ? 'is-invalid' : ''}`}
              id="confirmPassword"
              {...register('confirmPassword')}
              placeholder="••••••••"
            />
            {errors.confirmPassword && (
              <div className="invalid-feedback">{errors.confirmPassword.message}</div>
            )}
          </div>

          <div className="mb-3 form-check">
            <input
              type="checkbox"
              className={`form-check-input ${errors.terms ? 'is-invalid' : ''}`}
              id="terms"
              {...register('terms')}
            />
            <label className="form-check-label small" htmlFor="terms">
              I agree to the{' '}
              <a href="#" className="text-decoration-none">Terms of Service</a>
              {' '}and{' '}
              <a href="#" className="text-decoration-none">Privacy Policy</a>
            </label>
            {errors.terms && (
              <div className="invalid-feedback d-block">{errors.terms.message}</div>
            )}
          </div>

          <button
            type="submit"
            className="btn btn-primary w-100 mb-3"
            disabled={isLoading}
          >
            {isLoading ? 'Creating account...' : 'Create Account'}
          </button>

          <div className="text-center">
            <span className="text-muted">Already have an account?</span>{' '}
            <Link to="/login" className="text-decoration-none">
              Sign in
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}
