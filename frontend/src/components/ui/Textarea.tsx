import { cn } from '@/utils'
import type { TextareaHTMLAttributes } from 'react'

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  error?: string
}

export function Textarea({ error, className, ...props }: TextareaProps) {
  return (
    <div className="tf-textarea-wrapper">
      <textarea className={cn('tf-textarea', error && 'tf-textarea--error', className)} {...props} />
      {error && <span className="tf-textarea__error">{error}</span>}
    </div>
  )
}
