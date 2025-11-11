import { useState, useRef } from "react";
import { ArrowUp, Paperclip, X } from "lucide-react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { ChatContainer } from "./ChatContainer";
import type { Message } from "./ChatMessage";
import { sendChatMessage } from "@/lib/api";
import { toast } from "sonner";

interface PromptAreaProps {
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
}

export function PromptArea({ messages, setMessages }: PromptAreaProps) {
  const [prompt, setPrompt] = useState("");
  const [attachedFiles, setAttachedFiles] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = async () => {
    if (!prompt.trim() && attachedFiles.length === 0) return;
    
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: prompt.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setPrompt("");
    setIsLoading(true);

    try {
      // Prepare conversation history for API
      const history = messages.map((msg) => ({
        role: msg.role,
        content: msg.content,
      }));

      const response = await sendChatMessage(userMessage.content, history);

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      toast.error("Failed to send message. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    setAttachedFiles((prev) => [...prev, ...files]);
  };

  const removeFile = (index: number) => {
    setAttachedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="flex h-full flex-col">
      {/* Chat Messages */}
      {messages.length > 0 && (
        <ChatContainer messages={messages} isLoading={isLoading} />
      )}

      {/* Input Area - Only show when no messages or at bottom */}
      <div className="border-t border-border bg-background">
        <div className="mx-auto w-full max-w-3xl px-4 py-4">
          {/* Suggestions - Only show when no messages */}
          {messages.length === 0 && (
            <>
              <div className="mb-8 text-center">
                <h1 className="mb-2 text-2xl font-semibold">What would you like to solve?</h1>
                <p className="text-muted-foreground">
                  Describe the coding problem you want to practice
                </p>
              </div>

              <div className="mb-4 grid grid-cols-2 gap-3">
                <button
                  onClick={() =>
                    setPrompt(
                      "Create a medium difficulty problem about binary trees"
                    )
                  }
                  className="rounded-xl border border-border bg-card p-4 text-left hover:bg-accent transition-colors"
                >
                  <div className="mb-1">🌳 Binary Trees</div>
                  <div className="text-sm text-muted-foreground">
                    Generate tree traversal problems
                  </div>
                </button>

                <button
                  onClick={() =>
                    setPrompt(
                      "Create a hard difficulty problem involving dynamic programming"
                    )
                  }
                  className="rounded-xl border border-border bg-card p-4 text-left hover:bg-accent transition-colors"
                >
                  <div className="mb-1">💎 Dynamic Programming</div>
                  <div className="text-sm text-muted-foreground">
                    Generate DP optimization problems
                  </div>
                </button>

                <button
                  onClick={() =>
                    setPrompt(
                      "Create an easy problem about array manipulation"
                    )
                  }
                  className="rounded-xl border border-border bg-card p-4 text-left hover:bg-accent transition-colors"
                >
                  <div className="mb-1">📊 Arrays</div>
                  <div className="text-sm text-muted-foreground">
                    Generate array-based challenges
                  </div>
                </button>

                <button
                  onClick={() =>
                    setPrompt(
                      "Create a problem about graph algorithms and pathfinding"
                    )
                  }
                  className="rounded-xl border border-border bg-card p-4 text-left hover:bg-accent transition-colors"
                >
                  <div className="mb-1">🗺️ Graphs</div>
                  <div className="text-sm text-muted-foreground">
                    Generate graph traversal problems
                  </div>
                </button>
              </div>
            </>
          )}

          {/* Input Area */}
          <div className="relative">
            <div className="rounded-3xl border border-border bg-background shadow-lg">
              {/* Attached Files */}
              {attachedFiles.length > 0 && (
                <div className="flex flex-wrap gap-2 p-3 pb-0">
                  {attachedFiles.map((file, index) => (
                    <div
                      key={index}
                      className="flex items-center gap-2 rounded-lg bg-muted px-3 py-1.5"
                    >
                      <Paperclip className="h-3 w-3" />
                      <span className="text-sm">{file.name}</span>
                      <button
                        onClick={() => removeFile(index)}
                        className="rounded-full hover:bg-background p-0.5"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </div>
                  ))}
                </div>
              )}

              {/* Textarea */}
              <Textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type your message..."
                className="min-h-24 resize-none border-0 bg-transparent p-4 focus-visible:ring-0 focus-visible:ring-offset-0"
              />

              {/* Actions */}
              <div className="flex items-center justify-between p-3 pt-0">
                <div>
                  <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    className="hidden"
                    onChange={handleFileSelect}
                  />
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-9 w-9"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    <Paperclip className="h-5 w-5" />
                  </Button>
                </div>

                <Button
                  onClick={handleSubmit}
                  disabled={!prompt.trim() && attachedFiles.length === 0}
                  size="icon"
                  className="h-9 w-9 rounded-full"
                >
                  <ArrowUp className="h-5 w-5" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
