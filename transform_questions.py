"""Transform existing curated question bank to BountyCode Question Standard.

This script reads the existing questions_bank_curated.json and transforms each
question into the 4-layer BountyCode Question Standard format.

The 4 layers:
1. QUESTION - the actual question content
2. PEDAGOGY - why the student is learning it (skill, subtopic, pattern, objectives)
3. PLACEMENT METADATA - roles, companies, difficulty, stage, frequency
4. MACHINE-READABLE EVALUATION - complexity, test cases, mastery evidence, quality score

Every question type (coding, aptitude, logical, verbal, hr) is transformed
according to its appropriate schema, while preserving all existing data.
"""

import json, random, uuid, os, re
from collections import defaultdict

# ─── Configuration ──────────────────────────────────────────────────

COMPANIES_INDIAN = ["tcs", "infosys", "wipro", "cognizant", "hcl", "accenture", 
                    "capgemini", "tech_mahindra", "lti", "mphasis"]

# Mapping from old quality_score/tier to new system
QUALITY_TIER_MAP = {
    "A": {"tier": "A", "min_score": 90},
    "B": {"tier": "B", "min_score": 75},
    "C": {"tier": "C", "min_score": 50},
    "Q": {"tier": "Q", "max_score": 49},
}

# Skill mapping from existing topics
SKILL_MAP = {
    "arrays": "arrays",
    "array": "arrays",
    "arrays & hashing": "arrays",
    "hashing": "hashing",
    "hash table": "hashing",
    "two pointers": "two_pointers",
    "sliding window": "sliding_window",
    "binary search": "binary_search",
    "graphs": "graphs",
    "graph": "graphs",
    "trees": "trees",
    "binary search trees": "trees",
    "bST": "trees",
    "heaps": "heaps",
    "priority queue": "heaps",
    "dynamic programming": "dynamic_programming",
    "dp": "dynamic_programming",
    "greedy": "greedy",
    "bit manipulation": "bit_manipulation",
    "math": "math",
    "number theory": "math",
    "strings": "strings",
    "linked lists": "linked_lists",
    "linked list": "linked_lists",
    "stack": "stack",
    "queue": "queue",
    "binary search trees": "trees",
    "try": "trees",
}

# Pedagogy defaults by question type
PEDAGOGY_DEFAULTS = {
    "coding": {
        "mental_model": "Trade brute force for optimal data structure",
        "why_this_matters": "Foundation for efficient problem-solving",
        "real_world": "Building scalable software systems",
        "prerequisites": ["basic_dsa"],
        "learning_objectives": []
    },
    "aptitude": {
        "mental_model": "Quick quantitative reasoning",
        "why_this_matters": "Essential for placement tests",
        "real_world": "Everyday calculations",
        "prerequisites": ["secondary_math"],
        "learning_objectives": []
    },
    "logical": {
        "mental_model": "Deductive reasoning chains",
        "why_this_matters": "Structured thinking skill",
        "real_world": "Logic puzzles, interviews",
        "prerequisites": ["basic_logic"],
        "learning_objectives": []
    },
    "verbal": {
        "mental_model": "Grammar rules and language patterns",
        "why_this_matters": "Communication clarity",
        "real_world": "Professional writing",
        "prerequisites": ["high_school_english"],
        "learning_objectives": []
    },
    "hr": {
        "mental_model": "Behavioral framework (STAR)",
        "why_this_matters": "Employability skill",
        "real_world": "Workplace scenarios",
        "prerequisites": ["self_reflection"],
        "learning_objectives": []
    }
}

# ─── Helper Functions ───────────────────────────────────────────────


def map_skill(topic):
    """Map existing topic to standard skill."""
    topic_lower = topic.lower().strip()
    for k, v in SKILL_MAP.items():
        if k in topic_lower or topic_lower in k:
            return v
    # Fallback: try to extract first word
    first_word = topic_lower.split()[0] if topic_lower else ""
    return SKILL_MAP.get(first_word, "general")


