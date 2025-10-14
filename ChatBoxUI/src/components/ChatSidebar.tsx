import { Plus, MessageSquare, Trash2 } from "lucide-react";
import { Button } from "./ui/button";
import { ScrollArea } from "./ui/scroll-area";

interface ChatHistory {
  id: string;
  title: string;
  timestamp: string;
}

export function ChatSidebar() {
  // Mock chat history data
  const chatHistory: ChatHistory[] = [
    { id: "1", title: "Two Sum Problem", timestamp: "Today" },
    { id: "2", title: "Binary Search Tree", timestamp: "Today" },
    { id: "3", title: "Dynamic Programming", timestamp: "Yesterday" },
    { id: "4", title: "Graph Traversal", timestamp: "Yesterday" },
    { id: "5", title: "Linked List Reversal", timestamp: "Oct 12" },
    { id: "6", title: "Array Manipulation", timestamp: "Oct 12" },
    { id: "7", title: "String Algorithms", timestamp: "Oct 11" },
    { id: "8", title: "Tree Problems", timestamp: "Oct 10" },
  ];

  const groupedHistory = chatHistory.reduce((acc, chat) => {
    if (!acc[chat.timestamp]) {
      acc[chat.timestamp] = [];
    }
    acc[chat.timestamp].push(chat);
    return acc;
  }, {} as Record<string, ChatHistory[]>);

  return (
    <div className="flex h-full w-64 flex-col border-r border-border bg-background">
      {/* Header */}
      <div className="p-3 border-b border-border">
        <Button className="w-full justify-start gap-2" variant="outline">
          <Plus className="h-4 w-4" />
          New Chat
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
                  className="group relative flex items-center gap-2 rounded-lg px-3 py-2 hover:bg-accent cursor-pointer mb-1"
                >
                  <MessageSquare className="h-4 w-4 flex-shrink-0 text-muted-foreground" />
                  <span className="flex-1 truncate text-sm">{chat.title}</span>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
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
