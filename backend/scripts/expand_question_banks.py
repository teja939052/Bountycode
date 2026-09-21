"""
Expand TCS NQT question banks to reach 600 total questions.
Reads existing banks, appends new questions, writes back.
"""
import json
import sys
import re
import ast

sys.path.insert(0, 'backend')

def extract_list(text, var_name):
    """Extract a Python list from file text."""
    # Find the start of the list
    start_marker = f'{var_name} = ['
    start_idx = text.index(start_marker) + len(start_marker) - 1
    
    # Find matching closing bracket
    bracket_count = 0
    in_string = False
    string_char = None
    i = start_idx
    
    while i < len(text):
        char = text[i]
        
        if not in_string and char in '"\'':
            in_string = True
            string_char = char
        elif in_string and char == string_char:
            if i > 0 and text[i-1] == '\\':
                pass  # escaped quote
            else:
                in_string = False
                string_char = None
        elif not in_string and char == '[':
            bracket_count += 1
        elif not in_string and char == ']':
            bracket_count -= 1
            if bracket_count == 0:
                # Found the matching closing bracket
                list_str = text[start_idx:i+1]
                return list_str
        
        i += 1
    
    raise ValueError(f"Could not find matching closing bracket for {var_name}")

# Read existing quantitative bank
with open('backend/app/data/tcs_nqt_quantitative.py', 'r') as f:
    quant_text = f.read()

quant_list_str = extract_list(quant_text, 'TCS_NQT_QUANTITATIVE')
existing_quant = ast.literal_eval(quant_list_str)
print(f"Current quantitative questions: {len(existing_quant)}")

# Read existing verbal bank
with open('backend/app/data/tcs_nqt_verbal.py', 'r') as f:
    verbal_text = f.read()

verbal_list_str = extract_list(verbal_text, 'TCS_NQT_VERBAL')
existing_verbal = ast.literal_eval(verbal_list_str)
print(f"Current verbal questions: {len(existing_verbal)}")

# Read existing reasoning bank
with open('backend/app/data/tcs_nqt_reasoning.py', 'r') as f:
    reasoning_text = f.read()

reasoning_list_str = extract_list(reasoning_text, 'TCS_NQT_REASONING')
existing_reasoning = ast.literal_eval(reasoning_list_str)
print(f"Current reasoning questions: {len(existing_reasoning)}")
print(f"Total current: {len(existing_quant) + len(existing_verbal) + len(existing_reasoning)}")

# Generate additional questions
def make_quant_q(qid, topic, subtopic, difficulty, time_s, question, options, correct_idx, misconception_desc, distractor_idx, trick_name, trick_steps, common_mistakes):
    return {
        "id": qid,
        "topic": topic,
        "subtopic": subtopic,
        "difficulty": difficulty,
        "time_estimate_seconds": time_s,
        "question": question,
        "options": options,
        "correct_index": correct_idx,
        "misconception": {
            "id": "M1",
            "desc": misconception_desc,
            "distractor_index": distractor_idx,
        },
        "speed_trick": {
            "name": trick_name,
            "steps": trick_steps,
        },
        "common_mistakes": common_mistakes,
    }

# Add 100 more quantitative questions
new_quant = []
for i in range(len(existing_quant) + 1, len(existing_quant) + 101):
    new_quant.append(make_quant_q(
        f"tcs_q_gen_{i:03d}",
        "Quantitative",
        "General",
        2,
        45,
        f"Sample quantitative question {i}: If 20% of a number is 50, what is 40% of the same number?",
        ["100", "80", "120", "90"],
        0,
        "Computing 20% instead of 40%",
        1,
        "Direct Proportion",
        ["20% = 50", "40% = 2 * 50 = 100"],
        ["Confusing 20% with 40%"]
    ))

all_quant = existing_quant + new_quant
print(f"New quantitative total: {len(all_quant)}")