def map_subtopic(topic):
    """Map existing topic to standard subtopic."""
    # Extract common subtopics from topics like "arrays & hashing"
    topic_lower = topic.lower().strip()
    if "hashing" in topic_lower:
        return "hashing"
    elif "trees" in topic_lower and "bst" not in topic_lower:
        return "tree_traversal"
    elif "graph" in topic_lower:
        return "graph_traversal"
    elif "dp" in topic_lower or "dynamic" in topic_lower:
        return "dynamic_programming"
    elif "linked" in topic_lower:
        return "linked_list"
    elif "heap" in topic_lower:
        return "heap"
    elif "bit" in topic_lower:
        return "bit_manipulation"
    elif "binary" in topic_lower and "search" in topic_lower:
        return "binary_search"
    elif "string" in topic_lower:
        return "string_operations"
    elif "two pointers" in topic_lower:
        return "two_pointers"
    elif "sliding window" in topic_lower:
        return "sliding_window"
    elif "binary search" in topic_lower:
        return "binary_search"
    return "general"


def map_pattern(topic):
    """Map to pattern name."""
    topic_lower = topic.lower().strip()
    if "two sum" in topic_lower or "pair sum" in topic_lower:
        return "complement_lookup"
    elif "anagram" in topic_lower:
        return "anagram_grouping"
    elif "frequent" in topic_lower or "top k" in topic_lower:
        return "frequency_count"
    elif "product" in topic_lower:
        return "product_array"
    elif "substring" in topic_lower:
        return "substring_search"
    elif "palindrome" in topic_lower:
        return "palindrome_check"
    elif "reverse" in topic_lower:
        return "reverse"
    elif "sort" in topic_lower:
        return "sorting"
    elif "binary search" in topic_lower:
        return "binary_search"
    return "pattern_recognition"


def determine_difficulty_placement(q):
    """Determine placement difficulty from existing difficulty."""
    diff = q.get("difficulty", "easy").lower()
    if diff in ["hard", "very_hard"]:
        return "hard"
    elif diff in ["medium"]:
        return "medium"
    else:
        return "easy"


def determine_difficulty_cognitive(q, q_type):
    """Estimate cognitive difficulty."""
    if q_type == "coding":
        # Based on topic complexity
        topic = q.get("topic", "").lower()
        if any(x in topic for x in ["dynamic programming", "graph", "heap"]):
            return 5  # Transfer
        elif any(x in topic for x in ["trees", "binary search", "linked list"]):
            return 4
        elif any(x in topic for x in ["arrays", "strings", "linked list"]):
            return 3
        else:
            return 2
    elif q_type == "aptitude":
        return random.randint(2, 4)
    elif q_type == "logical":
        return random.randint(3, 5)
    elif q_type == "verbal":
        return random.randint(2, 4)
    elif q_type == "hr":
        return random.randint(2, 4)
    return 3


def determine_companies(q):
    """Extract and normalize company list."""
    companies = q.get("company", [])
    if isinstance(companies, str):
        companies = [c.strip() for c in companies.split(",")]
    # Normalize to lowercase
    normalized = []
    for c in companies:
        c_lower = c.lower().strip()
        # Map common variations
        mapping = {"amazon": "amazon", "google": "google", "microsoft": "microsoft",
                   "facebook": "meta", "apple": "apple", "netflix": "netflix"}
        normalized.append(mapping.get(c_lower, c_lower))
    # Only include Indian companies that are in our list
    result = [c for c in normalized if c in COMPANIES_INDIAN]
    # If no Indian companies found, keep original but lowercase
    if not result:
        result = normalized[:3]  # top 3
    return result


def determine_roles(q):
    """Extract roles."""
    roles = q.get("role", [])
    if isinstance(roles, str):
        roles = [roles]
    # Normalize
    result = []
    for r in roles:
        r_lower = r.lower().strip()
        if r_lower not in result:
            result.append(r_lower)
    return result if result else ["student"]


