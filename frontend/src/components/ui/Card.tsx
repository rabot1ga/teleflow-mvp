import { cn } from '@/utils'
import type { HTMLAttributes } from 'react'
import './Card.css'

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  title?: string | React.ReactNode
  subtitle?: string | React.ReactNode
  action?: React.ReactNode
  footer?: React.ReactNode
  noPadding?: boolean
  hoverable?: boolean
}

export function Card({
  className,
  title,
  subtitle,
  action,
  children,
  footer,
  noPadding = false,
  hoverable = false,
  ...props
}: CardProps) {
  return (
    <div
      className={cn(
        'tf-card',
        hoverable && 'tf-card--hoverable',
        className
      )}
      {...props}
    >
      {(title || subtitle || action) && (
        <div className="tf-card__header">
          <div className="tf-card__header-content">
            {typeof title === 'string' ? (
              <h3 className="tf-card__title">{title}</h3>
            ) : (
              title
            )}
            {typeof subtitle === 'string' ? (
              <p className="tf-card__subtitle">{subtitle}</p>
            ) : (
              subtitle
            )}
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
