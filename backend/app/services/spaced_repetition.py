"""
Spaced Repetition Engine (SM-2 Algorithm) for DSA Concept Mastery
Implements Anki/SuperMemo scheduling for optimal retention
"""
from datetime import datetime, timedelta

from app.utils.timeutil import utcnow
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import json


class ReviewGrade(Enum):
    """SM-2 review grades"""
    AGAIN = 0      # Complete blackout
    HARD = 1       # Incorrect but remembered with effort
    GOOD = 2       # Correct with some hesitation
    EASY = 3       # Perfect recall, instant


@dataclass
class SRSState:
    """Per-concept SRS state for a user"""
    concept_id: str
    user_id: str
    
    # SM-2 parameters
    interval: int = 0        # Days until next review (0 = new/learning)
    repetitions: int = 0     # Successful reviews in a row
    ease_factor: float = 2.5 # Multiplier for interval growth (default 2.5, min 1.3)
    
    # Scheduling
    next_review: datetime = None
    last_reviewed: datetime = None
    
    # Learning phase (interval < 1 day)
    learning_step: int = 0   # 0=10m, 1=1d, 2=3d (graduated to review)
    
    # Stats
    total_reviews: int = 0
    lapses: int = 0          # Times graded AGAIN after graduating
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.next_review is None:
            self.next_review = utcnow()
        if self.created_at is None:
            self.created_at = utcnow()
        if self.updated_at is None:
            self.updated_at = utcnow()