def determine_frequency(q):
    """Determine frequency from existing data or default."""
    freq = q.get("frequency", "common")
    # If freq is numeric (acceptance rate), convert
    if isinstance(freq, (int, float)):
        if freq > 50:
            return "common"
        elif freq > 20:
            return "occasionally"
        else:
            return "rare"
    return freq


def determine_question_stage(q_type, q_stage, q_difficulty):
    """Determine journey stage."""
    # Map existing question_stage to journey stages
    stage_map = {
        "easy": "concept",
        "medium": "guided_practice", 
        "hard": "independent_practice",
        "technical_interview": "placement",
        "placement": "placement",
        "interview": "interview",
        " OA": "oa",
        "interview_question": "interview",
    }
    # Use existing if meaningful, otherwise default
    if q_stage and q_stage in stage_map:
        return stage_map[q_stage]
    # Default based on type and difficulty
    diff = q_difficulty.lower()
    if q_type == "coding" and diff in ["hard", "very_hard"]:
        return "interview"
    return "concept"


def add_pedagogy(q_type, q):
    """Add pedagogy layer."""
    defaults = PEDAGOGY_DEFAULTS.get(q_type, PEDAGOGY_DEFAULTS["coding"])
    # Try to extract from existing data if available
    why_matters = q.get("why_this_matters", "")
    real_world = q.get("real_world", "")
    prerequisites = q.get("prerequisites", [])
    learning_objectives = q.get("learning_objectives", [])
    
    # If not provided, use defaults
    if not why_matters:
        why_matters = defaults["why_this_matters"]
    if not real_world:
        real_world = defaults["real_world"]
    if not prerequisites:
        prerequisites = defaults["prerequisites"]
    if not learning_objectives:
        learning_objectives = defaults["learning_objectives"]
    
    return {
        "skill": map_skill(q.get("topic", "")),
        "subtopic": map_subtopic(q.get("topic", "")),
        "pattern": map_pattern(q.get("topic", "")),
        "mental_model": defaults["mental_model"],
        "why_this_matters": why_matters,
        "real_world": real_world,
        "prerequisites": prerequisites,
        "learning_objectives": learning_objectives
    }


def add_placement_metadata(q):
    """Add placement metadata layer."""
    return {
        "roles": determine_roles(q),
        "companies": determine_companies(q),
        "difficulty_placement": determine_difficulty_placement(q),
        "difficulty_cognitive": determine_difficulty_cognitive(q, q.get("type", "coding")),
        "estimated_minutes": estimate_minutes(q),
        "frequency": determine_frequency(q),
        "placement_stage": determine_question_stage(q.get("type", "coding"), q.get("question_stage", ""))
    }


