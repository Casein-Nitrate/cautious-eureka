import api from './api.js';
export const counsellingService = {
  sendMessage: async (sessionId, speaker, message, language) =>
    (await api.post('/counselling/message', { session_id: sessionId, speaker, message, language })).data,
};
