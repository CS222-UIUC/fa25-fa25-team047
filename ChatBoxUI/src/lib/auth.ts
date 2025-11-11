import type { LoginCredentials, LoginResponse } from "../types/auth";

const DEFAULT_API_BASE_URL = "http://localhost:5000";

function getApiBaseUrl(): string {
  const configured = import.meta.env?.VITE_API_URL;
  if (configured && typeof configured === "string" && configured.trim().length > 0) {
    return configured.replace(/\/+$/, "");
  }
  return DEFAULT_API_BASE_URL;
}

export async function login(
  credentials: LoginCredentials,
): Promise<LoginResponse> {
  const response = await fetch(`${getApiBaseUrl()}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });

  const data = await response.json().catch(() => undefined);

  if (!response.ok) {
    const message =
      typeof data?.error === "string" && data.error.length > 0
        ? data.error
        : "Sign in failed. Please try again.";
    throw new Error(message);
  }

  if (
    typeof data?.token !== "string" ||
    data.token.length === 0 ||
    typeof data.email !== "string"
  ) {
    throw new Error("Unexpected response from server.");
  }

  return {
    token: data.token,
    email: data.email,
  };
}
