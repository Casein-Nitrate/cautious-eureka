import api from './api.js';
export const adminService = {
  getAnalyticsSummary: async () => (await api.get('/admin/analytics')).data,
  getDistrictAnalytics: async () => (await api.get('/admin/analytics/districts')).data,
  getTradeAnalytics: async () => (await api.get('/admin/analytics/trades')).data,
  getConcernAnalytics: async () => (await api.get('/admin/analytics/concerns')).data,
};
