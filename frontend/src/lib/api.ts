import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("vula_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("vula_token");
      localStorage.removeItem("vula_user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (email: string, password: string) =>
    api.post("/auth/register", { email, password }),
  login: (email: string, password: string) =>
    api.post("/auth/login", { email, password }),
  getMe: () => api.get("/auth/me"),
};

export const detectionAPI = {
  detect: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return api.post("/detect", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  getHistory: (skip = 0, limit = 10) =>
    api.get(`/detect/history?skip=${skip}&limit=${limit}`),
  getById: (id: number) => api.get(`/detect/${id}`),
};

export const analyticsAPI = {
  getStats: () => api.get("/analytics/stats"),
  getDiseaseDistribution: () => api.get("/analytics/disease-distribution"),
};
