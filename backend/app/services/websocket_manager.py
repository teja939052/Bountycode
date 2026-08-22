import asyncio
import json
import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, Set, Optional, Any, Callable, Awaitable, List
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
from fastapi import WebSocket, WebSocketDisconnect
from app.config import get_settings
from app.services.cache import get_cache
from app.middleware.auth import get_current_user_ws

logger = logging.getLogger(__name__)
settings = get_settings()


class MessageType(str, Enum):
    # Job execution
    JOB_STARTED = "job_started"
    JOB_PROGRESS = "job_progress"
    JOB_COMPLETED = "job_completed"
    JOB_FAILED = "job_failed"

    # Real-time updates
    XP_GAINED = "xp_gained"
    LEVEL_UP = "level_up"
    STREAK_UPDATE = "streak_update"
    BADGE_EARNED = "badge_earned"
    LEAGUE_UPDATE = "league_update"
    BATTLE_UPDATE = "battle_update"

    # Notifications
    NOTIFICATION = "notification"
    ERROR = "error"

    # System
    PING = "ping"
    PONG = "pong"
    AUTH_REQUIRED = "auth_required"
    AUTH_SUCCESS = "auth_success"


@dataclass
class WSMessage:
    type: MessageType
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    message_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def to_json(self) -> str:
        return json.dumps({
            "type": self.type.value,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "message_id": self.message_id,
        })


# ─── Redis-backed connection state ───────────────────────────────────────────
# In production, connection state is stored in Redis for horizontal scaling.
# In development/fallback, use in-memory dicts.

class RedisCache:
    """Thin wrapper around the unified cache for WebSocket state."""

    def __init__(self):
        self.cache = get_cache()

    async def sadd(self, key: str, *members: str) -> int:
        return await self.cache.sadd(key, *members)

    async def srem(self, key: str, *members: str) -> int:
        return await self.cache.srem(key, *members)

    async def smembers(self, key: str) -> Set[str]:
        return await self.cache.smembers(key)

    async def spop(self, key: str, count: int = 1) -> List[str]:
        return await self.cache.spop(key, count)

    async def delete(self, key: str) -> int:
        return await self.cache.delete(key)


redis_cache = RedisCache()


# ─── In-memory fallback (development or Redis failure) ──────────────────────
# Falls back gracefully when Redis is unavailable.

