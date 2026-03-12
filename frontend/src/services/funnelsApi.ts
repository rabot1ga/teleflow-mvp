import apiClient from './api'

export interface Funnel {
  id: string
  project_id: string
  name: string
  trigger_type: 'command' | 'keyword' | 'subscription'
  trigger_value?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface LeadMagnet {
  id: string
  project_id: string
  name: string
  type: 'text' | 'file' | 'link' | 'promo'
  content?: string
  file_url?: string
  delivery_message: string
  require_subscription: boolean
  created_at: string
}

export interface Broadcast {
  id: string
  project_id: string
  name: string
  message_type: 'text' | 'photo' | 'video'
  message_text?: string
  recipient_filter: { type: string }
  status: 'draft' | 'running' | 'completed' | 'cancelled'
  sent: number
  delivered: number
  failed: number
  created_at: string
}

export const funnelsApi = {
  // Funnels
  getFunnels: (projectId: string) =>
    apiClient.get('/funnels/funnels', { params: { project_id: projectId } }),

  createFunnel: (data: Partial<Funnel>) =>
    apiClient.post('/funnels/funnels', data),

  updateFunnel: (id: string, data: Partial<Funnel>) =>
    apiClient.patch(`/funnels/funnels/${id}`, data),

  deleteFunnel: (id: string) =>
    apiClient.delete(`/funnels/funnels/${id}`),

  // Lead Magnets
  getLeadMagnets: (projectId: string) =>
    apiClient.get('/funnels/lead-magnets', { params: { project_id: projectId } }),

  createLeadMagnet: (data: Partial<LeadMagnet>) =>
    apiClient.post('/funnels/lead-magnets', data),

  updateLeadMagnet: (id: string, data: Partial<LeadMagnet>) =>
    apiClient.patch(`/funnels/lead-magnets/${id}`, data),

  deleteLeadMagnet: (id: string) =>
    apiClient.delete(`/funnels/lead-magnets/${id}`),

  // Broadcasts
  getBroadcasts: (projectId: string) =>
    apiClient.get('/funnels/broadcasts', { params: { project_id: projectId } }),

  createBroadcast: (data: Partial<Broadcast>) =>
    apiClient.post('/funnels/broadcasts', data),

  startBroadcast: (id: string) =>
    apiClient.post(`/funnels/broadcasts/${id}/start`),

  cancelBroadcast: (id: string) =>
    apiClient.post(`/funnels/broadcasts/${id}/cancel`),

  deleteBroadcast: (id: string) =>
    apiClient.delete(`/funnels/broadcasts/${id}`),
}
