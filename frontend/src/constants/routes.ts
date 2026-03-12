// Route paths configuration
export const ROUTES = {
  // Auth
  LOGIN: '/login',
  REGISTER: '/register',
  FORGOT_PASSWORD: '/forgot-password',
  RESET_PASSWORD: '/reset-password',

  // Main
  DASHBOARD: '/dashboard',
  CONTENT: '/content',
  PUBLISHING: '/publishing',
  FUNNELS: '/funnels',
  USERBOT: '/userbot',
  PROMOTION: '/promotion',
  ANALYTICS: '/analytics',
  SETTINGS: '/settings',
} as const

export type RoutePath = (typeof ROUTES)[keyof typeof ROUTES]
