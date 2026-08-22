import { Component, type ReactNode, type ErrorInfo } from "react";
import { Link } from "react-router-dom";
import { AlertTriangle, RefreshCw, ChevronDown, ChevronUp } from "lucide-react";

interface FeatureErrorBoundaryProps {
  children?: ReactNode;
  featureName: string;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface FeatureErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
  detailsOpen: boolean;
}

export default class FeatureErrorBoundary extends Component<
  FeatureErrorBoundaryProps,
  FeatureErrorBoundaryState
> {
  state: FeatureErrorBoundaryState = {
    hasError: false,
    error: null,
    errorInfo: null,
    detailsOpen: false,
  };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error(`[${this.props.featureName}] ErrorBoundary caught:`, error, errorInfo);
    this.setState({ errorInfo });
    if (typeof this.props.onError === "function") {
      try {
        this.props.onError(error, errorInfo);
      } catch {}
    }
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null, detailsOpen: false });
  };

  toggleDetails = () => {
    this.setState((prev) => ({ detailsOpen: !prev.detailsOpen }));
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[50vh] flex items-center justify-center px-4 py-12">
          <div className="max-w-md w-full rounded-2xl border border-red-500/20 bg-red-500/5 backdrop-blur-sm p-6 text-center">
            <div className="w-14 h-14 rounded-2xl bg-red-500/10 flex items-center justify-center mx-auto mb-4">
              <AlertTriangle className="text-red-400" size={28} />
            </div>
            <h2 className="text-lg font-display font-bold text-brand-primary mb-1">
              {this.props.featureName} crashed
            </h2>
            <p className="text-sm text-brand-secondary mb-5">
              Something went wrong in the {this.props.featureName} section.
            </p>

            <div className="flex flex-col gap-2 sm:flex-row sm:justify-center">
              <button
                onClick={this.handleReset}
                className="inline-flex items-center justify-center gap-2 rounded-xl bg-brand-primary px-5 py-2.5 text-sm font-bold text-white hover:bg-brand-primary/80 transition-colors"
              >
                <RefreshCw size={14} />
                Try again
              </button>
              <Link
                to="/dashboard"
                className="inline-flex items-center justify-center gap-2 rounded-xl border border-brand-primary/20 bg-brand-primary/5 px-5 py-2.5 text-sm font-bold text-brand-primary hover:bg-brand-primary/10 transition-colors"
              >
                Go to dashboard
              </Link>
            </div>

            {this.state.error && (
              <div className="mt-5 text-left">
                <button
                  onClick={this.toggleDetails}
                  className="inline-flex items-center gap-1.5 text-[10px] font-mono uppercase tracking-wider text-brand-dim hover:text-brand-secondary transition-colors"
                >
                  {this.state.detailsOpen ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
                  Error details
                </button>
                {this.state.detailsOpen && (
                  <div className="mt-2 rounded-xl border border-red-500/10 bg-red-500/5 p-3 overflow-x-auto">
                    <p className="break-words font-mono text-xs text-red-400 mb-2">
                      {this.state.error.message}
                    </p>
                    {this.state.error.stack && (
                      <pre className="max-h-40 overflow-y-auto whitespace-pre-wrap break-words font-mono text-[10px] leading-tight text-red-400/70">
                        {this.state.error.stack}
                      </pre>
                    )}
                    {this.state.errorInfo?.componentStack && (
                      <pre className="mt-2 max-h-32 overflow-y-auto whitespace-pre-wrap break-words font-mono text-[10px] leading-tight text-red-400/50">
                        {this.state.errorInfo.componentStack}
                      </pre>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
