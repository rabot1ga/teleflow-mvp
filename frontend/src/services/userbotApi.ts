import apiClient from './api'

export interface UserbotAccount {
  id: string
  project_id: string
  name: string
  phone_number?: string
  telegram_id?: number
  username?: string
  first_name?: string
  last_name?: string
  status: 'inactive' | 'active' | 'banned' | 'needs_auth' | 'needs_2fa'
  is_warming_enabled: boolean
  warming_day: number
  is_online: boolean
  created_at: string
  updated_at: string
}

export interface Proxy {
  id: string
  account_id: string
  name: string
  proxy_type: 'mtproto' | 'socks5' | 'http'
  hostname: string
  port: number
  username?: string
  password?: string
  secret?: string
  is_active: boolean
  is_working?: boolean
  created_at: string
}

export const userbotApi = {
  // Accounts
  getAccounts: (projectId: string) =>
    apiClient.get('/userbot/accounts', { params: { project_id: projectId } }),

  createAccount: (data: { project_id: string; name: string }) =>
    apiClient.post('/userbot/accounts', data),

  deleteAccount: (id: string) =>
    apiClient.delete(`/userbot/accounts/${id}`),

  // Authorization
  sendCode: (accountId: string, phone: string) =>
    apiClient.post(`/userbot/accounts/${accountId}/send-code`, { phone }),

  verifyCode: (accountId: string, code: string) =>
    apiClient.post(`/userbot/accounts/${accountId}/verify`, { code }),

  submit2FA: (accountId: string, password: string) =>
    apiClient.post(`/userbot/accounts/${accountId}/2fa`, { password }),

  // Proxies
  getProxies: (accountId: string) =>
    apiClient.get('/userbot/proxies', { params: { account_id: accountId } }),

  createProxy: (data: Partial<Proxy>) =>
    apiClient.post('/userbot/proxies', data),

  updateProxy: (id: string, data: Partial<Proxy>) =>
    apiClient.patch(`/userbot/proxies/${id}`, data),

  deleteProxy: (id: string) =>
    apiClient.delete(`/userbot/proxies/${id}`),

  checkProxy: (id: string) =>
    apiClient.post(`/userbot/proxies/${id}/check`),
}
