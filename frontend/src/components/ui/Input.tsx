import React, { forwardRef, InputHTMLAttributes } from 'react'
import { cn } from '@/utils'
import './Input.css'

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  error?: boolean
  errorText?: string
  label?: string
  hint?: string
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      className,
      type = 'text',
      leftIcon,
      rightIcon,
      error = false,
      errorText,
      label,
      hint,
      disabled,
      id,
      ...props
    },
    ref
  ) => {
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`
    const hintId = `${inputId}-hint`
    const errorId = `${inputId}-error`

    return (
      <div className={cn('tf-input-wrapper', { 'tf-input-wrapper--error': error }, className)}>
        {label && (
          <label htmlFor={inputId} className="tf-input__label">
            {label}
          </label>
        )}
        <div className="tf-input__container">
          {leftIcon && <span className="tf-input__icon tf-input__icon--left">{leftIcon}</span>}
          <input
            ref={ref}
            type={type}
            id={inputId}
            className="tf-input"
            disabled={disabled}
            aria-invalid={error}
            aria-describedby={error ? errorId : hint ? hintId : undefined}
            {...props}
          />
          {rightIcon && <span className="tf-input__icon tf-input__icon--right">{rightIcon}</span>}
        </div>
        {hint && !error && (
          <span id={hintId} className="tf-input__hint">
            {hint}
          </span>
        )}
        {error && errorText && (
          <span id={errorId} className="tf-input__error">
            {errorText}
          </span>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'
