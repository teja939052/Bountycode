"""
Company-specific mock exam definitions.
Exact section structure, timing, and topics for each company.
"""

COMPANY_MOCKS = {
    "TCS_NQT_Foundation": {
        "id": "mock_tcs_nqt_foundation",
        "company": "TCS",
        "exam": "NQT Foundation",
        "duration_minutes": 75,
        "sections": [
            {
                "name": "Numerical Ability",
                "question_count": 20,
                "duration_minutes": 25,
                "negative_marking": False,
                "topics": [
                    "Percentages",
                    "Profit and Loss",
                    "Ratio",
                    "Time and Work",
                    "TSD",
                    "Averages",
                    "Number System"
                ]
            },
            {
                "name": "Reasoning Ability",
                "question_count": 20,
                "duration_minutes": 25,
                "negative_marking": False,
                "topics": [
                    "Series",
                    "Coding-Decoding",
                    "Blood Relations",
                    "Seating Arrangement",
                    "Syllogisms"
                ]
            },
            {
                "name": "Verbal Ability",
                "question_count": 25,
                "duration_minutes": 25,
                "negative_marking": False,
                "topics": [
                    "RC",
                    "Error Spotting",
                    "Sentence Completion",
                    "Para Jumbles",
                    "Synonyms"
                ]
            }
        ],
        "total_questions": 65,
        "cutoff_hint": "60-65% overall, sectional cutoffs apply"
    },
    "TCS_NQT_Advanced": {
        "id": "mock_tcs_nqt_advanced",
        "company": "TCS",
        "exam": "NQT Advanced",
        "duration_minutes": 60,
        "sections": [
            {
                "name": "Advanced Quantitative & Reasoning",
                "question_count": 15,
                "duration_minutes": 25,
                "negative_marking": False,
                "topics": [
                    "Advanced Quant",
                    "Critical Reasoning",
                    "Data Sufficiency"
                ]
            },
            {
                "name": "Advanced Coding",
                "question_count": 2,
                "duration_minutes": 35,
                "negative_marking": False,
                "topics": [
                    "Arrays",
                    "Strings",
                    "Basic Algorithms"
                ]
            }
        ],
        "total_questions": 17,
        "cutoff_hint": "Digital: 70%+, Prime: 80%+"
    },
    "Infosys_InfyTQ": {
        "id": "mock_infosys_infytq",
        "company": "Infosys",
        "exam": "InfyTQ",
        "duration_minutes": 120,
        "sections": [
            {
                "name": "Python/Java MCQ",
                "question_count": 30,
                "duration_minutes": 30,
                "negative_marking": False,
                "topics": [
                    "Python Basics",
                    "OOP",
                    "Data Structures",
                    "Algorithms"
                ]
            },
            {
                "name": "Aptitude",
                "question_count": 20,
                "duration_minutes": 30,
                "negative_marking": False,
                "topics": [
                    "Quantitative",
                    "Logical Reasoning"
                ]
            },
            {
                "name": "Coding",
                "question_count": 2,
                "duration_minutes": 60,
                "negative_marking": False,
                "topics": [
                    "Python Coding",
                    "Problem Solving"
                ]
            }
        ],
        "total_questions": 52,
        "cutoff_hint": "SE: 65%+, DSE: 75%+"
    },
    "Wipro_NLTH": {
        "id": "mock_wipro_nlth",
        "company": "Wipro",
        "exam": "NLTH (National Talent Hunt)",
        "duration_minutes": 128,
        "sections": [
            {
                "name": "Quantitative Ability",
                "question_count": 16,
                "duration_minutes": 16,
                "negative_marking": False,
                "topics": [
                    "Percentages",
                    "Profit Loss",
                    "TSD",
                    "Time Work",
                    "Averages"
                ]
            },
            {
                "name": "Logical Ability",
                "question_count": 14,
                "duration_minutes": 18,
                "negative_marking": False,
                "topics": [
                    "Series",
                    "Coding-Decoding",
                    "Blood Relations",
                    "Syllogisms"
                ]
            },
            {
                "name": "Verbal Ability",
                "question_count": 22,
                "duration_minutes": 14,
                "negative_marking": False,
                "topics": [
                    "RC",
                    "Grammar",
                    "Vocabulary",
                    "Sentence Completion"
                ]
            },
            {
                "name": "Written Communication",
                "question_count": 1,
                "duration_minutes": 20,
                "negative_marking": False,
                "topics": [
                    "Essay Writing"
                ]
            },
            {
                "name": "Coding Test",
                "question_count": 2,
                "duration_minutes": 60,
                "negative_marking": False,
                "topics": [
                    "Arrays",
                    "Strings",
                    "Patterns"
                ]
            }
        ],
        "total_questions": 55,
        "cutoff_hint": "70th percentile in each section"
    },
    "Accenture_Cognitive": {
        "id": "mock_accenture_cognitive",
        "company": "Accenture",
        "exam": "Cognitive Assessment",
        "duration_minutes": 90,
        "sections": [
            {
                "name": "Quantitative Aptitude",
                "question_count": 20,
                "duration_minutes": 30,
                "negative_marking": False,
                "topics": [
                    "Percentages",
                    "Ratio",
                    "TSD",
                    "Time Work",
                    "Profit Loss"
                ]
            },
            {
                "name": "Logical Reasoning",
                "question_count": 20,
                "duration_minutes": 30,
                "negative_marking": False,
                "topics": [
                    "Series",
                    "Puzzles",
                    "Coding-Decoding",
                    "Blood Relations"
                ]
            },
            {
                "name": "Verbal Ability",
                "question_count": 20,
                "duration_minutes": 30,
                "negative_marking": False,
                "topics": [
                    "RC",
                    "Grammar",
                    "Vocabulary"
                ]
            }
        ],
        "total_questions": 60,
        "cutoff_hint": "70th percentile overall"
    },
    "Cognizant_GenC": {
        "id": "mock_cognizant_genc",
        "company": "Cognizant",
        "exam": "GenC / GenC Next",
        "duration_minutes": 90,
        "sections": [
            {
                "name": "Quantitative",
                "question_count": 20,
                "duration_minutes": 30,
                "negative_marking": False,
                "topics": [
                    "Percentages",
                    "Ratio",
                    "TSD",
                    "Time Work",
                    "Averages"
                ]
            },
            {
                "name": "Logical",
                "question_count": 20,
                "duration_minutes": 30,
                "negative_marking": False,
                "topics": [
                    "Series",
                    "Coding-Decoding",
                    "Blood Relations",
                    "Syllogisms"
                ]
            },
            {
                "name": "Coding",
                "question_count": 2,
                "duration_minutes": 30,
                "negative_marking": False,
                "topics": [
                    "Arrays",
                    "Strings",
                    "Basic Algorithms"
                ]
            }
        ],
        "total_questions": 42,
        "cutoff_hint": "GenC: 60%+, GenC Next: 70%+"
    }
}


def get_mock_by_company(company: str) -> dict:
    """Get mock definition by company name."""
    for key, mock in COMPANY_MOCKS.items():
        if mock["company"].lower() == company.lower():
            return mock
    return None

def get_all_mocks() -> list:
    """Get all mock definitions."""
    return list(COMPANY_MOCKS.values())
