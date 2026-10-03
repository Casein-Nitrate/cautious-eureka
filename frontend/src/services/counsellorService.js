import api from './api.js';
export const counsellorService = {
  getCases: async (params = {}) => (await api.get('/counsellor/cases', { params })).data,
  updateCaseStatus: async (id, status) => (await api.patch(`/counsellor/cases/${id}`, { status })).data,
};
