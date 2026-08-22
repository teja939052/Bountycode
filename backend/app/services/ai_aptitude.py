"""Aptitude test AI functions."""

import logging
from typing import Dict, Any
from app.services.ai_core import chat_completion, parse_json, assign_companies

logger = logging.getLogger(__name__)

APTITUDE_SUB_CATEGORY_GUIDELINES = {
    "quant-shortcuts": """Focus on SPEED TRICKS for campus placement:
- Vedic Math: Vertically & Crosswise multiplication, Nikhilam division, squares/cubes shortcuts
- Approximation: Rounding for % calculations, fraction-to-% conversion tables
- Profit/Loss: Successive discount formula, marked price ↔ selling price tricks
- Time-Speed-Distance: Relative speed, average speed harmonic mean
- Mixture/Alligation: Visual diagram method, replacement problems
- Each question must teach a specific named trick (e.g., "Vedic: Vertically Crosswise")""",

    "syllogisms": """Focus on VENN DIAGRAM method:
- Standard form: All/Some/No statements → conclusions
- 2-statement & 3-statement syllogisms
- "Some A are B" vs "All A are B" conversion rules
- Include "Only a few" and "Few" new pattern questions (TCS recent)""",

    "blood-relations": """Focus on FAMILY TREE diagramming:
- Coded relations: A+B means A is father of B, A-B means A is sister...
- Multi-generation (3-4 levels), in-laws, step-relations
- "Pointing to a photograph" type questions
- Gender-neutral names to avoid assumptions""",

    "direction-sense": """Focus on COORDINATE/VECTOR visualization:
- Shadow problems (morning/evening sun → shadow direction)
- Distance using Pythagoras (3-4-5, 5-12-13 triplets)
- Turn sequences (L/R/U-turn), net displacement
- Map-based: city grid, landmarks""",

    "coding-decoding": """Focus on PATTERN RECOGNITION:
- Letter shifting (+1, -2, reverse, skip)
- Number coding (position in alphabet, prime/composite)
- Symbol substitution (⊕, ⊗, #, @ mapping)
- Mixed: letter-number-symbol combined
- New pattern: "If CAT=3120, DOG=?" (position + reverse)""",

    "series-completion": """Focus on MULTI-LEVEL patterns:
- Difference of differences (2nd/3rd order)
- Alternating series (two interleaved sequences)
- Prime/fibonacci/square/cube based
- Figure series: rotation, reflection, add/remove elements
- Wrong number identification (not just completion)""",

    "analogies": """Focus on RELATIONSHIP TYPES:
- Synonym/Antonym, Cause-Effect, Part-Whole, Tool-Worker
- Degree (hot:scorching :: cold:freezing)
- Number: 12:144 :: 13:? (square, cube, n*(n+1))
- Letter: ABC:ZYX :: DEF:? (reverse position)""",

    "puzzles": """Focus on CONSTRAINT SATISFACTION:
- Linear/Circular seating (facing in/out, dual row)
- Scheduling: days-months, floors-flats, boxes-stacking
- Conditional: "If A then B", "Either A or B but not both"
- 4-6 variables, 8-12 clues, unique solution""",

    "reading-comprehension": """Focus on PASSAGE-BASED inference:
- 150-300 word passages (tech/business/science topics)
- Question types: Main idea, Inference, Tone, Vocabulary in context, Title
- NO outside knowledge needed — answer from passage only
- Include "EXCEPT" and "NOT" questions""",

    "para-jumbles": """Focus on COHERENCE MARKERS:
- 4-6 sentences, identify opening/closing
- Pronoun antecedents, transition words (however, therefore, moreover)
- Chronological/logical flow, example-general-specific
- New pattern: "Odd sentence out" (5 sentences, 4 form paragraph)""",

    "sentence-correction": """Focus on GRAMMAR RULES tested in placements:
- Subject-verb agreement (collective nouns, intervening phrases)
- Parallelism (list items, comparisons, correlative conjunctions)
- Modifier placement (dangling/misplaced, only/just/even)
- Pronoun case/antecedent, verb tense consistency
- Idioms: 'not only...but also', 'between...and'""",

    "vocabulary": """Focus on CONTEXTUAL usage:
- Synonyms/Antonyms in sentence context (not isolated)
- Analogy: WORD1:WORD2 :: WORD3:? (degree, function, characteristic)
- Cloze test: 5-8 blanks in coherent passage
- Confusable words: affect/effect, imply/infer, complement/compliment""",

    "fill-in-blanks": """Focus on STRUCTURAL clues:
- Single blank: grammar (preposition, tense, form) + meaning
- Double blank: parallel structure, contrast/similarity markers
- Preposition-dependent verbs/adjectives
- Phrasal verbs in context""",

    "critical-reasoning": """Focus on ARGUMENT STRUCTURE:
- Assumption: necessary vs sufficient, negation test
- Strengthen/Weaken: alternative cause, reverse causality
- Inference: must be true, could be true
- Flaw: circular, sampling, correlation≠causation, false dilemma
- Boldface: role of statements (evidence/conclusion/counter)""",

    "data-interpretation": """Focus on CALCULATION SPEED:
- Table/Bar/Line/Pie/Radar charts + caselets (paragraph data)
- % change, ratio, average, growth rate (CAGR)
- Approximation: "closest to" options, eliminate by magnitude
- Multi-chart correlation (table + pie, line + bar)""",
}


