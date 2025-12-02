import { useEffect, useState } from "react";
import { Loader2, Sparkles } from "lucide-react";
import { ChatMessage, type Message } from "./ChatMessage";

interface ChatContainerProps {
  messages: Message[];
  isLoading?: boolean;
}

const loadingSteps = [
  {
    title: "Reading your request",
    caption: "Collecting the details to frame the challenge",
  },
  {
    title: "Drafting the problem",
    caption: "Shaping the prompt and constraints",
  },
  {
    title: "Assembling tests",
    caption: "Building visible and hidden cases",
  },
  {
    title: "Polishing the response",
    caption: "Making sure the output is ready to run",
  },
];

export function ChatContainer({ messages, isLoading = false }: ChatContainerProps) {
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    // Auto-scroll to bottom when new messages arrive
    const scrollContainer = document.querySelector('[data-radix-scroll-area-viewport]');
    if (scrollContainer) {
      scrollContainer.scrollTop = scrollContainer.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    if (!isLoading) return;
    setActiveStep(0);

    const interval = setInterval(() => {
      setActiveStep((prev) => (prev + 1) % loadingSteps.length);
    }, 1200);

    return () => clearInterval(interval);
  }, [isLoading]);

  return (
    <div className="flex-1 px-4 py-6 overflow-visible">
      <div className="max-w-6xl mx-auto">
        {messages.length === 0 ? (
          <div className="flex h-full items-center justify-center text-center text-muted-foreground">
            <div>
              <h2 className="text-xl font-semibold mb-2">Start a conversation</h2>
              <p>Type a message below to begin chatting with AI</p>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))
        )}
        {isLoading && (
          <div className="relative mt-6 overflow-hidden rounded-3xl border border-border bg-gradient-to-br from-primary/10 via-card to-background shadow-lg">
            <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(255,255,255,0.18),transparent_35%)]" />
            <div className="pointer-events-none absolute inset-y-0 right-0 w-24 bg-primary/10 blur-3xl" />

            <div className="relative p-6 md:p-7 space-y-5">
              <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/15">
                  <Loader2 className="h-6 w-6 text-primary animate-spin" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-primary">Talking to OpenAI</p>
                  <p className="text-sm text-muted-foreground">We are crafting your coding prompt and tests.</p>
                </div>
              </div>

              <div className="grid gap-2">
                {loadingSteps.map((step, idx) => (
                  <div
                    key={step.title}
                    className={`flex items-start gap-3 rounded-2xl border border-border/60 px-3 py-2.5 transition-colors ${
                      idx === activeStep ? "bg-primary/10 border-primary/40 shadow-sm" : "bg-background/70"
                    }`}
                  >
                    <div
                      className={`mt-1 h-2 w-2 rounded-full ${
                        idx <= activeStep ? "bg-primary animate-pulse" : "bg-muted-foreground/30"
                      }`}
                    />
                    <div>
                      <div className="flex items-center gap-2">
                        <p className="text-sm font-semibold">{step.title}</p>
                        {idx === activeStep && <Sparkles className="h-4 w-4 text-primary animate-pulse" />}
                      </div>
                      <p className="text-xs text-muted-foreground">{step.caption}</p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="h-2 w-full overflow-hidden rounded-full bg-background/70">
                <div
                  className="h-full rounded-full bg-primary transition-all duration-700"
                  style={{ width: `${((activeStep + 1) / loadingSteps.length) * 100}%` }}
                />
              </div>

              <p className="text-xs text-muted-foreground">
                Responses automatically appear here once OpenAI finishes.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
