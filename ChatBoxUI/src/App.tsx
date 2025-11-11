import { useState } from "react";
import { ChatSidebar } from "./components/ChatSidebar";
import { PromptArea } from "./components/PromptArea";
import { LoginPage } from "./components/LoginPage";
import { login } from "./lib/auth";
import type { LoginCredentials } from "./types/auth";

type AuthState =
  | { status: "unauthenticated" }
  | { status: "authenticating" }
  | { status: "authenticated"; email: string }
  | { status: "error"; message: string };

export default function App() {
  const [authState, setAuthState] = useState<AuthState>({
    status: "unauthenticated",
  });

  const handleLogin = async (credentials: LoginCredentials) => {
    try {
      setAuthState({ status: "authenticating" });
      const response = await login(credentials);
      try {
        sessionStorage.setItem("authToken", response.token);
      } catch {
        // Non-blocking: sessionStorage may be unavailable in some environments.
      }
      setAuthState({ status: "authenticated", email: response.email });
    } catch (error) {
      setAuthState({
        status: "error",
        message:
          error instanceof Error ? error.message : "Unable to sign in right now.",
      });
    }
  };

  if (authState.status !== "authenticated") {
    return (
      <LoginPage
        onSubmit={handleLogin}
        isSubmitting={authState.status === "authenticating"}
        errorMessage={authState.status === "error" ? authState.message : undefined}
      />
    );
  }

  return (
    <div className="flex h-full w-full bg-background">
      {/* Sidebar */}
      <ChatSidebar />

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <PromptArea />
      </div>
    </div>
  );
}
