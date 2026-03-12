import { cn } from '@/utils'
import type { InputHTMLAttributes } from 'react'
import './Input.css'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  error?: string
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  size?: 'sm' | 'md' | 'lg'
}

export function Input({
  className,
  error,
  leftIcon,
  rightIcon,
  size = 'md',
  ...props
}: InputProps) {
  return (
    <div className="tf-input-wrapper">
      <div className={cn('tf-input-container', `tf-input-container--${size}`, className)}>
        {leftIcon && <span className="tf-input__icon tf-input__icon--left">{leftIcon}</span>}
        <input
          className={cn(
            'tf-input',
            error && 'tf-input--error'
          )}
          {...props}
        />
        {rightIcon && <span className="tf-input__icon tf-input__icon--right">{rightIcon}</span>}
      </div>
      {error && <span className="tf-input__error">{error}</span>}
    </div>
  )
}