def add_complexity_coding(q):
    """Add complexity metadata for coding questions."""
    # Try to extract from explanation or set defaults
    explanation = q.get("explanation", "")
    
    # Set complexity based on topic
    topic = q.get("topic", "").lower()
    
    if any(x in topic for x in ["dynamic programming", "graph", "tree traversal"]):
        complexity = {
            "time": {
                "best": "O(n log n)",
                "average": "O(n log n)",
                "worst": "O(n²)"
            },
            "space": "O(n)",
            "auxiliary_space": "O(n)"
        }
        explanation_parts = []
        if "dynamic programming" in topic:
            explanation_parts.append("DP typically O(n²) or O(n·capacity)")
        if "graph" in topic:
            explanation_parts.append("Graph traversal O(V+E)")
        if "tree" in topic:
            explanation_parts.append("Tree traversal O(n)")
    elif any(x in topic for x in ["array", "hashing", "two pointers"]):
        complexity = {
            "time": {
                "best": "O(n)",
                "average": "O(n)",
                "worst": "O(n)"
            },
            "space": "O(n) or O(1)",
            "auxiliary_space": "O(n) or O(1)"
        }
        explanation_parts = []
        if "hash map" in explanation.lower():
            explanation_parts.append("Hash map lookup O(1) average")
        if "two pointers" in explanation.lower():
            explanation_parts.append("Single pass O(n)")
    else:
        complexity = {
            "time": {
                "best": "O(n log n)",
                "average": "O(n log n)",
                "worst": "O(n²)"
            },
            "space": "O(n)",
            "auxiliary_space": "O(n)"
        }
        explanation_parts = ["Standard complexity analysis"]
    
    # Add complexity explanation
    complexity_explanation = {}
    if "DP" in explanation or "dynamic" in explanation.lower():
        complexity_explanation["time"] = "Dynamic programming approach with state tracking"
    if "hash" in explanation.lower() or "map" in explanation.lower():
        complexity_explanation["time"] = "Hash map provides O(1) average lookup"
    if "two pointers" in explanation.lower():
        complexity_explanation["time"] = "Single pass without nested loops"
    if not complexity_explanation:
        complexity_explanation["time"] = "Each element processed once or twice"
    
    # Add alternative solutions
    alternatives = []
    if "hash map" in explanation.lower() or "map" in explanation.lower():
        alternatives.append({
            "name": "Brute Force",
            "time": "O(n²)",
            "space": "O(1)",
            "when_to_use": "Baseline before optimization"
        })
        alternatives.append({
            "name": "Hash Map",
            "time": "O(n)",
            "space": "O(n)",
            "when_to_use": "Trading memory for speed"
        })
    
    return {
        "complexity": complexity,
        "complexity_explanation": complexity_explanation,
        "alternative_solutions": alternatives
    }


def add_evaluation_coding(q):
    """Add machine-readable evaluation for coding questions."""
    # Check if we already have test cases
    test_cases_visible = q.get("test_cases", [])
    test_cases_hidden = q.get("hidden_test_cases", [])
    
    if not test_cases_visible:
        # Generate basic visible test cases from examples
        examples = q.get("examples", [])
        visible = []
        for ex in examples:
            if isinstance(ex, dict):
                visible.append({"input": ex.get("input", ""), "output": ex.get("output", "")})
            elif isinstance(ex, str):
                visible.append({"input": ex, "output": ""})
        if not visible:
            # Create basic test case from question
            visible = [{"input": "nums=[2,7,11,15], target=9", "output": "[0,1]"}]
        test_cases_visible = visible
    
    if not test_cases_hidden:
        # Create hidden test cases
        test_cases_hidden = [
            {"input": "nums=[3,3,4], target=6", "output": "[0,1]"},
            {"input": "nums=[1,2,3,4,5], target=10", "output": "[]"}
        ]
    
    # Determine mastery evidence
    mastery_evidence = []
    if q.get("correct_answer"):
        mastery_evidence.append("correct_solution")
    if q.get("explanation"):
        mastery_evidence.append("explains_reasoning")
    # Add based on question type
    if q.get("type") == "coding":
        mastery_evidence.extend(["edge_case_handling", "complexity_explanation"])
    
    return {
        "visible_test_cases": test_cases_visible,
        "hidden_test_cases": test_cases_hidden,
        "mastery_evidence": mastery_evidence,
        "rubric": {
            "correctness": 50,
            "edge_cases": 25,
            "complexity": 15,
            "code_quality": 10
        }
    }


def add_evaluation_aptitude(q):
    """Add evaluation for aptitude questions."""
    return {
        "visible_test_cases": [],
        "hidden_test_cases": [],
        "mastery_evidence": ["correct_answer", "formula_application"],
        "rubric": {
            "correctness": 50,
            "reasoning_steps": 30,
            "formula_usage": 20
        }
    }


def add_evaluation_logical(q):
    """Add evaluation for logical questions."""
    return {
        "visible_test_cases": [],
        "hidden_test_cases": [],
        "mastery_evidence": ["correct_reasoning"],
        "rubric": {
            "correctness": 50,
            "reasoning_quality": 30,
            "logic_chain": 20
        }
    }


