import React from 'react'
import { cn } from '@/utils/cn'
import './EmptyState.css'

export interface EmptyStateProps {
  className?: string
  title: string
  description?: string
  icon?: React.ReactNode
  action?: React.ReactNode
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  className,
  title,
  description,
  icon,
  action,
}) => {
  const classes = cn('tf-empty-state', className)

  return (
    <div className={classes}>
      {icon && <div className="tf-empty-state__icon">{icon}</div>}
      <div className="tf-empty-state__content">
        <h3 className="tf-empty-state__title">{title}</h3>
        {description && <p className="tf-empty-state__description">{description}</p>}
        {action && <div className="tf-empty-state__action">{action}</div>}
      </div>
    </div>
  )
}
