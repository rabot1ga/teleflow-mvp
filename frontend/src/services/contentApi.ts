import apiClient from './api'

export interface Source {
  id: string
  project_id: string
  name: string
  source_type: 'rss' | 'json_api' | 'scraper' | 'telegram' | 'webhook'
  url?: string
  fetch_interval_minutes: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Article {
  id: string
  project_id: string
  source_id: string
  title: string
  content?: string
  summary?: string
  url?: string
  image_url?: string
  category?: string
  tags: string[]
  status: 'pending' | 'approved' | 'rejected' | 'published'
  quality_score: number
  priority_score: number
  created_at: string
  updated_at: string
}

export const contentApi = {
  // Sources
  getSources: (projectId: string) =>
    apiClient.get('/api/v1/content/sources', {
      params: { project_id: projectId },
      headers: { 'X-Project-ID': projectId },
    }),

  createSource: (data: Partial<Source>) =>
    apiClient.post('/api/v1/content/sources', data, {
      headers: {
        'Content-Type': 'application/json',
        'X-Project-ID': data.project_id || '',
      },
    }),

  updateSource: (id: string, data: Partial<Source>) =>
    apiClient.patch(`/api/v1/content/sources/${id}`, data),

  deleteSource: (id: string) =>
    apiClient.delete(`/api/v1/content/sources/${id}`),

  fetchSource: (id: string) =>
    apiClient.post(`/api/v1/content/sources/${id}/fetch`),

  // Articles
  getArticles: (params: { project_id: string; status?: string; page?: number; per_page?: number }) =>
    apiClient.get('/api/v1/content/articles', { params }),

  getArticle: (id: string) =>
    apiClient.get(`/api/v1/content/articles/${id}`),

  updateArticle: (id: string, data: Partial<Article>) =>
    apiClient.patch(`/api/v1/content/articles/${id}`, data),

  deleteArticle: (id: string) =>
    apiClient.delete(`/api/v1/content/articles/${id}`),

  // Moderation
  getModerationQueue: (params: { status?: string; per_page?: number }) =>
    apiClient.get('/api/v1/content/moderation/queue', { params }),

  approveArticle: (id: string, target_id?: string) =>
    apiClient.post(`/api/v1/content/articles/${id}/approve`, { target_id }),

  rejectArticle: (id: string, reason: string, comment?: string) =>
    apiClient.post(`/api/v1/content/articles/${id}/reject`, { reason, comment }),

  // AI Operations
  rewriteArticle: (articleId: string, projectId: string, style?: string, tone?: string) =>
    apiClient.post('/api/v1/content/ai/rewrite', {
      article_id: articleId,
      project_id: projectId,
      style,
      tone,
    }),

  summarizeArticle: (articleId: string, projectId: string, max_length?: number) =>
    apiClient.post('/api/v1/content/ai/summarize', {
      article_id: articleId,
      project_id: projectId,
      max_length,
    }),

  classifyArticle: (articleId: string, projectId: string, categories?: string[]) =>
    apiClient.post('/api/v1/content/ai/classify', {
      article_id: articleId,
      project_id: projectId,
      categories,
    }),

  generateTags: (articleId: string, projectId: string, max_tags?: number) =>
    apiClient.post('/api/v1/content/ai/generate-tags', {
      article_id: articleId,
      project_id: projectId,
      max_tags,
    }),
}