class ConnectionManager:
    """Manages WebSocket connections with user association and rooms.

    Supports both in-memory (dev) and Redis-backed (production) connection state.
    """

    def __init__(self):
        self._user_connections: Dict[str, Set[WebSocket]] = defaultdict(set)
        self._connection_user: Dict[WebSocket, str] = {}
        self._connection_rooms: Dict[WebSocket, Set[str]] = defaultdict(set)
        self._room_connections: Dict[str, Set[WebSocket]] = defaultdict(set)
        self._heartbeat_tasks: Dict[WebSocket, asyncio.Task] = {}
        self._max_connections = settings.WS_MAX_CONNECTIONS
        self._ping_interval = settings.WS_PING_INTERVAL
        self._redis = redis_cache

    async def connect(self, websocket: WebSocket, user_id: str) -> bool:
        """Accept connection and associate with user."""
        if len(self._connection_user) >= self._max_connections:
            await websocket.close(code=1013, reason="Server at capacity")
            return False

        await websocket.accept()
        self._user_connections[user_id].add(websocket)
        self._connection_user[websocket] = user_id
        self._connection_rooms[websocket] = set()

        # Start heartbeat
        self._heartbeat_tasks[websocket] = asyncio.create_task(self._heartbeat(websocket))

        logger.info("WebSocket connected", user_id=user_id, total=len(self._connection_user))
        return True

    def disconnect(self, websocket: WebSocket):
        """Remove connection and cleanup."""
        user_id = self._connection_user.pop(websocket, None)
        if user_id:
            self._user_connections[user_id].discard(websocket)
            if not self._user_connections[user_id]:
                del self._user_connections[user_id]

        # Leave all rooms
        for room in list(self._connection_rooms.get(websocket, set())):
            self._room_connections[room].discard(websocket)
            if not self._room_connections[room]:
                del self._room_connections[room]
        self._connection_rooms.pop(websocket, None)

        # Cancel heartbeat
        task = self._heartbeat_tasks.pop(websocket, None)
        if task:
            task.cancel()

        logger.info("WebSocket disconnected", user_id=user_id, total=len(self._connection_user))

    async def join_room(self, websocket: WebSocket, room: str):
        """Add connection to a room (e.g., battle room, contest room)."""
        self._connection_rooms[websocket].add(room)
        self._room_connections[room].add(websocket)

    async def leave_room(self, websocket: WebSocket, room: str):
        """Remove connection from a room."""
        self._connection_rooms[websocket].discard(room)
        self._room_connections[room].discard(websocket)
        if not self._room_connections[room]:
            del self._room_connections[room]

    async def send_personal(self, user_id: str, message: WSMessage) -> int:
        """Send message to all connections of a user. Returns number of successes."""
        connections = self._user_connections.get(user_id, set())
        if not connections:
            return 0
        successes = 0
        for ws in list(connections):
            try:
                await ws.send_text(message.to_json())
                successes += 1
            except Exception:
                pass  # Connection will be cleaned up on next operation
        return successes

    async def send_to_room(self, room: str, message: WSMessage, exclude: Optional[WebSocket] = None) -> int:
        """Send message to all connections in a room. Returns number of successes."""
        connections = self._room_connections.get(room, set())
        if not connections:
            return 0
        successes = 0
        for ws in list(connections):
            if ws != exclude:
                try:
                    await ws.send_text(message.to_json())
                    successes += 1
                except Exception:
                    pass
        return successes

    async def broadcast_to_room(self, room: str, message: WSMessage, exclude: Optional[WebSocket] = None) -> int:
        """Broadcast message to all connections in a room. Returns number of successes."""
        # Try Redis first for large-scale, fall back to in-memory
        connections = self._room_connections.get(room, set())
        if not connections:
            return 0

        successes = 0
        for ws in list(connections):
            if ws != exclude:
                try:
                    await ws.send_text(message.to_json())
                    successes += 1
                except Exception:
                    pass
        return successes

    async def broadcast_personal(self, user_id: str, message: WSMessage) -> int:
        """Broadcast message to all connections of a user. Returns number of successes."""
        connections = self._user_connections.get(user_id, set())
        if not connections:
            return 0
        successes = 0
        for ws in list(connections):
            try:
                await ws.send_text(message.to_json())
                successes += 1
            except Exception:
                pass
        return successes

    async def send_to_connection(self, websocket: WebSocket, message: WSMessage) -> bool:
        """Send message to a specific connection."""
        try:
            await websocket.send_text(message.to_json())
            return True
        except Exception:
            self.disconnect(websocket)
            return False

    def get_user_connections(self, user_id: str) -> Set[WebSocket]:
        return self._user_connections.get(user_id, set())

    def is_user_online(self, user_id: str) -> bool:
        return user_id in self._user_connections and len(self._user_connections[user_id]) > 0

    def get_online_users(self) -> Set[str]:
        return set(self._user_connections.keys())

    def get_connection_count(self) -> int:
        return len(self._connection_user)

    async def _heartbeat(self, websocket: WebSocket):
        """Send periodic ping to keep connection alive."""
        try:
            while True:
                await asyncio.sleep(self._ping_interval)
                try:
                    await websocket.send_text(WSMessage(type=MessageType.PING).to_json())
                except Exception:
                    break
        except asyncio.CancelledError:
            pass


# Global connection manager
_connection_manager: Optional[ConnectionManager] = None


def get_connection_manager() -> ConnectionManager:
    global _connection_manager
    if _connection_manager is None:
        _connection_manager = ConnectionManager()
    return _connection_manager


