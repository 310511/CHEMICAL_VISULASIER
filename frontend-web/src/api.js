import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  login: (credentials) => api.post('/auth/login/', credentials),
  logout: () => api.post('/auth/logout/'),
};

// Equipment API calls
export const equipmentAPI = {
  uploadCSV: (formData) => {
    const uploadApi = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    const token = localStorage.getItem('authToken');
    if (token) {
      uploadApi.defaults.headers.Authorization = `Token ${token}`;
    }
    
    return uploadApi.post('/upload/', formData);
  },
  
  getEquipment: (datasetId) => api.get('/equipment/', { params: { dataset_id: datasetId } }),
  getSummary: (datasetId) => api.get('/summary/', { params: { dataset_id: datasetId } }),
  getHistory: () => api.get('/history/'),
  downloadPDF: (datasetId) => {
    const pdfApi = axios.create({
      baseURL: API_BASE_URL,
      responseType: 'blob',
    });
    
    const token = localStorage.getItem('authToken');
    if (token) {
      pdfApi.defaults.headers.Authorization = `Token ${token}`;
    }
    
    return pdfApi.get('/report/pdf/', { params: { dataset_id: datasetId } });
  },
};

export default api;
