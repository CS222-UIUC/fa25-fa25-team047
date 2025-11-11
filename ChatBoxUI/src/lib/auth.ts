import type { LoginCredentials } from "../types/auth";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

export interface AuthResponse {
  token: string;
  email: string;
  user: {
    id: number;
    email: string;
    created_at: string;
  };
}

export async function login(
  credentials: LoginCredentials
): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Login failed");
  }

  return {
    token: data.token,
    email: data.user.email,
    user: data.user,
  };
}

export async function register(
  credentials: LoginCredentials
): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Registration failed");
  }

  return {
    token: data.token,
    email: data.user.email,
    user: data.user,
  };
}

export async function getCurrentUser(token: string) {
  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Failed to get user info");
  }

  return data.user;
}
