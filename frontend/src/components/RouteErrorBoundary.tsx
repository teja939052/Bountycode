import { Component, type ReactNode, type ErrorInfo } from "react";
import { Link } from "react-router-dom";

interface RouteErrorBoundaryProps {
  children?: ReactNode;
}

interface RouteErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export default class RouteErrorBoundary extends Component<RouteErrorBoundaryProps, RouteErrorBoundaryState> {
  state: RouteErrorBoundaryState = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("Route error:", error, info?.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center px-4">
          <div className="card max-w-md w-full text-center p-8">
            <p className="text-4xl mb-4">⚠️</p>
            <h2 className="text-xl font-bold text-text-primary mb-2">Something went wrong</h2>
            <p className="text-gray-500 text-sm mb-6">{this.state.error?.message || "An unexpected error occurred"}</p>
            <div className="flex gap-3 justify-center">
              <button onClick={() => this.setState({ hasError: false })} className="btn-primary">Try Again</button>
              <Link to="/dashboard" className="btn-secondary">Go to Dashboard</Link>
            </div>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
