import { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { cn } from "./ui/utils";
import type { LoginCredentials } from "../types/auth";

interface LoginPageProps {
  onSubmit: (values: LoginCredentials) => Promise<void> | void;
  isSubmitting?: boolean;
  errorMessage?: string;
}

export function LoginPage({
  onSubmit,
  isSubmitting = false,
  errorMessage,
}: LoginPageProps) {
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
    await onSubmit({
      email: formValues.email.trim(),
      password: formValues.password,
    });
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4 py-12">
      <div className="w-full max-w-md space-y-6 rounded-3xl border border-border bg-card p-8 shadow-xl">
        <header className="space-y-2 text-center">
          <h1 className="text-2xl font-semibold">Welcome back</h1>
          <p className="text-sm text-muted-foreground">
            Sign in to continue managing your conversations.
          </p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2 text-left">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="you@example.edu"
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
              placeholder="********"
              autoComplete="current-password"
              value={formValues.password}
              onChange={handleChange("password")}
              required
            />
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
            {isSubmitting ? "Signing in..." : "Sign in"}
          </Button>
        </form>

        <div className="space-y-3">
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <span className="h-px flex-1 bg-border" />
            or continue with
            <span className="h-px flex-1 bg-border" />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <OAuthButton provider="Slack" />
            <OAuthButton provider="Discord" />
          </div>
        </div>
      </div>
    </div>
  );
}

function OAuthButton({ provider }: { provider: "Slack" | "Discord" }) {
  return (
    <Button
      type="button"
      variant="outline"
      className={cn("w-full rounded-full")}
      disabled
    >
      {provider}
    </Button>
  );
}
