import React, { forwardRef } from 'react'
import { cn } from '@/utils'
import './Switch.css'

export interface SwitchProps {
  checked: boolean
  onChange: (checked: boolean) => void
  disabled?: boolean
  label?: string
  description?: string
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export const Switch = forwardRef<HTMLInputElement, SwitchProps>(
  (
    {
      checked,
      onChange,
      disabled = false,
      label,
      description,
      size = 'md',
      className,
    },
    ref
  ) => {
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      onChange(e.target.checked)
    }

    return (
      <label className={cn('tf-switch-wrapper', `tf-switch-wrapper--${size}`, { 'tf-switch-wrapper--disabled': disabled }, className)}>
        <div className="tf-switch">
          <input
            ref={ref}
            type="checkbox"
            className="tf-switch__input"
            checked={checked}
            onChange={handleChange}
            disabled={disabled}
          />
          <span className="tf-switch__track">
            <span className="tf-switch__thumb" />
          </span>
        </div>
        {(label || description) && (
          <div className="tf-switch__content">
            {label && <span className="tf-switch__label">{label}</span>}
            {description && <span className="tf-switch__description">{description}</span>}
          </div>
        )}
      </label>
    )
  }
)

Switch.displayName = 'Switch'
