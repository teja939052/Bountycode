import asyncio
import docker
import tempfile
import os
import json
import time
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from dataclasses import dataclass
from app.config import get_settings
from app.services.request_metrics import metrics as request_metrics
from app.services.structured_logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


@dataclass
class SandboxResult:
    success: bool
    exit_code: int = 1
    stdout: str = ""
    stderr: str = ""
    compile_error: Optional[str] = None
    execution_time: float = 0.0
    memory_usage: int = 0
    error: Optional[str] = None
    language: str = ""
    source: str = "docker_sandbox"


LANGUAGE_CONFIGS = {
    "python": {
        "image": "python:3.11-slim",
        "file_ext": "py",
        "compile_cmd": None,
        "run_cmd": "python {filename}",
    },
    "javascript": {
        "image": "node:20-slim",
        "file_ext": "js",
        "compile_cmd": None,
        "run_cmd": "node {filename}",
    },
    "typescript": {
        "image": "node:20-slim",
        "file_ext": "ts",
        "compile_cmd": "npx tsc {filename} --noEmit --skipLibCheck",
        "run_cmd": "node {filename}".replace(".ts", ".js"),
    },
    "java": {
        "image": "openjdk:17-slim",
        "file_ext": "java",
        "compile_cmd": "javac {filename}",
        "run_cmd": "java {classname}",
    },
    "cpp": {
        "image": "gcc:13",
        "file_ext": "cpp",
        "compile_cmd": "g++ -std=c++17 -O2 -pipe -static -s {filename} -o {output}",
        "run_cmd": "./{output}",
    },
    "c": {
        "image": "gcc:13",
        "file_ext": "c",
        "compile_cmd": "gcc -std=c11 -O2 -pipe -static -s {filename} -o {output}",
        "run_cmd": "./{output}",
    },
    "go": {
        "image": "golang:1.21",
        "file_ext": "go",
        "compile_cmd": None,
        "run_cmd": "go run {filename}",
    },
    "rust": {
        "image": "rust:1.75",
        "file_ext": "rs",
        "compile_cmd": "rustc {filename} -o {output}",
        "run_cmd": "./{output}",
    },
    "ruby": {
        "image": "ruby:3.2-slim",
        "file_ext": "rb",
        "compile_cmd": None,
        "run_cmd": "ruby {filename}",
    },
    "php": {
        "image": "php:8.2-cli",
        "file_ext": "php",
        "compile_cmd": None,
        "run_cmd": "php {filename}",
    },
    "swift": {
        "image": "swift:5.9",
        "file_ext": "swift",
        "compile_cmd": "swiftc {filename} -o {output}",
        "run_cmd": "./{output}",
    },
    "kotlin": {
        "image": "openjdk:17-slim",
        "file_ext": "kt",
        "compile_cmd": "kotlinc {filename} -include-runtime -d {output}.jar",
        "run_cmd": "java -jar {output}.jar",
    },
}


