import axios from 'axios';

// Get backend URL with fallback
const getBackendUrl = (): string => {
  // Try environment variable first, then fallback to localhost
  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000';
  
  // Remove trailing slashes for consistent URL construction
  return backendUrl.replace(/\/+$/, '');
};

// Create axios instance with baseURL
export const api = axios.create({
  baseURL: getBackendUrl(),
  timeout: 30000, // Increased to 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle common errors
    if (error.response) {
      const { status } = error.response;
      
      if (status === 401) {
        // Unauthorized - clear token and redirect to login
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    } else if (error.request) {
      console.error('Network error - please check your connection');
    }
    
    return Promise.reject(error);
  }
);

// Helper function to check if backend is configured
export const isBackendConfigured = (): boolean => {
  return !!import.meta.env.VITE_BACKEND_URL;
};

