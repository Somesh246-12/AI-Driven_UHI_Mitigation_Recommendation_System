import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 8000, // 8 second timeout for all requests
});

export const getHeatmapData = async () => {
  const response = await api.get('/api/v1/heatmap_data');
  return response.data;
};

export const simulateIntervention = async (interventions) => {
  const response = await api.post('/api/v1/simulate_intervention', {
    interventions,
  });
  return response.data;
};

export const getRecommendations = async () => {
  const response = await api.get('/api/v1/recommendations');
  return response.data;
};

export const getHealthPrecautions = async (lat = null, lon = null) => {
  const params = {};
  if (lat !== null) params.lat = lat;
  if (lon !== null) params.lon = lon;
  const response = await api.get('/api/v1/health_precautions', { params });
  return response.data;
};

export default api;


