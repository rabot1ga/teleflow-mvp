# TeleFlow Frontend

React-based Single Page Application for TeleFlow Platform.

## 🛠 Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **React Router v6** - Routing
- **Zustand** - State management
- **TanStack Query** - Data fetching
- **React Hook Form + Zod** - Forms & validation
- **Bootstrap 5** - UI framework
- **Recharts** - Charts
- **React Hot Toast** - Notifications

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/           # Basic UI components
│   │   ├── layout/       # Layout components (AuthLayout, DashboardLayout)
│   │   └── common/       # Shared components
│   ├── pages/
│   │   ├── auth/         # Auth pages (Login, Register)
│   │   ├── dashboard/    # Dashboard page
│   │   ├── content/      # Content module
│   │   ├── publishing/   # Publishing module
│   │   ├── funnels/      # Funnels module
│   │   ├── userbot/      # Userbot module
│   │   ├── promotion/    # Promotion module
│   │   ├── analytics/    # Analytics module
│   │   └── settings/     # Settings module
│   ├── stores/           # Zustand stores (auth, etc.)
│   ├── hooks/            # Custom hooks
│   ├── services/         # API clients
│   ├── types/            # TypeScript types
│   ├── utils/            # Utility functions
│   └── styles/           # CSS styles
├── package.json
├── vite.config.ts
├── tsconfig.json
└── Dockerfile
```

## 🚀 Quick Start

### Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Open http://localhost:3000
```

### Build

```bash
# Production build
npm run build

# Preview production build
npm run preview
```

### Docker

```bash
# Start with docker compose
docker compose up frontend

# Build and start
docker compose up frontend --build
```

## 📝 Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

## 🔌 API Integration

The frontend connects to the backend API through Traefik gateway.

**Environment Variables:**

```bash
VITE_API_BASE_URL=http://localhost/api/v1
VITE_WS_URL=ws://localhost/ws
```

**API Client:**

```typescript
import apiClient from '@/services/api'

// GET request
const response = await apiClient.get('/content/sources')

// POST request
const response = await apiClient.post('/content/sources', data)

// With authentication (automatic via interceptor)
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

## 🎨 UI Components

### Basic Components (to be implemented)

- Button (primary, secondary, danger, ghost)
- Input (text, password, email, number, textarea)
- Select, Checkbox, Radio, Switch
- Modal, Drawer, Dropdown
- Table, Pagination
- Card, Badge, Avatar
- Toast/Alert
- Loading/Skeleton

### Layout Components

- **AuthLayout** - Centered layout for auth pages
- **DashboardLayout** - Sidebar + Header layout for main app

## 📱 Pages

### Auth Module
- `/login` - Login page
- `/register` - Registration page
- `/forgot-password` - Password recovery
- `/reset-password/:token` - Password reset

### Main Module
- `/dashboard` - Overview dashboard
- `/content/*` - Content management
- `/publishing/*` - Publishing management
- `/funnels/*` - Funnels management
- `/userbot/*` - Userbot management
- `/promotion/*` - Promotion management
- `/analytics/*` - Analytics & reports
- `/settings/*` - Settings

## 🔐 Authentication

Authentication is handled via JWT tokens stored in localStorage.

**Auth Store (Zustand):**

```typescript
import { useAuthStore } from '@/stores/authStore'

const { user, token, isAuthenticated, login, logout } = useAuthStore()

// Login
await login('email@example.com', 'password')

// Logout
logout()

// Check authentication
if (isAuthenticated) {
  // Access protected routes
}
```

**Protected Routes:**

```typescript
<ProtectedRoute>
  <DashboardPage />
</ProtectedRoute>
```

## 📊 State Management

**Zustand Stores:**

- `authStore` - Authentication state
- `contentStore` - Content state (to be implemented)
- `funnelStore` - Funnel state (to be implemented)

**TanStack Query:**

```typescript
import { useQuery } from '@tanstack/react-query'
import apiClient from '@/services/api'

function SourcesList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['sources'],
    queryFn: () => apiClient.get('/content/sources'),
  })
}
```

## 🎯 Development Guidelines

### Component Structure

```typescript
import { useState } from 'react'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

// Types
interface ComponentProps {
  title: string
  onAction: () => void
}

// Schema (if using forms)
const schema = z.object({
  field: z.string().min(1),
})

// Component
export function Component({ title, onAction }: ComponentProps) {
  const [state, setState] = useState(false)
  
  return (
    <div>
      <h1>{title}</h1>
    </div>
  )
}
```

### File Naming

- Components: `PascalCase.tsx` (e.g., `LoginPage.tsx`)
- Utilities: `camelCase.ts` (e.g., `formatDate.ts`)
- Styles: `index.css` (per module)

## 📋 TODO

### Phase 1 (Current) - ✅ COMPLETED
- [x] Project setup
- [x] Vite + React + TypeScript config
- [x] Routing setup
- [x] Auth pages (Login, Register)
- [x] Dashboard layout
- [x] Auth store (Zustand)
- [x] API client
- [x] UI Components:
  - [x] Button (variants, sizes, icons)
  - [x] Card, StatCard
  - [x] Badge, StatusBadge
  - [x] Modal, ConfirmModal
  - [x] Table, Pagination
  - [x] Form, FormField, Input, Select, Textarea
  - [x] FileUpload, FileList
  - [x] Search, Filter
  - [x] Skeleton, LoadingOverlay
  - [x] Breadcrumbs, PageHeader
  - [x] EmptyState, ErrorState
  - [x] Tabs, TabContent
  - [x] Charts (Area, Bar, Pie, Line)
- [x] API services (content, funnels, userbot, promotion, analytics)
- [x] Module pages (Content, Funnels, Userbot, Promotion, Analytics)
- [x] Custom hooks (useLocalStorage, useApi)
- [x] Analytics with charts (Recharts)

### Phase 2 (Next)
- [ ] Full wizards for complex operations
- [ ] Real-time updates (WebSocket)
- [ ] Error boundaries
- [ ] Responsive design improvements
- [ ] Accessibility (ARIA labels, keyboard navigation)

### Phase 3
- [ ] Funnels visual builder (drag & drop)
- [ ] Userbot authorization wizard (complete)
- [ ] Promotion task wizards (full configuration)
- [ ] Settings pages (full)
- [ ] Performance optimization
- [ ] PWA support

## 📖 Documentation

- [UI Screens Specification](../UI_SCREENS.md)
- [API Documentation](../README.md#api-документация)
- [TeleFlow Platform README](../README.md)

---

*Created: 12 March 2026*
