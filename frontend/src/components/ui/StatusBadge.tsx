import { cn } from '@/utils'
import './Badge.css'

export type StatusBadgeStatus = 'active' | 'pending' | 'success' | 'warning' | 'danger' | 'neutral'

export interface StatusBadgeProps {
  status: StatusBadgeStatus
  className?: string
  children?: React.ReactNode
}

const statusMap: Record<StatusBadgeStatus, { label: string; variant: string }> = {
  active: { label: 'Active', variant: 'success' },
  pending: { label: 'Pending', variant: 'warning' },
  success: { label: 'Success', variant: 'success' },
  warning: { label: 'Warning', variant: 'warning' },
  danger: { label: 'Failed', variant: 'danger' },
  neutral: { label: 'Neutral', variant: 'neutral' },
}

export function StatusBadge({ status, className, children }: StatusBadgeProps) {
  const config = statusMap[status] || statusMap.neutral
  const variant = config.variant as 'success' | 'warning' | 'danger' | 'neutral' | 'primary' | 'info'

  return (
    <span className={cn('tf-badge', `tf-badge--${variant}`, className)}>
      {children || config.label}
    </span>
  )
}
