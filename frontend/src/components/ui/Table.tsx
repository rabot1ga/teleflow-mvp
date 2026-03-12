import { cn } from '@/utils'

interface TableProps<T> {
  data: T[]
  columns: Column<T>[]
  onRowClick?: (item: T) => void
  className?: string
  emptyMessage?: string
}

interface Column<T> {
  key: keyof T | string
  title: string
  render?: (item: T) => React.ReactNode
  className?: string
}

export function Table<T>({
  data,
  columns,
  onRowClick,
  className,
  emptyMessage = 'No data available',
}: TableProps<T>) {
  const getValue = (item: T, key: string) => {
    const keys = key.split('.')
    let value: any = item
    for (const k of keys) {
      value = value?.[k as keyof typeof value]
    }
    return value
  }

  if (data.length === 0) {
    return (
      <div className={cn('text-center text-muted py-5', className)}>
        {emptyMessage}
      </div>
    )
  }

  return (
    <div className={cn('table-responsive', className)}>
      <table className="table table-hover">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={String(column.key)} className={column.className}>
                {column.title}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr
              key={index}
              onClick={() => onRowClick?.(item)}
              style={{ cursor: onRowClick ? 'pointer' : 'default' }}
            >
              {columns.map((column) => (
                <td key={String(column.key)} className={column.className}>
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
}

export function Pagination({
  currentPage,
  totalPages,
  onPageChange,
  totalItems,
  itemsPerPage = 20,
}: PaginationProps) {
  const pages = Array.from({ length: totalPages }, (_, i) => i + 1)
  const startItem = (currentPage - 1) * itemsPerPage + 1
  const endItem = Math.min(currentPage * itemsPerPage, totalItems || 0)

  return (
    <div className="d-flex justify-content-between align-items-center">
      {totalItems && (
        <small className="text-muted">
          Showing {startItem}-{endItem} of {totalItems} items
        </small>
      )}
      <div className="d-flex gap-1">
        <button
          className="btn btn-sm btn-outline-secondary"
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
        >
          Previous
        </button>
        {pages.map((page) => (
          <button
            key={page}
            className={cn(
              'btn btn-sm',
              page === currentPage ? 'btn-primary' : 'btn-outline-secondary'
            )}
            onClick={() => onPageChange(page)}
          >
            {page}
          </button>
        ))}
        <button
          className="btn btn-sm btn-outline-secondary"
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
        >
          Next
        </button>
      </div>
    </div>
  )
}
