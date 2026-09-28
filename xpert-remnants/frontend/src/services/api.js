import { appConfig } from '../config/appConfig';

const API_BASE = appConfig.apiBaseUrl;

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };

  try {
    const response = await fetch(url, { ...options, headers });
    if (!response.ok) {
      const errBody = await response.text();
      let errJson;
      try { errJson = JSON.parse(errBody); } catch (_) {}
      throw new Error(errJson?.detail || `HTTP ${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`API Error on ${endpoint}:`, error.message);
    throw error;
  }
}

export const api = {
  // Health
  async checkHealth() {
    try {
      return await request('/api/health');
    } catch (error) {
      return { status: 'offline', application: appConfig.appName, error: error.message };
    }
  },

  // Decision Intelligence: Ask & Feedback
  async ask(query, optionsOrProjectId = null, contextHint = null) {
    let projectId = null;
    let expertId = null;
    let hint = contextHint;

    if (optionsOrProjectId && typeof optionsOrProjectId === 'object') {
      projectId = optionsOrProjectId.projectId || null;
      expertId = optionsOrProjectId.expertId || null;
      hint = optionsOrProjectId.contextHint || hint;
    } else {
      projectId = optionsOrProjectId;
    }

    return await request('/api/ask', {
      method: 'POST',
      body: JSON.stringify({
        query,
        project_id: projectId ? Number(projectId) : null,
        expert_id: expertId ? Number(expertId) : null,
        context_hint: hint
      })
    });
  },

  async submitFeedback(askQuery, feedbackType, actualResult = null, decisionMemoryId = null) {
    return await request('/api/ask/feedback', {
      method: 'POST',
      body: JSON.stringify({
        ask_query: askQuery,
        feedback_type: feedbackType,
        actual_result: actualResult,
        decision_memory_id: decisionMemoryId ? Number(decisionMemoryId) : null
      })
    });
  },

  // Memories & Ingestion
  async getMemories(params = {}) {
    const search = new URLSearchParams();
    if (params.type) search.append('type', params.type);
    if (params.projectId) search.append('project_id', params.projectId);
    if (params.expertId) search.append('expert_id', params.expertId);
    if (params.status) search.append('status', params.status);
    if (params.verificationStatus) search.append('verification_status', params.verificationStatus);
    if (params.skip) search.append('skip', params.skip);
    if (params.limit) search.append('limit', params.limit || 50);

    const queryStr = search.toString() ? `?${search.toString()}` : '';
    return await request(`/api/memories${queryStr}`);
  },

  async getMemory(id) {
    return await request(`/api/memories/${id}`);
  },

  async createMemory(memoryData) {
    return await request('/api/memories', {
      method: 'POST',
      body: JSON.stringify(memoryData)
    });
  },

  async extractDocument(docData) {
    return await request('/api/memories/extract', {
      method: 'POST',
      body: JSON.stringify(docData)
    });
  },

  async approveMemory(id) {
    return await request(`/api/memories/${id}/approve`, {
      method: 'PUT'
    });
  },

  async updateMemoryStatus(id, status, verificationStatus = null) {
    return await request(`/api/memories/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status, verification_status: verificationStatus })
    });
  },

  // Projects & Knowledge Map
  async getProjects() {
    return await request('/api/projects');
  },

  async getProject(id) {
    return await request(`/api/projects/${id}`);
  },

  async getProjectRisks(id) {
    return await request(`/api/projects/${id}/knowledge-risks`);
  },

  async getProjectMap(id) {
    return await request(`/api/projects/${id}/knowledge-map`);
  },

  // Decisions & Replay
  async getDecisions(params = {}) {
    const search = new URLSearchParams();
    if (params.projectId) search.append('project_id', params.projectId);
    if (params.expertId) search.append('expert_id', params.expertId);
    const qs = search.toString() ? `?${search.toString()}` : '';
    return await request(`/api/decisions${qs}`);
  },

  async getDecisionReplay(id) {
    return await request(`/api/decisions/${id}`);
  },

  // Experts & People
  async getExperts() {
    return await request('/api/experts');
  },

  async getExpert(id) {
    return await request(`/api/experts/${id}`);
  },

  async getPeople() {
    return await request('/api/people');
  },

  // Risks
  async getRisks() {
    return await request('/api/risks');
  },

  // Expert Knowledge Handoff
  async submitHandoff(handoffData) {
    return await request('/api/knowledge-handoff', {
      method: 'POST',
      body: JSON.stringify(handoffData)
    });
  },

  // Administration & Diagnostics
  async getAdminStatus() {
    return await request('/api/admin/status');
  },

  async triggerSeed(profile = 'DEV') {
    return await request('/api/admin/seed', {
      method: 'POST',
      body: JSON.stringify({ profile })
    });
  },

  async syncHindsight() {
    return await request('/api/admin/sync-hindsight', {
      method: 'POST'
    });
  }
};