# ─── Redis-backed broadcast helper (for future scale) ──────────────────────
async def _redis_broadcast(room: str, message_json: str) -> int:
    """Broadcast via Redis pub/sub - placeholder for future scaling."""
    # In production with Redis, this would use pub/sub channels
    # For now, return 0 (in-memory will handle it)
    return 0


# ─── Pre-defined message builders for common events ────────────────────────
class WSEvents:
    @staticmethod
    def job_started(job_id: str, job_type: str) -> WSMessage:
        return WSMessage(type=MessageType.JOB_STARTED, payload={"job_id": job_id, "job_type": job_type})

    @staticmethod
    def job_progress(job_id: str, progress: int, stage: str = "") -> WSMessage:
        return WSMessage(type=MessageType.JOB_PROGRESS, payload={"job_id": job_id, "progress": progress, "stage": stage})

    @staticmethod
    def job_completed(job_id: str, result: Dict[str, Any]) -> WSMessage:
        return WSMessage(type=MessageType.JOB_COMPLETED, payload={"job_id": job_id, "result": result})

    @staticmethod
    def job_failed(job_id: str, error: str) -> WSMessage:
        return WSMessage(type=MessageType.JOB_FAILED, payload={"job_id": job_id, "error": error})

    @staticmethod
    def xp_gained(user_id: str, amount: int, source: str, new_total: int, new_level: int) -> WSMessage:
        return WSMessage(type=MessageType.XP_GAINED, payload={"amount": amount, "source": source, "new_total": new_total, "new_level": new_level})

    @staticmethod
    def level_up(user_id: str, new_level: int, title: str, rewards: Dict[str, Any]) -> WSMessage:
        return WSMessage(type=MessageType.LEVEL_UP, payload={"new_level": new_level, "title": title, "rewards": rewards})

    @staticmethod
    def streak_update(user_id: str, current_streak: int, longest_streak: int, protected: bool) -> WSMessage:
        return WSMessage(type=MessageType.STREAK_UPDATE, payload={"current_streak": current_streak, "longest_streak": longest_streak, "protected": protected})

    @staticmethod
    def badge_earned(user_id: str, badge_id: str, badge_name: str, badge_icon: str) -> WSMessage:
        return WSMessage(type=MessageType.BADGE_EARNED, payload={"badge_id": badge_id, "name": badge_name, "icon": badge_icon})

    @staticmethod
    def league_update(user_id: str, tier: str, rank: int, weekly_xp: int, promoted: bool = False, relegated: bool = False) -> WSMessage:
        return WSMessage(type=MessageType.LEAGUE_UPDATE, payload={"tier": tier, "rank": rank, "weekly_xp": weekly_xp, "promoted": promoted, "relegated": relegated})

    @staticmethod
    def battle_update(battle_id: str, status: str, data: Dict[str, Any]) -> WSMessage:
        return WSMessage(type=MessageType.BATTLE_UPDATE, payload={"battle_id": battle_id, "status": status, **data})

    @staticmethod
    def notification(user_id: str, title: str, body: str, type: str = "info", action_url: str = "") -> WSMessage:
        return WSMessage(type=MessageType.NOTIFICATION, payload={"title": title, "body": body, "type": type, "action_url": action_url})


