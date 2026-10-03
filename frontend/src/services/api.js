import axios from 'axios';
import { mockRequest } from './mock.js';

export const USE_MOCKS = import.meta.env.VITE_USE_MOCKS !== 'false';
const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
});

const wrap = (data) => ({ data });
const api = {
  get: (url, cfg) => (USE_MOCKS ? mockRequest('get', url, null, cfg?.params).then(wrap) : http.get(url, cfg)),
  post: (url, body) => (USE_MOCKS ? mockRequest('post', url, body).then(wrap) : http.post(url, body)),
  patch: (url, body) => (USE_MOCKS ? mockRequest('patch', url, body).then(wrap) : http.patch(url, body)),
};

// Turns any failure into { status, kind, message, fields } so pages can react consistently.
export function parseError(err) {
  const status = err?.response?.status;
  const detail = err?.response?.data?.detail;
  const fields = {};
  if (Array.isArray(detail)) detail.forEach((d) => { fields[d.loc?.[d.loc.length - 1]] = d.msg; });
  if (!err?.response) return { kind: 'network', status: 0, message: 'Cannot reach the server. Check your connection and try again.', fields };
  if (status === 404) return { kind: 'notfound', status, message: 'This session was not found.', fields };
  if (status === 422) return { kind: 'validation', status, message: 'Some details are missing or invalid.', fields };
  if (status === 503) return { kind: 'unavailable', status, message: 'The AI assistant is temporarily unavailable. Please try again in a moment.', fields };
  return { kind: 'server', status, message: 'Something went wrong. Please try again.', fields };
}
export default api;
