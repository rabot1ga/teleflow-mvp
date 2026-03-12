import React from 'react'
import { cn } from '@/utils/cn'
import './Badge.css'

export type BadgeVariant = 'neutral' | 'primary' | 'success' | 'warning' | 'danger' | 'info'
export type BadgeSize = 'sm' | 'md'

export interface BadgeProps {
  className?: string
  variant?: BadgeVariant
  size?: BadgeSize
  children: React.ReactNode
}

export const Badge: React.FC<BadgeProps> = ({
  className,
  variant = 'neutral',
  size = 'md',
  children,
}) => {
  const classes = cn(
    'tf-badge',
    `tf-badge--${variant}`,
    `tf-badge--${size}`,
    className
  )

  return <span className={classes}>{children}</span>
}
