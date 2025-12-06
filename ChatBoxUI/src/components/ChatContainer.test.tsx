import { act, render, screen } from "@testing-library/react";
import { ChatContainer } from "./ChatContainer";
import type { Message } from "./ChatMessage";
import { vi } from "vitest";

function buildMessage(overrides: Partial<Message> = {}): Message {
  return {
    id: "1",
    role: "assistant",
    content: "Hello world",
    timestamp: new Date(),
    ...overrides,
  };
}

describe("ChatContainer loading indicator", () => {
  test("shows loading panel and steps when loading", () => {
    render(<ChatContainer messages={[buildMessage()]} isLoading />);

    expect(screen.getByText(/Talking to OpenAI/i)).toBeInTheDocument();
    expect(screen.getByText(/Reading your request/i)).toBeInTheDocument();
    expect(screen.getByText(/Drafting the problem/i)).toBeInTheDocument();
    expect(screen.getByText(/Assembling tests/i)).toBeInTheDocument();
    expect(screen.getByText(/Polishing the response/i)).toBeInTheDocument();
  });

  test("progress bar advances over time while loading", () => {
    vi.useFakeTimers();
    const { container } = render(
      <ChatContainer messages={[buildMessage()]} isLoading />,
    );

    const bar = container.querySelector("div[style]");
    expect(bar?.getAttribute("style")).toContain("25%");

    act(() => {
      vi.advanceTimersByTime(1200);
    });
    expect(bar?.getAttribute("style")).toContain("50%");

    vi.useRealTimers();
  });

  test("shows empty-state copy when no messages", () => {
    render(<ChatContainer messages={[]} isLoading={false} />);
    expect(screen.getByText(/start a conversation/i)).toBeInTheDocument();
  });
});
