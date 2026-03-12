import { Button } from './Button'
import { cn } from '@/utils'

interface EmptyStateProps {
  icon?: string
  title: string
  description?: string
  action?: {
    label: string
    onClick: () => void
    variant?: 'primary' | 'secondary' | 'success' | 'danger'
  }
  className?: string
}

export function EmptyState({
  icon = '📭',
  title,
  description,
  action,
  className,
}: EmptyStateProps) {
  return (
    <div className={cn('text-center py-5', className)}>
      <div className="mb-3">
        <span className="display-1">{icon}</span>
      </div>
      <h3 className="h4 mb-2">{title}</h3>
      {description && (
        <p className="text-muted mb-4">{description}</p>
      )}
      {action && (
        <Button variant={action.variant} onClick={action.onClick}>
          {action.label}
        </Button>
      )}
    </div>
  )
}

interface ErrorStateProps {
  title: string
  description?: string
  onRetry?: () => void
  className?: string
}

export function ErrorState({
  title = 'Something went wrong',
  description,
  onRetry,
  className,
}: ErrorStateProps) {
  return (
    <div className={cn('text-center py-5', className)}>
      <div className="mb-3">
        <span className="display-1">❌</span>
      </div>
      <h3 className="h4 mb-2 text-danger">{title}</h3>
      {description && (
        <p className="text-muted mb-4">{description}</p>
      )}
      {onRetry && (
        <Button variant="primary" onClick={onRetry}>
          🔄 Try Again
        </Button>
      )}
    </div>
  )
}