class SpacedRepetitionEngine:
    """
    SM-2 Algorithm Implementation
    
    Key parameters:
    - Initial ease factor: 2.5
    - Minimum ease factor: 1.3
    - Learning steps: 10 minutes, 1 day, 3 days
    - Graduating interval: 1 day
    - Easy bonus: 1.3x interval
    """
    
    LEARNING_STEPS_MINUTES = [10, 1440, 4320]  # 10m, 1d, 3d
    GRADUATING_INTERVAL = 1  # days
    EASY_INTERVAL = 4        # days (for first EASY review)
    MIN_EASE_FACTOR = 1.3
    MAX_INTERVAL_DAYS = 36500  # ~100 years
    
    def __init__(self):
        pass
    
    def create_new_card(self, concept_id: str, user_id: str) -> SRSState:
        """Create a new SRS state for a concept"""
        return SRSState(
            concept_id=concept_id,
            user_id=user_id,
            interval=0,
            repetitions=0,
            ease_factor=2.5,
            next_review=utcnow(),
            learning_step=0,
            total_reviews=0,
            lapses=0,
        )
    
    def _calculate_next_interval(self, state: SRSState, grade: ReviewGrade) -> int:
        """Calculate next interval in days based on SM-2"""
        if grade == ReviewGrade.AGAIN:
            # Reset to learning phase
            return 0
        
        if state.repetitions == 0:
            # First successful review
            if grade == ReviewGrade.EASY:
                return self.EASY_INTERVAL
            return self.GRADUATING_INTERVAL
        
        if state.repetitions == 1:
            # Second successful review
            if grade == ReviewGrade.EASY:
                return max(6, int(state.interval * state.ease_factor * 1.3))
            return max(6, int(state.interval * state.ease_factor))
        
        # Third+ review
        if grade == ReviewGrade.EASY:
            return min(self.MAX_INTERVAL_DAYS, int(state.interval * state.ease_factor * 1.3))
        elif grade == ReviewGrade.GOOD:
            return min(self.MAX_INTERVAL_DAYS, int(state.interval * state.ease_factor))
        else:  # HARD
            return min(self.MAX_INTERVAL_DAYS, int(state.interval * state.ease_factor * 0.85))
    
    def _update_ease_factor(self, state: SRSState, grade: ReviewGrade) -> float:
        """Update ease factor based on grade (SM-2 formula)"""
        if grade == ReviewGrade.AGAIN:
            # Ease factor penalty
            new_ef = state.ease_factor - 0.2
        elif grade == ReviewGrade.HARD:
            new_ef = state.ease_factor - 0.15
        elif grade == ReviewGrade.GOOD:
            new_ef = state.ease_factor  # No change
        else:  # EASY
            new_ef = state.ease_factor + 0.15
        
        return max(self.MIN_EASE_FACTOR, new_ef)
    
    def review(self, state: SRSState, grade: ReviewGrade) -> SRSState:
        """
        Process a review and return updated state
        """
        now = utcnow()
        new_state = SRSState(**asdict(state))  # Copy
        new_state.last_reviewed = now
        new_state.total_reviews += 1
        new_state.updated_at = now
        
        if grade == ReviewGrade.AGAIN:
            # Lapse - reset to learning phase
            if new_state.repetitions > 0:
                new_state.lapses += 1
            new_state.repetitions = 0
            new_state.learning_step = 0
            new_state.interval = 0
            new_state.next_review = now + timedelta(minutes=self.LEARNING_STEPS_MINUTES[0])
            new_state.ease_factor = self._update_ease_factor(new_state, grade)
            return new_state
        
        # Correct answer
        if new_state.interval == 0:
            # In learning phase
            new_state.learning_step += 1
            if new_state.learning_step >= len(self.LEARNING_STEPS_MINUTES):
                # Graduated!
                new_state.interval = self.GRADUATING_INTERVAL
                new_state.repetitions = 1
                new_state.next_review = now + timedelta(days=new_state.interval)
            else:
                # Still learning
                minutes = self.LEARNING_STEPS_MINUTES[new_state.learning_step]
                new_state.next_review = now + timedelta(minutes=minutes)
        else:
            # In review phase
            new_state.repetitions += 1
            new_state.interval = self._calculate_next_interval(new_state, grade)
            new_state.next_review = now + timedelta(days=new_state.interval)
        
        new_state.ease_factor = self._update_ease_factor(new_state, grade)
        return new_state
    
    def get_due_cards(self, states: List[SRSState], limit: int = 20) -> List[SRSState]:
        """Get cards due for review, sorted by overdue-ness"""
        now = utcnow()
        due = [s for s in states if s.next_review <= now]
        # Sort: overdue first (most overdue), then by ease factor (hardest first)
        due.sort(key=lambda s: (s.next_review, s.ease_factor))
        return due[:limit]
    
    def get_stats(self, states: List[SRSState]) -> Dict[str, Any]:
        """Get SRS statistics for a user"""
        now = utcnow()
        total = len(states)
        new_cards = sum(1 for s in states if s.repetitions == 0 and s.interval == 0)
        learning = sum(1 for s in states if s.interval == 0 and s.repetitions > 0)
        review = sum(1 for s in states if s.interval > 0)
        due_now = sum(1 for s in states if s.next_review <= now)
        overdue = sum(1 for s in states if s.next_review < now - timedelta(days=1))
        
        avg_ease = sum(s.ease_factor for s in states) / total if total > 0 else 2.5
        total_reviews = sum(s.total_reviews for s in states)
        total_lapses = sum(s.lapses for s in states)
        
        # Retention rate
        retention = 1 - (total_lapses / total_reviews) if total_reviews > 0 else 1.0
        
        return {
            "total_concepts": total,
            "new": new_cards,
            "learning": learning,
            "review": review,
            "due_now": due_now,
            "overdue": overdue,
            "avg_ease_factor": round(avg_ease, 2),
            "total_reviews": total_reviews,
            "total_lapses": total_lapses,
            "retention_rate": round(retention * 100, 1),
        }
    
    def simulate_forecast(self, state: SRSState, days: int = 30) -> List[Dict[str, Any]]:
        """Forecast review schedule for next N days"""
        forecast = []
        current = state
        for day in range(days):
            due_count = 1 if current.next_review <= utcnow() + timedelta(days=day+1) else 0
            forecast.append({
                "day": day + 1,
                "date": (utcnow() + timedelta(days=day)).strftime("%Y-%m-%d"),
                "reviews_due": due_count,
            })
        return forecast


