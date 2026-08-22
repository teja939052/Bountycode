import { useCallback, useEffect, useRef, useState } from "react";

export type BattleLiveStatus = "connecting" | "open" | "closed";

export interface BattleLiveMessage {
  type: string;
  data?: Record<string, unknown>;
}

function buildWsUrl(battleId: string) {
  const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${proto}//${window.location.host}/api/v1/battles/ws?battle_id=${encodeURIComponent(battleId)}`;
}

/**
 * useBattleLive — live opponent feed for 1v1 coding duels.
 *
 * Connects to `/api/v1/battles/ws?battle_id=...` (same-origin so the httpOnly
 * `pp_token` cookie authenticates automatically). Only sanitized metrics are
 * transmitted — opponent progress shows lines-of-code + submit status, never
 * code content. Auto-reconnects with capped exponential backoff and heartbeats
 * with `{"type":"ping"}` -> `{"type":"pong"}`.
 */
export function useBattleLive({
  battleId,
  enabled = true,
  pingIntervalMs = 25_000,
  onMessage,
}: {
  battleId: string | null;
  enabled?: boolean;
  pingIntervalMs?: number;
  onMessage?: (msg: BattleLiveMessage) => void;
}) {
  const [status, setStatus] = useState<BattleLiveStatus>("closed");
  const wsRef = useRef<WebSocket | null>(null);
  const pingRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const reconnectRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const attemptRef = useRef(0);
  const cbRef = useRef(onMessage);
  cbRef.current = onMessage;

  const cleanup = useCallback(() => {
    if (pingRef.current) {
      clearInterval(pingRef.current);
      pingRef.current = null;
    }
    if (reconnectRef.current) {
      clearTimeout(reconnectRef.current);
      reconnectRef.current = null;
    }
    if (wsRef.current) {
      const ws = wsRef.current;
      ws.onopen = ws.onclose = ws.onmessage = ws.onerror = null;
      try {
        ws.close(1000, "cleanup");
      } catch {
        /* noop */
      }
      wsRef.current = null;
    }
  }, []);

  const connect = useCallback(() => {
    if (!enabled || !battleId) return;
    cleanup();
    setStatus("connecting");

    let ws: WebSocket;
    try {
      ws = new WebSocket(buildWsUrl(battleId));
    } catch {
      setStatus("closed");
      return;
    }
    wsRef.current = ws;

    ws.onopen = () => {
      setStatus("open");
      attemptRef.current = 0;
      pingRef.current = setInterval(() => {
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
          wsRef.current.send(JSON.stringify({ type: "ping" }));
        }
      }, pingIntervalMs);
    };

    ws.onmessage = (ev) => {
      let msg: BattleLiveMessage;
      try {
        msg = JSON.parse(ev.data);
      } catch {
        return;
      }
      cbRef.current?.(msg);
    };

    ws.onclose = () => {
      setStatus("closed");
      if (pingRef.current) {
        clearInterval(pingRef.current);
        pingRef.current = null;
      }
      if (enabled && battleId) {
        const delay = Math.min(1000 * 2 ** attemptRef.current, 30_000);
        attemptRef.current += 1;
        reconnectRef.current = setTimeout(connect, delay);
      }
    };
    ws.onerror = () => {
      // onclose fires next; nothing to do here to avoid duplicate reconnects
    };
  }, [enabled, battleId, pingIntervalMs, cleanup]);

  useEffect(() => {
    if (!enabled || !battleId) {
      cleanup();
      setStatus("closed");
      return;
    }
    connect();
    return cleanup;
  }, [enabled, battleId, connect, cleanup]);

  const send = useCallback((payload: Record<string, unknown>) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(payload));
      return true;
    }
    return false;
  }, []);

  return { status, send };
}

export default useBattleLive;