def add_evaluation_verbal(q):
    """Add evaluation for verbal questions."""
    return {
        "visible_test_cases": [],
        "hidden_test_cases": [],
        "mastery_evidence": ["correct_answer", "grammar_rule_application"],
        "rubric": {
            "correctness": 50,
            "grammar_application": 30,
            "explanation_quality": 20
        }
    }


def add_evaluation_hr(q):
    """Add evaluation for HR questions."""
    return {
        "visible_test_cases": [],
        "hidden_test_cases": [],
        "mastery_evidence": ["framework_usage", "specific_example"],
        "rubric": {
            "structure": 25,
            "ownership": 25,
            "communication": 25,
            "judgment": 25
        }
    }


def estimate_minutes(q):
    """Estimate time based on difficulty and type."""
    diff = q.get("difficulty", "easy").lower()
    q_type = q.get("type", "coding")
    
    base_minutes = {
        ("coding", "easy"): 15,
        ("coding", "medium"): 25,
        ("coding", "hard"): 45,
        ("aptitude", "easy"): 30,
        ("aptitude", "medium"): 45,
        ("aptitude", "hard"): 60,
        ("logical", "easy"): 45,
        ("logical", "medium"): 60,
        ("logical", "hard"): 90,
        ("verbal", "easy"): 20,
        ("verbal", "medium"): 30,
        ("hr", "easy"): 15,
        ("hr", "medium"): 20,
    }
    
    key = (q_type, diff)
    return base_minutes.get(key, 20)


def determine_quality_tier(score):
    """Determine quality tier from score."""
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 50:
        return "C"
    else:
        return "Q"


def transform_coding_question(q):
    """Transform a coding question to the new standard."""
    new_q = {
        # Layer 1: Question
        "id": q.get("id", str(uuid.uuid4())),
        "type": "coding",
        "stage": q.get("question_stage", "concept"),
        "title": q.get("question", "")[:80] + ("..." if len(q.get("question", "")) > 80 else ""),
        "prompt": q.get("question", ""),
        "constraints": extract_constraints(q.get("question", "")),
        "examples": q.get("examples", []),
        "expected_output": None,
        
        # Layer 2: Pedagogy
        "pedagogy": add_pedagogy("coding", q),
        
        # Layer 3: Placement Metadata
        "placement_metadata": add_placement_metadata(q),
        
        # Layer 4: Machine-Readable Evaluation
        "evaluation": add_evaluation_coding(q),
        
        # Quality
        "quality_score": q.get("quality_score", 0.8),
        "quality_tier": q.get("quality_tier", "B"),
        
        # Preserve existing useful fields
        "topic": q.get("topic", ""),
        "difficulty": q.get("difficulty", "medium"),
        "company": q.get("company", ["tcs"]),
        "role": q.get("role", "student"),
        "correct_answer": q.get("correct_answer"),
        "solution": q.get("solution"),
        "hints": q.get("hints", []),
        "frequency": q.get("frequency", 1),
    }
    
    # Add complexity if not already detailed
    if "complexity" not in new_q:
        new_q["complexity"] = add_complexity_coding(q)
    
    # Add evaluation if not detailed
    if "evaluation" not in new_q:
        new_q["evaluation"] = add_evaluation_coding(q)
    
    return new_q


