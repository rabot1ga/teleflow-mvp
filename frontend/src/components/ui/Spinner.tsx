import React from 'react'
import { cn } from '@/utils/cn'
import './Spinner.css'

export type SpinnerSize = 'sm' | 'md' | 'lg'

export interface SpinnerProps {
  className?: string
  size?: SpinnerSize
  color?: string
}

export const Spinner: React.FC<SpinnerProps> = ({
  className,
  size = 'md',
  color,
}) => {
  const classes = cn(
    'tf-spinner',
    `tf-spinner--${size}`,
    className
  )

  return (
    <svg
      className={classes}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{ color }}
    >
      <circle
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="3"
        strokeOpacity="0.2"
      />
      <path
        d="M12 2C16.9706 2 21 6.02944 21 11"
        stroke="currentColor"
        strokeWidth="3"
        strokeLinecap="round"
      />
    </svg>
  )
}
