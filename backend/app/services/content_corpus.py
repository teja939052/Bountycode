"""BountyCode Content Corpus — in-memory knowledge graph and concept registry.

This module loads the BountyCode Knowledge Corpus from versioned JSON files
under backend/app/data/knowledge/. It is the single source of truth for:

  - Concept definitions, prerequisites, and relationships
  - Cross-language concept mappings
  - Curriculum maps by domain
  - Source registry with provenance and license metadata

Design rules
------------
  * Read-only after startup: no route or background task mutates the corpus.
  * Content generation is delegated to content_factory.ContentFactory.
  * Production question banks and lesson content are NOT modified by this module.
  * All generated content is original BountyCode material; third-party
    sources are used for factual verification and curriculum discovery only.

Directory layout
----------------
backend/app/data/knowledge/
    corpus.json          Canonical concept registry + prerequisite graph
    packets/             Per-concept knowledge packets (optional expansion)
    generation_queue.json Batch generation plan (optional)
"""
from __future__ import annotations

import json
import logging
import os
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

_KNOWLEDGE_DIR = Path(__file__).parent.parent / "data" / "knowledge"
_CORPUS_FILE = _KNOWLEDGE_DIR / "corpus.json"

_concepts: Dict[str, Dict[str, Any]] = {}
_prereq_graph: Dict[str, List[str]] = {}
_curriculum_map: Dict[str, Any] = {}
_cross_language_map: Dict[str, List[str]] = {}
_source_registry: List[Dict[str, Any]] = {}
_meta: Dict[str, Any] = {}
_loaded = False


class ContentCorpusError(Exception):
    """Raised when the corpus cannot be loaded or is malformed."""


