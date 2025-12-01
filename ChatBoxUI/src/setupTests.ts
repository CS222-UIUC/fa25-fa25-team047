import "@testing-library/jest-dom";
import { vi } from "vitest";

// Provide a default Pyodide mock for tests.
if (!("loadPyodide" in window)) {
  (window as any).loadPyodide = vi.fn(async () => ({
    runPythonAsync: vi.fn(async () => "test output"),
  }));
}
