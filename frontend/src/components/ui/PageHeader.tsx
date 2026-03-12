import { cn } from '@/utils'
import './PageHeader.css'

interface PageHeaderProps {
  title: string
  description?: string
  action?: React.ReactNode
  className?: string
}

export function PageHeader({ title, description, action, className }: PageHeaderProps) {
  return (
    <div className={cn('tf-page-header', className)}>
      <div className="tf-page-header__content">
        <h1 className="tf-page-header__title">{title}</h1>
        {description && <p className="tf-page-header__description">{description}</p>}
      </div>
      {action && <div className="tf-page-header__action">{action}</div>}
    </div>
  )
}
