import React, { useState, useCallback } from 'react'
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
      onClick,
      ...props
    },
    ref
  ) => {
    const [ripples, setRipples] = useState<{ x: number; y: number; id: number }[]>([])

    const createRipple = useCallback((event: React.MouseEvent<HTMLButtonElement>) => {
      if (isLoading || disabled) return

      const button = event.currentTarget
      const rect = button.getBoundingClientRect()
      const size = Math.max(rect.width, rect.height)
      const x = event.clientX - rect.left - size / 2
      const y = event.clientY - rect.top - size / 2
      const id = Date.now()

      setRipples((prev) => [...prev, { x, y, id }])

      // Cleanup ripple after animation
      setTimeout(() => {
        setRipples((prev) => prev.filter((ripple) => ripple.id !== id))
      }, 600)
    }, [isLoading, disabled])

    const handleClick = useCallback((event: React.MouseEvent<HTMLButtonElement>) => {
      createRipple(event)
      onClick?.(event)
    }, [createRipple, onClick])

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
      <button
        ref={ref}
        className={classes}
        disabled={disabled || isLoading}
        onClick={handleClick}
        {...props}
      >
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
        
        {/* Ripple effects */}
        {ripples.map((ripple) => (
          <span
            key={ripple.id}
            className="tf-button__ripple"
            style={{
              left: ripple.x,
              top: ripple.y,
              width: '20px',
              height: '20px',
            }}
          />
        ))}
      </button>
    )
  }
)

Button.displayName = 'Button'
