import { ReactNode } from 'react'
import { cn } from '@/utils'

interface Tab {
  id: string
  label: string
  icon?: string
  badge?: number
  disabled?: boolean
}

interface TabsProps {
  tabs: Tab[]
  activeTab?: string
  onChange: (tabId: string) => void
  children?: ReactNode
  className?: string
  variant?: 'default' | 'pills' | 'underline'
}

export function Tabs({
  tabs,
  activeTab,
  onChange,
  children,
  className,
  variant = 'default',
}: TabsProps) {
  const selectedTab = activeTab || tabs[0]?.id

  const variantClasses = {
    default: 'nav-tabs',
    pills: 'nav-pills',
    underline: 'nav-underline',
  }

  return (
    <div className={className}>
      <ul className={cn('nav', variantClasses[variant], 'mb-3')}>
        {tabs.map((tab) => (
          <li key={tab.id} className="nav-item">
            <button
              className={cn(
                'nav-link',
                selectedTab === tab.id && 'active',
                tab.disabled && 'disabled'
              )}
              onClick={() => !tab.disabled && onChange(tab.id)}
              disabled={tab.disabled}
            >
              {tab.icon && <span className="me-2">{tab.icon}</span>}
              {tab.label}
              {tab.badge !== undefined && (
                <span className={cn(
                  'badge ms-2',
                  selectedTab === tab.id ? 'bg-light text-dark' : 'bg-secondary'
                )}>
                  {tab.badge}
                </span>
              )}
            </button>
          </li>
        ))}
      </ul>
      {children}
    </div>
  )
}

interface TabContentProps {
  tabId: string
  activeTab: string
  children: ReactNode
  className?: string
}

export function TabContent({ tabId, activeTab, children, className }: TabContentProps) {
  if (tabId !== activeTab) return null
  
  return <div className={className}>{children}</div>
}
