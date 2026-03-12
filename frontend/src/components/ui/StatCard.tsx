import { cn } from '@/utils'
import type { HTMLAttributes } from 'react'
import './StatCard.css'

interface StatCardProps extends HTMLAttributes<HTMLDivElement> {
  title: string
  value: string | number
  icon?: string | React.ReactNode
  trend?: {
    value: number
    isPositive: boolean
    label?: string
  }
  description?: string
}

export function StatCard({
  title,
  value,
  icon,
  trend,
  description,
  className,
  ...props
}: StatCardProps) {
  return (
    <div className={cn('tf-stat-card', className)} {...props}>
      <div className="tf-stat-card__header">
        <span className="tf-stat-card__title">{title}</span>
        {icon && (
          <span className="tf-stat-card__icon">
            {typeof icon === 'string' ? icon : icon}
          </span>
        )}
      </div>
      <div className="tf-stat-card__value">{value}</div>
      {description && <p className="tf-stat-card__description">{description}</p>}
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
          {trend.label && <span className="tf-stat-card__trend-label">{trend.label}</span>}
        </div>
      )}
    </div>
  )
}
