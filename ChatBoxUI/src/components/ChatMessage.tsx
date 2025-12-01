import { useEffect, useRef, useState } from "react";

export interface TestCase {
  description: string;
  input_json: string;
  expected_json: string;
}

export interface ChallengePayload {
  title: string;
  difficulty: string;
  description: string;
  function_signature: string;
  starter_code: string;
  visible_tests: TestCase[];
  hidden_tests: TestCase[];
}

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  challenge?: ChallengePayload;
}

interface ChatMessageProps {
  message: Message;
}

interface TestResult {
  name: string;
  status: "passed" | "failed" | "error";
  output?: string;
  expected?: string;
  error?: string;
  isHidden?: boolean;
}

declare global {
  interface Window {
    loadPyodide?: (options?: { indexURL?: string }) => Promise<any>;
  }
}

function PythonSandbox({
  starterCode,
  visibleTests,
  hiddenTests,
}: {
  starterCode?: string;
  visibleTests: TestCase[];
  hiddenTests: TestCase[];
}) {
  const [code, setCode] = useState(
    starterCode || "# Write your Python solution here\n\ndef solution():\n    return \"Hello, sandbox!\"\n"
  );
  const [output, setOutput] = useState("Waiting to run...");
  const [pyodide, setPyodide] = useState<any>(null);
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");
  const [isRunning, setIsRunning] = useState(false);
  const [testResults, setTestResults] = useState<TestResult[]>([]);
  const [isTesting, setIsTesting] = useState<"visible" | "all" | null>(null);
  const codeAreaRef = useRef<HTMLTextAreaElement>(null);
  const [editorHeight, setEditorHeight] = useState(360);

  useEffect(() => {
    let isMounted = true;

    async function loadPyodide() {
      try {
        if (!window.loadPyodide) {
          await new Promise<void>((resolve, reject) => {
            const script = document.createElement("script");
            script.src = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js";
            script.onload = () => resolve();
            script.onerror = () => reject(new Error("Failed to load Pyodide script"));
            document.body.appendChild(script);
          });
        }

        const instance = await window.loadPyodide?.({
          indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/",
        });

        if (isMounted) {
          setPyodide(instance);
          setStatus("ready");
        }
      } catch (err) {
        console.error(err);
        if (isMounted) {
          setStatus("error");
          setOutput("Failed to load Python runtime. Check your network and try again.");
        }
      }
    }

    loadPyodide();
    return () => {
      isMounted = false;
    };
  }, []);

  const runCode = async () => {
    if (!pyodide) return;
    setIsRunning(true);
    setOutput("Running...");
    try {
      const wrapped = `
import sys, io, traceback
_buffer = io.StringIO()
_stdout = sys.stdout
_stderr = sys.stderr
sys.stdout = _buffer
sys.stderr = _buffer
try:
    exec(${JSON.stringify(code)}, {})
except Exception:
    traceback.print_exc()
finally:
    sys.stdout = _stdout
    sys.stderr = _stderr
_buffer.getvalue()
`;
      const result = await pyodide.runPythonAsync(wrapped);
      setOutput((result || "").trim() || "(no output)");
    } catch (err: any) {
      setOutput(`Runtime error: ${err?.message || err}`);
    } finally {
      setIsRunning(false);
    }
  };

  const autoResize = () => {
    const el = codeAreaRef.current;
    if (!el) return;
    el.style.height = "0px";
    const newHeight = Math.min(Math.max(el.scrollHeight, 320), 1000);
    el.style.height = `${newHeight}px`;
    setEditorHeight(newHeight);
  };

  useEffect(() => {
    autoResize();
  }, [code]);

  const runTests = async (mode: "visible" | "all") => {
    if (!pyodide) return;
    const tests = [
      ...visibleTests.map((t) => ({ ...t, is_hidden: false })),
      ...(mode === "all" ? hiddenTests.map((t) => ({ ...t, is_hidden: true })) : []),
    ];
    if (!tests.length) {
      setTestResults([{ name: "No tests available", status: "error", error: "No tests provided." }]);
      return;
    }

    setIsTesting(mode);
    setTestResults([]);

    try {
      const testsPayload = JSON.stringify(tests);
      const pyCode = `
import json, traceback

code_str = ${JSON.stringify(code)}
tests = json.loads(${JSON.stringify(testsPayload)})
results = []

globals_dict = {}
try:
    exec(code_str, globals_dict)
except Exception:
    results.append({"name": "compile", "status": "error", "error": traceback.format_exc(), "isHidden": False})
else:
    solve = globals_dict.get("solve")
    if not callable(solve):
        results.append({"name": "compile", "status": "error", "error": "solve() is not defined", "isHidden": False})
    else:
        for idx, t in enumerate(tests):
            name = t.get("description") or f"Test {idx+1}"
            is_hidden = bool(t.get("is_hidden"))
            try:
                inp = json.loads(t["input_json"])
                expected = json.loads(t["expected_json"])
            except Exception:
                results.append({"name": name, "status": "error", "error": "Invalid test JSON", "isHidden": is_hidden})
                continue
            try:
                out = solve(inp)
                passed = out == expected
                results.append({
                    "name": name,
                    "status": "passed" if passed else "failed",
                    "output": json.dumps(out, ensure_ascii=False),
                    "expected": json.dumps(expected, ensure_ascii=False),
                    "isHidden": is_hidden,
                })
            except Exception:
                results.append({"name": name, "status": "error", "error": traceback.format_exc(), "isHidden": is_hidden})

json.dumps({"results": results})
`;

      const raw = await pyodide.runPythonAsync(pyCode);
      const parsed = JSON.parse(raw);
      setTestResults(parsed.results || []);
    } catch (err: any) {
      setTestResults([
        {
          name: "runner",
          status: "error",
          error: err?.message || String(err),
        },
      ]);
    } finally {
      setIsTesting(null);
    }
  };

  const disabled = status !== "ready" || isRunning;
  const testsDisabled = status !== "ready" || isTesting !== null;
  const statusText =
    status === "loading"
      ? "Loading Python runtime..."
      : status === "error"
        ? "Python runtime failed to load"
        : "Ready to run";

  return (
    <div className="rounded-2xl border border-border bg-card/70 p-4 md:p-6 shadow-sm space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <div className="text-sm font-medium">Python Sandbox</div>
          <div className="text-xs text-muted-foreground">{statusText}</div>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={runCode}
            disabled={disabled}
            className="rounded-lg bg-primary px-3 py-2 text-sm font-medium text-primary-foreground disabled:opacity-50"
          >
            {isRunning ? "Running..." : "Submit"}
          </button>
          <button
            type="button"
            onClick={() => runTests("visible")}
            disabled={testsDisabled}
            className="rounded-lg border border-border px-3 py-2 text-sm font-medium disabled:opacity-50"
          >
            {isTesting === "visible" ? "Running..." : "Run 3 tests"}
          </button>
          <button
            type="button"
            onClick={() => runTests("all")}
            disabled={testsDisabled}
            className="rounded-lg border border-border px-3 py-2 text-sm font-medium disabled:opacity-50"
          >
            {isTesting === "all" ? "Submitting..." : "Submit all tests"}
          </button>
        </div>
      </div>

      <div className="grid gap-3 md:grid-cols-2">
        <textarea
          ref={codeAreaRef}
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className="w-full rounded-xl border border-border bg-background font-mono text-sm p-3 outline-none focus:ring-2 focus:ring-primary"
          spellCheck={false}
        />
        <div
          className="rounded-xl border border-border bg-background p-3 overflow-auto"
          style={{ height: `${editorHeight}px` }}
        >
          <div className="text-xs uppercase tracking-wide text-muted-foreground mb-2">Output</div>
          <pre className="whitespace-pre-wrap text-sm font-mono">{output}</pre>
        </div>
      </div>

      <div className="text-xs text-muted-foreground">
        Code runs fully in-browser via Pyodide. No server round-trips; hidden tests are not executed here.
      </div>

      {testResults.length > 0 && (
        <div className="rounded-xl border border-border bg-background p-3">
          <div className="text-xs uppercase tracking-wide text-muted-foreground mb-2">Test results</div>
          <div className="space-y-2">
            {testResults.map((res, idx) => (
              <div key={idx} className="rounded-lg border border-border p-2">
                <div className="flex items-center justify-between text-sm font-medium">
                  <span>
                    {res.name} {res.isHidden ? "(hidden)" : ""}
                  </span>
                  <span
                    className={
                      res.status === "passed"
                        ? "text-emerald-600"
                        : res.status === "failed"
                          ? "text-red-600"
                          : "text-amber-600"
                    }
                  >
                    {res.status}
                  </span>
                </div>
                {res.status === "failed" && (
                  <div className="mt-1 text-xs text-muted-foreground">
                    <div>Expected: {res.expected}</div>
                    <div>Got: {res.output}</div>
                  </div>
                )}
                {res.status === "error" && (
                  <pre className="mt-1 whitespace-pre-wrap text-xs text-red-600">{res.error}</pre>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function ChallengeCard({ challenge }: { challenge: ChallengePayload }) {
  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-border bg-card/70 p-4 md:p-6 shadow-sm">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <div className="text-sm uppercase tracking-wide text-muted-foreground">
              {challenge.difficulty || "Hard"}
            </div>
            <h3 className="text-xl font-semibold">{challenge.title}</h3>
          </div>
        </div>
        <p className="mt-3 text-sm whitespace-pre-wrap leading-relaxed">{challenge.description}</p>
        <div className="mt-3 rounded-md bg-muted px-3 py-2 text-sm font-mono whitespace-pre-wrap">
          {challenge.function_signature}
        </div>
      </div>

      <PythonSandbox
        starterCode={challenge.starter_code}
        visibleTests={challenge.visible_tests || []}
        hiddenTests={challenge.hidden_tests || []}
      />

      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-2xl border border-border bg-card/70 p-4 shadow-sm">
          <div className="text-sm font-medium">Visible test cases (3)</div>
          <div className="text-xs text-muted-foreground mb-3">Provided by the model.</div>
          <div className="space-y-2">
            {(challenge.visible_tests || []).map((test, idx) => (
              <div key={idx} className="rounded-lg border border-border bg-background p-3">
                <div className="text-sm font-semibold">{test.description || `Test ${idx + 1}`}</div>
                <div className="text-xs text-muted-foreground">Input</div>
                <div className="rounded bg-muted px-2 py-1 font-mono text-xs whitespace-pre-wrap">
                  {test.input_json}
                </div>
                <div className="text-xs text-muted-foreground mt-1">Expected</div>
                <div className="rounded bg-muted px-2 py-1 font-mono text-xs whitespace-pre-wrap">
                  {test.expected_json}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-2xl border border-border bg-card/70 p-4 shadow-sm">
          <div className="text-sm font-medium mb-1">Hidden tests</div>
          <div className="text-xs text-muted-foreground mb-2">15 additional cases generated by the model.</div>
          <div className="text-sm">
            Run your solution in CodeSandbox to validate against hidden cases.
          </div>
        </div>
      </div>
    </div>
  );
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";
  const isChallenge = !!message.challenge;
  const widthClass = isChallenge ? "w-full" : "max-w-[80%]";
  const basePadding = isChallenge ? "p-0" : "px-4 py-3";
  const bgClass = isUser
    ? "bg-primary text-primary-foreground"
    : isChallenge
      ? "bg-transparent"
      : "bg-muted";

  return (
    <div className={`flex w-full ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div className={`${widthClass} rounded-2xl ${basePadding} ${bgClass}`}>
        {isChallenge ? (
          <div className="w-full">
            <ChallengeCard challenge={message.challenge!} />
          </div>
        ) : (
          <div className="whitespace-pre-wrap break-words">{message.content}</div>
        )}
      </div>
    </div>
  );
}

export type { Message };
