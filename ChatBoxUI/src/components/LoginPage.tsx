import { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { cn } from "./ui/utils";
import type { LoginCredentials } from "../types/auth";

interface LoginPageProps {
  onSubmit: (values: LoginCredentials) => Promise<void> | void;
  onRegister: (values: LoginCredentials) => Promise<void> | void;
  isSubmitting?: boolean;
  errorMessage?: string;
}

export function LoginPage({
  onSubmit,
  onRegister,
  isSubmitting = false,
  errorMessage,
}: LoginPageProps) {
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [formValues, setFormValues] = useState<LoginCredentials>({
    email: "",
    password: "",
  });

  const handleChange = (field: keyof LoginCredentials) => {
    return (event: React.ChangeEvent<HTMLInputElement>) => {
      setFormValues((prev) => ({ ...prev, [field]: event.target.value }));
    };
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!formValues.email.trim() || !formValues.password.trim()) {
      return;
    }

    const credentials = {
      email: formValues.email.trim(),
      password: formValues.password,
    };

    if (isLoginMode) {
      await onSubmit(credentials);
    } else {
      await onRegister(credentials);
    }
  };

  const toggleMode = () => {
    setIsLoginMode(!isLoginMode);
    setFormValues({ email: "", password: "" });
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4 py-12">
      <div className="w-full max-w-md space-y-6 rounded-3xl border border-border bg-card p-8 shadow-xl">
        <header className="space-y-2 text-center">
          <h1 className="text-2xl font-semibold">
            {isLoginMode ? "Welcome back" : "Create an account"}
          </h1>
          <p className="text-sm text-muted-foreground">
            {isLoginMode
              ? "Sign in to continue practicing your coding skills"
              : "Sign up to start your coding journey"}
          </p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2 text-left">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="you@example.com"
              autoComplete="email"
              value={formValues.email}
              onChange={handleChange("email")}
              required
            />
          </div>

          <div className="space-y-2 text-left">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              placeholder={isLoginMode ? "********" : "At least 8 characters"}
              autoComplete={isLoginMode ? "current-password" : "new-password"}
              value={formValues.password}
              onChange={handleChange("password")}
              required
              minLength={8}
            />
            {!isLoginMode && (
              <p className="text-xs text-muted-foreground">
                Password must be at least 8 characters long
              </p>
            )}
          </div>

          {errorMessage ? (
            <div className="rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">
              {errorMessage}
            </div>
          ) : null}

          <Button
            type="submit"
            className="w-full rounded-full"
            disabled={isSubmitting}
          >
            {isSubmitting
              ? isLoginMode
                ? "Signing in..."
                : "Creating account..."
              : isLoginMode
              ? "Sign in"
              : "Create account"}
          </Button>
        </form>

        <div className="text-center">
          <button
            type="button"
            onClick={toggleMode}
            className="text-sm text-primary hover:underline"
            disabled={isSubmitting}
          >
            {isLoginMode
              ? "Don't have an account? Sign up"
              : "Already have an account? Sign in"}
          </button>
        </div>
      </div>
    </div>
  );
}
