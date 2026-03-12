import { forwardRef, SelectHTMLAttributes } from 'react'
import { cn } from '@/utils'
import './Select.css'

export interface SelectOption {
  value: string
  label: string
  disabled?: boolean
}

export interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  options: SelectOption[]
  error?: boolean
  errorText?: string
  label?: string
  hint?: string
  placeholder?: string
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  (
    {
      className,
      options,
      error = false,
      errorText,
      label,
      hint,
      placeholder,
      disabled,
      id,
      ...props
    },
    ref
  ) => {
    const selectId = id || `select-${Math.random().toString(36).substr(2, 9)}`
    const hintId = `${selectId}-hint`
    const errorId = `${selectId}-error`

    return (
      <div className={cn('tf-select-wrapper', { 'tf-select-wrapper--error': error }, className)}>
        {label && (
          <label htmlFor={selectId} className="tf-select__label">
            {label}
          </label>
        )}
        <div className="tf-select__container">
          <select
            ref={ref}
            id={selectId}
            className={cn('tf-select', { 'tf-select--error': error })}
            disabled={disabled}
            aria-invalid={error}
            aria-describedby={error ? errorId : hint ? hintId : undefined}
            {...props}
          >
            {placeholder && (
              <option value="" disabled>
                {placeholder}
              </option>
            )}
            {options.map((option) => (
              <option
                key={option.value}
                value={option.value}
                disabled={option.disabled}
              >
                {option.label}
              </option>
            ))}
          </select>
          <div className="tf-select__icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="6,9 12,15 18,9" />
            </svg>
          </div>
        </div>
        {hint && !error && (
          <span id={hintId} className="tf-select__hint">
            {hint}
          </span>
        )}
        {error && errorText && (
          <span id={errorId} className="tf-select__error">
            {errorText}
          </span>
        )}
      </div>
    )
  }
)

Select.displayName = 'Select'
