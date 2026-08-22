import { useCallback, useEffect, useRef, useState } from "react";

export type WSStatus = "connecting" | "open" | "closed";

const WS_PATH = "/ws";

function buildWsUrl() {
  const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
  const host = window.location.host;
  return `${proto}//${host}${WS_PATH}`;
}

/**
 * useWebSocket — connects to the backend real-time endpoint `/ws`.
 *
 * - Same-origin URL (goes through the Vite proxy in dev) so the httpOnly
 *   `pp_token` cookie is sent automatically — no token in the query string.
 * - Auto-reconnects with capped exponential backoff.
 * - Sends `{"type":"ping"}` every `pingIntervalMs` and expects `{"type":"pong"}`.
 * - Dispatches typed messages to `onMessage`; keeps a `lastMessage` for render.
 */
export function useWebSocket({
  enabled = true,
  pingIntervalMs = 30_000,
  onMessage,
  onOpen,
  onClose,
}: {
  enabled?: boolean;
  pingIntervalMs?: number;
  onMessage?: (msg: { type: string; payload?: unknown; job_id?: string }) => void;
  onOpen?: () => void;
  onClose?: (code?: number) => void;
}) {
  const [status, setStatus] = useState<WSStatus>("connecting");
  const [lastMessage, setLastMessage] = useState<{ type: string; payload?: unknown; job_id?: string } | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const pingTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const reconnectTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const reconnectAttemptRef = useRef(0);
  const callbacksRef = useRef({ onMessage, onOpen, onClose });
  callbacksRef.current = { onMessage, onOpen, onClose };

  const cleanup = useCallback(() => {
    if (pingTimerRef.current) {
      clearInterval(pingTimerRef.current);
      pingTimerRef.current = null;
    }
    if (wsRef.current) {
      const ws = wsRef.current;
      ws.onclose = null;
      ws.onerror = null;
      ws.onmessage = null;
      ws.onopen = null;
      try {
        ws.close(1000, "cleanup");
      } catch {
        /* noop */
      }
      wsRef.current = null;
    }
  }, []);

  const connect = useCallback(() => {
    if (!enabled) return;
    cleanup();
    setStatus("connecting");

    let ws: WebSocket;
    try {
      ws = new WebSocket(buildWsUrl());
    } catch {
      setStatus("closed");
      return;
    }
    wsRef.current = ws;

    ws.onopen = () => {
      setStatus("open");
      reconnectAttemptRef.current = 0;
      callbacksRef.current.onOpen?.();

      // Heartbeat: server expects {"type":"ping"} -> {"type":"pong"}
      pingTimerRef.current = setInterval(() => {
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
          wsRef.current.send(JSON.stringify({ type: "ping" }));
        }
      }, pingIntervalMs);
    };

    ws.onmessage = (ev) => {
      let msg: { type: string; payload?: unknown; job_id?: string };
      try {
        msg = JSON.parse(ev.data);
      } catch {
        return;
      }
      setLastMessage(msg);
      callbacksRef.current.onMessage?.(msg);
    };

    ws.onclose = (ev) => {
      setStatus("closed");
      callbacksRef.current.onClose?.(ev.code);
      if (pingTimerRef.current) {
        clearInterval(pingTimerRef.current);
        pingTimerRef.current = null;
      }
      // Reconnect with capped exponential backoff (1s -> 30s max)
      if (enabled) {
        const delay = Math.min(1000 * 2 ** reconnectAttemptRef.current, 30_000);
        reconnectAttemptRef.current += 1;
        reconnectTimerRef.current = setTimeout(connect, delay);
      }
    };

    ws.onerror = () => {
      // onclose fires next; nothing to do here to avoid duplicate reconnect
    };
  }, [enabled, pingIntervalMs, cleanup]);

  useEffect(() => {
    if (!enabled) {
      cleanup();
      setStatus("closed");
      return;
    }
    connect();
    return () => {
      cleanup();
      if (reconnectTimerRef.current) clearTimeout(reconnectTimerRef.current);
    };
  }, [enabled, connect, cleanup]);

  const send = useCallback(
    (payload: unknown) => {
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(typeof payload === "string" ? payload : JSON.stringify(payload));
        return true;
      }
      return false;
    },
    []
  );

  return { status, lastMessage, send, connect };
}

export default useWebSocket;
