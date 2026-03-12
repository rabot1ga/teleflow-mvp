import { useEffect } from 'react'

interface SkeletonProps {
  width?: string | number
  height?: string | number
  borderRadius?: string | number
  className?: string
}

export function Skeleton({
  width = '100%',
  height = '1rem',
  borderRadius = '0.25rem',
  className,
}: SkeletonProps) {
  return (
    <div
      className={cn('skeleton', className)}
      style={{
        width: typeof width === 'number' ? `${width}px` : width,
        height: typeof height === 'number' ? `${height}px` : height,
        borderRadius: typeof borderRadius === 'number' ? `${borderRadius}px` : borderRadius,
      }}
    />
  )
}

import { cn } from '@/utils'

interface SkeletonListProps {
  count?: number
  height?: string
  className?: string
}

export function SkeletonList({ count = 5, height = '3rem', className }: SkeletonListProps) {
  return (
    <div className={className}>
      {Array.from({ length: count }).map((_, i) => (
        <Skeleton key={i} height={height} className="mb-2" />
      ))}
    </div>
  )
}

interface SkeletonTableProps {
  rows?: number
  columns?: number
  className?: string
}

export function SkeletonTable({ rows = 5, columns = 4, className }: SkeletonTableProps) {
  return (
    <div className={className}>
      {/* Header */}
      <div className="row mb-2">
        {Array.from({ length: columns }).map((_, i) => (
          <div key={i} className="col">
            <Skeleton height="1.5rem" />
          </div>
        ))}
      </div>
      
      {/* Rows */}
      {Array.from({ length: rows }).map((_, rowIndex) => (
        <div key={rowIndex} className="row mb-2">
          {Array.from({ length: columns }).map((_, colIndex) => (
            <div key={colIndex} className="col">
              <Skeleton height="2rem" />
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}

interface LoadingOverlayProps {
  isLoading: boolean
  children: React.ReactNode
  message?: string
}

export function LoadingOverlay({ isLoading, children, message = 'Loading...' }: LoadingOverlayProps) {
  useEffect(() => {
    if (isLoading) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    
    return () => {
      document.body.style.overflow = ''
    }
  }, [isLoading])

  if (!isLoading) return <>{children}</>

  return (
    <div style={{ position: 'relative', minHeight: '200px' }}>
      {children}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(255, 255, 255, 0.8)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 9999,
        }}
      >
        <div className="spinner-border text-primary" role="status" style={{ width: '3rem', height: '3rem' }}>
          <span className="visually-hidden">Loading...</span>
        </div>
        {message && <p className="mt-3 text-muted">{message}</p>}
      </div>
    </div>
  )
}