def transform_aptitude_question(q):
    """Transform an aptitude question."""
    new_q = {
        "id": q.get("id", str(uuid.uuid4())),
        "type": "aptitude",
        "stage": q.get("question_stage", "concept"),
        "title": q.get("question", "")[:80] + ("..." if len(q.get("question", "")) > 80 else ""),
        "prompt": q.get("question", ""),
        "description": q.get("description", ""),
        
        # Layer 2: Pedagogy
        "pedagogy": add_pedagogy("aptitude", q),
        
        # Layer 3: Placement Metadata
        "placement_metadata": add_placement_metadata(q),
        
        # Layer 4: Machine-Readable Evaluation
        "evaluation": add_evaluation_aptitude(q),
        
        # Quality
        "quality_score": q.get("quality_score", 0.8),
        "quality_tier": q.get("quality_tier", "B"),
        
        # Preserve existing fields
        "topic": q.get("topic", "aptitude"),
        "difficulty": q.get("difficulty", "easy"),
        "company": q.get("company", ["tcs"]),
        "role": q.get("role", ["student"]),
        "correct_answer": q.get("correct_answer"),
        "solution": q.get("solution"),
        "options": q.get("options", []),
        "examples": q.get("examples", []),
        "testcases": q.get("testcases", []),
        "frequency": q.get("frequency", 1),
        "xp_points": q.get("xp_points", 10),
    }
    
    # Add complexity (aptitude doesn't need detailed complexity)
    new_q["complexity"] = None
    
    # Add evaluation
    new_q["evaluation"] = add_evaluation_aptitude(q)
    
    return new_q


def transform_logical_question(q):
    """Transform a logical question."""
    new_q = {
        "id": q.get("id", str(uuid.uuid4())),
        "type": "logical",
        "stage": q.get("question_stage", "concept"),
        "title": q.get("question", "")[:80] + ("..." if len(q.get("question", "")) > 80 else ""),
        "prompt": q.get("question", ""),
        "description": q.get("description", ""),
        
        # Layer 2: Pedagogy
        "pedagogy": add_pedagogy("logical", q),
        
        # Layer 3: Placement Metadata
        "placement_metadata": add_placement_metadata(q),
        
        # Layer 4: Machine-Readable Evaluation
        "evaluation": add_evaluation_logical(q),
        
        # Quality
        "quality_score": q.get("quality_score", 0.8),
        "quality_tier": q.get("quality_tier", "B"),
        
        # Preserve existing fields
        "topic": q.get("topic", "logical reasoning"),
        "difficulty": q.get("difficulty", "hard"),
        "company": q.get("company", ["tcs"]),
        "role": q.get("role", ["student"]),
        "correct_answer": q.get("correct_answer"),
        "solution": q.get("solution"),
        "hints": q.get("hints", []),
        "examples": q.get("examples", []),
    }
    
    # Add evaluation
    new_q["evaluation"] = add_evaluation_logical(q)
    
    # Add complexity
    new_q["complexity"] = None
    
    return new_q


def transform_verbal_question(q):
    """Transform a verbal question."""
    new_q = {
        "id": q.get("id", str(uuid.uuid4())),
        "type": "verbal",
        "stage": q.get("question_stage", "concept"),
        "title": q.get("question", "")[:80] + ("..." if len(q.get("question", "")) > 80 else ""),
        "prompt": q.get("question", ""),
        "description": q.get("description", ""),
        
        # Layer 2: Pedagogy
        "pedagogy": add_pedagogy("verbal", q),
        
        # Layer 3: Placement Metadata
        "placement_metadata": add_placement_metadata(q),
        
        # Layer 4: Machine-Readable Evaluation
        "evaluation": add_evaluation_verbal(q),
        
        # Quality
        "quality_score": q.get("quality_score", 0.8),
        "quality_tier": q.get("quality_tier", "B"),
        
        # Preserve existing fields
        "topic": q.get("topic", "verbal ability"),
        "difficulty": q.get("difficulty", "medium"),
        "company": q.get("company", ["tcs"]),
        "role": q.get("role", ["student"]),
        "correct_answer": q.get("correct_answer"),
        "explanation": q.get("explanation"),
        "options": q.get("options", []),
    }
    
    # Add evaluation
    new_q["evaluation"] = add_evaluation_verbal(q)
    
    # Add complexity
    new_q["complexity"] = None
    
    return new_q


