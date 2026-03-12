import { useState, useRef } from 'react'
import { cn } from '@/utils'
import { Button } from './Button'

interface FileUploadProps {
  accept?: string
  multiple?: boolean
  maxSize?: number // in MB
  onFileSelect: (files: File[]) => void
  className?: string
  label?: string
  hint?: string
}

export function FileUpload({
  accept,
  multiple = false,
  maxSize,
  onFileSelect,
  className,
  label = 'Upload files',
  hint,
}: FileUploadProps) {
  const [dragOver, setDragOver] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const validateFile = (file: File): boolean => {
    if (maxSize && file.size > maxSize * 1024 * 1024) {
      setError(`File ${file.name} is larger than ${maxSize}MB`)
      return false
    }
    setError(null)
    return true
  }

  const handleFiles = (files: FileList | null) => {
    if (!files) return
    
    const fileArray = Array.from(files)
    const validFiles = fileArray.filter(validateFile)
    
    if (validFiles.length > 0) {
      onFileSelect(validFiles)
    }
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setDragOver(false)
    handleFiles(e.dataTransfer.files)
  }

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setDragOver(true)
  }

  const handleDragLeave = () => {
    setDragOver(false)
  }

  return (
    <div className={cn('file-upload', className)}>
      {label && <label className="form-label">{label}</label>}
      
      <div
        className={cn(
          'border-2 border-dashed rounded p-4 text-center',
          dragOver ? 'border-primary bg-light' : 'border-secondary',
          error && 'border-danger'
        )}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => fileInputRef.current?.click()}
        style={{ cursor: 'pointer', minHeight: '150px' }}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept={accept}
          multiple={multiple}
          onChange={(e) => handleFiles(e.target.files)}
          style={{ display: 'none' }}
        />
        
        <div className="text-muted">
          <span className="fs-1">📁</span>
          <p className="mt-2 mb-0">
            Drag & drop files here or <strong>click to browse</strong>
          </p>
          {hint && <small className="text-muted">{hint}</small>}
        </div>
      </div>
      
      {error && (
        <div className="invalid-feedback d-block mt-2">
          {error}
        </div>
      )}
    </div>
  )
}

interface FileListProps {
  files: File[]
  onRemove: (index: number) => void
}

export function FileList({ files, onRemove }: FileListProps) {
  if (files.length === 0) return null

  return (
    <ul className="list-group mt-2">
      {files.map((file, index) => (
        <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
          <div>
            <span className="me-2">📄</span>
            <strong>{file.name}</strong>
            <small className="text-muted ms-2">
              ({(file.size / 1024).toFixed(1)} KB)
            </small>
          </div>
          <Button
            size="sm"
            variant="danger"
            onClick={(e) => {
              e.stopPropagation()
              onRemove(index)
            }}
          >
            ✕
          </Button>
        </li>
      ))}
    </ul>
  )
}
