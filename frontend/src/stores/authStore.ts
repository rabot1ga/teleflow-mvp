import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  telegram_username?: string
  role: string
}

interface AuthState {
  user: User | null
  token: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, firstName: string, lastName: string) => Promise<void>
  logout: () => void
  setUser: (user: User) => void
  clearUser: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (email: string, password: string) => {
        set({ isLoading: true })
        try {
          const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
          })

          if (!response.ok) {
            const error = await response.json()
            throw new Error(error.error?.message || 'Login failed')
          }

          const data = await response.json()
          const { access_token, refresh_token } = data.data

          set({
            token: access_token,
            refreshToken: refresh_token,
            isAuthenticated: true,
            isLoading: false,
          })

          // Fetch user info
          try {
            const meResponse = await fetch('/api/v1/auth/me', {
              headers: { 'Authorization': `Bearer ${access_token}` },
            })
            const meData = await meResponse.json()
            set({ user: meData.data })
          } catch (e) {
            // Ignore me fetch error
          }
        } catch (error: any) {
          set({ isLoading: false })
          throw error
        }
      },

      register: async (email: string, password: string, firstName: string, lastName: string) => {
        set({ isLoading: true })
        try {
          const response = await fetch('/api/v1/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              email,
              password,
              first_name: firstName,
              last_name: lastName,
            }),
          })

          if (!response.ok) {
            const errorText = await response.text()
            let errorData = { error: { message: 'Registration failed' } }
            try {
              errorData = JSON.parse(errorText)
            } catch (e) {
              // Ignore parse error
            }
            throw new Error(errorData.error?.message || 'Registration failed')
          }

          // Auto login after registration
          const loginResponse = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
          })

          if (!loginResponse.ok) {
            throw new Error('Auto-login failed after registration')
          }

          const loginData = await loginResponse.json()
          set({
            token: loginData.data.access_token,
            refreshToken: loginData.data.refresh_token,
            isAuthenticated: true,
            isLoading: false,
          })
        } catch (error: any) {
          set({ isLoading: false })
          throw error
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          refreshToken: null,
          isAuthenticated: false,
        })
      },

      setUser: (user: User) => {
        set({ user })
      },

      clearUser: () => {
        set({ user: null })
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        token: state.token,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
        user: state.user,
      }),
    }
  )
)
