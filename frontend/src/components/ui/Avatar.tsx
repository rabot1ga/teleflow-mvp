import React, { useState } from 'react'
import { cn } from '@/utils'
import { getInitials } from '@/utils/getInitials'
import './Avatar.css'

export interface AvatarProps {
  src?: string
  alt?: string
  name?: string
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'circle' | 'rounded' | 'square'
  showStatus?: boolean
  status?: 'online' | 'offline' | 'busy' | 'away'
  className?: string
}

export const Avatar: React.FC<AvatarProps> = ({
  src,
  alt,
  name,
  size = 'md',
  variant = 'circle',
  showStatus = false,
  status = 'offline',
  className,
}) => {
  const [imageError, setImageError] = useState(false)
  const hasImage = src && !imageError
  const initials = name ? getInitials(name) : '?'

  const statusColors = {
    online: 'tf-avatar__status--online',
    offline: 'tf-avatar__status--offline',
    busy: 'tf-avatar__status--busy',
    away: 'tf-avatar__status--away',
  }

  return (
    <div
      className={cn(
        'tf-avatar',
        `tf-avatar--${size}`,
        `tf-avatar--${variant}`,
        { 'tf-avatar--with-status': showStatus },
        className
      )}
    >
      {hasImage ? (
        <img
          src={src}
          alt={alt || name || 'Avatar'}
          className="tf-avatar__image"
          onError={() => setImageError(true)}
        />
      ) : (
        <div className="tf-avatar__fallback">
          <span className="tf-avatar__initials">{initials}</span>
        </div>
      )}
      {showStatus && (
        <span className={cn('tf-avatar__status', statusColors[status])} />
      )}
    </div>
  )
}
