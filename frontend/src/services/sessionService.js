import api from './api.js';
export const sessionService = {
  createSession: async (ctx) => (await api.post('/session', ctx)).data,
  getSession: async (id) => (await api.get(`/session/${id}`)).data,
  getConcernState: async (id) => (await api.get(`/session/${id}/concerns`)).data,
  getEvidenceHistory: async (id) => (await api.get(`/session/${id}/evidence`)).data,
};
