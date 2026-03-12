import apiClient from '@/services/api'

export interface Target {
  id: string
  name: string
  chat_id: string
  type: 'channel' | 'group'
  is_active: boolean
  created_at: string
}

export interface Template {
  id: string
  name: string
  content: string
  is_default: boolean
  created_at: string
}

export interface PublishJob {
  id: string
  target_id: string
  template_id: string
  scheduled_at: string
  status: 'pending' | 'published' | 'failed'
}

export const publishingApi = {
  getTargets: (projectId: string) =>
    apiClient.get(`/api/v1/publishing/targets?project_id=${projectId}`),

  createTarget: (data: { project_id: string; name: string; chat_id: string; type: 'channel' | 'group' }) =>
    apiClient.post('/api/v1/publishing/targets', data),

  updateTarget: (id: string, data: Partial<Target>) =>
    apiClient.put(`/api/v1/publishing/targets/${id}`, data),

  deleteTarget: (id: string) =>
    apiClient.delete(`/api/v1/publishing/targets/${id}`),

  getTemplates: (projectId: string) =>
    apiClient.get(`/api/v1/publishing/templates?project_id=${projectId}`),

  createTemplate: (data: { project_id: string; name: string; content: string }) =>
    apiClient.post('/api/v1/publishing/templates', data),

  updateTemplate: (id: string, data: Partial<Template>) =>
    apiClient.put(`/api/v1/publishing/templates/${id}`, data),

  deleteTemplate: (id: string) =>
    apiClient.delete(`/api/v1/publishing/templates/${id}`),

  getJobs: (projectId: string) =>
    apiClient.get(`/api/v1/publishing/jobs?project_id=${projectId}`),

  createJob: (data: { project_id: string; target_id: string; template_id: string; scheduled_at: string }) =>
    apiClient.post('/api/v1/publishing/jobs', data),

  updateJob: (id: string, data: Partial<PublishJob>) =>
    apiClient.put(`/api/v1/publishing/jobs/${id}`, data),

  deleteJob: (id: string) =>
    apiClient.delete(`/api/v1/publishing/jobs/${id}`),
}
