import { cn } from '@/utils'
import './StatCard.css'

interface StatCardProps {
  title: string
  value: string | number
  icon?: string
  trend?: { value: number; isPositive: boolean }
  className?: string
}

export function StatCard({ title, value, icon, trend, className }: StatCardProps) {
  return (
    <div className={cn('tf-stat-card', className)}>
      <div className="tf-stat-card__header">
        <span className="tf-stat-card__title">{title}</span>
        {icon && <span className="tf-stat-card__icon">{icon}</span>}
      </div>
      <div className="tf-stat-card__value">{value}</div>
      {trend && (
        <div className="tf-stat-card__trend">
          <span className={cn('badge', trend.isPositive ? 'badge-success' : 'badge-danger')}>
            {trend.isPositive ? '↑' : '↓'} {trend.value}%
          </span>
          <small className="text-muted ms-2">from last month</small>
        </div>
      )}
    </div>
  )
}

interface StatusBadgeProps {
  status: 'active' | 'inactive' | 'pending' | 'success' | 'error' | 'running' | 'completed'
  className?: string
}

export function StatusBadge({ status, className }: StatusBadgeProps) {
  const statusMap: Record<string, { label: string; variant: string }> = {
    active: { label: 'Active', variant: 'success' },
    inactive: { label: 'Inactive', variant: 'secondary' },
    pending: { label: 'Pending', variant: 'warning' },
    success: { label: 'Success', variant: 'success' },
    error: { label: 'Error', variant: 'danger' },
    running: { label: 'Running', variant: 'primary' },
    completed: { label: 'Completed', variant: 'success' },
  }

  const config = statusMap[status] || statusMap.pending

  return (
    <span className={cn('badge', `badge-${config.variant}`, className)}>
      {config.label}
    </span>
  )
}
