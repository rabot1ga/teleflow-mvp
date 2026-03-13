import React from 'react'
import { cn } from '@/utils'
import './Button.css'

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'success' | 'danger' | 'warning'
export type ButtonSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl'

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  size?: ButtonSize
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  isLoading?: boolean
  fullWidth?: boolean
  children: React.ReactNode
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant = 'primary',
      size = 'md',
      leftIcon,
      rightIcon,
      isLoading = false,
      fullWidth = false,
      disabled,
      children,
      ...props
    },
    ref
  ) => {
    const classes = cn(
      'tf-button',
      `tf-button--${variant}`,
      `tf-button--${size}`,
      {
        'tf-button--loading': isLoading,
        'tf-button--full-width': fullWidth,
        'tf-button--disabled': disabled || isLoading,
      },
      className
    )

    return (
      <button ref={ref} className={classes} disabled={disabled || isLoading} {...props}>
        {isLoading && (
          <span className="tf-button__loader">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeOpacity="0.2" />
              <path
                d="M12 2C16.9706 2 21 6.02944 21 11"
                stroke="currentColor"
                strokeWidth="3"
                strokeLinecap="round"
              />
            </svg>
          </span>
        )}
        {leftIcon && <span className="tf-button__icon tf-button__icon--left">{leftIcon}</span>}
        <span className="tf-button__content">{children}</span>
        {rightIcon && <span className="tf-button__icon tf-button__icon--right">{rightIcon}</span>}
      </button>
    )
  }
)

Button.displayName = 'Button'
