import { cn } from '@/utils'
import type { HTMLAttributes } from 'react'
import './PageHeader.css'

interface PageHeaderProps extends HTMLAttributes<HTMLDivElement> {
  title: string | React.ReactNode
  description?: string | React.ReactNode
  action?: React.ReactNode
}

export function PageHeader({
  title,
  description,
  action,
  className,
  ...props
}: PageHeaderProps) {
  return (
    <div className={cn('tf-page-header', className)} {...props}>
      <div className="tf-page-header__content">
        {typeof title === 'string' ? (
          <h1 className="tf-page-header__title">{title}</h1>
        ) : (
          title
        )}
        {typeof description === 'string' ? (
          <p className="tf-page-header__description">{description}</p>
        ) : (
          description
        )}
      </div>
      {action && <div className="tf-page-header__action">{action}</div>}
    </div>
  )
}
