import { useState } from 'react'
import { cn } from '@/utils'
import { Button } from './Button'

interface SearchProps {
  value: string
  onChange: (value: string) => void
  onSearch?: (value: string) => void
  placeholder?: string
  className?: string
  debounceMs?: number
}

export function Search({
  value,
  onChange,
  onSearch,
  placeholder = 'Search...',
  className,
  debounceMs = 300,
}: SearchProps) {
  const [localValue, setLocalValue] = useState(value)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value
    setLocalValue(newValue)
    onChange(newValue)

    if (onSearch && debounceMs > 0) {
      const timeout = setTimeout(() => {
        onSearch(newValue)
      }, debounceMs)

      return () => clearTimeout(timeout)
    } else if (onSearch) {
      onSearch(newValue)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && onSearch) {
      onSearch(localValue)
    }
  }

  const handleClear = () => {
    setLocalValue('')
    onChange('')
    if (onSearch) {
      onSearch('')
    }
  }

  return (
    <div className={cn('input-group', className)}>
      <span className="input-group-text">🔍</span>
      <input
        type="text"
        className="form-control"
        placeholder={placeholder}
        value={localValue}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
      />
      {localValue && (
        <button
          className="btn btn-outline-secondary"
          type="button"
          onClick={handleClear}
        >
          ✕
        </button>
      )}
    </div>
  )
}

interface FilterProps {
  filters: {
    key: string
    label: string
    options: { value: string; label: string }[]
  }[]
  values: Record<string, string>
  onChange: (key: string, value: string) => void
  onApply?: (values: Record<string, string>) => void
  className?: string
}

export function Filter({
  filters,
  values,
  onChange,
  onApply,
  className,
}: FilterProps) {
  const handleApply = () => {
    if (onApply) {
      onApply(values)
    }
  }

  const handleReset = () => {
    filters.forEach((filter) => {
      onChange(filter.key, '')
    })
    if (onApply) {
      onApply({})
    }
  }

  return (
    <div className={cn('card mb-3', className)}>
      <div className="card-body">
        <div className="row g-3">
          {filters.map((filter) => (
            <div key={filter.key} className="col-md-3">
              <label className="form-label small">{filter.label}</label>
              <select
                className="form-select form-select-sm"
                value={values[filter.key] || ''}
                onChange={(e) => onChange(filter.key, e.target.value)}
              >
                <option value="">All</option>
                {filter.options.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>
          ))}
          <div className="col-md-3 d-flex align-items-end gap-2">
            <Button variant="primary" size="sm" onClick={handleApply}>
              Apply
            </Button>
            <Button variant="outline" size="sm" onClick={handleReset}>
              Reset
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
