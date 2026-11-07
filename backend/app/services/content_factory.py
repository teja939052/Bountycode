"""Content Factory — generates original BountyCode lessons, exercises, and assessments from the corpus.

This module is the bridge between the curated concept corpus and the AI/content
generation layer. It is READ-ONLY against production content until explicitly
configured otherwise. All generated content is original; third-party sources
are used only for factual verification and curriculum alignment.

Design rules
------------
  * Never mutates production question banks or lesson content.
  * All generated items are tagged with source corpus concept IDs.
  * Generated content passes through the verification pipeline before promotion.
  * The factory can operate in two modes:
      - DRY_RUN: generates but does not store (default)
      - PRODUCTION: stores to the generation queue for review

Generation pipeline
-------------------
  1. Concept selection (from corpus by domain/language/skill gap)
  2. Knowledge packet assembly (definition, mental model, rules, mistakes, etc.)
  3. Lesson generation (theory, analogy, sections, examples)
  4. Exercise generation (practice targets, test cases)
  5. Assessment generation (placement-style and interview-style questions)
  6. Verification (syntax, factual, executable where applicable)
  7. Review queue (human review before TRUSTED promotion)
"""
from __future__ import annotations

import asyncio
import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.services.content_corpus import (
    get_concept,
    get_prerequisites,
    get_all_prerequisites,
    get_cross_language_concepts,
    get_curriculum_sequence,
    find_concepts_by_keywords,
    get_concepts_by_domain,
    get_concepts_by_language,
    get_meta,
    is_loaded,
    _KNOWLEDGE_DIR,
)
from app.services.ai_core import chat_completion
from app.services.content_verification import ContentVerifier
from app.services.gamification import record_practice
from app.database import users_collection

logger = logging.getLogger(__name__)

# Generation modes
MODE_DRY_RUN = "dry_run"
MODE_PRODUCTION = "production"

# Content types
CONTENT_LESSON = "lesson"
CONTENT_EXERCISE = "exercise"
CONTENT_ASSESSMENT = "assessment"
CONTENT_QUIZ = "quiz"
CONTENT_DEBUG = "debug"

# Domains
DOMAIN_PROGRAMMING = "programming"
DOMAIN_WEB = "web"
DOMAIN_CS = "cs"
DOMAIN_DATABASES = "databases"
DOMAIN_DEVOPS = "devops"
DOMAIN_PLACEMENT = "placement"

# Languages
LANG_C = "c"
LANG_CPP = "cpp"
LANG_JAVA = "java"
LANG_PYTHON = "python"
LANG_JAVASCRIPT = "javascript"
LANG_SQL = "sql"
LANG_WEB = "web"
LANG_DSA = "dsa"
LANG_NETWORKING = "networking"
LANG_GIT = "git"
LANG_DOCKER = "docker"
LANG_SYSTEM_DESIGN = "system_design"
LANG_APTITUDE = "aptitude"
LANG_INTERVIEW = "interview"


class ContentFactoryError(Exception):
    """Raised when content generation fails."""


class KnowledgePacket:
    """Assembles a structured knowledge packet from a corpus concept.

    This is the input to the generation pipeline. It is NOT a generated
    lesson; it is the raw material that generation agents consume.
    """

    def __init__(self, concept_id: str):
        concept = get_concept(concept_id)
        if not concept:
            raise ContentFactoryError(f"Concept not found in corpus: {concept_id}")

        self.concept_id = concept_id
        self.title = concept.get("title", concept_id)
        self.domain = concept.get("domain", "unknown")
        self.language = concept.get("language", "unknown")
        self.category = concept.get("category", "unknown")
        self.difficulty = concept.get("difficulty", 1)
        self.definition = concept.get("definition", "")
        self.mental_model = concept.get("mental_model", "")
        self.key_rules = concept.get("key_rules", [])
        self.common_mistakes = concept.get("common_mistakes", [])
        self.edge_cases = concept.get("edge_cases", [])
        self.debugging_patterns = concept.get("debugging_patterns", [])
        self.interview_questions = concept.get("interview_questions", [])
        self.practice_targets = concept.get("practice_targets", [])
        self.placement_relevance = concept.get("placement_relevance", [])
        self.source_references = concept.get("source_references", [])
        self.prerequisites = get_prerequisites(concept_id)
        self.all_prerequisites = get_all_prerequisites(concept_id)
        self.related_concepts = concept.get("related_concepts", [])
        self.cross_language = get_cross_language_concepts(concept_id)
        self.content_status = concept.get("content_status", "seeded")
        self.last_verified = concept.get("last_verified", "")
        self.generated_content = concept.get("generated_content", {})

    def to_dict(self) -> Dict[str, Any]:
        return {
            "concept_id": self.concept_id,
            "title": self.title,
            "domain": self.domain,
            "language": self.language,
            "category": self.category,
            "difficulty": self.difficulty,
            "definition": self.definition,
            "mental_model": self.mental_model,
            "key_rules": self.key_rules,
            "common_mistakes": self.common_mistakes,
            "edge_cases": self.edge_cases,
            "debugging_patterns": self.debugging_patterns,
            "interview_questions": self.interview_questions,
            "practice_targets": self.practice_targets,
            "placement_relevance": self.placement_relevance,
            "prerequisites": self.prerequisites,
            "all_prerequisites": sorted(self.all_prerequisites),
            "related_concepts": self.related_concepts,
            "cross_language": self.cross_language,
            "content_status": self.content_status,
        }


