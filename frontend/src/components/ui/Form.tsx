import React from 'react'
import { useForm, type UseFormProps } from 'react-hook-form'
import { cn } from '@/utils'

interface FormProps<T extends Record<string, any>> extends UseFormProps<T> {
  onSubmit: (data: T) => void
  children: React.ReactNode | ((props: any) => React.ReactNode)
  className?: string
}

export function Form<T extends Record<string, any>>({
  onSubmit,
  children,
  className,
  ...props
}: FormProps<T>) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<T>({
    ...props,
  })

  const handleFormSubmit = async (data: T) => {
    await onSubmit(data)
    reset()
  }

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className={className} noValidate>
      {typeof children === 'function' ? children({ register, errors, isSubmitting }) : children}
    </form>
  )
}

interface FormFieldProps {
  label: string
  error?: string
  children: React.ReactNode
  className?: string
  required?: boolean
}

export function FormField({ label, error, children, className, required }: FormFieldProps) {
  return (
    <div className={cn('mb-3', className)}>
      <label className="form-label">
        {label}
        {required && <span className="text-danger ms-1">*</span>}
      </label>
      {children}
      {error && <div className="invalid-feedback d-block">{error}</div>}
    </div>
  )
}

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ error, className, ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={cn('form-control', error && 'is-invalid', className)}
        {...props}
      />
    )
  }
)

Input.displayName = 'Input'

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  error?: string
  options: { value: string; label: string }[]
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ error, className, options, ...props }, ref) => {
    return (
      <select ref={ref} className={cn('form-select', error && 'is-invalid', className)} {...props}>
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    )
  }
)

Select.displayName = 'Select'

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  error?: string
}

export const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ error, className, ...props }, ref) => {
    return (
      <textarea
        ref={ref}
        className={cn('form-control', error && 'is-invalid', className)}
        {...props}
      />
    )
  }
)

Textarea.displayName = 'Textarea'
