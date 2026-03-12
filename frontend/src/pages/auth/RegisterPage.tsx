import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import toast from 'react-hot-toast'
import { useAuthStore } from '../../stores/authStore'
import { Button, Input } from '@/components/ui'
import './AuthForm.css'

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

      <div className="grid-2">
        <div className="auth-form__field">
          <label htmlFor="firstName" className="auth-form__label">
            First Name
          </label>
          <Input
            id="firstName"
            placeholder="John"
            error={errors.firstName?.message}
            {...register('firstName')}
          />
        </div>

        <div className="auth-form__field">
          <label htmlFor="lastName" className="auth-form__label">
            Last Name
          </label>
          <Input
            id="lastName"
            placeholder="Doe"
            error={errors.lastName?.message}
            {...register('lastName')}
          />
        </div>
      </div>

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

      <div className="auth-form__field">
        <label htmlFor="confirmPassword" className="auth-form__label">
          Confirm Password
        </label>
        <Input
          id="confirmPassword"
          type="password"
          placeholder="••••••••"
          error={errors.confirmPassword?.message}
          {...register('confirmPassword')}
        />
      </div>

      <Button type="submit" variant="primary" size="lg" fullWidth isLoading={isLoading}>
        {isLoading ? 'Creating account...' : 'Create Account'}
      </Button>

      <div className="auth-form__footer">
        Already have an account?{' '}
        <Link to="/login" className="auth-form__link">
          Sign in
        </Link>
      </div>
    </form>
  )
}
