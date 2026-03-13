import React from 'react'
import { cn } from '@/utils'
import './ProgressBar.css'

export interface ProgressBarProps {
  value: number
  max?: number
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'primary'
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
  label?: string
  className?: string
  animated?: boolean
  striped?: boolean
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  max = 100,
  variant = 'default',
  size = 'md',
  showLabel = false,
  label,
  className,
  animated = false,
  striped = false,
}) => {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100))
  const displayLabel = label || `${Math.round(percentage)}%`

  return (
    <div className={cn('tf-progress-bar-wrapper', `tf-progress-bar-wrapper--${size}`, className)}>
      <div
        className={cn(
          'tf-progress-bar',
          `tf-progress-bar--${variant}`,
          {
            'tf-progress-bar--animated': animated,
            'tf-progress-bar--striped': striped,
          }
        )}
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
        aria-label={label}
      >
        <div
          className="tf-progress-bar__fill"
          style={{ width: `${percentage}%` }}
        >
          {showLabel && (
            <span className="tf-progress-bar__label">{displayLabel}</span>
          )}
        </div>
      </div>
    </div>
  )
}
