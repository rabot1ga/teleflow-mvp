import { cn } from '@/utils'

interface CardProps {
  className?: string
  title?: string
  subtitle?: string
  action?: React.ReactNode
  children: React.ReactNode
  footer?: React.ReactNode
  noPadding?: boolean
}

export function Card({
  className,
  title,
  subtitle,
  action,
  children,
  footer,
  noPadding = false,
}: CardProps) {
  return (
    <div className={cn('tf-card', className)}>
      {(title || subtitle || action) && (
        <div className="tf-card__header">
          <div className="tf-card__header-content">
            {title && <h3 className="tf-card__title">{title}</h3>}
            {subtitle && <p className="tf-card__subtitle">{subtitle}</p>}
          </div>
          {action && <div className="tf-card__action">{action}</div>}
        </div>
      )}
      <div className={cn('tf-card__body', noPadding && 'tf-card__body--no-padding')}>
        {children}
      </div>
      {footer && <div className="tf-card__footer">{footer}</div>}
    </div>
  )
}
