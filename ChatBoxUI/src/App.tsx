import { ChatSidebar } from "./components/ChatSidebar";
import { PromptArea } from "./components/PromptArea";

export default function App() {
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
