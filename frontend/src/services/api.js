import axios from 'axios';

// Base API URL - would come from environment variables in a real app
const API_URL = 'http://localhost:5000/api';

// Add auth token to all requests
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth services
export const authService = {
  login: (username, password) => 
    axios.post(`${API_URL}/auth/login`, { username, password }),
  
  register: (userData) => 
    axios.post(`${API_URL}/auth/register`, userData),
  
  getCurrentUser: () => 
    axios.get(`${API_URL}/auth/me`)
};

// Transaction services
export const transactionService = {
  getAll: (filters = {}) => 
    axios.get(`${API_URL}/transactions`, { params: filters }),
  
  getById: (id) => 
    axios.get(`${API_URL}/transactions/${id}`),
  
  create: (transaction) => 
    axios.post(`${API_URL}/transactions`, transaction),
  
  update: (id, transaction) => 
    axios.put(`${API_URL}/transactions/${id}`, transaction),
  
  delete: (id) => 
    axios.delete(`${API_URL}/transactions/${id}`)
};

// User services (for admin)
export const userService = {
  getAll: () => 
    axios.get(`${API_URL}/users`),
  
  getById: (id) => 
    axios.get(`${API_URL}/users/${id}`),
  
  update: (id, userData) => 
    axios.put(`${API_URL}/users/${id}`, userData),
  
  delete: (id) => 
    axios.delete(`${API_URL}/users/${id}`)
};
