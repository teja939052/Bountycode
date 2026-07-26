import re
from typing import Dict, Any, List
from app.services.ai import chat_completion, parse_json


class ProfileSync:
    """Import profile data from GitHub and LinkedIn."""

    async def parse_github_profile(self, github_url: str) -> Dict[str, Any]:
        """
        Parse a GitHub profile URL to extract projects and skills.
        Uses GitHub API (free tier: 60 requests/hour).
        """
        # Extract username from URL
        username = self._extract_username(github_url)
        if not username:
            return {"error": "Invalid GitHub URL"}

        # Use GitHub API (no auth needed for public profiles)
        import httpx

        try:
            async with httpx.AsyncClient() as client:
                # Get user info
                user_resp = await client.get(f"https://api.github.com/users/{username}")
                user_data = user_resp.json()

                # Get repos
                repos_resp = await client.get(
                    f"https://api.github.com/users/{username}/repos",
                    params={"sort": "updated", "per_page": 10}
                )
                repos = repos_resp.json()

            # Extract skills from repos
            skills = self._extract_skills_from_repos(repos)

            # Extract project descriptions
            projects = []
            for repo in repos[:5]:
                projects.append({
                    "name": repo.get("name", ""),
                    "description": repo.get("description", ""),
                    "language": repo.get("language", ""),
                    "stars": repo.get("stargazers_count", 0),
                    "url": repo.get("html_url", ""),
                })

            return {
                "username": username,
                "name": user_data.get("name", username),
                "bio": user_data.get("bio", ""),
                "skills": skills,
                "projects": projects,
                "total_repos": user_data.get("public_repos", 0),
                "followers": user_data.get("followers", 0),
            }

        except Exception as e:
            return {"error": f"Failed to fetch GitHub profile: {str(e)}"}

    def _extract_username(self, url: str) -> str:
        """Extract GitHub username from URL."""
        patterns = [
            r'github\.com/([^/]+)/?$',
            r'github\.com/([^/]+)/',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return ""

    def _extract_skills_from_repos(self, repos: List[Dict]) -> List[str]:
        """Extract programming languages and skills from repos."""
        languages = set()
        for repo in repos:
            lang = repo.get("language")
            if lang:
                languages.add(lang.lower())

        # Map languages to skills
        skill_map = {
            "python": ["python", "django", "flask", "fastapi"],
            "javascript": ["javascript", "react", "node.js", "express"],
            "typescript": ["typescript", "react", "angular", "vue"],
            "java": ["java", "spring", "android"],
            "go": ["golang", "microservices"],
            "rust": ["rust", "systems programming"],
            "ruby": ["ruby", "rails"],
            "php": ["php", "laravel"],
            "c++": ["c++", "algorithms", "data structures"],
            "c": ["c", "embedded", "systems"],
        }

        skills = set()
        for lang in languages:
            if lang in skill_map:
                skills.update(skill_map[lang])

        return list(skills)

    async def generate_resume_bullets_from_projects(
        self,
        projects: List[Dict],
        role: str = "Software Engineer",
    ) -> List[Dict[str, Any]]:
        """Generate resume bullet points from GitHub projects."""
        projects_text = "\n".join([
            f"- {p['name']}: {p.get('description', 'No description')} ({p.get('language', 'Unknown')})"
            for p in projects
        ])

        messages = [
            {
                "role": "system",
                "content": "Convert GitHub projects into resume bullet points using the X-Y-Z formula. Return valid JSON.",
            },
            {
                "role": "user",
                "content": f"Generate resume bullets from these projects:\n\n{projects_text}\n\nRole: {role}",
            },
        ]

        response = await chat_completion(messages)
        return parse_json(response)

    async def parse_linkedin_about(self, linkedin_url: str) -> Dict[str, Any]:
        """
        Parse LinkedIn profile (requires authentication in production).
        For now, returns a template for manual input.
        """
        # LinkedIn API requires OAuth - this is a placeholder
        return {
            "message": "LinkedIn import requires authentication",
            "template": {
                "headline": "",
                "summary": "",
                "experience": [],
                "skills": [],
                "education": [],
            },
            "instructions": "Copy-paste your LinkedIn About section for AI optimization",
        }
