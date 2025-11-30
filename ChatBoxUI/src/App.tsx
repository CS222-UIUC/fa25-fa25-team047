import { useState } from "react";
import { ChatSidebar } from "./components/ChatSidebar";
import { PromptArea } from "./components/PromptArea";
import { LoginPage } from "./components/LoginPage";
import { login } from "./lib/auth";
import type { LoginCredentials } from "./types/auth";
import type { Message } from "./components/ChatMessage";
import { useMemo } from "react";

type ChatSession = {
  id: string;
  title: string;
  createdAt: string;
  messages: Message[];
};

type AuthState =
  | { status: "unauthenticated" }
  | { status: "authenticating" }
  | { status: "authenticated"; email: string }
  | { status: "error"; message: string };

export default function App() {
  const [authState, setAuthState] = useState<AuthState>({
    status: "unauthenticated",
  });
  const [chats, setChats] = useState<ChatSession[]>([
    {
      id: crypto.randomUUID(),
      title: "New Chat",
      createdAt: new Date().toISOString(),
      messages: [],
    },
  ]);
  const [currentChatId, setCurrentChatId] = useState<string>(() => chats[0].id);

  const currentChat = useMemo(
    () => chats.find((c) => c.id === currentChatId) ?? chats[0],
    [chats, currentChatId]
  );

  const updateCurrentMessages = (updater: (prev: Message[]) => Message[]) => {
    setChats((prev) =>
      prev.map((chat) =>
        chat.id === currentChatId
          ? { ...chat, messages: updater(chat.messages) }
          : chat
      )
    );
  };

  const renameCurrentChat = (title: string) => {
    setChats((prev) =>
      prev.map((chat) =>
        chat.id === currentChatId ? { ...chat, title } : chat
      )
    );
  };

  const handleNewChat = () => {
    const id = crypto.randomUUID();
    const next: ChatSession = {
      id,
      title: "New Chat",
      createdAt: new Date().toISOString(),
      messages: [],
    };
    setChats((prev) => [next, ...prev]);
    setCurrentChatId(id);
  };

  const handleSelectChat = (id: string) => {
    setCurrentChatId(id);
  };

  const handleDeleteChat = (id: string) => {
    setChats((prev) => {
      const remaining = prev.filter((chat) => chat.id !== id);
      if (remaining.length === 0) {
        const newId = crypto.randomUUID();
        const blank: ChatSession = {
          id: newId,
          title: "New Chat",
          createdAt: new Date().toISOString(),
          messages: [],
        };
        setCurrentChatId(newId);
        return [blank];
      }
      if (id === currentChatId) {
        setCurrentChatId(remaining[0].id);
      }
      return remaining;
    });
  };

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
    <div className="flex min-h-screen w-full bg-background overflow-visible">
      {/* Sidebar */}
      <ChatSidebar
        chats={chats}
        currentChatId={currentChatId}
        onNewChat={handleNewChat}
        onSelectChat={handleSelectChat}
        onDeleteChat={handleDeleteChat}
      />

      {/* Main Content */}
      <div className="flex-1 overflow-visible">
        <PromptArea
          messages={currentChat?.messages ?? []}
          updateMessages={updateCurrentMessages}
          renameChat={renameCurrentChat}
        />
      </div>
    </div>
  );
}
