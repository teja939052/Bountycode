import asyncio
import json
import uuid
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Callable, Awaitable
from enum import Enum
from dataclasses import dataclass, field, asdict
import aio_pika
from aio_pika import ExchangeType, Message, DeliveryMode
from aio_pika.abc import AbstractRobustConnection, AbstractChannel, AbstractQueue, AbstractExchange
from app.config import get_settings
from app.services.request_metrics import metrics as request_metrics
from app.services.structured_logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


class JobStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class JobType(str, Enum):
    CODE_EXECUTION = "code_execution"
    TEST_CASES = "test_cases"
    EXECUTION_TRACE = "execution_trace"


@dataclass
class Job:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: JobType = JobType.CODE_EXECUTION
    status: JobStatus = JobStatus.PENDING
    payload: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    user_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    priority: int = 0


@dataclass
class WorkerConfig:
    queue_name: str = settings.RABBITMQ_EXECUTION_QUEUE
    result_exchange: str = settings.RABBITMQ_RESULT_EXCHANGE
    concurrency: int = settings.RABBITMQ_WORKER_CONCURRENCY
    prefetch_count: int = settings.RABBITMQ_PREFETCH_COUNT
    connection_url: str = settings.RABBITMQ_URL


class JobQueue:
    """Async job queue using RabbitMQ for code execution."""

    def __init__(self, config: Optional[WorkerConfig] = None):
        self.config = config or WorkerConfig()
        self._connection: Optional[AbstractRobustConnection] = None
        self._channel: Optional[AbstractChannel] = None
        self._queue: Optional[AbstractQueue] = None
        self._result_exchange: Optional[AbstractExchange] = None
        self._handlers: Dict[JobType, Callable[[Job], Awaitable[Dict[str, Any]]]] = {}
        self._running = False
        self._consumer_tags = []

    async def connect(self):
        """Establish RabbitMQ connection and declare queue/exchange."""
        if self._connection and not self._connection.is_closed:
            return

        self._connection = await aio_pika.connect_robust(self.config.connection_url)
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=self.config.prefetch_count)

        self._queue = await self._channel.declare_queue(
            self.config.queue_name,
            durable=True,
            arguments={
                "x-max-priority": 10,
                "x-message-ttl": 300000,  # 5 min TTL
            }
        )

        self._result_exchange = await self._channel.declare_exchange(
            self.config.result_exchange,
            ExchangeType.TOPIC,
            durable=True,
        )

        logger.info("JobQueue connected", queue=self.config.queue_name)

    async def close(self):
        """Close RabbitMQ connection."""
        self._running = False
        for tag in self._consumer_tags:
            try:
                await self._channel.cancel(tag)
            except Exception:
                pass
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        logger.info("JobQueue closed")

    def register_handler(self, job_type: JobType, handler: Callable[[Job], Awaitable[Dict[str, Any]]]):
        """Register a handler for a job type."""
        self._handlers[job_type] = handler

    async def enqueue(self, job: Job) -> str:
        """Add a job to the queue."""
        await self.connect()

        job.status = JobStatus.QUEUED
        job.updated_at = datetime.now(timezone.utc)

        message_body = json.dumps({
            "id": job.id,
            "type": job.type.value,
            "payload": job.payload,
            "user_id": job.user_id,
            "priority": job.priority,
            "max_retries": job.max_retries,
            "created_at": job.created_at.isoformat(),
        }).encode()

        message = Message(
            body=message_body,
            delivery_mode=DeliveryMode.PERSISTENT,
            priority=job.priority,
            message_id=job.id,
            timestamp=job.created_at,
            headers={"x-job-type": job.type.value},
        )

        await self._channel.default_exchange.publish(
            message,
            routing_key=self.config.queue_name,
        )

        logger.info("Job enqueued", job_id=job.id, type=job.type.value)
        return job.id

    async def start_consuming(self):
        """Start consuming jobs from the queue."""
        await self.connect()
        self._running = True

        async def process_message(message: aio_pika.abc.AbstractIncomingMessage):
            async with message.process():
                await self._process_message(message)

        consumer_tag = await self._queue.consume(process_message)
        self._consumer_tags.append(consumer_tag)
        logger.info("JobQueue started consuming", queue=self.config.queue_name)

    async def _process_message(self, message: aio_pika.abc.AbstractIncomingMessage):
        try:
            data = json.loads(message.body.decode())
            job = Job(
                id=data["id"],
                type=JobType(data["type"]),
                payload=data["payload"],
                user_id=data.get("user_id"),
                priority=data.get("priority", 0),
                max_retries=data.get("max_retries", 3),
                created_at=datetime.fromisoformat(data["created_at"]),
            )
            job.status = JobStatus.RUNNING
            job.started_at = datetime.now(timezone.utc)
            job.updated_at = job.started_at

            handler = self._handlers.get(job.type)
            if not handler:
                raise ValueError(f"No handler for job type: {job.type}")

            result = await handler(job)
            job.result = result
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.now(timezone.utc)
            job.updated_at = job.completed_at

            await self._publish_result(job)
            await request_metrics.record("job_queue", "success", duration_ms=(
                job.completed_at - job.started_at).total_seconds() * 1000)

        except Exception as e:
            logger.error("Job processing failed", job_id=message.message_id, error=str(e))
            await self._handle_failure(message, e)

    async def _handle_failure(self, message: aio_pika.abc.AbstractIncomingMessage, error: Exception):
        try:
            data = json.loads(message.body.decode())
            retry_count = message.headers.get("x-retry-count", 0) if message.headers else 0
            max_retries = data.get("max_retries", 3)

            if retry_count < max_retries:
                # Requeue with incremented retry count
                new_headers = dict(message.headers or {})
                new_headers["x-retry-count"] = retry_count + 1

                new_message = Message(
                    body=message.body,
                    delivery_mode=DeliveryMode.PERSISTENT,
                    priority=message.priority,
                    message_id=message.message_id,
                    headers=new_headers,
                )

                await self._channel.default_exchange.publish(
                    new_message,
                    routing_key=self.config.queue_name,
                )
                logger.info("Job requeued", job_id=message.message_id, retry=retry_count + 1)
            else:
                # Max retries exceeded - publish failure result
                job = Job(
                    id=data["id"],
                    type=JobType(data["type"]),
                    payload=data["payload"],
                    user_id=data.get("user_id"),
                    status=JobStatus.FAILED,
                    error=str(error),
                    retry_count=retry_count,
                    completed_at=datetime.now(timezone.utc),
                )
                await self._publish_result(job)
                await request_metrics.record("job_queue", "failure", error=str(error))
        except Exception as e:
            logger.error("Failure handling failed", error=str(e))

    async def _publish_result(self, job: Job):
        """Publish job result to result exchange."""
        if not self._result_exchange:
            return

        result_data = {
            "job_id": job.id,
            "type": job.type.value,
            "status": job.status.value,
            "result": job.result,
            "error": job.error,
            "user_id": job.user_id,
            "created_at": job.created_at.isoformat(),
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "duration_ms": (
                (job.completed_at - job.started_at).total_seconds() * 1000
                if job.started_at and job.completed_at else None
            ),
        }

        message = Message(
            body=json.dumps(result_data).encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
            message_id=f"result-{job.id}",
            headers={"x-job-id": job.id, "x-job-type": job.type.value},
        )

        await self._result_exchange.publish(
            message,
            routing_key=f"result.{job.type.value}.{job.status.value}",
        )


# Global job queue instance
_job_queue: Optional[JobQueue] = None


def get_job_queue() -> JobQueue:
    global _job_queue
    if _job_queue is None:
        _job_queue = JobQueue()
    return _job_queue


async def init_job_queue():
    """Initialize job queue on startup."""
    queue = get_job_queue()
    await queue.connect()
    return queue


async def close_job_queue():
    """Close job queue on shutdown."""
    global _job_queue
    if _job_queue:
        await _job_queue.close()
        _job_queue = None