import { cn } from '@/utils'
import type { HTMLAttributes } from 'react'
import './StatCard.css'

interface StatCardProps extends HTMLAttributes<HTMLDivElement> {
  title: string
  value: string | number
  icon?: string
  trend?: {
    value: number
    isPositive: boolean
    label?: string
  }
  description?: string
  color?: 'purple' | 'blue' | 'green' | 'orange' | 'red'
}

const colorVariants = {
  purple: {
    bg: 'var(--tf-primary-50)',
    border: 'var(--tf-primary-200)',
    text: 'var(--tf-primary-700)',
    gradient: 'linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%)',
  },
  blue: {
    bg: 'var(--tf-accent-50)',
    border: 'var(--tf-accent-200)',
    text: 'var(--tf-accent-700)',
    gradient: 'linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)',
  },
  green: {
    bg: 'var(--tf-success-50)',
    border: 'var(--tf-success-200)',
    text: 'var(--tf-success-700)',
    gradient: 'linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)',
  },
  orange: {
    bg: 'var(--tf-warning-50)',
    border: 'var(--tf-warning-200)',
    text: 'var(--tf-warning-700)',
    gradient: 'linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)',
  },
  red: {
    bg: 'var(--tf-danger-50)',
    border: 'var(--tf-danger-200)',
    text: 'var(--tf-danger-700)',
    gradient: 'linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%)',
  },
}

export function StatCard({
  title,
  value,
  icon,
  trend,
  description,
  color = 'purple',
  className,
  ...props
}: StatCardProps) {
  const colors = colorVariants[color]

  return (
    <div className={cn('tf-stat-card', className)} style={{ background: colors.gradient }} {...props}>
      <div className="tf-stat-card__header">
        <div className="tf-stat-card__title-wrapper">
          <span className="tf-stat-card__title">{title}</span>
          {icon && (
            <span className="tf-stat-card__icon" style={{ background: colors.bg, color: colors.text }}>
              {icon}
            </span>
          )}
        </div>
      </div>
      
      <div className="tf-stat-card__value" style={{ color: colors.text }}>
        {value}
      </div>
      
      {description && (
        <p className="tf-stat-card__description">{description}</p>
      )}
      
      {trend && (
        <div className="tf-stat-card__trend">
          <span
            className={cn(
              'tf-stat-card__trend-value',
              trend.isPositive ? 'tf-stat-card__trend--positive' : 'tf-stat-card__trend--negative'
            )}
          >
            {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}%
          </span>
          {trend.label && (
            <span className="tf-stat-card__trend-label">{trend.label}</span>
          )}
        </div>
      )}
    </div>
  )
}