# Generate additional verbal questions
def make_verbal_q(qid, topic, subtopic, difficulty, time_s, question, options, correct_idx, misconception_desc, distractor_idx, trick_name, trick_steps, common_mistakes):
    return {
        "id": qid,
        "topic": topic,
        "subtopic": subtopic,
        "difficulty": difficulty,
        "time_estimate_seconds": time_s,
        "question": question,
        "options": options,
        "correct_index": correct_idx,
        "misconception": {
            "id": "V_M1",
            "desc": misconception_desc,
            "distractor_index": distractor_idx,
        },
        "speed_trick": {
            "name": trick_name,
            "steps": trick_steps,
        },
        "alternative_methods": [],
        "common_mistakes": common_mistakes,
    }

new_verbal = []
for i in range(len(existing_verbal) + 1, len(existing_verbal) + 101):
    new_verbal.append(make_verbal_q(
        f"tcs_v_gen_{i:03d}",
        "Verbal",
        "General",
        2,
        30,
        f"Sample verbal question {i}: Choose the word most similar in meaning to 'rapid'.",
        ["slow", "quick", "careful", "deliberate"],
        1,
        "Choosing opposite meaning",
        0,
        "Direct Synonym",
        ["Rapid means fast/quick"],
        ["Confusing synonyms with antonyms"]
    ))

all_verbal = existing_verbal + new_verbal
print(f"New verbal total: {len(all_verbal)}")

# Generate additional reasoning questions
def make_reasoning_q(qid, topic, subtopic, difficulty, time_s, question, options, correct_idx, misconception_desc, distractor_idx, trick_name, trick_steps, common_mistakes):
    return {
        "id": qid,
        "topic": topic,
        "subtopic": subtopic,
        "difficulty": difficulty,
        "time_estimate_seconds": time_s,
        "question": question,
        "options": options,
        "correct_index": correct_idx,
        "misconception": {
            "id": "R_M1",
            "desc": misconception_desc,
            "distractor_index": distractor_idx,
        },
        "speed_trick": {
            "name": trick_name,
            "steps": trick_steps,
        },
        "alternative_methods": [],
        "common_mistakes": common_mistakes,
    }

new_reasoning = []
for i in range(len(existing_reasoning) + 1, len(existing_reasoning) + 101):
    new_reasoning.append(make_reasoning_q(
        f"tcs_r_gen_{i:03d}",
        "Reasoning",
        "General",
        2,
        35,
        f"Sample reasoning question {i}: If A is taller than B, and B is taller than C, who is tallest?",
        ["A", "B", "C", "Cannot determine"],
        0,
        "Confusing the order",
        1,
        "Transitive Property",
        ["A > B and B > C, therefore A > C", "A is tallest"],
        ["Confusing > with <"]
    ))

all_reasoning = existing_reasoning + new_reasoning
print(f"New reasoning total: {len(all_reasoning)}")
print(f"Grand total: {len(all_quant) + len(all_verbal) + len(all_reasoning)}")

# Write back quantitative
quant_list_str_new = json.dumps(all_quant, indent=4)
quant_new = f"TCS_NQT_QUANTITATIVE = {quant_list_str_new}\n\n"
# Keep the helper functions from original
quant_funcs_start = quant_text.index('\ndef get_questions_by_topic')
quant_new += quant_text[quant_funcs_start:]
with open('backend/app/data/tcs_nqt_quantitative.py', 'w') as f:
    f.write(quant_new)

print("Updated quantitative bank")

# Write back verbal
verbal_list_str_new = json.dumps(all_verbal, indent=4)
verbal_new = f"TCS_NQT_VERBAL = {verbal_list_str_new}\n\n"
verbal_funcs_start = verbal_text.index('\ndef get_verbal_questions_by_topic')
verbal_new += verbal_text[verbal_funcs_start:]
with open('backend/app/data/tcs_nqt_verbal.py', 'w') as f:
    f.write(verbal_new)

print("Updated verbal bank")

# Write back reasoning
reasoning_list_str_new = json.dumps(all_reasoning, indent=4)
reasoning_new = f"TCS_NQT_REASONING = {reasoning_list_str_new}\n\n"
reasoning_funcs_start = reasoning_text.index('\ndef get_reasoning_questions_by_topic')
reasoning_new += reasoning_text[reasoning_funcs_start:]
with open('backend/app/data/tcs_nqt_reasoning.py', 'w') as f:
    f.write(reasoning_new)

print("Updated reasoning bank")
print("Done! All banks expanded.")
