import { Toaster } from 'react-hot-toast'
import { ReactNode } from 'react'

interface ToastProviderProps {
  children: ReactNode
}

export function ToastProvider({ children }: ToastProviderProps) {
  return (
    <>
      {children}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: 'var(--tf-bg-surface)',
            color: 'var(--tf-text-primary)',
            borderRadius: 'var(--tf-radius-lg)',
            boxShadow: 'var(--tf-shadow-lg)',
            border: '1px solid var(--tf-border-primary)',
          },
          success: {
            iconTheme: {
              primary: 'var(--tf-success-600)',
              secondary: 'white',
            },
            style: {
              border: '1px solid var(--tf-border-success)',
            },
          },
          error: {
            iconTheme: {
              primary: 'var(--tf-danger-600)',
              secondary: 'white',
            },
            style: {
              border: '1px solid var(--tf-border-error)',
            },
          },
        }}
      />
    </>
  )
}
