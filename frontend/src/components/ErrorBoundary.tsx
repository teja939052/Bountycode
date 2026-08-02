import { Component, type ReactNode, type ErrorInfo } from "react";
import { AlertTriangle, RefreshCw, Copy } from "lucide-react";
import { trackError } from "../services/errorTracker";

interface ErrorBoundaryProps {
  children?: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export default class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("ErrorBoundary caught:", error, errorInfo);
    try {
      trackError(error, "ErrorBoundary");
    } catch {}
    if (typeof this.props.onError === "function") {
      try {
        this.props.onError(error, errorInfo);
      } catch {}
    }
  }

  copyDetails = () => {
    const text = `${this.state.error?.stack || this.state.error?.message || ""}\n\n${this.state.errorInfo?.componentStack || ""}`;
    try {
      navigator.clipboard.writeText(text);
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
              An unexpected error occurred. The details are below — please copy and share them.
            </p>
            {this.state.error?.message && (              <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-left">
                <p className="break-words font-mono text-xs text-red-700">{this.state.error.message}</p>
                {this.state.error?.stack && (
                  <pre className="mt-2 max-h-48 overflow-y-auto whitespace-pre-wrap break-words font-mono text-[10px] leading-tight text-red-600">
                    {this.state.error.stack}
                  </pre>
                )}
                {this.state.errorInfo?.componentStack && (
                  <pre className="mt-2 max-h-32 overflow-y-auto whitespace-pre-wrap break-words font-mono text-[10px] leading-tight text-red-400">
                    {this.state.errorInfo.componentStack}
                  </pre>
                )}
              </div>
            )}
            <div className="flex flex-col gap-2 sm:flex-row sm:justify-center">
              <button
                onClick={() => {
                  this.setState({ hasError: false, error: null, errorInfo: null });
                  window.location.reload();
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
                Copy Error Details
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
