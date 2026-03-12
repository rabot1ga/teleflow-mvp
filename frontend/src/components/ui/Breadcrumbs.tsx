import { Link, useLocation } from 'react-router-dom'
import { cn } from '@/utils'

interface BreadcrumbItem {
  label: string
  path?: string
}

interface BreadcrumbsProps {
  items?: BreadcrumbItem[]
  className?: string
}

export function Breadcrumbs({ items, className }: BreadcrumbsProps) {
  const location = useLocation()

  const getDefaultItems = (): BreadcrumbItem[] => {
    const pathnames = location.pathname.split('/').filter(Boolean)
    const items: BreadcrumbItem[] = [{ label: 'Home', path: '/dashboard' }]

    let currentPath = ''
    pathnames.forEach((part) => {
      currentPath += `/${part}`
      items.push({
        label: part.charAt(0).toUpperCase() + part.slice(1),
        path: currentPath,
      })
    })

    return items
  }

  const breadcrumbItems = items || getDefaultItems()

  return (
    <nav aria-label="breadcrumb" className={cn('mb-4', className)}>
      <ol className="breadcrumb">
        {breadcrumbItems.map((item, index) => (
          <li
            key={item.path || index}
            className={cn('breadcrumb-item', index === breadcrumbItems.length - 1 && 'active')}
          >
            {item.path && index !== breadcrumbItems.length - 1 ? (
              <Link to={item.path} className="text-decoration-none">
                {item.label}
              </Link>
            ) : (
              <span>{item.label}</span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  )
}

interface PageHeaderProps {
  title: string
  description?: string
  action?: React.ReactNode
  className?: string
}

export function PageHeader({ title, description, action, className }: PageHeaderProps) {
  return (
    <div className={cn('d-flex justify-content-between align-items-center mb-4', className)}>
      <div>
        <h1 className="h2 mb-1">{title}</h1>
        {description && <p className="text-muted mb-0">{description}</p>}
      </div>
      {action && <div>{action}</div>}
    </div>
  )
}