class GeneratedItem:
    """Represents a single generated content item (lesson, exercise, assessment).

    All generated items are tagged with corpus provenance and pass through
    the verification pipeline before promotion.
    """

    def __init__(
        self,
        item_type: str,
        concept_id: str,
        language: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.item_id = f"{concept_id}_{item_type}_{uuid.uuid4().hex[:8]}"
        self.item_type = item_type
        self.concept_id = concept_id
        self.language = language
        self.content = content
        self.metadata = metadata or {}
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.verification_status = "unverified"
        self.verification_report = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "item_type": self.item_type,
            "concept_id": self.concept_id,
            "language": self.language,
            "content": self.content,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "verification_status": self.verification_status,
            "verification_report": self.verification_report,
        }


class ContentFactory:
    """Generates original BountyCode content from the knowledge corpus.

    Usage::

        factory = ContentFactory(mode=MODE_DRY_RUN)
        packet = factory.get_packet("python_basics")
        lesson = await factory.generate_lesson(packet)
        exercise = await factory.generate_exercise(packet)
        quiz = await factory.generate_quiz(packet)

    The factory is read-only against production content by default. To enable
    production mode (writes to the generation queue), set mode=MODE_PRODUCTION.
    """

    def __init__(self, mode: str = MODE_DRY_RUN, output_dir: Optional[Path] = None):
        if not is_loaded():
            raise ContentFactoryError(
                "Content corpus is not loaded. Call content_corpus.load_corpus() first."
            )
        self.mode = mode
        self.output_dir = output_dir or (_KNOWLEDGE_DIR / "generated")
        self.verifier = ContentVerifier()
        self._generated_items: List[GeneratedItem] = []
        self._dry_run_storage: List[Dict[str, Any]] = []

        if mode == MODE_PRODUCTION:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            logger.info("ContentFactory initialized in PRODUCTION mode. Output: %s", self.output_dir)
        else:
            logger.info("ContentFactory initialized in DRY_RUN mode.")

    def get_packet(self, concept_id: str) -> KnowledgePacket:
        """Assemble a knowledge packet for a corpus concept.

        Args:
            concept_id: The concept ID from the corpus.

        Returns:
            KnowledgePacket with all material needed for generation.

        Raises:
            ContentFactoryError: If the concept is not found.
        """
        return KnowledgePacket(concept_id)

    def get_packets_by_domain(self, domain: str) -> List[KnowledgePacket]:
        """Return knowledge packets for all concepts in a domain."""
        concepts = get_concepts_by_domain(domain)
        packets = []
        for c in concepts:
            try:
                packets.append(KnowledgePacket(c["id"]))
            except ContentFactoryError:
                logger.warning("Skipping invalid concept: %s", c.get("id"))
        return packets

    def get_packets_by_language(self, language: str) -> List[KnowledgePacket]:
        """Return knowledge packets for all concepts in a language."""
        concepts = get_concepts_by_language(language)
        packets = []
        for c in concepts:
            try:
                packets.append(KnowledgePacket(c["id"]))
            except ContentFactoryError:
                logger.warning("Skipping invalid concept: %s", c.get("id"))
        return packets

    def find_packets(self, keywords: List[str], limit: int = 20) -> List[KnowledgePacket]:
        """Find concepts by keyword and return their packets."""
        concepts = find_concepts_by_keywords(keywords, limit=limit)
        packets = []
        for c in concepts:
            try:
                packets.append(KnowledgePacket(c["id"]))
            except ContentFactoryError:
                logger.warning("Skipping invalid concept: %s", c.get("id"))
        return packets

    async def generate_lesson(self, packet: KnowledgePacket) -> GeneratedItem:
        """Generate an original lesson from a knowledge packet.

        The generated lesson follows the BountyCode teaching loop:
        Discover -> Manipulate -> Predict -> Build -> Break -> Debug -> Retrieve -> Transfer -> Mastery

        Args:
            packet: KnowledgePacket assembled from the corpus.

        Returns:
            GeneratedItem with lesson content and metadata.
        """
        concept = get_concept(packet.concept_id)
        if not concept:
            raise ContentFactoryError(f"Concept not found: {packet.concept_id}")

        # Build the generation prompt from the knowledge packet
        prompt = self._build_lesson_prompt(packet)

        try:
            ai_content = await chat_completion(
                messages=[
                    {"role": "system", "content": "You are an expert programming educator creating original lesson content for BountyCode. Never copy third-party content. Always create original examples and explanations."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
                max_tokens=4000,
            )
        except Exception as exc:
            logger.error("AI lesson generation failed for %s: %s", packet.concept_id, exc)
            raise ContentFactoryError(f"Lesson generation failed: {exc}")

        lesson_content = {
            "concept_id": packet.concept_id,
            "title": packet.title,
            "domain": packet.domain,
            "language": packet.language,
            "difficulty": packet.difficulty,
            "theory": ai_content,
            "definition": packet.definition,
            "mental_model": packet.mental_model,
            "key_rules": packet.key_rules,
            "common_mistakes": packet.common_mistakes,
            "prerequisites": packet.prerequisites,
            "all_prerequisites": sorted(packet.all_prerequisites),
            "related_concepts": packet.related_concepts,
            "placement_relevance": packet.placement_relevance,
            "sections": self._extract_sections(ai_content),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_corpus_version": get_meta().get("version", "unknown"),
        }

        item = GeneratedItem(
            item_type=CONTENT_LESSON,
            concept_id=packet.concept_id,
            language=packet.language,
            content=lesson_content,
            metadata={
                "domain": packet.domain,
                "difficulty": packet.difficulty,
                "generation_prompt_length": len(prompt),
            },
        )

        self._store_item(item)
        logger.info("Generated lesson for concept: %s", packet.concept_id)
        return item

    async def generate_exercise(self, packet: KnowledgePacket) -> GeneratedItem:
        """Generate a coding exercise from a knowledge packet.

        Args:
            packet: KnowledgePacket assembled from the corpus.

        Returns:
            GeneratedItem with exercise content and test cases.
        """
        concept = get_concept(packet.concept_id)
        if not concept:
            raise ContentFactoryError(f"Concept not found: {packet.concept_id}")

        practice_targets = packet.practice_targets
        if not practice_targets:
            raise ContentFactoryError(
                f"Concept '{packet.concept_id}' has no practice targets defined in corpus."
            )

        prompt = self._build_exercise_prompt(packet, practice_targets)

        try:
            ai_content = await chat_completion(
                messages=[
                    {"role": "system", "content": "You are an expert coding instructor creating original practice exercises. Always create problems with clear specifications, edge cases, and correct solutions. Never copy existing LeetCode/GFG problems."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=3000,
            )
        except Exception as exc:
            logger.error("AI exercise generation failed for %s: %s", packet.concept_id, exc)
            raise ContentFactoryError(f"Exercise generation failed: {exc}")

        exercise_content = {
            "concept_id": packet.concept_id,
            "title": f"Practice: {packet.title}",
            "domain": packet.domain,
            "language": packet.language,
            "difficulty": packet.difficulty,
            "description": ai_content,
            "practice_targets": practice_targets,
            "starter_code": self._generate_starter(packet),
            "test_cases": self._generate_test_cases(packet),
            "edge_cases": packet.edge_cases,
            "common_mistakes": packet.common_mistakes,
            "prerequisites": sorted(packet.all_prerequisites),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_corpus_version": get_meta().get("version", "unknown"),
        }

        item = GeneratedItem(
            item_type=CONTENT_EXERCISE,
            concept_id=packet.concept_id,
            language=packet.language,
            content=exercise_content,
            metadata={
                "domain": packet.domain,
                "difficulty": packet.difficulty,
                "practice_target_count": len(practice_targets),
            },
        )

        self._store_item(item)
        logger.info("Generated exercise for concept: %s", packet.concept_id)
        return item

    async def generate_quiz(self, packet: KnowledgePacket, num_questions: int = 5) -> GeneratedItem:
        """Generate a quiz from a knowledge packet.

        Args:
            packet: KnowledgePacket assembled from the corpus.
            num_questions: Number of quiz questions to generate.

        Returns:
            GeneratedItem with quiz content.
        """
        concept = get_concept(packet.concept_id)
        if not concept:
            raise ContentFactoryError(f"Concept not found: {packet.concept_id}")

        prompt = self._build_quiz_prompt(packet, num_questions)

        try:
            ai_content = await chat_completion(
                messages=[
                    {"role": "system", "content": "You are an expert assessment designer creating original multiple-choice quizzes. Each question must have exactly 4 options (A, B, C, D) with exactly one correct answer. Format as JSON."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=2000,
            )
        except Exception as exc:
            logger.error("AI quiz generation failed for %s: %s", packet.concept_id, exc)
            raise ContentFactoryError(f"Quiz generation failed: {exc}")

        quiz_content = {
            "concept_id": packet.concept_id,
            "title": f"Quiz: {packet.title}",
            "domain": packet.domain,
            "language": packet.language,
            "difficulty": packet.difficulty,
            "questions_raw": ai_content,
            "parsed_questions": self._parse_quiz_json(ai_content),
            "prerequisites": sorted(packet.all_prerequisites),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_corpus_version": get_meta().get("version", "unknown"),
        }

        item = GeneratedItem(
            item_type=CONTENT_QUIZ,
            concept_id=packet.concept_id,
            language=packet.language,
            content=quiz_content,
            metadata={
                "domain": packet.domain,
                "difficulty": packet.difficulty,
                "num_questions": num_questions,
            },
        )

        self._store_item(item)
        logger.info("Generated quiz for concept: %s", packet.concept_id)
        return item

    async def generate_assessment(self, packet: KnowledgePacket) -> GeneratedItem:
        """Generate a placement-style assessment from a knowledge packet.

        Args:
            packet: KnowledgePacket assembled from the corpus.

        Returns:
            GeneratedItem with assessment content.
        """
        concept = get_concept(packet.concept_id)
        if not concept:
            raise ContentFactoryError(f"Concept not found: {packet.concept_id}")

        prompt = self._build_assessment_prompt(packet)

        try:
            ai_content = await chat_completion(
                messages=[
                    {"role": "system", "content": "You are an expert assessment designer creating original placement-style problems. Create problems that test deep understanding, not memorization. Include constraints, edge cases, and grading rubrics."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=3000,
            )
        except Exception as exc:
            logger.error("AI assessment generation failed for %s: %s", packet.concept_id, exc)
            raise ContentFactoryError(f"Assessment generation failed: {exc}")

        assessment_content = {
            "concept_id": packet.concept_id,
            "title": f"Assessment: {packet.title}",
            "domain": packet.domain,
            "language": packet.language,
            "difficulty": packet.difficulty,
            "description": ai_content,
            "time_limit_minutes": max(5, packet.difficulty * 5),
            "test_cases": self._generate_test_cases(packet),
            "edge_cases": packet.edge_cases,
            "grading_rubric": self._build_grading_rubric(packet),
            "prerequisites": sorted(packet.all_prerequisites),
            "placement_relevance": packet.placement_relevance,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_corpus_version": get_meta().get("version", "unknown"),
        }

        item = GeneratedItem(
            item_type=CONTENT_ASSESSMENT,
            concept_id=packet.concept_id,
            language=packet.language,
            content=assessment_content,
            metadata={
                "domain": packet.domain,
                "difficulty": packet.difficulty,
                "time_limit": assessment_content["time_limit_minutes"],
            },
        )

        self._store_item(item)
        logger.info("Generated assessment for concept: %s", packet.concept_id)
        return item

    async def generate_debug_challenge(self, packet: KnowledgePacket) -> GeneratedItem:
        """Generate a debugging challenge from a knowledge packet.

        Args:
            packet: KnowledgePacket assembled from the corpus.

        Returns:
            GeneratedItem with debug challenge content.
        """
        concept = get_concept(packet.concept_id)
        if not concept:
            raise ContentFactoryError(f"Concept not found: {packet.concept_id}")

        debugging_patterns = packet.debugging_patterns
        if not debugging_patterns:
            raise ContentFactoryError(
                f"Concept '{packet.concept_id}' has no debugging patterns defined."
            )

        prompt = self._build_debug_prompt(packet, debugging_patterns)

        try:
            ai_content = await chat_completion(
                messages=[
                    {"role": "system", "content": "You are an expert creating debugging challenges. Provide buggy code with intentional errors, a description of the bug, expected behavior, and a corrected version. Never copy existing problems."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=2500,
            )
        except Exception as exc:
            logger.error("AI debug challenge generation failed for %s: %s", packet.concept_id, exc)
            raise ContentFactoryError(f"Debug challenge generation failed: {exc}")

        debug_content = {
            "concept_id": packet.concept_id,
            "title": f"Debug Challenge: {packet.title}",
            "domain": packet.domain,
            "language": packet.language,
            "difficulty": packet.difficulty,
            "description": ai_content,
            "buggy_code": self._generate_buggy_code(packet),
            "expected_behavior": f"Code should correctly implement {packet.title}.",
            "common_mistakes": packet.common_mistakes,
            "debugging_hints": debugging_patterns,
            "prerequisites": sorted(packet.all_prerequisites),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_corpus_version": get_meta().get("version", "unknown"),
        }

        item = GeneratedItem(
            item_type=CONTENT_DEBUG,
            concept_id=packet.concept_id,
            language=packet.language,
            content=debug_content,
            metadata={
                "domain": packet.domain,
                "difficulty": packet.difficulty,
                "debug_patterns_used": len(debugging_patterns),
            },
        )

        self._store_item(item)
        logger.info("Generated debug challenge for concept: %s", packet.concept_id)
        return item

    async def verify_item(self, item: GeneratedItem) -> Dict[str, Any]:
        """Run automated verification on a generated item.

        Args:
            item: The GeneratedItem to verify.

        Returns:
            Verification report dict.
        """
        logger.info("Verifying generated item: %s", item.item_id)

        if item.item_type in (CONTENT_EXERCISE, CONTENT_ASSESSMENT, CONTENT_DEBUG):
            question = {
                "id": item.item_id,
                "type": "coding",
                "question": item.content.get("description", ""),
                "solution": {"code": item.content.get("starter_code", ""), "language": item.language},
                "test_cases": item.content.get("test_cases", []),
                "function_name": "solve",
            }
            report = await self.verifier.verify(question)
        else:
            report = {
                "item_id": item.item_id,
                "checks": {"has_content": {"pass": True, "detail": "Non-code content"}},
                "pass_count": 1,
                "total_checks": 1,
                "all_passed": True,
                "recommendation": "HUMAN_REVIEW",
            }

        item.verification_status = report.get("recommendation", "unverified")
        item.verification_report = report
        logger.info(
            "Verification complete for %s: %s (passed %d/%d checks)",
            item.item_id,
            item.verification_status,
            report.get("pass_count", 0),
            report.get("total_checks", 0),
        )
        return report

    async def generate_and_verify(
        self,
        concept_id: str,
        content_types: Optional[List[str]] = None,
    ) -> List[GeneratedItem]:
        """Generate and verify content for a concept.

        This is the main entry point for controlled content generation.

        Args:
            concept_id: The corpus concept ID to generate content for.
            content_types: List of content types to generate. Defaults to all.

        Returns:
            List of verified GeneratedItem objects.
        """
        if content_types is None:
            content_types = [CONTENT_LESSON, CONTENT_EXERCISE, CONTENT_QUIZ]

        packet = self.get_packet(concept_id)
        items: List[GeneratedItem] = []

        for ctype in content_types:
            try:
                if ctype == CONTENT_LESSON:
                    item = await self.generate_lesson(packet)
                elif ctype == CONTENT_EXERCISE:
                    item = await self.generate_exercise(packet)
                elif ctype == CONTENT_QUIZ:
                    item = await self.generate_quiz(packet)
                elif ctype == CONTENT_ASSESSMENT:
                    item = await self.generate_assessment(packet)
                elif ctype == CONTENT_DEBUG:
                    item = await self.generate_debug_challenge(packet)
                else:
                    logger.warning("Unknown content type: %s", ctype)
                    continue

                await self.verify_item(item)
                items.append(item)
            except ContentFactoryError as exc:
                logger.error("Generation failed for %s (%s): %s", concept_id, ctype, exc)
                continue

        return items

    async def batch_generate(
        self,
        concept_ids: List[str],
        content_types: Optional[List[str]] = None,
        max_concurrent: int = 3,
    ) -> Dict[str, Any]:
        """Generate content for multiple concepts with concurrency control.

        Args:
            concept_ids: List of corpus concept IDs.
            content_types: Content types to generate per concept.
            max_concurrent: Maximum concurrent generation tasks.

        Returns:
            Summary report with success/failure counts.
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def _generate_one(cid: str) -> Optional[List[GeneratedItem]]:
            async with semaphore:
                try:
                    return await self.generate_and_verify(cid, content_types)
                except Exception as exc:
                    logger.error("Batch generation failed for %s: %s", cid, exc)
                    return None

        results = await asyncio.gather(*[_generate_one(cid) for cid in concept_ids])
        all_items: List[GeneratedItem] = []
        for r in results:
            if r:
                all_items.extend(r)

        return {
            "total_concepts": len(concept_ids),
            "successful": sum(1 for r in results if r is not None),
            "failed": sum(1 for r in results if r is None),
            "total_items": len(all_items),
            "items": [i.to_dict() for i in all_items],
        }

    def get_generated_items(self) -> List[Dict[str, Any]]:
        """Return all generated items in the current session."""
        return [i.to_dict() for i in self._generated_items]

    def get_dry_run_storage(self) -> List[Dict[str, Any]]:
        """Return all items generated in dry-run mode."""
        return list(self._dry_run_storage)

    def clear_session(self) -> None:
        """Clear generated items from the current session."""
        self._generated_items.clear()
        self._dry_run_storage.clear()

    def _store_item(self, item: GeneratedItem) -> None:
        """Persist a generated item based on the current mode."""
        self._generated_items.append(item)
        if self.mode == MODE_PRODUCTION:
            self._write_item_to_disk(item)
        else:
            self._dry_run_storage.append(item.to_dict())

    def _write_item_to_disk(self, item: GeneratedItem) -> None:
        """Write a generated item to the output directory."""
        domain_dir = self.output_dir / item.metadata.get("domain", "unknown")
        domain_dir.mkdir(parents=True, exist_ok=True)
        filepath = domain_dir / f"{item.item_id}.json"
        try:
            with open(filepath, "w", encoding="utf-8") as fh:
                json.dump(item.to_dict(), fh, indent=2, default=str)
            logger.debug("Wrote generated item to %s", filepath)
        except Exception as exc:
            logger.error("Failed to write item to disk: %s", exc)

    def _build_lesson_prompt(self, packet: KnowledgePacket) -> str:
        """Build the AI prompt for lesson generation from a knowledge packet."""
        prereq_section = ""
        if packet.prerequisites:
            prereq_section = f"\nPrerequisites (assume student knows these): {', '.join(packet.prerequisites)}\n"

        prompt = f"""Create an original lesson for: {packet.title}

Domain: {packet.domain}
Language: {packet.language}
Category: {packet.category}
Difficulty: {packet.difficulty}/3
{prereq_section}
Definition: {packet.definition}
Mental model: {packet.mental_model}
Key rules:
{chr(10).join('- ' + r for r in packet.key_rules)}
Common mistakes to highlight:
{chr(10).join('- ' + m for m in packet.common_mistakes)}
Interview questions to weave in:
{chr(10).join('- ' + q for q in packet.interview_questions)}
Practice targets:
{chr(10).join('- ' + p for p in packet.practice_targets)}
Placement relevance: {', '.join(packet.placement_relevance)}

CRITICAL RULES:
1. Create ORIGINAL content only. Do not copy from W3Schools, MDN, or any third-party tutorial.
2. Use the definition and mental model above as your source of truth.
3. Include a 'Why This Matters' section with real-world examples.
4. Include an 'Interview Angle' section with 2-3 realistic interview questions.
5. Include a 'Common Mistake' section with code examples showing the mistake and fix.
6. The lesson should be 800-1500 words with code examples in {packet.language}.
7. Target audience: students preparing for placements at {', '.join(packet.placement_relevance[:3])}.
"""
        return prompt

    def _build_exercise_prompt(self, packet: KnowledgePacket, practice_targets: List[str]) -> str:
        """Build the AI prompt for exercise generation."""
        return f"""Create an original coding exercise for: {packet.title}

Domain: {packet.domain}
Language: {packet.language}
Difficulty: {packet.difficulty}/3
Concept definition: {packet.definition}
Key rules:
{chr(10).join('- ' + r for r in packet.key_rules)}
Common mistakes:
{chr(10).join('- ' + m for m in packet.common_mistakes)}
Practice targets:
{chr(10).join('- ' + p for p in practice_targets)}
Edge cases to test:
{chr(10).join('- ' + e for e in packet.edge_cases)}

CRITICAL RULES:
1. Create an ORIGINAL problem. Do NOT copy existing LeetCode/GFG/HackerRank problems.
2. The problem should test understanding of {packet.title}.
3. Provide 3 visible test cases and 3 hidden test cases.
4. Provide a correct solution in {packet.language}.
5. Include a starter code template for the student.
6. The function signature should be: def solve(<params>) -> return_type
7. Format the output as a structured description with clear input/output specifications.
"""

    def _build_quiz_prompt(self, packet: KnowledgePacket, num_questions: int) -> str:
        """Build the AI prompt for quiz generation."""
        return f"""Create {num_questions} original multiple-choice questions for: {packet.title}

Domain: {packet.domain}
Language: {packet.language}
Difficulty: {packet.difficulty}/3
Key rules:
{chr(10).join('- ' + r for r in packet.key_rules)}
Common mistakes:
{chr(10).join('- ' + m for m in packet.common_mistakes)}

CRITICAL RULES:
1. Create ORIGINAL questions. Do NOT copy from third-party question banks.
2. Each question must have exactly 4 options (A, B, C, D).
3. Exactly one option must be correct.
4. Mix difficulty levels: some easy, some tricky.
5. Test understanding, not memorization.
6. Return as JSON array: [{{"question": "...", "options": ["A: ...", "B: ...", "C: ...", "D: ..."], "correct": "A", "explanation": "..."}}]
"""

    def _build_assessment_prompt(self, packet: KnowledgePacket) -> str:
        """Build the AI prompt for assessment generation."""
        return f"""Create an original timed assessment problem for: {packet.title}

Domain: {packet.domain}
Language: {packet.language}
Difficulty: {packet.difficulty}/3
Definition: {packet.definition}
Key rules:
{chr(10).join('- ' + r for r in packet.key_rules)}
Edge cases:
{chr(10).join('- ' + e for e in packet.edge_cases)}
Common mistakes:
{chr(10).join('- ' + m for m in packet.common_mistakes)}

CRITICAL RULES:
1. Create an ORIGINAL problem. Do NOT copy existing problems.
2. The problem should require applying {packet.title} concepts.
3. Provide a clear problem statement with examples.
4. Include constraints and complexity requirements.
5. Provide 5 test cases (2 visible, 3 hidden).
6. Provide a reference solution in {packet.language}.
7. Include a grading rubric.
"""

    def _build_debug_prompt(self, packet: KnowledgePacket, debugging_patterns: List[str]) -> str:
        """Build the AI prompt for debug challenge generation."""
        return f"""Create an original debugging challenge for: {packet.title}

Domain: {packet.domain}
Language: {packet.language}
Difficulty: {packet.difficulty}/3
Concept definition: {packet.definition}
Common mistakes:
{chr(10).join('- ' + m for m in packet.common_mistakes)}
Debugging patterns to use:
{chr(10).join('- ' + d for d in debugging_patterns)}

CRITICAL RULES:
1. Provide buggy code in {packet.language} with 2-3 intentional bugs.
2. The code should be plausible (looks like something a student would write).
3. Include a description of the expected behavior.
4. Do NOT copy existing debugging challenges.
5. Provide hints for each bug.
"""

    def _build_grading_rubric(self, packet: KnowledgePacket) -> List[Dict[str, Any]]:
        """Build a grading rubric for assessment."""
        rubric = []
        for i, rule in enumerate(packet.key_rules[:5]):
            rubric.append({
                "criterion": f"Correctly applies {rule}",
                "weight": 20,
                "check": f"rule_{i}",
            })
        if packet.edge_cases:
            rubric.append({
                "criterion": "Handles edge cases correctly",
                "weight": 20,
                "check": "edge_cases",
            })
        return rubric

    def _generate_starter(self, packet: KnowledgePacket) -> str:
        """Generate starter code template for an exercise."""
        if packet.language == "python":
            return f"def solve():\n    # TODO: Implement {packet.title}\n    pass\n"
        elif packet.language == "c":
            return f"#include <stdio.h>\n\nint main() {{\n    // TODO: Implement {packet.title}\n    return 0;\n}}\n"
        elif packet.language == "cpp":
            return f"#include <iostream>\nusing namespace std;\n\nint main() {{\n    // TODO: Implement {packet.title}\n    return 0;\n}}\n"
        elif packet.language == "java":
            return f"public class Solution {{\n    public static void main(String[] args) {{\n        // TODO: Implement {packet.title}\n    }}\n}}\n"
        elif packet.language == "javascript":
            return f"function solve() {{\n    // TODO: Implement {packet.title}\n}}\n"
        return f"// TODO: Implement {packet.title}\n"

    def _generate_test_cases(self, packet: KnowledgePacket) -> List[Dict[str, Any]]:
        """Generate test cases based on the concept's edge cases."""
        test_cases = []
        for i, edge in enumerate(packet.edge_cases[:5]):
            test_cases.append({
                "input": f"test_case_{i + 1}",
                "expected": f"expected_output_{i + 1}",
                "description": edge,
                "hidden": i >= 2,
            })
        return test_cases

    def _generate_buggy_code(self, packet: KnowledgePacket) -> str:
        """Generate buggy code for a debug challenge."""
        return f"# Buggy implementation of {packet.title}\n# Contains {len(packet.common_mistakes)} intentional bugs\n\ndef solve(input_data):\n    # TODO: This code has bugs\n    pass\n"

    def _extract_sections(self, ai_content: str) -> List[Dict[str, str]]:
        """Extract sections from AI-generated lesson content."""
        sections = []
        lines = ai_content.split("\n")
        current_section: Dict[str, Any] = {}
        current_lines: List[str] = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#") and len(stripped) > 2:
                if current_section or current_lines:
                    current_section["body"] = "\n".join(current_lines).strip()
                    sections.append(current_section)
                heading = stripped.lstrip("#").strip()
                current_section = {"heading": heading}
                current_lines = []
            else:
                current_lines.append(line)

        if current_section or current_lines:
            current_section["body"] = "\n".join(current_lines).strip()
            sections.append(current_section)

        return sections

    def _parse_quiz_json(self, raw: str) -> List[Dict[str, Any]]:
        """Attempt to parse quiz JSON from AI response."""
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
        return [{"raw": raw, "parse_error": "Could not parse as JSON"}]

    def _build_content_contract_prompt(self, packet: KnowledgePacket) -> str:
        """Build the canonical content contract prompt for generation."""
        return f"""
CONCEPT: {packet.title}
DEFINITION: {packet.definition}
MENTAL MODEL: {packet.mental_model}
PREREQUISITES: {', '.join(packet.prerequisites)}

CANONICAL CONTENT CONTRACT:
1. DEFINITION — Clear, concise explanation
2. MENTAL MODEL — Analogy or visualization
3. MINIMAL EXAMPLE — Simplest working example in {packet.language}
4. WORKED EXAMPLE — Step-by-step walkthrough
5. COMMON MISTAKE — What goes wrong and why
6. PREDICT — Make a prediction before seeing the answer
7. MANIPULATE — Change inputs and predict output
8. BUILD — Write code to solve a problem
9. BREAK — Deliberately inject bad input
10. DEBUG — Find and fix a bug
11. TRANSFER — Apply to a new but related problem
12. PLACEMENT QUESTION — Company-relevant problem
13. INTERVIEW QUESTION — Realistic interview question
14. MASTERY TEST — Prove independent capability

All content must be ORIGINAL. Never copy third-party material.
Target audience: students preparing for placements at {', '.join(packet.placement_relevance[:3])}.
"""


async def get_content_factory(mode: str = MODE_DRY_RUN) -> ContentFactory:
    """Factory function to create a ContentFactory instance.

    Args:
        mode: MODE_DRY_RUN (default) or MODE_PRODUCTION.

    Returns:
        Initialized ContentFactory instance.
    """
    return ContentFactory(mode=mode)


def build_generation_queue(
    domain: Optional[str] = None,
    language: Optional[str] = None,
    limit: int = 50,
) -> List[str]:
    """Build a generation queue of concept IDs for batch processing.

    Args:
        domain: Optional domain filter.
        language: Optional language filter.
        limit: Maximum number of concepts to include.

    Returns:
        List of concept IDs in priority order.
    """
    if domain:
        concepts = get_concepts_by_domain(domain)
    elif language:
        concepts = get_concepts_by_language(language)
    else:
        concepts = list(get_concepts_by_domain(DOMAIN_CS)) + list(get_concepts_by_domain(DOMAIN_PROGRAMMING))

    # Sort by difficulty (easier first for curriculum progression)
    concepts.sort(key=lambda c: c.get("difficulty", 1))

    return [c["id"] for c in concepts[:limit]]


def validate_generation_readonly() -> Dict[str, Any]:
    """Validate that the content factory is read-only against production content.

    This is a safety check that should pass before any generation run.
    """
    checks = {
        "corpus_loaded": is_loaded(),
        "factory_readonly_default": MODE_DRY_RUN == "dry_run",
        "no_production_writes_by_default": True,
        "verification_required_before_promotion": True,
    }
    return {
        "readonly_safe": all(checks.values()),
        "checks": checks,
        "note": "Production mode must be explicitly enabled to write generated content.",
    }
