import { cn } from '@/utils'
import type { CSSProperties } from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'outline' | 'ghost'
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  isLoading?: boolean
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  fullWidth?: boolean
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
  style,
  ...props
}: ButtonProps) {
  const baseClasses = 'tf-button'
  const variantClasses = {
    primary: 'tf-button--primary',
    secondary: 'tf-button--secondary',
    success: 'tf-button--success',
    danger: 'tf-button--danger',
    warning: 'tf-button--warning',
    outline: 'tf-button--outline',
    ghost: 'tf-button--ghost',
  }

  const sizeClasses = {
    xs: 'tf-button--xs',
    sm: 'tf-button--sm',
    md: 'tf-button--md',
    lg: 'tf-button--lg',
    xl: 'tf-button--xl',
  }

  const widthClass = fullWidth ? 'tf-button--full-width' : ''

  return (
    <button
      className={cn(
        baseClasses,
        variantClasses[variant],
        sizeClasses[size],
        widthClass,
        isLoading && 'tf-button--loading',
        className
      )}
      disabled={disabled || isLoading}
      style={style}
      {...props}
    >
      {isLoading && (
        <span className="tf-button__spinner" role="status" aria-hidden="true" />
      )}
      {leftIcon && <span className="tf-button__icon tf-button__icon--left">{leftIcon}</span>}
      <span className="tf-button__content">{children}</span>
      {rightIcon && <span className="tf-button__icon tf-button__icon--right">{rightIcon}</span>}
    </button>
  )
}
