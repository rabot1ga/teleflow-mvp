import { cn } from '@/utils'

interface BadgeProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' | 'light' | 'dark'
  className?: string
}

export function Badge({ children, variant = 'secondary', className }: BadgeProps) {
  return (
    <span className={cn('badge', `bg-${variant}`, className)}>
      {children}
    </span>
  )
}

interface StatusBadgeProps {
  status: 'pending' | 'active' | 'completed' | 'failed' | 'cancelled' | 'running'
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const variants = {
    pending: 'secondary' as const,
    active: 'success' as const,
    completed: 'success' as const,
    failed: 'danger' as const,
    cancelled: 'secondary' as const,
    running: 'primary' as const,
  }

  const icons = {
    pending: '⏳',
    active: '✅',
    completed: '✅',
    failed: '❌',
    cancelled: '🚫',
    running: '🔄',
  }

  return (
    <Badge variant={variants[status]}>
      <span className="me-1">{icons[status]}</span>
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </Badge>
  )
}