async def generate_aptitude_questions(
    category: str,
    difficulty: str,
    count: int,
) -> Dict[str, Any]:
    sub_guidelines = APTITUDE_SUB_CATEGORY_GUIDELINES.get(category, "")

    system_prompt = f"""You are an expert aptitude test question writer for campus placement preparation.
Category: {category}
Difficulty: {difficulty}
Number of questions: {count}

Generate {count} multiple-choice questions (MCQs) appropriate for campus placement tests.
Favor questions that require 2-4 steps of reasoning, not one-line trivia.

CATEGORY GUIDELINES:
- quant: Quantitative aptitude (math, percentages, profit/loss, time-speed-distance, probability, permutations)
- quant-shortcuts: SPEED TRICKS — Vedic math, approximation, %/ratio shortcuts, named techniques
- logical: Logical reasoning (series, analogies, coding-decoding, blood relations, direction sense, syllogisms)
- syllogisms: VENN DIAGRAM method, 2/3 statement, "Only a few" patterns
- blood-relations: FAMILY TREE diagramming, coded relations, multi-generation
- direction-sense: COORDINATE/VECTOR visualization, shadow problems, turn sequences
- coding-decoding: PATTERN RECOGNITION, letter/number/symbol/mixed
- series-completion: MULTI-LEVEL patterns, difference-of-differences, alternating
- analogies: RELATIONSHIP TYPES (synonym, cause-effect, part-whole, degree)
- puzzles: CONSTRAINT SATISFACTION, seating/scheduling/floor/box
- verbal: Verbal ability (grammar, vocabulary, comprehension)
- reading-comprehension: PASSAGE-BASED inference, 150-300 words, main idea/inference/tone
- para-jumbles: COHERENCE MARKERS, pronoun antecedents, transition words, odd-one-out
- sentence-correction: GRAMMAR RULES (SVA, parallelism, modifiers, pronouns, idioms)
- vocabulary: CONTEXTUAL usage, synonyms/antonyms in sentence, analogies, cloze
- fill-in-blanks: STRUCTURAL clues, single/double blank, phrasal verbs
- critical-reasoning: ARGUMENT STRUCTURE (assumption, strengthen/weaken, inference, flaw, boldface)
- technical: Programming basics, data structures, OS, DBMS, networking
- data-interpretation: CALCULATION SPEED, charts/tables/caselets, % change/ratio/growth

{sub_guidelines}

Each question must have exactly 4 options (A, B, C, D).
Questions should be realistic and similar to TCS, Infosys, Wipro, Cognizant placement papers.
Distractors should be plausible and test conceptual understanding, not random wrong answers.

Each question must include 2-5 company tags from this pool indicating which companies have asked similar questions:
TCS, Infosys, Wipro, Cognizant, HCL Tech, Accenture, Capgemini, Tech Mahindra, L&T Infotech, Mphasis, Hexaware, IBM, Flipkart, Zomato, Razorpay, Google, Microsoft, Amazon

Mass recruiters (TCS, Infosys, Wipro, Cognizant) should appear more frequently (~30% more often).

The output MUST be valid JSON with this exact structure:
{{
    "questions": [
        {{
            "question": "Question text here?",
            "options": {{
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
            }},
            "correct_answer": "B",
            "explanation": "Detailed explanation of the correct answer",
            "topic": "sub-topic name",
            "difficulty": "{difficulty}",
            "companies": ["TCS", "Infosys", "Wipro"]
        }}
    ]
}}

Each question must have exactly 4 options.
Correct answer must be one of "A", "B", "C", "D".
Provide clear explanations for all answers.
Each question must have 2-5 company tags from the pool above.

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate {count} {difficulty} {category} aptitude questions."},
    ]

    result = await chat_completion(messages, max_tokens=6000)
    parsed = parse_json(result)

    parsed.setdefault("questions", [])
    for q in parsed["questions"]:
        q.setdefault("question", "")
        q.setdefault("options", {"A": "", "B": "", "C": "", "D": ""})
        q.setdefault("correct_answer", "A")
        q.setdefault("explanation", "")
        q.setdefault("topic", category)
        q.setdefault("difficulty", difficulty)
        if not q.get("companies"):
            q["companies"] = assign_companies()

    return parsed


async def evaluate_aptitude_answer(
    question: str,
    selected_option: str,
    correct_answer: str,
) -> Dict[str, Any]:
    is_correct = selected_option.upper().strip() == correct_answer.upper().strip()

    system_prompt = f"""You are an aptitude test evaluator.

Question: {question}
Selected Answer: {selected_option}
Correct Answer: {correct_answer}

Generate a brief explanation of why the correct answer is correct.
The output MUST be valid JSON:
{{
    "is_correct": {"true" if is_correct else "false"},
    "correct_answer": "{correct_answer}",
    "explanation": "Brief explanation of why this is the correct answer"
}}

Return ONLY the JSON object."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Evaluate: Selected={selected_option}, Correct={correct_answer}"},
    ]

    result = await chat_completion(messages)
    parsed = parse_json(result)

    parsed["is_correct"] = is_correct
    parsed.setdefault("correct_answer", correct_answer)
    parsed.setdefault("explanation", f"The correct answer is {correct_answer}.")

    return parsed