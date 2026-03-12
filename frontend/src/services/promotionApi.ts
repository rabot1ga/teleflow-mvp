import apiClient from './api'

export interface PromotionTask {
  id: string
  project_id: string
  name: string
  task_type: 'parse' | 'invite' | 'masslook' | 'comment'
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  target_chat_id?: string
  source_chat_id?: string
  config: Record<string, any>
  total_count: number
  processed_count: number
  success_count: number
  failed_count: number
  created_at: string
  updated_at: string
}

export interface ParsedUser {
  id: string
  task_id: string
  project_id: string
  telegram_id: number
  username?: string
  first_name?: string
  last_name?: string
  phone?: string
  is_bot: boolean
  is_premium: boolean
  has_photo: boolean
  last_seen_days?: number
  is_invited: boolean
  invited_at?: string
  invite_error?: string
  created_at: string
}

export const promotionApi = {
  // Tasks
  getTasks: (projectId: string, params?: { task_type?: string; status?: string }) =>
    apiClient.get('/promotion/tasks', { params: { project_id: projectId, ...params } }),

  createTask: (data: Partial<PromotionTask>) =>
    apiClient.post('/promotion/tasks', data),

  startTask: (id: string) =>
    apiClient.post(`/promotion/tasks/${id}/start`),

  cancelTask: (id: string) =>
    apiClient.post(`/promotion/tasks/${id}/cancel`),

  deleteTask: (id: string) =>
    apiClient.delete(`/promotion/tasks/${id}`),

  // Parsed Users
  getParsedUsers: (projectId: string, params?: { task_id?: string; is_invited?: boolean }) =>
    apiClient.get('/promotion/parsed-users', { params: { project_id: projectId, ...params } }),

  inviteUser: (id: string) =>
    apiClient.post(`/promotion/parsed-users/${id}/invite`),
}
