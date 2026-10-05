import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const sendChatQuery = async (query, targetLanguage = 'en', history = []) => {
  try {
    const response = await apiClient.post('/api/chat', {
      query: query,
      target_language: targetLanguage,
      conversation_history: history,
    });
    return response.data;
  } catch (error) {
    console.error('API Chat Query Error:', error);
    throw error;
  }
};

export const fetchHealthStatus = async () => {
  try {
    const response = await apiClient.get('/api/health');
    return response.data;
  } catch (error) {
    console.error('API Health Check Error:', error);
    return { status: 'offline' };
  }
};

export const fetchAllSchemes = async () => {
  try {
    const response = await apiClient.get('/api/schemes');
    return response.data;
  } catch (error) {
    console.error('API Fetch Schemes Error:', error);
    return { schemes: [] };
  }
};

export const getTTSAudioUrl = (text, language = 'en') => {
  return `${API_BASE_URL}/api/text-to-speech`;
};
