import { Component, type ReactNode, type ErrorInfo } from "react";
import { AlertTriangle, RefreshCw, Copy } from "lucide-react";
import { trackError } from "../services/errorTracker";
import { captureException } from "../observability/sentry";

interface ErrorBoundaryProps {
  children?: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
  errorId: string | null;
}

export default class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null, errorId: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    const errorId = crypto.randomUUID?.() || Math.random().toString(36).slice(2);
    // Development-only console diagnostics — never shown to students
    if (import.meta.env.DEV) {
      console.error("ErrorBoundary caught:", error, errorInfo);
    }
    try {
      trackError(error, "ErrorBoundary");
    } catch {}
    try {
      // Send to Sentry with only the error ID as context (no raw stack/component stack)
      captureException(error, { errorId });
    } catch {}
    this.setState({ errorId });
    if (typeof this.props.onError === "function") {
      try {
        this.props.onError(error, errorInfo);
      } catch {}
    }
  }

  copyDetails = () => {
    // Copy only the safe error reference ID — never raw stack or component stack
    const text = `Error reference: ${this.state.errorId}`;
    try {
      void navigator.clipboard?.writeText(text);
    } catch {}
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="min-h-[60vh] flex items-center justify-center px-4">
          <div className="text-center max-w-md">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <AlertTriangle className="text-red-600" size={32} />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Something went wrong
            </h2>
            <p className="text-gray-600 mb-4">
              An unexpected error occurred. Your work has not been lost — please
              try again or contact support with the error reference below.
            </p>
            {this.state.errorId && (
              <div className="mb-4 rounded-lg border border-amber-200 bg-amber-50 p-3 text-left">
                <p className="font-mono text-xs text-amber-700 break-all">
                  Error reference: {this.state.errorId}
                </p>
              </div>
            )}
            <div className="flex flex-col gap-2 sm:flex-row sm:justify-center">
              <button
                onClick={() => {
                  this.setState({ hasError: false, error: null, errorInfo: null, errorId: null });
                  if (typeof window !== "undefined") {
                    window.location.reload();
                  }
                }}
                className="btn-primary inline-flex items-center justify-center gap-2"
              >
                <RefreshCw size={16} />
                Refresh Page
              </button>
              <button
                onClick={this.copyDetails}
                className="inline-flex items-center justify-center gap-2 rounded-lg border border-gray-300 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
              >
                <Copy size={16} />
                Copy Error ID
              </button>
            </div>
            <p className="mt-4 text-sm text-gray-500">
              Internal diagnostics are never shown to students. Use the error
              reference ID when contacting support.
            </p>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
