import { forwardRef, TextareaHTMLAttributes } from 'react'
import { cn } from '@/utils'
import './Textarea.css'

export interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  error?: boolean
  errorText?: string
  label?: string
  hint?: string
  resize?: 'none' | 'vertical' | 'auto'
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  (
    {
      className,
      error = false,
      errorText,
      label,
      hint,
      resize = 'vertical',
      disabled,
      id,
      rows = 4,
      ...props
    },
    ref
  ) => {
    const textareaId = id || `textarea-${Math.random().toString(36).substr(2, 9)}`
    const hintId = `${textareaId}-hint`
    const errorId = `${textareaId}-error`

    return (
      <div className={cn('tf-textarea-wrapper', { 'tf-textarea-wrapper--error': error }, className)}>
        {label && (
          <label htmlFor={textareaId} className="tf-textarea__label">
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          id={textareaId}
          className={cn('tf-textarea', `tf-textarea--resize-${resize}`, { 'tf-textarea--error': error })}
          rows={rows}
          disabled={disabled}
          aria-invalid={error}
          aria-describedby={error ? errorId : hint ? hintId : undefined}
          {...props}
        />
        {hint && !error && (
          <span id={hintId} className="tf-textarea__hint">
            {hint}
          </span>
        )}
        {error && errorText && (
          <span id={errorId} className="tf-textarea__error">
            {errorText}
          </span>
        )}
      </div>
    )
  }
)

Textarea.displayName = 'Textarea'
