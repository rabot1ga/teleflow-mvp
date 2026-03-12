import { cn } from '@/utils'
import type { ButtonHTMLAttributes } from 'react'
import './Button.css'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'outline' | 'ghost' | 'link'
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  isLoading?: boolean
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  fullWidth?: boolean
  asChild?: boolean
}

export function Button({
  children,
  className,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  rightIcon,
  disabled,
  fullWidth = false,
  asChild = false,
  ...props
}: ButtonProps) {
  const baseClass = 'tf-button'
  const variantClass = `tf-button--${variant}`
  const sizeClass = `tf-button--${size}`
  const widthClass = fullWidth ? 'tf-button--full-width' : ''
  const loadingClass = isLoading ? 'tf-button--loading' : ''
  const disabledClass = disabled || isLoading ? 'tf-button--disabled' : ''

  const Component = asChild ? 'span' : 'button'

  return (
    <Component
      className={cn(
        baseClass,
        variantClass,
        sizeClass,
        widthClass,
        loadingClass,
        disabledClass,
        className
      )}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && (
        <span className="tf-button__spinner" role="status" aria-hidden="true" />
      )}
      {leftIcon && <span className="tf-button__icon tf-button__icon--left">{leftIcon}</span>}
      <span className="tf-button__content">{children}</span>
      {rightIcon && <span className="tf-button__icon tf-button__icon--right">{rightIcon}</span>}
    </Component>
  )
}
