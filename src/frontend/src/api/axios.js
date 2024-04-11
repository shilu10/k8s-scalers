import axios from 'axios';
import { toast } from 'react-toastify';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  res => res,
  async err => {
    const originalRequest = err.config;

    if (
      err.response?.status === 401 &&
      err.response.data?.error === 'Token expired' &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        const refreshRes = await axios.post('http://locahost:8000/api/v1/refresh', {
          refresh_token: localStorage.getItem('refreshToken'),
        });

        const newAccessToken = refreshRes.data.accessToken;
        localStorage.setItem('accessToken', newAccessToken);

        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // ✅ Show toast and redirect
        toast.error('Session expired. Please log in again.');

        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');

        setTimeout(() => {
          window.location.href = '/login';
        }, 1500); // Delay so user sees the toast

        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(err);
  }
);

export default api;
