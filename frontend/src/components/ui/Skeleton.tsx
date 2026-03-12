import React from 'react'
import { cn } from '@/utils/cn'
import './Skeleton.css'

export interface SkeletonProps {
  className?: string
  width?: number | string
  height?: number | string
  radius?: number | string
  circle?: boolean
  variant?: 'text' | 'circular' | 'rectangular' | 'rounded'
}

export const Skeleton: React.FC<SkeletonProps> = ({
  className,
  width,
  height,
  radius,
  circle = false,
  variant = 'text',
}) => {
  const classes = cn(
    'tf-skeleton',
    {
      'tf-skeleton--circle': circle,
      'tf-skeleton--text': variant === 'text',
      'tf-skeleton--circular': variant === 'circular',
      'tf-skeleton--rectangular': variant === 'rectangular',
      'tf-skeleton--rounded': variant === 'rounded',
    },
    className
  )

  const style: React.CSSProperties = {
    width,
    height,
    borderRadius: radius,
  }

  return <span className={classes} style={style} />
}
