import { ReactNode } from 'react'
import { cn } from '@/utils'
import './Tabs.css'

interface Tab {
  id: string
  label: string
  icon?: ReactNode
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
  size?: 'sm' | 'md' | 'lg'
}

export function Tabs({
  tabs,
  activeTab,
  onChange,
  children,
  className,
  variant = 'default',
  size = 'md',
}: TabsProps) {
  const selectedTab = activeTab || tabs[0]?.id

  return (
    <div className={cn('tf-tabs', className)}>
      <div className={cn('tf-tabs-list', `tf-tabs-list--${size}`, `tf-tabs-list--${variant}`)}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={cn(
              'tf-tabs-item',
              selectedTab === tab.id && 'tf-tabs-item--active',
              tab.disabled && 'tf-tabs-item--disabled'
            )}
            onClick={() => !tab.disabled && onChange(tab.id)}
            disabled={tab.disabled}
            role="tab"
            aria-selected={selectedTab === tab.id}
          >
            {tab.icon && <span className="tf-tabs-item-icon">{tab.icon}</span>}
            <span className="tf-tabs-item-label">{tab.label}</span>
            {tab.badge !== undefined && (
              <span className={cn('tf-tabs-item-badge', selectedTab === tab.id ? 'tf-tabs-item-badge--active' : '')}>
                {tab.badge}
              </span>
            )}
          </button>
        ))}
      </div>
      {children && <div className="tf-tabs-content">{children}</div>}
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

  return <div className={cn('tf-tab-content', className)}>{children}</div>
}
