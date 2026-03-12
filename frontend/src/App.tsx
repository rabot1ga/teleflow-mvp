import { RouterProvider } from 'react-router-dom'
import { QueryProvider, ToastProvider } from './app/providers'
import { router } from './app/router/routes'
import './styles/index.css'

function App() {
  return (
    <QueryProvider>
      <ToastProvider>
        <RouterProvider router={router} />
      </ToastProvider>
    </QueryProvider>
  )
}

export default App
