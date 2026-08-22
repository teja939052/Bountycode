import asyncio
import logging
from typing import Dict, Any, List, Optional
from app.services.job_queue import JobQueue, Job, JobType, JobStatus, get_job_queue
from app.services.docker_sandbox import get_docker_sandbox, SandboxResult, LANGUAGE_CONFIGS
from app.services.code_executor import CodeExecutionEngine
from app.services.websocket_manager import get_connection_manager, WSEvents, MessageType
from app.services.request_metrics import metrics as request_metrics
from app.services.structured_logging import get_logger
from app.config import get_settings
from datetime import datetime, timezone

logger = get_logger(__name__)
settings = get_settings()


class CodeExecutionWorker:
    """Worker that processes code execution jobs from the queue."""

    def __init__(self, job_queue: JobQueue):
        self.job_queue = job_queue
        self.sandbox = get_docker_sandbox()
        self.engine = CodeExecutionEngine()
        self.ws_manager = get_connection_manager()
        self._running = False

        # Register handlers
        self.job_queue.register_handler(JobType.CODE_EXECUTION, self._handle_code_execution)
        self.job_queue.register_handler(JobType.TEST_CASES, self._handle_test_cases)
        self.job_queue.register_handler(JobType.EXECUTION_TRACE, self._handle_execution_trace)

    async def start(self):
        """Start the worker."""
        self._running = True
        await self.job_queue.start_consuming()
        logger.info("CodeExecutionWorker started")

    async def stop(self):
        """Stop the worker."""
        self._running = False
        await self.job_queue.close()
        await self.sandbox.close()
        await self.engine.close()
        logger.info("CodeExecutionWorker stopped")

    async def _handle_code_execution(self, job: Job) -> Dict[str, Any]:
        """Handle single code execution job."""
        payload = job.payload
        code = payload.get("code", "")
        language = payload.get("language", "python")
        stdin = payload.get("stdin", "")
        timeout = payload.get("timeout", 5)

        # Notify user via WebSocket
        if job.user_id:
            await self.ws_manager.send_personal(job.user_id, WSEvents.job_started(job.id, "code_execution"))
            await self.ws_manager.send_personal(job.user_id, WSEvents.job_progress(job.id, 10, "starting_sandbox"))

        try:
            # Try Docker sandbox first if enabled
            if settings.DOCKER_SANDBOX_ENABLED and language.lower() in LANGUAGE_CONFIGS:
                if job.user_id:
                    await self.ws_manager.send_personal(job.user_id, WSEvents.job_progress(job.id, 30, "running_docker"))
                
                result = await self.sandbox.execute(code, language, stdin, timeout)
                return self._sandbox_result_to_dict(result)

            # Fallback to Piston API
            if job.user_id:
                await self.ws_manager.send_personal(job.user_id, WSEvents.job_progress(job.id, 50, "running_piston"))

            result = await self.engine.execute_code(code, language, stdin, timeout)
            return result

        except Exception as e:
            logger.error("Code execution failed", job_id=job.id, error=str(e))
            return {
                "success": False,
                "error": f"Execution failed: {str(e)}",
                "language": language,
            }

    async def _handle_test_cases(self, job: Job) -> Dict[str, Any]:
        """Handle test case execution job."""
        payload = job.payload
        code = payload.get("code", "")
        language = payload.get("language", "python")
        test_cases = payload.get("test_cases", [])

        if job.user_id:
            await self.ws_manager.send_personal(job.user_id, WSEvents.job_started(job.id, "test_cases"))
            await self.ws_manager.send_personal(job.user_id, WSEvents.job_progress(job.id, 10, "preparing"))

        try:
            total = len(test_cases)
            results = []
            passed_count = 0

            for idx, case in enumerate(test_cases):
                if job.user_id:
                    progress = 10 + int((idx / total) * 80)
                    await self.ws_manager.send_personal(job.user_id, WSEvents.job_progress(
                        job.id, progress, f"running_test_{idx + 1}"
                    ))

                stdin = case.get("input", "")
                expected = case.get("expected", case.get("expected_output", ""))
                is_hidden = case.get("is_hidden", False)

                # Execute single test case
                if settings.DOCKER_SANDBOX_ENABLED and language.lower() in LANGUAGE_CONFIGS:
                    result = await self.sandbox.execute(code, language, stdin, 10)
                    execution = self._sandbox_result_to_dict(result)
                else:
                    execution = await self.engine.execute_code(code, language, stdin, 10)

                passed = False
                actual = ""
                if execution["success"]:
                    actual = self._normalize_text(execution["stdout"])
                    passed = actual == self._normalize_text(expected)
                else:
                    actual = execution.get("error", "Execution failed")

                results.append({
                    "test_case_index": idx + 1,
                    "passed": passed,
                    "is_hidden": is_hidden,
                    "input": stdin if not is_hidden else "[HIDDEN]",
                    "expected": expected if not is_hidden else "[HIDDEN]",
                    "actual": actual if not is_hidden else "[HIDDEN]",
                    "error": execution.get("error") if not execution["success"] else None,
                    "execution_time": execution.get("execution_time", 0),
                })

                if passed:
                    passed_count += 1

            all_passed = passed_count == total
            score = round(passed_count / total * 100, 1) if total > 0 else 0

            result = {
                "success": True,
                "all_passed": all_passed,
                "passed_count": passed_count,
                "total_count": total,
                "score": score,
                "summary": f"{passed_count}/{total} Test Cases Passed",
                "results": results,
            }

            if job.user_id:
                await self.ws_manager.send_personal(job.user_id, WSEvents.job_progress(job.id, 95, "finalizing"))
                await self.ws_manager.send_personal(job.user_id, WSEvents.job_completed(job.id, result))

            return result

        except Exception as e:
            logger.error("Test cases execution failed", job_id=job.id, error=str(e))
            error_result = {
                "success": False,
                "error": f"Test execution failed: {str(e)}",
            }
            if job.user_id:
                await self.ws_manager.send_personal(job.user_id, WSEvents.job_failed(job.id, str(e)))
            return error_result

    async def _handle_execution_trace(self, job: Job) -> Dict[str, Any]:
        """Handle execution trace generation job."""
        payload = job.payload
        code = payload.get("code", "")
        language = payload.get("language", "python")
        stdin = payload.get("stdin", "")

        if job.user_id:
            await self.ws_manager.send_personal(job.user_id, WSEvents.job_started(job.id, "execution_trace"))
            await self.ws_manager.send_personal(job.user_id, WSEvents.job_progress(job.id, 20, "generating_trace"))

        try:
            trace = await self.engine.generate_execution_trace(code, language, stdin)
            
            if job.user_id:
                await self.ws_manager.send_personal(job.user_id, WSEvents.job_completed(job.id, trace))
            
            return trace
        except Exception as e:
            logger.error("Execution trace failed", job_id=job.id, error=str(e))
            error_result = {
                "success": False,
                "error": f"Trace generation failed: {str(e)}",
            }
            if job.user_id:
                await self.ws_manager.send_personal(job.user_id, WSEvents.job_failed(job.id, str(e)))
            return error_result

    def _sandbox_result_to_dict(self, result: SandboxResult) -> Dict[str, Any]:
        return {
            "success": result.success,
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "compile_error": result.compile_error,
            "language": result.language,
            "execution_time": result.execution_time,
            "memory_usage": result.memory_usage,
            "error": result.error,
        }

    @staticmethod
    def _normalize_text(value: str) -> str:
        return "\n".join(line.rstrip() for line in (value or "").strip().splitlines())


# Global worker instance
_worker: Optional[CodeExecutionWorker] = None


async def init_code_execution_worker() -> CodeExecutionWorker:
    """Initialize and start the code execution worker."""
    global _worker
    queue = get_job_queue()
    _worker = CodeExecutionWorker(queue)
    await _worker.start()
    return _worker


async def close_code_execution_worker():
    """Stop the code execution worker."""
    global _worker
    if _worker:
        await _worker.stop()
        _worker = None