def transform_hr_question(q):
    """Transform an HR/behavioral question."""
    new_q = {
        "id": q.get("id", str(uuid.uuid4())),
        "type": "hr",
        "stage": q.get("question_stage", "concept"),
        "title": q.get("question", "")[:80] + ("..." if len(q.get("question", "")) > 80 else ""),
        "prompt": q.get("question", ""),
        "description": q.get("description", ""),
        
        # Layer 2: Pedagogy
        "pedagogy": add_pedagogy("hr", q),
        
        # Layer 3: Placement Metadata
        "placement_metadata": add_placement_metadata(q),
        
        # Layer 4: Machine-Readable Evaluation
        "evaluation": add_evaluation_hr(q),
        
        # Quality
        "quality_score": q.get("quality_score", 0.8),
        "quality_tier": q.get("quality_tier", "B"),
        
        # Preserve existing fields
        "topic": q.get("topic", "cultural_fit"),
        "difficulty": q.get("difficulty", "easy"),
        "company": q.get("company", ["tcs"]),
        "role": q.get("role", "hr"),
        "correct_answer": q.get("correct_answer"),
        "explanation": q.get("explanation"),
        "options": q.get("options", []),
        "hints": q.get("hints", []),
    }
    
    # Add evaluation
    new_q["evaluation"] = add_evaluation_hr(q)
    
    # Add complexity
    new_q["complexity"] = None
    
    return new_q


def transform_unknown_question(q):
    """Transform questions with unknown type."""
    # These seem to have a different format
    new_q = {
        "id": q.get("id", str(uuid.uuid4())),
        "type": "coding",  # default to coding
        "stage": q.get("question_stage", "concept"),
        "title": q.get("title", q.get("question", "")[:80] + ("..." if len(q.get("question", "")) > 80 else "")),
        "prompt": q.get("question", q.get("description", "")),
        "constraints": q.get("constraints", []),
        
        # Layer 2: Pedagogy
        "pedagogy": {
            "skill": map_skill(q.get("topic", "")),
            "subtopic": map_subtopic(q.get("topic", "")),
            "pattern": map_pattern(q.get("topic", "")),
            "mental_model": "Standard problem-solving approach",
            "why_this_matters": "Educational problem",
            "real_world": "Practice problem",
            "prerequisites": [],
            "learning_objectives": []
        },
        
        # Layer 3: Placement Metadata
        "placement_metadata": {
            "roles": ["student"],
            "companies": ["tcs"],
            "difficulty_placement": "medium",
            "difficulty_cognitive": 3,
            "estimated_minutes": 20,
            "frequency": "common",
            "placement_stage": "concept"
        },
        
        # Layer 4: Machine-Readable Evaluation
        "evaluation": {
            "visible_test_cases": [],
            "hidden_test_cases": [],
            "mastery_evidence": ["attempted"],
            "rubric": {
                "correctness": 50,
                "attempt": 50
            }
        },
        
        # Quality
        "quality_score": q.get("quality_score", 0.5),
        "quality_tier": "C",
        
        # Preserve existing
        "topic": q.get("topic", "arrays"),
        "difficulty": q.get("difficulty", "easy"),
        "company": q.get("companies", ["tcs"]),
        "role": q.get("role", ["student"]),
    }
    
    return new_q


def extract_constraints(question_text):
    """Try to extract constraints from question text."""
    # Very basic extraction - look for common constraint patterns
    constraints = []
    # Look for "1 <= n <=", "0 <=", etc.
    matches = re.findall(r'[\d]+\s*[<>=]\s*[\d]+', question_text)
    for m in matches:
        constraints.append(m)
    # If no constraints found, add default
    if not constraints:
        constraints = ["1 <= n <= 100000"]
    return constraints


# ─── Main Transformation ──────────────────────────────────────────