class DockerSandbox:
    """Secure Docker-based code execution sandbox."""

    def __init__(self):
        self._client: Optional[docker.DockerClient] = None
        self._client_lock = asyncio.Lock()
        self._image_cache: Dict[str, bool] = {}

    async def _get_client(self) -> docker.DockerClient:
        if self._client is not None:
            try:
                self._client.ping()
                return self._client
            except Exception:
                self._client = None

        async with self._client_lock:
            if self._client is None:
                self._client = docker.from_env()
        return self._client

    async def _ensure_image(self, image_name: str) -> bool:
        """Pull image if not present locally."""
        if image_name in self._image_cache:
            return True

        client = await self._get_client()
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: client.images.pull(image_name))
            self._image_cache[image_name] = True
            logger.info("Docker image pulled", image=image_name)
            return True
        except Exception as e:
            logger.error("Failed to pull image", image=image_name, error=str(e))
            return False

    async def execute(
        self,
        code: str,
        language: str,
        stdin: str = "",
        timeout: int = 5,
    ) -> SandboxResult:
        """Execute code in Docker sandbox."""
        lang = language.lower()
        if lang not in LANGUAGE_CONFIGS:
            return SandboxResult(
                success=False,
                error=f"Language '{language}' not supported",
                language=language,
            )

        config = LANGUAGE_CONFIGS[lang]
        if not await self._ensure_image(config["image"]):
            return SandboxResult(
                success=False,
                error=f"Failed to prepare execution environment for {language}",
                language=language,
            )

        # Generate unique filenames
        job_id = str(uuid.uuid4())[:8]
        filename = f"main.{config['file_ext']}"
        output_name = f"main_{job_id}"

        # Prepare code file
        with tempfile.TemporaryDirectory() as tmpdir:
            code_path = os.path.join(tmpdir, filename)
            with open(code_path, "w") as f:
                f.write(code)

            # For Java, ensure class name matches filename
            if lang == "java":
                # Extract or enforce class name
                if "public class" not in code:
                    code = f"public class Main {{\n    public static void main(String[] args) {{\n        // Your code here\n    }}\n}}"
                    with open(code_path, "w") as f:
                        f.write(code)

            client = await self._get_client()
            started = time.perf_counter()

            try:
                # Compile if needed
                compile_error = None
                if config["compile_cmd"]:
                    compile_cmd = config["compile_cmd"].format(
                        filename=filename,
                        output=output_name,
                        classname="Main",
                    )
                    compile_result = await self._run_in_container(
                        client=client,
                        image=config["image"],
                        command=f"sh -c '{compile_cmd}'",
                        working_dir="/workspace",
                        volumes={tmpdir: {"bind": "/workspace", "mode": "rw"}},
                        timeout=timeout,
                    )
                    if compile_result["exit_code"] != 0:
                        compile_error = compile_result["stderr"]
                        return SandboxResult(
                            success=False,
                            exit_code=compile_result["exit_code"],
                            stdout=compile_result["stdout"],
                            stderr=compile_result["stderr"],
                            compile_error=compile_error,
                            execution_time=(time.perf_counter() - started) * 1000,
                            language=language,
                        )

                # Run the code
                run_cmd = config["run_cmd"].format(
                    filename=filename,
                    output=output_name,
                    classname="Main",
                )
                run_result = await self._run_in_container(
                    client=client,
                    image=config["image"],
                    command=f"sh -c '{run_cmd}'",
                    working_dir="/workspace",
                    volumes={tmpdir: {"bind": "/workspace", "mode": "rw"}},
                    stdin=stdin,
                    timeout=timeout,
                )

                execution_time = (time.perf_counter() - started) * 1000
                success = run_result["exit_code"] == 0

                return SandboxResult(
                    success=success,
                    exit_code=run_result["exit_code"],
                    stdout=run_result["stdout"].strip(),
                    stderr=run_result["stderr"].strip(),
                    compile_error=compile_error,
                    execution_time=execution_time,
                    memory_usage=run_result.get("memory_usage", 0),
                    language=language,
                )

            except asyncio.TimeoutError:
                return SandboxResult(
                    success=False,
                    error="Execution timed out",
                    execution_time=(time.perf_counter() - started) * 1000,
                    language=language,
                )
            except Exception as e:
                logger.error("Sandbox execution error", error=str(e))
                return SandboxResult(
                    success=False,
                    error=f"Sandbox error: {str(e)}",
                    execution_time=(time.perf_counter() - started) * 1000,
                    language=language,
                )

    async def _run_in_container(
        self,
        client: docker.DockerClient,
        image: str,
        command: str,
        working_dir: str,
        volumes: Dict[str, Dict[str, str]],
        stdin: str = "",
        timeout: int = 5,
    ) -> Dict[str, Any]:
        """Run a command in a container with strict resource limits."""
        loop = asyncio.get_event_loop()

        container_config = {
            "image": image,
            "command": ["sh", "-c", command],
            "working_dir": working_dir,
            "volumes": volumes,
            "stdin_open": bool(stdin),
            "detach": True,
            "cpu_quota": settings.DOCKER_SANDBOX_CPU_QUOTA,
            "cpu_period": 100000,
            "mem_limit": settings.DOCKER_SANDBOX_MEMORY_LIMIT,
            "memswap_limit": settings.DOCKER_SANDBOX_MEMORY_LIMIT,
            "pids_limit": settings.DOCKER_SANDBOX_PIDS_LIMIT,
            "network_disabled": settings.DOCKER_SANDBOX_NETWORK_DISABLED,
            "read_only": settings.DOCKER_SANDBOX_READ_ONLY_ROOTFS,
            "tmpfs": {"/tmp": "noexec,nosuid,size=50m"} if settings.DOCKER_SANDBOX_TMPFS else None,
            "security_opt": ["no-new-privileges"],
            "cap_drop": ["ALL"],
            "user": "1000:1000",  # Non-root user
        }

        # Filter None values
        container_config = {k: v for k, v in container_config.items() if v is not None}

        container = await loop.run_in_executor(None, lambda: client.containers.run(**container_config))

        try:
            # Wait for container to finish with timeout
            def wait_with_stdin():
                if stdin:
                    # Write stdin to container
                    sock = container.attach_socket(params={"stdin": 1, "stdout": 1, "stderr": 1, "stream": 1})
                    sock._sock.send(stdin.encode())
                    sock._sock.shutdown(1)  # SHUT_WR

                result = container.wait(timeout=timeout)
                logs = container.logs(stdout=True, stderr=True).decode("utf-8", errors="replace")
                stdout, stderr = self._split_logs(logs)
                return result, stdout, stderr

            result, stdout, stderr = await asyncio.wait_for(
                loop.run_in_executor(None, wait_with_stdin),
                timeout=timeout + 2,  # Extra buffer for container startup
            )

            exit_code = result.get("StatusCode", 1)
            memory_usage = 0
            try:
                stats = container.stats(stream=False)
                memory_usage = stats.get("memory_stats", {}).get("max_usage", 0)
            except Exception:
                pass

            return {
                "exit_code": exit_code,
                "stdout": stdout,
                "stderr": stderr,
                "memory_usage": memory_usage,
            }

        except asyncio.TimeoutError:
            try:
                container.kill()
            except Exception:
                pass
            raise
        finally:
            try:
                await loop.run_in_executor(None, lambda: container.remove(force=True))
            except Exception:
                pass

    def _split_logs(self, logs: str) -> tuple[str, str]:
        """Split mixed stdout/stderr logs (Docker doesn't separate by default in some configs)."""
        # For simplicity, return all as stdout; stderr will be captured via exit code
        return logs, ""

    async def close(self):
        """Close Docker client."""
        if self._client:
            self._client.close()
            self._client = None


# Global sandbox instance
_docker_sandbox: Optional[DockerSandbox] = None


def get_docker_sandbox() -> DockerSandbox:
    global _docker_sandbox
    if _docker_sandbox is None:
        _docker_sandbox = DockerSandbox()
    return _docker_sandbox