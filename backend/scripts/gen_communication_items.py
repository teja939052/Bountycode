"""Essay prompts, a scoring rubric and spoken-English tasks (intake candidates).

Wipro, Tech Mahindra, Infosys, Cognizant and LTIMindtree all test written or
spoken English, and the bank had no such content. These are PRACTICE material:
the rubric is a starting point to be calibrated against human-scored essays
before any score counts toward readiness (see the AI section of the design spec).
Nothing here is loaded by question_store.

Usage: python scripts/gen_communication_items.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "app", "data", "intake")

ESSAY_THEMES = {
    "technology": [
        "Artificial intelligence will create more jobs than it removes. Do you agree?",
        "Should students be allowed to use smartphones in college?",
        "The advantages and risks of working from home.",
        "How has online payment (UPI) changed everyday life in India?",
        "Social media: a tool for connection or a cause of distraction?",
        "Is it safe to share personal data with apps? Discuss.",
        "The role of coding skills for students of every branch.",
    ],
    "education_career": [
        "Marks or skills: which matters more for getting a job?",
        "Why continuous learning matters in an IT career.",
        "Is an engineering degree still necessary to work in technology?",
        "Describe how you handle pressure during exams or deadlines.",
        "The importance of internships for fresh graduates.",
        "Teamwork or individual talent: which leads to better results?",
        "What makes a good leader in a project team?",
    ],
    "society": [
        "How can cities reduce traffic congestion?",
        "The importance of saving water and what students can do.",
        "Should voting be made compulsory? Give your views.",
        "Does a healthy lifestyle improve work performance?",
        "How can we reduce plastic waste in our daily lives?",
        "The benefits of learning more than one language.",
        "Is online shopping better than visiting a market?",
    ],
    "workplace": [
        "Why honesty matters in the workplace.",
        "How should a new employee handle a mistake at work?",
        "The value of time management for a young professional.",
        "Relocating for a first job: opportunity or burden?",
        "How can companies support the mental well-being of employees?",
        "What does being a responsible engineer mean to you?",
        "Customer feedback: how should a company respond to criticism?",
    ],
}

RUBRIC = {
    "scale": "0 to 5 per criterion, total 20",
    "criteria": [
        {"id": "relevance_ideas", "name": "Relevance and ideas",
         "5": "Answers the prompt directly with 2 or more distinct, specific points and an example",
         "3": "On topic but points are general or repeated; no concrete example",
         "1": "Mostly off topic or only restates the prompt"},
        {"id": "structure", "name": "Structure",
         "5": "Clear opening, 2 to 3 organised body paragraphs, a conclusion that follows from the points",
         "3": "Some order but missing an opening or conclusion, or paragraphs mix ideas",
         "1": "One block of text with no visible order"},
        {"id": "language", "name": "Grammar and vocabulary",
         "5": "Few or no errors; varied, accurate word choice",
         "3": "Some errors that do not block meaning; simple vocabulary",
         "1": "Frequent errors that make sentences hard to follow"},
        {"id": "clarity", "name": "Clarity and length",
         "5": "Within the word range; every sentence adds something; easy to read",
         "3": "Within about 20% of the range, or some padding",
         "1": "Far below or above the range, or mostly filler"},
    ],
    "automatic_checks": [
        "word count inside the prompt's range", "no sentence repeated more than once",
        "at least 3 paragraphs", "mentions at least one key term from the prompt",
    ],
    "ai_use": "A model may apply this rubric and must quote the sentence behind each score. It must be checked "
              "against at least 30 human-scored essays before its score affects readiness.",
}

READ_ALOUD = [
    "The new software update will be released next Thursday.",
    "Please submit your assignment before the deadline.",
    "She sells sea shells by the sea shore.",
    "The manager scheduled a meeting to discuss the quarterly results.",
    "Technology has changed the way we learn and work.",
    "I would like to thank everyone for their support.",
    "The company offers training programs for fresh graduates.",
    "Regular practice improves both speed and accuracy.",
    "Our team successfully completed the project ahead of schedule.",
    "Could you please repeat the question more slowly?",
    "The weather forecast predicts heavy rain this weekend.",
    "Communication is an essential skill in every profession.",
]
REPEAT = [
    "I am a final year student.",
    "I enjoy solving problems with code.",
    "My strength is that I learn new things quickly.",
    "I completed a project on a library management system.",
    "I would like to work in a team that values learning.",
    "During my internship I learned how to write and test small programs.",
    "When I face a difficult problem, I break it into smaller steps and solve each one.",
    "I believe consistent daily practice is more useful than studying only before exams.",
    "Although the deadline was tight, our team divided the work and finished on time.",
    "I am excited about this opportunity because it matches my interest in building reliable software.",
]
ANSWER = [
    ("Introduce yourself in about 30 seconds.", 30),
    ("Tell me about your final year project in about 45 seconds.", 45),
    ("What are your strengths? Give one example.", 40),
    ("Why do you want to join this company?", 40),
    ("Describe a time you worked in a team.", 45),
    ("Where do you see yourself in three years?", 30),
    ("How do you handle a deadline when you have too much to do?", 40),
    ("Tell me about a mistake you made and what you learned.", 45),
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    essays, n = [], 0
    for theme, prompts in ESSAY_THEMES.items():
        for p in prompts:
            n += 1
            essays.append({
                "id": f"gen2-essay-{n:03d}", "type": "essay", "theme": theme, "prompt": p,
                "word_range": [200, 300], "minutes": 20,
                "companies": ["wipro", "tech_mahindra", "infosys", "cognizant", "ltimindtree"],
                "trust_status": "unverified", "source_bank": "handwritten_communication_v2",
            })
    spoken, m = [], 0
    for s in READ_ALOUD:
        m += 1
        spoken.append({"id": f"gen2-spoken-{m:03d}", "type": "read_aloud", "text": s, "max_seconds": 15})
    for s in REPEAT:
        m += 1
        spoken.append({"id": f"gen2-spoken-{m:03d}", "type": "repeat_sentence", "text": s,
                       "max_seconds": 20, "level": 1 + (len(s.split()) > 8) + (len(s.split()) > 14)})
    for q, secs in ANSWER:
        m += 1
        spoken.append({"id": f"gen2-spoken-{m:03d}", "type": "short_answer", "prompt": q, "max_seconds": secs})
    for t in spoken:
        t.update({"companies": ["cognizant", "tech_mahindra", "ltimindtree", "wipro"], "trust_status": "unverified",
                  "source_bank": "handwritten_communication_v2"})
    with open(os.path.join(OUT_DIR, "essay_prompts_v2.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"rubric": RUBRIC, "prompts": essays}, f, indent=2, ensure_ascii=False)
        f.write("\n")
    with open(os.path.join(OUT_DIR, "spoken_english_tasks_v2.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(spoken, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {len(essays)} essay prompts and {len(spoken)} spoken-English tasks")


if __name__ == "__main__":
    main()
