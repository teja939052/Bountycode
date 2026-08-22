"""Project generator AI functions."""

import logging
from typing import Dict, Any, List
from app.services.ai_core import chat_completion, parse_json

logger = logging.getLogger(__name__)


async def generate_project(
    description: str,
    language: str,
    framework: str = "",
) -> Dict[str, Any]:
    system_prompt = f"""You are an expert full-stack developer and project generator.

Generate a complete project based on the description.
Language: {language}
Framework: {framework or "default for " + language}

The output MUST be valid JSON:
{{
    "project_name": "Project Name",
    "description": "Brief project description",
    "files": [
        {{
            "path": "src/main.py",
            "content": "Full file content..."
        }}
    ],
    "setup_instructions": "How to set up and run the project",
    "dependencies": ["dependency1", "dependency2"],
    "features": ["Feature 1", "Feature 2"]
}}

Generate a complete, runnable project with all necessary files.
Include a README.md, main application code, and configuration files.
Make the project production-ready with proper error handling and logging.

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate a project: {description}"},
    ]

    result = await chat_completion(messages, max_tokens=8000)
    parsed = parse_json(result)

    parsed.setdefault("project_name", "Generated Project")
    parsed.setdefault("description", description)
    parsed.setdefault("files", [])
    parsed.setdefault("setup_instructions", "Run `pip install -r requirements.txt` and then `python main.py`")
    parsed.setdefault("dependencies", [])
    parsed.setdefault("features", [])

    return parsed


async def review_project(files: list) -> Dict[str, Any]:
    files_text = ""
    for f in files:
        files_text += f"--- {f.get('path', 'unknown')} ---\n{f.get('content', '')}\n\n"

    system_prompt = """You are an expert code reviewer. Review the provided project files and give actionable feedback.

Focus on:
1. Code quality and readability
2. Security vulnerabilities
3. Performance issues
4. Best practices and patterns
5. Missing error handling
6. Testing gaps

The output MUST be valid JSON:
{
    "overall_score": 7,
    "strengths": ["Strength 1", "Strength 2"],
    "issues": [
        {"file": "path/to/file", "line": 42, "severity": "high|medium|low", "message": "Issue description", "suggestion": "How to fix it"}
    ],
    "suggestions": ["General suggestion 1", "General suggestion 2"],
    "summary": "Overall assessment paragraph"
}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Review this project:\n\n{files_text[:8000]}"},
    ]

    result = await chat_completion(messages, max_tokens=4000)
    parsed = parse_json(result)

    parsed.setdefault("overall_score", 5)
    parsed.setdefault("strengths", ["Project has a clear structure"])
    parsed.setdefault("issues", [])
    parsed.setdefault("suggestions", ["Add more error handling", "Write unit tests"])
    parsed.setdefault("summary", "The project is functional but has room for improvement.")

    return parsed


async def improve_code(code: str, language: str, aspect: str) -> Dict[str, Any]:
    system_prompt = f"""You are an expert {language} developer. Improve the provided code focusing on: {aspect}.

The output MUST be valid JSON:
{{
    "improved_code": "The improved code...",
    "changes": [
        "Change 1: description"
    ],
    "explanation": "Why these changes improve the code"
}}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Improve this {language} code (focus: {aspect}):\n\n{code}"},
    ]

    result = await chat_completion(messages, max_tokens=4000)
    parsed = parse_json(result)

    parsed.setdefault("improved_code", code)
    parsed.setdefault("changes", ["No significant changes suggested"])
    parsed.setdefault("explanation", "The code is already well-written.")

    return parsed


async def generate_setup_instructions(files: list, language: str) -> str:
    file_names = [f.get("path", "unknown") for f in files]

    system_prompt = f"""You are a technical writer. Generate setup instructions for a {language} project.

Project files: {', '.join(file_names)}

The output MUST be valid JSON:
{{
    "setup_instructions": "Step-by-step setup instructions",
    "dependencies": ["dep1", "dep2"],
    "run_command": "How to run the project",
    "test_command": "How to test the project"
}}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate setup instructions for a {language} project with files: {', '.join(file_names)}"},
    ]

    result = await chat_completion(messages)
    parsed = parse_json(result)

    return parsed.get("setup_instructions", "Run the project using the default command for the language.")