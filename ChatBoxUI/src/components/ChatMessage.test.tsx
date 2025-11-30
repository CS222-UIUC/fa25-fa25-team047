import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import { ChatMessage } from "./ChatMessage";

function buildMessage() {
  return {
    id: "1",
    role: "assistant" as const,
    content: "challenge",
    timestamp: new Date(),
    challenge: {
      title: "Sample Challenge",
      difficulty: "Easy",
      description: "Do the thing",
      function_signature: "def solve(input): pass",
      starter_code: "def solve(x):\n    return x",
      visible_tests: [
        { description: "visible 1", input_json: "1", expected_json: "1" },
        { description: "visible 2", input_json: "2", expected_json: "2" },
        { description: "visible 3", input_json: "3", expected_json: "3" },
      ],
      hidden_tests: [
        { description: "hidden 1", input_json: "4", expected_json: "4" },
        { description: "hidden 2", input_json: "5", expected_json: "5" },
      ],
    },
  };
}

function mockPyodide({ onRunTests }: { onRunTests?: () => string }) {
  const runPythonAsync = vi.fn(async (code: string) => {
    if (code.includes('"results"')) {
      const results = onRunTests ? onRunTests() : JSON.stringify({ results: [] });
      return results;
    }
    return "stdout from code";
  });
  (window as any).loadPyodide = vi.fn(async () => ({ runPythonAsync }));
  return runPythonAsync;
}

describe("ChatMessage Python sandbox", () => {
  test("renders sandbox and executes code on Submit", async () => {
    const runPythonAsync = mockPyodide({});
    render(<ChatMessage message={buildMessage()} />);

    await waitFor(() => expect(runPythonAsync).toHaveBeenCalled());

    const submit = screen.getByRole("button", { name: /submit/i });
    await userEvent.click(submit);

    await waitFor(() => expect(runPythonAsync).toHaveBeenCalledTimes(2));
    expect(screen.getByText("stdout from code")).toBeInTheDocument();
  });

  test("runs visible tests and shows pass/fail", async () => {
    const runPythonAsync = mockPyodide({
      onRunTests: () =>
        JSON.stringify({
          results: [
            { name: "visible 1", status: "passed", isHidden: false },
            { name: "visible 2", status: "failed", output: "2", expected: "3", isHidden: false },
          ],
        }),
    });
    render(<ChatMessage message={buildMessage()} />);

    const runVisible = await screen.findByRole("button", { name: /run 3 tests/i });
    await userEvent.click(runVisible);

    await waitFor(() => expect(runPythonAsync).toHaveBeenCalledTimes(2));

    expect(screen.getByText("visible 1")).toBeInTheDocument();
    expect(screen.getByText("passed")).toBeInTheDocument();
    expect(screen.getByText("visible 2")).toBeInTheDocument();
    expect(screen.getByText("failed")).toBeInTheDocument();
    expect(screen.getByText(/Expected:/)).toBeInTheDocument();
  });

  test("runs all tests and labels hidden ones", async () => {
    const runPythonAsync = mockPyodide({
      onRunTests: () =>
        JSON.stringify({
          results: [
            { name: "visible 1", status: "passed", isHidden: false },
            { name: "hidden 1", status: "passed", isHidden: true },
          ],
        }),
    });
    render(<ChatMessage message={buildMessage()} />);

    const submitAll = await screen.findByRole("button", { name: /submit all tests/i });
    await userEvent.click(submitAll);

    await waitFor(() => expect(runPythonAsync).toHaveBeenCalledTimes(2));
    expect(screen.getByText(/hidden 1/i)).toHaveTextContent("(hidden)");
  });
});