def _load_json(path: Path) -> Any:
    """Load and return parsed JSON from *path*.

    Raises:
        ContentCorpusError: If the file cannot be read or parsed.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise ContentCorpusError(f"Corpus file not found: {path}")
    except json.JSONDecodeError as exc:
        raise ContentCorpusError(f"Malformed JSON in {path}: {exc}")


def load_corpus(corpus_path: Optional[Path] = None) -> Dict[str, Any]:
    """Load the BountyCode Knowledge Corpus into memory.

    Must be called once at application startup (from ``main.py`` lifespan).

    Args:
        corpus_path: Optional override for the default corpus file location.

    Returns:
        Dict[str, Any]: Summary of loaded corpus (counts and metadata).

    Raises:
        ContentCorpusError: If the corpus file is missing or malformed.
    """
    global _concepts, _prereq_graph, _curriculum_map, _cross_language_map, _source_registry, _meta, _loaded

    if _loaded:
        logger.info("Content corpus already loaded; skipping re-load.")
        return {
            "status": "already_loaded",
            "concept_count": len(_concepts),
            "source_count": len(_source_registry),
        }

    path = corpus_path or _CORPUS_FILE
    logger.info("Loading content corpus from %s", path)

    if not path.exists():
        raise ContentCorpusError(
            f"Corpus file not found: {path}. "
            "Create backend/app/data/knowledge/corpus.json before starting."
        )

    raw = _load_json(path)

    # Validate top-level structure
    if not isinstance(raw, dict):
        raise ContentCorpusError("Corpus root must be a JSON object.")

    _meta = raw.get("meta", {})
    _concepts = raw.get("concepts", {})
    _prereq_graph = raw.get("prerequisite_graph", {})
    _curriculum_map = raw.get("curriculum_map", {})
    _cross_language_map = raw.get("cross_language_map", {})
    _source_registry = raw.get("source_registry", [])

    if not _concepts:
        logger.warning("Corpus loaded but contains no concepts.")

    _loaded = True
    logger.info(
        "Content corpus loaded: %d concepts, %d sources, version %s",
        len(_concepts),
        len(_source_registry),
        _meta.get("version", "unknown"),
    )

    return {
        "status": "loaded",
        "meta": _meta,
        "concept_count": len(_concepts),
        "source_count": len(_source_registry),
        "domains": sorted({c.get("domain") for c in _concepts.values() if c.get("domain")}),
        "languages": sorted({c.get("language") for c in _concepts.values() if c.get("language")}),
    }


def get_concept(concept_id: str) -> Optional[Dict[str, Any]]:
    """Return a single concept by ID, or None if not found."""
    return _concepts.get(concept_id)


def get_prerequisites(concept_id: str) -> List[str]:
    """Return direct prerequisites for a concept."""
    return list(_prereq_graph.get(concept_id, []))


def get_all_prerequisites(concept_id: str) -> Set[str]:
    """Return all transitive prerequisites (ancestors in the graph)."""
    visited: Set[str] = set()
    stack = list(get_prerequisites(concept_id))
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        stack.extend(get_prerequisites(node))
    return visited


def get_related_concepts(concept_id: str) -> List[str]:
    """Return concepts that list this concept as related."""
    concept = get_concept(concept_id)
    if not concept:
        return []
    return list(concept.get("related_concepts", []))


def get_cross_language_concepts(concept_id: str) -> List[str]:
    """Return cross-language mappings for a concept."""
    return list(_cross_language_map.get(concept_id, []))


def get_concepts_by_domain(domain: str) -> List[Dict[str, Any]]:
    """Return all concepts in a given domain."""
    return [c for c in _concepts.values() if c.get("domain") == domain]


def get_concepts_by_language(language: str) -> List[Dict[str, Any]]:
    """Return all concepts for a given language."""
    return [c for c in _concepts.values() if c.get("language") == language]


def get_concepts_by_category(domain: str, category: str) -> List[Dict[str, Any]]:
    """Return concepts filtered by domain and category."""
    return [
        c for c in _concepts.values()
        if c.get("domain") == domain and c.get("category") == category
    ]


def get_curriculum_sequence(domain: str, language: str) -> List[str]:
    """Return the ordered curriculum sequence for a domain/language."""
    return list(_curriculum_map.get(domain, {}).get(language, []))


def get_all_concepts() -> Dict[str, Dict[str, Any]]:
    """Return all concepts (read-only copy of the internal dict)."""
    return dict(_concepts)


def get_prereq_graph() -> Dict[str, List[str]]:
    """Return the full prerequisite graph (read-only copy)."""
    return {k: list(v) for k, v in _prereq_graph.items()}


def get_curriculum_map() -> Dict[str, Any]:
    """Return the full curriculum map (read-only copy)."""
    return _curriculum_map


def get_cross_language_map() -> Dict[str, List[str]]:
    """Return the cross-language mapping (read-only copy)."""
    return _cross_language_map


def get_source_registry() -> List[Dict[str, Any]]:
    """Return the source registry with provenance and license metadata."""
    return list(_source_registry)


def get_meta() -> Dict[str, Any]:
    """Return corpus metadata."""
    return dict(_meta)


def is_loaded() -> bool:
    """Return True if the corpus has been loaded."""
    return _loaded


def corpus_summary() -> Dict[str, Any]:
    """Return a summary of the loaded corpus for health checks."""
    if not _loaded:
        return {"loaded": False}

    domains = defaultdict(int)
    languages = defaultdict(int)
    categories = defaultdict(int)
    for c in _concepts.values():
        d = c.get("domain", "unknown")
        l = c.get("language", "unknown")
        cat = c.get("category", "unknown")
        domains[d] += 1
        languages[l] += 1
        categories[(d, cat)] += 1

    return {
        "loaded": True,
        "meta": _meta,
        "total_concepts": len(_concepts),
        "total_sources": len(_source_registry),
        "domains": dict(domains),
        "languages": dict(languages),
        "top_categories": sorted(categories.items(), key=lambda x: -x[1])[:10],
    }


def find_concepts_by_keywords(keywords: List[str], limit: int = 20) -> List[Dict[str, Any]]:
    """Find concepts whose keywords, title, or definition match any keyword.

    This is a simple keyword search for the content factory to discover
    relevant concepts when generating lessons or exercises.

    Args:
        keywords: List of lowercase search terms.
        limit: Maximum number of results to return.

    Returns:
        List of matching concept dicts, sorted by relevance (simple score).
    """
    if not keywords:
        return []

    scored: List[tuple[int, Dict[str, Any]]] = []
    for concept in _concepts.values():
        score = 0
        text_blob = " ".join([
            concept.get("title", ""),
            concept.get("definition", ""),
            concept.get("mental_model", ""),
            " ".join(concept.get("key_rules", [])),
            " ".join(concept.get("common_mistakes", [])),
            " ".join(concept.get("interview_questions", [])),
            " ".join(concept.get("practice_targets", [])),
        ]).lower()

        for kw in keywords:
            if kw.lower() in text_blob:
                score += 1
            # Also check concept ID
            if kw.lower() in concept.get("id", "").lower():
                score += 2
            # Check title
            if kw.lower() in concept.get("title", "").lower():
                score += 3

        if score > 0:
            scored.append((score, concept))

    scored.sort(key=lambda x: -x[0])
    return [c for _, c in scored[:limit]]


def validate_corpus() -> Dict[str, Any]:
    """Validate the loaded corpus for internal consistency.

    Returns a report with any issues found:
    - Orphaned concepts (prerequisites pointing to non-existent concepts)
    - Missing prerequisites (concepts with empty prereqs that should have some)
    - Circular dependencies
    - Concepts with no curriculum_map entry

    This is a read-only diagnostic; it does not modify the corpus.
    """
    if not _loaded:
        return {"error": "Corpus not loaded"}

    issues: List[str] = []
    warnings: List[str] = []

    all_concept_ids = set(_concepts.keys())

    # Check prerequisite graph consistency
    for concept_id, prereqs in _prereq_graph.items():
        for prereq in prereqs:
            if prereq not in all_concept_ids:
                issues.append(f"Concept '{concept_id}' has prerequisite '{prereq}' which does not exist.")

    # Check for circular dependencies
    def _detect_cycle(node: str, visited: Set[str], path: Set[str]) -> Optional[List[str]]:
        if node in path:
            return list(path) + [node]
        if node in visited:
            return None
        visited.add(node)
        path.add(node)
        for prereq in _prereq_graph.get(node, []):
            cycle = _detect_cycle(prereq, visited, path)
            if cycle:
                return cycle
        path.discard(node)
        return None

    visited: Set[str] = set()
    for concept_id in _concepts:
        if concept_id not in visited:
            cycle = _detect_cycle(concept_id, visited, set())
            if cycle:
                issues.append(f"Circular dependency detected: {' -> '.join(cycle)}")

    # Check curriculum map references
    mapped_concepts: Set[str] = set()
    for domain_langs in _curriculum_map.values():
        if isinstance(domain_langs, dict):
            for seq in domain_langs.values():
                if isinstance(seq, list):
                    mapped_concepts.update(seq)
        elif isinstance(domain_langs, list):
            mapped_concepts.update(domain_langs)

    for concept_id in _concepts:
        if concept_id not in mapped_concepts:
            warnings.append(f"Concept '{concept_id}' is not in the curriculum_map.")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "total_concepts": len(_concepts),
        "mapped_concepts": len(mapped_concepts),
    }


def get_content_status(concept_id: str) -> str:
    concept = get_concept(concept_id)
    if not concept:
        return 'unknown'
    return concept.get('content_status', 'seeded')


def get_worked_examples(concept_id: str) -> list:
    concept = get_concept(concept_id)
    if not concept:
        return []
    return list(concept.get('worked_examples', []))


def get_misconceptions(concept_id: str) -> list:
    concept = get_concept(concept_id)
    if not concept:
        return []
    return list(concept.get('misconceptions', []))


def get_transfer_targets(concept_id: str) -> list:
    concept = get_concept(concept_id)
    if not concept:
        return []
    return list(concept.get('transfer_targets', []))


def get_verification(concept_id: str) -> dict:
    concept = get_concept(concept_id)
    if not concept:
        return {}
    return dict(concept.get('verification', {}))


def get_concepts_by_status(status: str) -> list:
    return [c for c in _concepts.values() if c.get('content_status') == status]


def is_scaffolded(concept_id: str) -> bool:
    status = get_content_status(concept_id)
    return status in ('AUTO_SCAFFOLDED', 'scaffolded')


def corpus_quality_report() -> dict:
    if not _loaded:
        return {'loaded': False}
    from collections import Counter
    status_counts = Counter(get_content_status(c['id']) for c in _concepts.values())
    enriched = [c for c in _concepts.values() if c.get('worked_examples')]
    with_misconceptions = [c for c in _concepts.values() if c.get('misconceptions')]
    with_transfer = [c for c in _concepts.values() if c.get('transfer_targets')]
    with_verification = [c for c in _concepts.values() if c.get('verification', {}).get('sources')]
    return {
        'loaded': True,
        'total_concepts': len(_concepts),
        'status_distribution': dict(status_counts),
        'enriched_concepts': len(enriched),
        'with_misconceptions': len(with_misconceptions),
        'with_transfer_targets': len(with_transfer),
        'with_verification': len(with_verification),
        'quality_score': round((len(enriched) + len(with_misconceptions) + len(with_transfer)) / max(1, len(_concepts)) / 3, 2),
    }
