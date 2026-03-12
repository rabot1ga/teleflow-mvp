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
  firstName: z.string().min(1, 'Required'),
  lastName: z.string().min(1, 'Required'),
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters'),
  confirmPassword: z.string(),
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
      toast.success('Account created!')
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
          <span className="auth-alert__icon">⚠️</span>
          {error}
        </div>
      )}

      <div className="grid-2">
        <div className="auth-form__group">
          <label className="auth-form__label" htmlFor="firstName">
            First Name
          </label>
          <Input
            id="firstName"
            placeholder="John"
            error={errors.firstName?.message}
            {...register('firstName')}
          />
        </div>

        <div className="auth-form__group">
          <label className="auth-form__label" htmlFor="lastName">
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

      <div className="auth-form__group">
        <label className="auth-form__label" htmlFor="email">
          Email
        </label>
        <Input
          id="email"
          type="email"
          placeholder="you@example.com"
          error={errors.email?.message}
          {...register('email')}
        />
      </div>

      <div className="auth-form__group">
        <label className="auth-form__label" htmlFor="password">
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

      <div className="auth-form__group">
        <label className="auth-form__label" htmlFor="confirmPassword">
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
            Creating account...
          </>
        ) : (
          'Create Account'
        )}
      </Button>

      <p className="auth-form__footer">
        Already have an account?{' '}
        <Link to="/login" className="auth-form__link auth-form__link--bold">
          Sign in
        </Link>
      </p>
    </form>
  )
}
