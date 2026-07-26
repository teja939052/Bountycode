import random
import hashlib
from typing import Dict, Any, List


class AntiPlagiarismEngine:
    """
    Humanize AI-generated content to avoid plagiarism detection.
    Each student gets unique variations.
    """

    # Verb mutations - same meaning, different words
    VERB_MUTATIONS = {
        "Orchestrated": ["Spearheaded", "Architected", "Steered", "Drove the execution of", "Directed"],
        "Optimized": ["Streamlined", "Refactored", "Pruned", "Overhauled", "Fine-tuned"],
        "Increased": ["Boosted", "Elevated", "Scaled", "Amplified", "Expanded"],
        "Reduced": ["Minimized", "Cut", "Decreased", "Trimmed", "Lowered"],
        "Implemented": ["Deployed", "Built", "Constructed", "Established", "Launched"],
        "Developed": ["Engineered", "Crafted", "Designed", "Created", "Constructed"],
        "Managed": ["Oversaw", "Directed", "Supervised", "Administered", "Governed"],
        "Led": ["Headed", "Championed", "Pioneered", "Spearheaded", "Drove"],
        "Created": ["Built", "Established", "Founded", "Instituted", "Designed"],
        "Improved": ["Enhanced", "Refined", "Elevated", "Upgraded", "Advanced"],
        "Generated": ["Produced", "Yielded", "Delivered", "Cultivated", "Formulated"],
        "Achieved": ["Attained", "Accomplished", "Secured", "Realized", "Reached"],
    }

    # Phrase variations
    PHRASE_MUTATIONS = {
        "resulting in": ["leading to", "which resulted in", "producing", "generating"],
        "by doing": ["through", "via", "by means of", "utilizing"],
        "which led to": ["resulting in", "that resulted in", "leading to", "causing"],
        "in order to": ["to", "for the purpose of", "with the goal of"],
        "a total of": ["approximately", "roughly", "over", "more than"],
    }

    # Style profiles for different "writing styles"
    STYLE_PROFILES = {
        "concise": {
            "max_sentence_length": 15,
            "prefer_active_voice": True,
            "use_contractions": False,
        },
        "detailed": {
            "max_sentence_length": 25,
            "prefer_active_voice": True,
            "use_contractions": False,
        },
        "technical": {
            "max_sentence_length": 20,
            "prefer_active_voice": True,
            "use_contractions": False,
            "add_technical_terms": True,
        },
    }

    def __init__(self):
        self.mutation_cache = {}

    def generate_user_seed(self, user_id: str, bullet_text: str) -> int:
        """Generate a consistent seed for each user+bullet combo."""
        content = f"{user_id}:{bullet_text}"
        return int(hashlib.md5(content.encode()).hexdigest()[:8], 16)

    def humanize_bullet(self, bullet: str, user_id: str = None) -> str:
        """
        Mutate AI-generated bullet to be unique per user.
        Prevents institutional plagiarism flags.
        """
        # Use user-specific seed for consistent but unique mutations
        seed = self.generate_user_seed(user_id or "default", bullet)
        rng = random.Random(seed)

        result = bullet

        # Mutate verbs
        for generic, variations in self.VERB_MUTATIONS.items():
            if generic in result:
                # Each user gets a different variation
                mutated = rng.choice(variations)
                result = result.replace(generic, mutated, 1)

        # Mutate phrases
        for generic, variations in self.PHRASE_MUTATIONS.items():
            if generic in result:
                mutated = rng.choice(variations)
                result = result.replace(generic, mutated, 1)

        # Add subtle stylistic variations
        result = self._apply_style_variation(result, rng)

        return result

    def _apply_style_variation(self, text: str, rng: random.Random) -> str:
        """Apply subtle style variations."""
        # Occasionally restructure sentences
        if rng.random() < 0.3:
            # Move prepositional phrases
            text = self._restructure_prepositions(text, rng)

        return text

    def _restructure_prepositions(self, text: str, rng: random.Random) -> str:
        """Move prepositional phrases for variety."""
        import re
        # Find "X by doing Y" patterns and optionally reorder
        pattern = r'(.+?)\s+(by doing|through|via)\s+(.+)'
        match = re.match(pattern, text)
        if match and rng.random() < 0.5:
            main, connector, detail = match.groups()
            return f"{detail.strip()} {connector} {main.strip()}"
        return text

    def humanize_resume(self, resume_text: str, user_id: str = None) -> str:
        """Apply humanization to entire resume."""
        lines = resume_text.split('\n')
        humanized_lines = []

        for line in lines:
            stripped = line.strip()
            if stripped and (stripped.startswith('•') or stripped.startswith('-') or stripped.startswith('▸')):
                # It's a bullet point - humanize it
                bullet_text = stripped.luster('•-▸').strip()
                humanized = self.humanize_bullet(bullet_text, user_id)
                humanized_lines.append(f"• {humanized}")
            else:
                humanized_lines.append(line)

        return '\n'.join(humanized_lines)

    def generate_unique_variations(self, bullet: str, count: int = 3) -> List[str]:
        """Generate multiple unique variations of a bullet."""
        variations = []
        for i in range(count):
            seed = self.generate_user_seed(f"variation_{i}", bullet)
            rng = random.Random(seed)
            result = bullet

            for generic, mutations in self.VERB_MUTATIONS.items():
                if generic in result:
                    result = result.replace(generic, rng.choice(mutations), 1)

            for generic, mutations in self.PHRASE_MUTATIONS.items():
                if generic in result:
                    result = result.replace(generic, rng.choice(mutations), 1)

            variations.append(result)

        return variations

    def check_plagiarism_risk(self, text: str) -> Dict[str, Any]:
        """Check if text looks like generic AI output."""
        ai_indicators = [
            "leveraged", "synergized", "utilized", "facilitated",
            "streamlined", "orchestrated", "spearheaded",
        ]

        indicator_count = sum(1 for word in ai_indicators if word.lower() in text.lower())
        risk_score = min(100, indicator_count * 15)

        return {
            "risk_score": risk_score,
            "risk_level": "high" if risk_score > 60 else "medium" if risk_score > 30 else "low",
            "indicators_found": indicator_count,
            "recommendation": "Run through humanizer" if risk_score > 30 else "Looks good",
        }