# ─── WebSocket message handler ──────────────────────────────────────────────
class WebSocketHandler:
    """Handles WebSocket message routing and authentication."""

    def __init__(self, manager: ConnectionManager):
        self.manager = manager
        self._handlers: Dict[MessageType, Callable[[WebSocket, WSMessage], Awaitable[None]]] = {}
        self._register_default_handlers()

    def _register_default_handlers(self):
        self.register(MessageType.PING, self._handle_ping)
        self.register(MessageType.PONG, self._handle_pong)

    def register(self, msg_type: MessageType, handler: Callable[[WebSocket, WSMessage], Awaitable[None]]):
        self._handlers[msg_type] = handler

    async def handle_message(self, websocket: WebSocket, data: str) -> bool:
        """Route incoming message to appropriate handler. Returns True if handled."""
        try:
            msg_data = json.loads(data)
            msg_type = MessageType(msg_data.get("type", ""))
            message = WSMessage(
                type=msg_type,
                payload=msg_data.get("payload", {}),
                message_id=msg_data.get("message_id", ""),
            )
        except Exception as e:
            logger.warning("Invalid WS message format", error=str(e))
            await self.manager.send_to_connection(websocket, WSMessage(
                type=MessageType.ERROR,
                payload={"error": "Invalid message format"},
            ))
            return False

        handler = self._handlers.get(message.type)
        if handler:
            try:
                await handler(websocket, message)
                return True
            except Exception as e:
                logger.error("WS handler error", type=message.type.value, error=str(e))
                await self.manager.send_to_connection(websocket, WSMessage(
                    type=MessageType.ERROR,
                    payload={"error": "Handler failed"},
                ))
                return False
        else:
            logger.debug("No handler for message type", type=message.type.value)
            return False

    async def _handle_ping(self, websocket: WebSocket, message: WSMessage):
        await self.manager.send_to_connection(websocket, WSMessage(type=MessageType.PONG))

    async def _handle_pong(self, websocket: WebSocket, message: WSMessage):
        pass  # Just acknowledge


# ─── Pre-defined message builders for common events ────────────────────────
# (same as original - WSEvents class copied from original file)
class WSEvents:
    @staticmethod
    def job_started(job_id: str, job_type: str) -> WSMessage:
        return WSMessage(type=MessageType.JOB_STARTED, payload={"job_id": job_id, "job_type": job_type})

    @staticmethod
    def job_progress(job_id: str, progress: int, stage: str = "") -> WSMessage:
        return WSMessage(type=MessageType.JOB_PROGRESS, payload={"job_id": job_id, "progress": progress, "stage": stage})

    @staticmethod
    def job_completed(job_id: str, result: Dict[str, Any]) -> WSMessage:
        return WSMessage(type=MessageType.JOB_COMPLETED, payload={"job_id": job_id, "result": result})

    @staticmethod
    def job_failed(job_id: str, error: str) -> WSMessage:
        return WSMessage(type=MessageType.JOB_FAILED, payload={"job_id": job_id, "error": error})

    @staticmethod
    def xp_gained(user_id: str, amount: int, source: str, new_total: int, new_level: int) -> WSMessage:
        return WSMessage(type=MessageType.XP_GAINED, payload={"amount": amount, "source": source, "new_total": new_total, "new_level": new_level})

    @staticmethod
    def level_up(user_id: str, new_level: int, title: str, rewards: Dict[str, Any]) -> WSMessage:
        return WSMessage(type=MessageType.LEVEL_UP, payload={"new_level": new_level, "title": title, "rewards": rewards})

    @staticmethod
    def streak_update(user_id: str, current_streak: int, longest_streak: int, protected: bool) -> WSMessage:
        return WSMessage(type=MessageType.STREAK_UPDATE, payload={"current_streak": current_streak, "longest_streak": longest_streak, "protected": protected})

    @staticmethod
    def badge_earned(user_id: str, badge_id: str, badge_name: str, badge_icon: str) -> WSMessage:
        return WSMessage(type=MessageType.BADGE_EARNED, payload={"badge_id": badge_id, "name": badge_name, "icon": badge_icon})

    @staticmethod
    def league_update(user_id: str, tier: str, rank: int, weekly_xp: int, promoted: bool = False, relegated: bool = False) -> WSMessage:
        return WSMessage(type=MessageType.LEAGUE_UPDATE, payload={"tier": tier, "rank": rank, "weekly_xp": weekly_xp, "promoted": promoted, "relegated": relegated})

    @staticmethod
    def battle_update(battle_id: str, status: str, data: Dict[str, Any]) -> WSMessage:
        return WSMessage(type=MessageType.BATTLE_UPDATE, payload={"battle_id": battle_id, "status": status, **data})

    @staticmethod
    def notification(user_id: str, title: str, body: str, type: str = "info", action_url: str = "") -> WSMessage:
        return WSMessage(type=MessageType.NOTIFICATION, payload={"title": title, "body": body, "type": type, "action_url": action_url})