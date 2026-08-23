import { useState, useEffect } from "react";
import api from "../services/api";

interface BreakerState {
  is_open: boolean;
  failures: number;
  last_failure_time?: string | null;
}

interface HealthStatus {
  status: string;
  version: string;
  database: string;
  cache: { status: string; stats: Record<string, unknown> };
  circuit_breakers: { ai: BreakerState; compiler: BreakerState };
  memory_mb: number;
  metrics: { services: string[]; failures: Record<string, number>; last_error: Record<string, string> };
  timestamp: string;
}

export default function HealthDashboard() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    const fetchHealth = async () => {
      try {
        const data = await api.getHealth?.() ?? (await fetch("/health").then((r) => r.json()));
        if (!cancelled) {
          setHealth(data);
          setLoading(false);
        }
      } catch (err) {
        if (!cancelled) {
          setError("Failed to fetch health status");
          setLoading(false);
        }
      }
    };
    fetchHealth();
    const interval = setInterval(fetchHealth, 30000);
    return () => { cancelled = true; clearInterval(interval); };
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-pulse text-lg">Loading health dashboard...</div>
      </div>
    );
  }

  if (error || !health) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-red-400 text-lg">{error ?? "No health data available"}</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold text-text-primary mb-6">System Health Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-gray-800 rounded-lg p-4">
          <h2 className="text-sm text-gray-400 mb-1">Status</h2>
          <span className={`text-lg font-semibold ${health.status === "healthy" ? "text-green-400" : "text-yellow-400"}`}>
            {health.status.toUpperCase()}
          </span>
        </div>
        <div className="bg-gray-800 rounded-lg p-4">
          <h2 className="text-sm text-gray-400 mb-1">Version</h2>
          <span className="text-lg font-semibold text-text-primary">{health.version}</span>
        </div>
        <div className="bg-gray-800 rounded-lg p-4">
          <h2 className="text-sm text-gray-400 mb-1">Database</h2>
          <span className={`text-lg font-semibold ${health.database === "connected" ? "text-green-400" : "text-red-400"}`}>
            {health.database}
          </span>
        </div>
        <div className="bg-gray-800 rounded-lg p-4">
          <h2 className="text-sm text-gray-400 mb-1">Cache</h2>
          <span className="text-lg font-semibold text-text-primary">{health.cache.status}</span>
        </div>
        <div className="bg-gray-800 rounded-lg p-4">
          <h2 className="text-sm text-gray-400 mb-1">Memory</h2>
          <span className="text-lg font-semibold text-text-primary">{health.memory_mb.toFixed(1)} MB</span>
        </div>
        <div className="bg-gray-800 rounded-lg p-4">
          <h2 className="text-sm text-gray-400 mb-1">Services</h2>
          <span className="text-lg font-semibold text-text-primary">{health.metrics.services.length}</span>
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg p-4 mb-6">
        <h2 className="text-sm text-gray-400 mb-3">Circuit Breakers</h2>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <h3 className="text-text-primary font-medium mb-1">AI</h3>
            <p className={`text-sm ${health.circuit_breakers.ai.is_open ? "text-red-400" : "text-green-400"}`}>
              {health.circuit_breakers.ai.is_open ? "OPEN" : "CLOSED"}
            </p>
            <p className="text-sm text-gray-500">Failures: {health.circuit_breakers.ai.failures}</p>
          </div>
          <div>
            <h3 className="text-text-primary font-medium mb-1">Compiler</h3>
            <p className={`text-sm ${health.circuit_breakers.compiler.is_open ? "text-red-400" : "text-green-400"}`}>
              {health.circuit_breakers.compiler.is_open ? "OPEN" : "CLOSED"}
            </p>
            <p className="text-sm text-gray-500">Failures: {health.circuit_breakers.compiler.failures}</p>
          </div>
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg p-4">
        <h2 className="text-sm text-gray-400 mb-3">Request Metrics</h2>
        <pre className="text-sm text-gray-300 overflow-auto">
          {JSON.stringify(health.metrics, null, 2)}
        </pre>
      </div>

      <p className="text-xs text-gray-600 mt-4">Last updated: {health.timestamp}</p>
    </div>
  );
}