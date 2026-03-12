import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'
import { Skeleton } from './Skeleton'

interface AreaChartProps {
  data: Array<Record<string, any>>
  xKey: string
  yKeys: Array<{ key: string; color: string; name?: string }>
  height?: number
  title?: string
  showGrid?: boolean
  className?: string
}

export function SimpleAreaChart({
  data,
  xKey,
  yKeys,
  height = 300,
  title,
  showGrid = true,
  className,
}: AreaChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className={className}>
        {title && <h5 className="mb-3">{title}</h5>}
        <Skeleton height={height} />
      </div>
    )
  }

  return (
    <div className={className}>
      {title && <h5 className="mb-3">{title}</h5>}
      <ResponsiveContainer width="100%" height={height}>
        <AreaChart data={data}>
          {showGrid && <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />}
          <XAxis dataKey={xKey} stroke="#666" />
          <YAxis stroke="#666" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e0e0e0',
              borderRadius: '8px',
            }}
          />
          <Legend />
          {yKeys.map(({ key, color, name }) => (
            <Area
              key={key}
              type="monotone"
              dataKey={key}
              stroke={color}
              fill={color}
              fillOpacity={0.3}
              name={name || key}
            />
          ))}
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}

import {
  BarChart,
  Bar,
  Cell,
} from 'recharts'

interface BarChartProps {
  data: Array<Record<string, any>>
  xKey: string
  yKey: string
  height?: number
  title?: string
  color?: string
  className?: string
}

export function SimpleBarChart({
  data,
  xKey,
  yKey,
  height = 300,
  title,
  color = '#0d6efd',
  className,
}: BarChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className={className}>
        {title && <h5 className="mb-3">{title}</h5>}
        <Skeleton height={height} />
      </div>
    )
  }

  return (
    <div className={className}>
      {title && <h5 className="mb-3">{title}</h5>}
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis dataKey={xKey} stroke="#666" />
          <YAxis stroke="#666" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e0e0e0',
              borderRadius: '8px',
            }}
          />
          <Bar dataKey={yKey} fill={color} radius={[4, 4, 0, 0]}>
            {data.map((_entry, index) => (
              <Cell key={`cell-${index}`} fill={color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

import {
  PieChart,
  Pie,
  Cell as RechartsCell,
} from 'recharts'

interface PieChartProps {
  data: Array<{ name: string; value: number; color?: string }>
  height?: number
  title?: string
  showLegend?: boolean
  className?: string
}

const COLORS = [
  '#0d6efd',
  '#198754',
  '#ffc107',
  '#dc3545',
  '#0dcaf0',
  '#6f42c1',
  '#fd7e14',
  '#20c997',
]

export function SimplePieChart({
  data,
  height = 300,
  title,
  showLegend = true,
  className,
}: PieChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className={className}>
        {title && <h5 className="mb-3">{title}</h5>}
        <Skeleton height={height} />
      </div>
    )
  }

  const total = data.reduce((sum, item) => sum + item.value, 0)

  return (
    <div className={className}>
      {title && <h5 className="mb-3">{title}</h5>}
      <ResponsiveContainer width="100%" height={height}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, value }) => `${name}: ${value} (${((value / total) * 100).toFixed(1)}%)`}
            outerRadius={height / 2 - 40}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <RechartsCell
                key={`cell-${index}`}
                fill={entry.color || COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e0e0e0',
              borderRadius: '8px',
            }}
          />
          {showLegend && <Legend />}
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}

import {
  LineChart,
  Line,
} from 'recharts'

interface LineChartProps {
  data: Array<Record<string, any>>
  xKey: string
  yKeys: Array<{ key: string; color: string; name?: string }>
  height?: number
  title?: string
  className?: string
}

export function SimpleLineChart({
  data,
  xKey,
  yKeys,
  height = 300,
  title,
  className,
}: LineChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className={className}>
        {title && <h5 className="mb-3">{title}</h5>}
        <Skeleton height={height} />
      </div>
    )
  }

  return (
    <div className={className}>
      {title && <h5 className="mb-3">{title}</h5>}
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis dataKey={xKey} stroke="#666" />
          <YAxis stroke="#666" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e0e0e0',
              borderRadius: '8px',
            }}
          />
          <Legend />
          {yKeys.map(({ key, color, name }) => (
            <Line
              key={key}
              type="monotone"
              dataKey={key}
              stroke={color}
              strokeWidth={2}
              dot={{ r: 4 }}
              activeDot={{ r: 6 }}
              name={name || key}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
