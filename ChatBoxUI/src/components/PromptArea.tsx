import { useState, useRef } from "react";
import { ArrowUp, Paperclip, X } from "lucide-react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";

export function PromptArea() {
  const [prompt, setPrompt] = useState("");
  const [attachedFiles, setAttachedFiles] = useState<File[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = () => {
    if (!prompt.trim() && attachedFiles.length === 0) return;
    console.log("Submitting:", { prompt, files: attachedFiles });
    // Handle submission logic here
    setPrompt("");
    setAttachedFiles([]);
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
    <div className="flex h-full flex-col items-center justify-center px-4">
      <div className="w-full max-w-3xl">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="mb-2">What would you like to solve?</h1>
          <p className="text-muted-foreground">
            Describe the coding problem you want to practice
          </p>
        </div>

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
              placeholder="e.g., Create a problem about finding the longest palindrome in a string..."
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

        {/* Suggestions */}
        <div className="mt-8 grid grid-cols-2 gap-3">
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
      </div>
    </div>
  );
}
