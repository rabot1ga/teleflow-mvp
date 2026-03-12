import React from 'react'
import { cn } from '@/utils'
import './Table.css'

interface TableProps<T> {
  data: T[]
  columns: Column<T>[]
  onRowClick?: (item: T) => void
  className?: string
  emptyMessage?: string
  isLoading?: boolean
  size?: 'sm' | 'md' | 'lg'
}

interface Column<T> {
  key: keyof T | string
  title: string
  render?: (item: T) => React.ReactNode
  className?: string
  width?: number | string
  align?: 'left' | 'center' | 'right'
}

export function Table<T>({
  data,
  columns,
  onRowClick,
  className,
  emptyMessage = 'No data available',
  isLoading = false,
  size = 'md',
}: TableProps<T>) {
  const safeData = Array.isArray(data) ? data : []
  const getValue = (item: T, key: string) => {
    const keys = key.split('.')
    let value: any = item
    for (const k of keys) {
      value = value?.[k as keyof typeof value]
    }
    return value
  }

  if (isLoading) {
    return (
      <div className={cn('tf-table-wrapper', className)}>
        <div className="tf-table-loading">
          <div className="tf-table-loading-spinner" />
          <span className="tf-table-loading-text">Loading...</span>
        </div>
      </div>
    )
  }

  if (safeData.length === 0) {
    return (
      <div className={cn('tf-table-wrapper', className)}>
        <div className="tf-table-empty">
          <div className="tf-table-empty-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <line x1="3" y1="9" x2="21" y2="9" />
              <line x1="9" y1="21" x2="9" y2="9" />
            </svg>
          </div>
          <p className="tf-table-empty-text">{emptyMessage}</p>
        </div>
      </div>
    )
  }

  return (
    <div className={cn('tf-table-wrapper', className)}>
      <table className={cn('tf-table', `tf-table--${size}`)}>
        <thead>
          <tr>
            {columns.map((column) => (
              <th
                key={String(column.key)}
                className={cn(
                  column.className,
                  column.align && `tf-table-cell--${column.align}`
                )}
                style={{ width: column.width }}
              >
                {column.title}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr
              key={index}
              className={cn(onRowClick && 'tf-table-row--clickable')}
              onClick={() => onRowClick?.(item)}
            >
              {columns.map((column) => (
                <td
                  key={String(column.key)}
                  className={cn(
                    column.className,
                    column.align && `tf-table-cell--${column.align}`
                  )}
                >
                  {column.render
                    ? column.render(item)
                    : String(getValue(item, String(column.key)))}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

interface PaginationProps {
  currentPage: number
  totalPages: number
  onPageChange: (page: number) => void
  totalItems?: number
  itemsPerPage?: number
  size?: 'sm' | 'md'
}

export function Pagination({
  currentPage,
  totalPages,
  onPageChange,
  totalItems,
  itemsPerPage = 20,
  size = 'md',
}: PaginationProps) {
  const getPageNumbers = () => {
    const pages: (number | string)[] = []
    const maxVisible = 5
    let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2))
    let endPage = Math.min(totalPages, startPage + maxVisible - 1)

    if (endPage - startPage < maxVisible - 1) {
      startPage = Math.max(1, endPage - maxVisible + 1)
    }

    if (startPage > 1) {
      pages.push(1)
      if (startPage > 2) {
        pages.push('...')
      }
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i)
    }

    if (endPage < totalPages) {
      if (endPage < totalPages - 1) {
        pages.push('...')
      }
      pages.push(totalPages)
    }

    return pages
  }

  const startItem = (currentPage - 1) * itemsPerPage + 1
  const endItem = Math.min(currentPage * itemsPerPage, totalItems || 0)

  return (
    <div className={cn('tf-pagination', `tf-pagination--${size}`)}>
      <div className="tf-pagination-info">
        {totalItems ? (
          <span>Showing {startItem}-{endItem} of {totalItems} items</span>
        ) : (
          <span>Page {currentPage} of {totalPages}</span>
        )}
      </div>
      <div className="tf-pagination-controls">
        <button
          className="tf-pagination-button"
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          aria-label="Previous page"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="15,18 9,12 15,6" />
          </svg>
        </button>
        {getPageNumbers().map((page, index) => (
          page === '...' ? (
            <span key={`ellipsis-${index}`} className="tf-pagination-ellipsis">…</span>
          ) : (
            <button
              key={page}
              className={cn(
                'tf-pagination-button',
                page === currentPage && 'tf-pagination-button--active'
              )}
              onClick={() => onPageChange(page as number)}
              aria-label={`Page ${page}`}
              aria-current={page === currentPage ? 'page' : undefined}
            >
              {page}
            </button>
          )
        ))}
        <button
          className="tf-pagination-button"
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          aria-label="Next page"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="9,18 15,12 9,6" />
          </svg>
        </button>
      </div>
    </div>
  )
}
