import React from 'react'
import { cn } from '@/utils/cn'
import './Card.css'

export interface CardProps {
  className?: string
  children?: React.ReactNode
  title?: string
  subtitle?: string
  action?: React.ReactNode
  footer?: React.ReactNode
  noPadding?: boolean
  hoverable?: boolean
}

export const Card: React.FC<CardProps> = ({
  className,
  children,
  title,
  subtitle,
  action,
  footer,
  noPadding = false,
  hoverable = false,
}) => {
  const classes = cn(
    'tf-card',
    {
      'tf-card--no-padding': noPadding,
      'tf-card--hoverable': hoverable,
    },
    className
  )

  return (
    <div className={classes}>
      {(title || subtitle || action) && (
        <div className="tf-card__header">
          <div className="tf-card__header-content">
            {title && <h3 className="tf-card__title">{title}</h3>}
            {subtitle && <p className="tf-card__subtitle">{subtitle}</p>}
          </div>
          {action && <div className="tf-card__action">{action}</div>}
        </div>
      )}
      <div className="tf-card__content">{children}</div>
      {footer && <div className="tf-card__footer">{footer}</div>}
    </div>
  )
}