def main():
    print("=" * 70)
    print("TRANSFORMING QUESTION BANK TO BOUNTYCODE QUESTION STANDARD")
    print("=" * 70)
    
    # Read existing curated bank
    input_path = r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json"
    output_path = r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json"
    usable_path = r"D:\Project-Fremen\backend\app\data\questions_usable.json"
    
    with open(input_path, "r", encoding="utf-8") as f:
        curated = json.load(f)
    
    print("\nTotal questions in bank: {}".format(len(curated)))
    
    # Categorize by type
    by_type = defaultdict(list)
    for q in curated:
        q_type = q.get("type", "unknown")
        by_type[q_type].append(q)
    
    print("Question types: {}".format(dict(by_type)))
    
    # Transform each question
    transformed = []
    stats = {
        "coding": 0,
        "aptitude": 0,
        "logical": 0,
        "verbal": 0,
        "hr": 0,
        "unknown": 0,
    }
    
    for q in curated:
        q_type = q.get("type", "unknown")
        
        if q_type == "coding":
            new_q = transform_coding_question(q)
            stats["coding"] += 1
        elif q_type == "aptitude":
            new_q = transform_aptitude_question(q)
            stats["aptitude"] += 1
        elif q_type == "logical":
            new_q = transform_logical_question(q)
            stats["logical"] += 1
        elif q_type == "verbal":
            new_q = transform_verbal_question(q)
            stats["verbal"] += 1
        elif q_type == "hr":
            new_q = transform_hr_question(q)
            stats["hr"] += 1
        else:
            new_q = transform_unknown_question(q)
            stats["unknown"] += 1
        
        transformed.append(new_q)
    
    # Write transformed bank
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    
    print("\nTransformed bank written: {} questions".format(len(transformed)))
    
    # Rebuild questions_usable.json
    print("\nRebuilding questions_usable.json topic index...")
    
    usable = []
    seen_questions = set()
    seen_ids = set()
    
    for q in transformed:
        question_text = q.get("prompt", q.get("title", "")).lower().strip()
        question_id = q.get("id", "")
        
        # Deduplicate by question text
        if question_text in seen_questions or question_id in seen_ids:
            continue
        seen_questions.add(question_text)
        seen_ids.add(question_id)
        
        # Build usable entry
        entry = {
            "id": q.get("id", ""),
            "type": q.get("type", "coding"),
            "company": q.get("placement_metadata", {}).get("companies", ["tcs"])[:3],
            "role": q.get("placement_metadata", {}).get("roles", ["student"])[0] if q.get("placement_metadata", {}).get("roles") else "student",
            "difficulty": q.get("placement_metadata", {}).get("difficulty_placement", "medium"),
            "topic": q.get("pedagogy", {}).get("skill", ""),
            "sub_topic": q.get("pedagogy", {}).get("subtopic", ""),
            "question": q.get("prompt", q.get("title", "")),
            "options": q.get("options", []),
            "correct_answer": q.get("correct_answer"),
            "explanation": q.get("evaluation", {}).get("mastery_evidence", []),
            "hints": [],  # Will be populated by renderer
            "topic": q.get("pedagogy", {}).get("skill", ""),
        }
        usable.append(entry)
    
    # Write usable index
    with open(usable_path, "w", encoding="utf-8") as f:
        json.dump(usable, f, indent=2, ensure_ascii=False)
    
    print("questions_usable.json written: {} entries".format(len(usable)))
    
    # Print summary
    print("\n" + "=" * 70)
    print("TRANSFORMATION SUMMARY")
    print("=" * 70)
    print("Original: {} questions".format(len(curated)))
    print("Transformed: {} questions".format(len(transformed)))
    print()
    for t, c in stats.items():
        print("  {}: {} questions".format(t.capitalize(), c))
    print()
    print("Quality distribution (original):")
    # Count quality tiers
    tier_counts = defaultdict(int)
    for q in transformed:
        tier = q.get("quality_tier", "B")
        tier_counts[tier] += 1
    for t, c in sorted(tier_counts.items()):
        print("  {} tier: {} questions".format(t, c))
    print()
    print("Topics covered: {}".format(
        len(set(q.get("pedagogy", {}).get("skill", "") for q in transformed if q.get("pedagogy")))))
    print("=" * 70)


if __name__ == "__main__":
    main()