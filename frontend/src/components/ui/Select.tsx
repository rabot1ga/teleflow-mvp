import { cn } from '@/utils'
import type { SelectHTMLAttributes } from 'react'

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  options?: Array<{ value: string; label: string }>
  error?: string
}

export function Select({ options = [], error, className, ...props }: SelectProps) {
  return (
    <div className="tf-select-wrapper">
      <select className={cn('tf-select', error && 'tf-select--error', className)} {...props}>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && <span className="tf-select__error">{error}</span>}
    </div>
  )
}
