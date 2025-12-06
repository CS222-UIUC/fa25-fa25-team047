import { Plus, MessageSquare, Trash2 } from "lucide-react";
import { Button } from "./ui/button";
import { ScrollArea } from "./ui/scroll-area";

interface ChatHistory {
  id: string;
  title: string;
  createdAt: string;
}

interface ChatSidebarProps {
  chats: ChatHistory[];
  currentChatId: string;
  onNewChat: () => void;
  onSelectChat: (id: string) => void;
  onDeleteChat: (id: string) => void;
}

function formatDateLabel(dateStr: string): string {
  const date = new Date(dateStr);
  const now = new Date();
  const diff = (now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24);
  if (diff < 1) return "Today";
  if (diff < 2) return "Yesterday";
  return date.toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

export function ChatSidebar({ chats, currentChatId, onNewChat, onSelectChat, onDeleteChat }: ChatSidebarProps) {
  const groupedHistory = chats.reduce((acc, chat) => {
    const label = formatDateLabel(chat.createdAt);
    if (!acc[label]) {
      acc[label] = [];
    }
    acc[label].push(chat);
    return acc;
  }, {} as Record<string, ChatHistory[]>);

  return (
    <div className="flex h-full w-64 flex-col border-r border-border bg-background">
      {/* Header */}
      <div className="p-3 border-b border-border">
        <Button
          className="w-full justify-start gap-3 bg-transparent text-white border border-white/30 hover:bg-accent cursor-pointer"
          variant="outline"
          onClick={onNewChat}
        >
          <span className="flex h-8 w-8 items-center justify-center rounded-full border border-white/30 bg-white/10 text-white">
            <Plus className="h-4 w-4 fill-white" />
          </span>
          <span className="text-sm font-medium text-white">New Chat</span>
        </Button>
      </div>

      {/* Chat History */}
      <ScrollArea className="flex-1">
        <div className="p-2">
          {Object.entries(groupedHistory).map(([timestamp, chats]) => (
            <div key={timestamp} className="mb-4">
              <div className="px-3 py-2 text-xs text-muted-foreground">
                {timestamp}
              </div>
              {chats.map((chat) => (
                <div
                  key={chat.id}
                  onClick={() => onSelectChat(chat.id)}
                  className={`group relative flex items-center gap-2 rounded-lg px-3 py-2 hover:bg-accent cursor-pointer mb-1 ${
                    chat.id === currentChatId ? "bg-accent" : ""
                  }`}
                >
                  <span className="flex h-8 w-8 items-center justify-center rounded-full border border-white/30 bg-white/10 text-white">
                    <MessageSquare className="h-4 w-4 flex-shrink-0 text-white fill-white" />
                  </span>
                  <span className="flex-1 truncate text-sm text-white">
                    {chat.title || "New Chat"}
                  </span>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteChat(chat.id);
                    }}
                  >
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </div>
              ))}
            </div>
          ))}
        </div>
      </ScrollArea>

      {/* Footer */}
      <div className="p-3 border-t border-border">
        <div className="text-xs text-muted-foreground text-center">
          AI LeetCode Generator
        </div>
      </div>
    </div>
  );
}
