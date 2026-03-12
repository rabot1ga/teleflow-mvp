import { cn } from '@/utils'

interface SimpleChartProps {
  data?: any[]
  title?: string
  height?: number
  className?: string
}

export function SimpleAreaChart({ data, title, height = 200, className }: SimpleChartProps) {
  return (
    <div className={cn('tf-chart', className)} style={{ height }}>
      {title && <h4 className="tf-chart__title">{title}</h4>}
      <div className="tf-chart__placeholder">
        <div className="tf-chart__icon">📈</div>
        <p className="tf-chart__text">Area Chart</p>
        <small className="text-muted">Data visualization coming soon</small>
      </div>
    </div>
  )
}

export function SimpleBarChart({ data, title, height = 200, className }: SimpleChartProps) {
  return (
    <div className={cn('tf-chart', className)} style={{ height }}>
      {title && <h4 className="tf-chart__title">{title}</h4>}
      <div className="tf-chart__placeholder">
        <div className="tf-chart__icon">📊</div>
        <p className="tf-chart__text">Bar Chart</p>
        <small className="text-muted">Data visualization coming soon</small>
      </div>
    </div>
  )
}

export function SimplePieChart({ data, title, height = 200, className }: SimpleChartProps) {
  return (
    <div className={cn('tf-chart', className)} style={{ height }}>
      {title && <h4 className="tf-chart__title">{title}</h4>}
      <div className="tf-chart__placeholder">
        <div className="tf-chart__icon">🥧</div>
        <p className="tf-chart__text">Pie Chart</p>
        <small className="text-muted">Data visualization coming soon</small>
      </div>
    </div>
  )
}

export function SimpleLineChart({ data, title, height = 200, className }: SimpleChartProps) {
  return (
    <div className={cn('tf-chart', className)} style={{ height }}>
      {title && <h4 className="tf-chart__title">{title}</h4>}
      <div className="tf-chart__placeholder">
        <div className="tf-chart__icon">📉</div>
        <p className="tf-chart__text">Line Chart</p>
        <small className="text-muted">Data visualization coming soon</small>
      </div>
    </div>
  )
}
