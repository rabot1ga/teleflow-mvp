import { cn } from '@/utils'

interface CardProps {
  children: React.ReactNode
  className?: string
  title?: string
  action?: React.ReactNode
}

export function Card({ children, className, title, action }: CardProps) {
  return (
    <div className={cn('card', className)}>
      {(title || action) && (
        <div className="card-header d-flex justify-content-between align-items-center">
          {title && <h5 className="mb-0">{title}</h5>}
          {action && <div>{action}</div>}
        </div>
      )}
      <div className="card-body">{children}</div>
    </div>
  )
}

interface StatCardProps {
  title: string
  value: string | number
  icon?: string
  trend?: {
    value: number
    isPositive: boolean
  }
  className?: string
}

export function StatCard({ title, value, icon, trend, className }: StatCardProps) {
  return (
    <div className={cn('card h-100', className)}>
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-center">
          <div>
            <p className="text-muted mb-1">{title}</p>
            <h3 className="mb-0">{value}</h3>
          </div>
          {icon && <span className="fs-1">{icon}</span>}
        </div>
        {trend && (
          <div className={cn('mt-3', trend.isPositive ? 'text-success' : 'text-danger')}>
            <small>
              {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}% from last week
            </small>
          </div>
        )}
      </div>
    </div>
  )
}
