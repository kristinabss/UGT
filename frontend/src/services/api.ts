import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Технологии
export const technologiesApi = {
  getAll: (params?: { industry_id?: number; enterprise_id?: number }) =>
    api.get('/technologies', { params }),
  
  getById: (id: number) =>
    api.get(`/technologies/${id}`),
  
  create: (data: any) =>
    api.post('/technologies', data),
  
  update: (id: number, data: any) =>
    api.put(`/technologies/${id}`, data),
  
  delete: (id: number) =>
    api.delete(`/technologies/${id}`),
  
  assess: (id: number, data: any) =>
    api.post(`/technologies/${id}/assess`, data),
  
  getAssessments: (id: number) =>
    api.get(`/technologies/${id}/assessments`),
  
  forecast: (id: number, target_ugt?: number) =>
    api.get(`/technologies/${id}/forecast`, { params: { target_ugt } }),
};

// Продукция
export const productsApi = {
  getAll: (params?: { technology_id?: number; enterprise_id?: number }) =>
    api.get('/products', { params }),
  
  getById: (id: number) =>
    api.get(`/products/${id}`),
  
  create: (data: any) =>
    api.post('/products', data),
  
  update: (id: number, data: any) =>
    api.put(`/products/${id}`, data),
  
  delete: (id: number) =>
    api.delete(`/products/${id}`),
  
  getCharacteristics: (id: number) =>
    api.get(`/products/${id}/characteristics`),
  
  addCharacteristic: (id: number, data: any) =>
    api.post(`/products/${id}/characteristics`, data),
  
  getProductionMetrics: (id: number) =>
    api.get(`/products/${id}/production-metrics`),
  
  addProductionMetric: (id: number, data: any) =>
    api.post(`/products/${id}/production-metrics`, data),
  
  getEconomicMetrics: (id: number) =>
    api.get(`/products/${id}/economic-metrics`),
  
  addEconomicMetric: (id: number, data: any) =>
    api.post(`/products/${id}/economic-metrics`, data),
};

// Дашборд
export const dashboardApi = {
  getStats: () =>
    api.get('/dashboard/stats'),
  
  getUgtTrend: (days?: number) =>
    api.get('/dashboard/ugt-trend', { params: { days } }),
};