# DSA Concept taxonomy for SRS
DSA_CONCEPTS = {
    "arrays": {
        "name": "Arrays & Strings",
        "subtopics": [
            "two-pointers", "sliding-window", "prefix-sum", "kadane", 
            "dutch-flag", "binary-search-array", "rotate", "merge-intervals"
        ]
    },
    "linked-lists": {
        "name": "Linked Lists",
        "subtopics": [
            "reverse", "cycle-detection", "merge-two-lists", "palindrome",
            "intersection", "remove-nth-from-end", "copy-random-pointer"
        ]
    },
    "stacks-queues": {
        "name": "Stacks & Queues",
        "subtopics": [
            "valid-parentheses", "min-stack", "eval-rpn", "daily-temperatures",
            "largest-rectangle", "sliding-window-max", "queue-using-stacks"
        ]
    },
    "trees": {
        "name": "Trees & BST",
        "subtopics": [
            "traversals", "max-depth", "validate-bst", "lowest-common-ancestor",
            "serialize-deserialize", "path-sum", "diameter", "bst-from-preorder"
        ]
    },
    "graphs": {
        "name": "Graphs",
        "subtopics": [
            "bfs-dfs", "topological-sort", "dijkstra", "bellman-ford",
            "union-find", "mst-kruskal", "mst-prim", "strongly-connected",
            "bipartite", "cycle-detection", "shortest-path"
        ]
    },
    "dynamic-programming": {
        "name": "Dynamic Programming",
        "subtopics": [
            "fibonacci", "climbing-stairs", "coin-change", "knapsack-01",
            "lcs", "lis", "edit-distance", "house-robber", "max-subarray",
            "partition-equal-subset", "word-break", "dp-on-trees"
        ]
    },
    "heaps": {
        "name": "Heaps & Priority Queues",
        "subtopics": [
            "kth-largest", "merge-k-lists", "top-k-frequent", "median-stream",
            "task-scheduler", "reorganize-string"
        ]
    },
    "tries": {
        "name": "Tries",
        "subtopics": [
            "implement-trie", "word-search-ii", "autocomplete", "max-xor"
        ]
    },
    "backtracking": {
        "name": "Backtracking",
        "subtopics": [
            "subsets", "permutations", "combinations", "combination-sum",
            "palindrome-partition", "n-queens", "sudoku-solver"
        ]
    },
    "bit-manipulation": {
        "name": "Bit Manipulation",
        "subtopics": [
            "single-number", "hamming-weight", "counting-bits", "power-of-two",
            "missing-number", "single-number-ii", "bitwise-and-range"
        ]
    },
    "math-geometry": {
        "name": "Math & Geometry",
        "subtopics": [
            "gcd-lcm", "modular-arithmetic", "sieve", "prime-factorization",
            "combinatorics", "probability", "coordinate-geometry"
        ]
    },
}


def get_all_concept_ids() -> List[str]:
    """Get all DSA concept IDs for SRS initialization"""
    ids = []
    for topic, data in DSA_CONCEPTS.items():
        for sub in data["subtopics"]:
            ids.append(f"{topic}:{sub}")
    return ids


def initialize_user_srs(user_id: str) -> List[SRSState]:
    """Initialize SRS states for all DSA concepts for a new user"""
    engine = SpacedRepetitionEngine()
    return [engine.create_new_card(cid, user_id) for cid in get_all_concept_ids()]


# Example usage and testing
if __name__ == "__main__":
    engine = SpacedRepetitionEngine()
    
    # Create a new card
    state = engine.create_new_card("arrays:two-pointers", "user123")
    print(f"New card: {state}")
    
    # Simulate reviews
    for i, grade in enumerate([ReviewGrade.GOOD, ReviewGrade.GOOD, ReviewGrade.EASY, ReviewGrade.GOOD]):
        state = engine.review(state, grade)
        print(f"Review {i+1} ({grade.name}): interval={state.interval}d, ef={state.ease_factor:.2f}, next={state.next_review}")
    
    # Stats
    stats = engine.get_stats([state])
    print(f"Stats: {stats}")