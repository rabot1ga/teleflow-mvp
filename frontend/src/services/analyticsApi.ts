import apiClient from './api'

export const analyticsApi = {
  // Dashboard
  getOverview: (projectId: string, days: number = 7) =>
    apiClient.get('/analytics/dashboard/overview', { params: { project_id: projectId, days } }),

  getContentStats: (projectId: string, days: number = 30) =>
    apiClient.get('/analytics/dashboard/content', { params: { project_id: projectId, days } }),

  getFunnelStats: (projectId: string, days: number = 30) =>
    apiClient.get('/analytics/dashboard/funnels', { params: { project_id: projectId, days } }),

  getBroadcastStats: (projectId: string, days: number = 30) =>
    apiClient.get('/analytics/dashboard/broadcasts', { params: { project_id: projectId, days } }),

  getPromotionStats: (projectId: string, days: number = 30) =>
    apiClient.get('/analytics/dashboard/promotion', { params: { project_id: projectId, days } }),
}
