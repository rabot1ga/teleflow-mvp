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
    apiClient.get('/content/sources', { params: { project_id: projectId } }),

  createSource: (data: Partial<Source>) =>
    apiClient.post('/content/sources', data),

  updateSource: (id: string, data: Partial<Source>) =>
    apiClient.patch(`/content/sources/${id}`, data),

  deleteSource: (id: string) =>
    apiClient.delete(`/content/sources/${id}`),

  fetchSource: (id: string) =>
    apiClient.post(`/content/sources/${id}/fetch`),

  // Articles
  getArticles: (params: { project_id: string; status?: string; page?: number; per_page?: number }) =>
    apiClient.get('/content/articles', { params }),

  getArticle: (id: string) =>
    apiClient.get(`/content/articles/${id}`),

  updateArticle: (id: string, data: Partial<Article>) =>
    apiClient.patch(`/content/articles/${id}`, data),

  deleteArticle: (id: string) =>
    apiClient.delete(`/content/articles/${id}`),

  // Moderation
  getModerationQueue: (params: { status?: string; per_page?: number }) =>
    apiClient.get('/content/moderation/queue', { params }),

  approveArticle: (id: string, target_id?: string) =>
    apiClient.post(`/content/articles/${id}/approve`, { target_id }),

  rejectArticle: (id: string, reason: string, comment?: string) =>
    apiClient.post(`/content/articles/${id}/reject`, { reason, comment }),

  // AI Operations
  rewriteArticle: (articleId: string, projectId: string, style?: string, tone?: string) =>
    apiClient.post('/content/ai/rewrite', {
      article_id: articleId,
      project_id: projectId,
      style,
      tone,
    }),

  summarizeArticle: (articleId: string, projectId: string, max_length?: number) =>
    apiClient.post('/content/ai/summarize', {
      article_id: articleId,
      project_id: projectId,
      max_length,
    }),

  classifyArticle: (articleId: string, projectId: string, categories?: string[]) =>
    apiClient.post('/content/ai/classify', {
      article_id: articleId,
      project_id: projectId,
      categories,
    }),

  generateTags: (articleId: string, projectId: string, max_tags?: number) =>
    apiClient.post('/content/ai/generate-tags', {
      article_id: articleId,
      project_id: projectId,
      max_tags,
    }),
}
