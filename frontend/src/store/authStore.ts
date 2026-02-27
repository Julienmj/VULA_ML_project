import { create } from "zustand";
import type { User } from "@/types";
import { authAPI } from "@/lib/api";

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
  loadFromStorage: () => void;
  fetchUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,

  setAuth: (user, token) => {
    localStorage.setItem("vula_token", token);
    localStorage.setItem("vula_user", JSON.stringify(user));
    set({ user, token, isAuthenticated: true });
  },

  logout: () => {
    localStorage.removeItem("vula_token");
    localStorage.removeItem("vula_user");
    set({ user: null, token: null, isAuthenticated: false });
  },

  loadFromStorage: () => {
    const token = localStorage.getItem("vula_token");
    const userStr = localStorage.getItem("vula_user");
    if (token && userStr) {
      try {
        const user = JSON.parse(userStr);
        set({ user, token, isAuthenticated: true });
      } catch {
        set({ user: null, token: null, isAuthenticated: false });
      }
    }
  },

  fetchUser: async () => {
    try {
      const { data } = await authAPI.getMe();
      const token = localStorage.getItem("vula_token");
      if (token) {
        set({ user: data, token, isAuthenticated: true });
        localStorage.setItem("vula_user", JSON.stringify(data));
      }
    } catch {
      set({ user: null, token: null, isAuthenticated: false });
    }
  },
}));
