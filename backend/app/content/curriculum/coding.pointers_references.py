"""Lesson module — Pointers and References"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'coding.pointers_references',
            'module_id': 'coding.pointers_references',
            'title': 'Pointers and References',
            'description': 'Pointers and references are core to C/C++ and are frequently asked in technical interviews.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Pointers and References'],
            'srs_concept_tag': 'coding.pointers_references',
            'domain': 'coding',
            'captain_byte': {
            'intro': 'A pointer holds a memory address. A reference is an alias for an existing variable.',
            'correct': ['Right address.', 'Correct dereference.', 'Right reference usage.'],
            'wrong': ['A pointer stores an address, not the value.', 'References must be initialized and cannot be reseated.', 'Use * to access the pointed value.'],
            'after_break': 'You found the pointer error. Now fix the address or dereference.',
            'after_mastery': "You can now reason about pointers and references. That's interview-ready C/C++ skill.",
            'retry_prompt': 'Try again. Distinguish address from value.'
        },
            'story_context': {
            'title': 'Pointers and References',
            'narration': 'Pointers and references are core to C/C++ and are frequently asked in technical interviews.',
            'setting': 'pointers_and_references',
            'character': 'Captain Byte',
            'intro_text': 'Pointers and references are core to C/C++ and are frequently asked in technical interviews.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'transform'],
            'steps': [{
            'action': 'see_address',
            'narration': 'int x = 5; int *p = &x; p holds the address of x.',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'What does p contain?',
            'options': [{
            'id': 'a',
            'text': '5',
            'correct': False
        }, {
            'id': 'b',
            'text': 'Address of x',
            'correct': True
        }, {
            'id': 'c',
            'text': 'Name of x',
            'correct': False
        }, {
            'id': 'd',
            'text': 'Type of x',
            'correct': False
        }],
            'explanation': 'p is a pointer; it stores the address of x.'
        }
        }, {
            'action': 'see_dereference',
            'narration': '*p gives the value at the address stored in p.',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'If x=5 and p=&x, what is *p?',
            'options': [{
            'id': 'a',
            'text': 'Address',
            'correct': False
        }, {
            'id': 'b',
            'text': '5',
            'correct': True
        }, {
            'id': 'c',
            'text': 'p',
            'correct': False
        }, {
            'id': 'd',
            'text': 'x',
            'correct': False
        }],
            'explanation': '*p dereferences the pointer to get the value 5.'
        }
        }],
            'conclusion': 'Pointer = address holder. & gives address. * gives value. Reference = alias, no separate address.'
        },
            'understand': 'A pointer stores a memory address. & gets the address of a variable. * dereferences to get the value. A reference is an alias; it must be initialized and cannot be null or reseated.',
            'manipulate': {
            'prompt': 'Write C++ code that uses a pointer to change x from 5 to 10.',
            'answer': 'int x = 5;\nint *p = &x;\n*p = 10;',
            'hint': 'Dereference the pointer and assign the new value.',
            'interaction_kind': 'code_build'
        },
            'predict': {
            'prompt': 'What does this print?\nint x = 5;\nint &r = x;\nr = 10;\ncout << x;',
            'answer': '10',
            'options': ['5', '10', 'Address', 'Error'],
            'interaction_kind': 'trace_challenge'
        },
            'build': {
            'prompt': 'Write a C++ function swap that swaps two integers using references.',
            'answer': 'void swap(int &a, int &b) {\n    int temp = a;\n    a = b;\n    b = temp;\n}',
            'explanation': 'References act as aliases, so changes affect the original variables.',
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'A student dereferences an uninitialized pointer. What happens?',
            'common_mistake': 'Undefined behavior; likely crash or garbage value.',
            'correct_reasoning': 'Always initialize pointers before dereferencing.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix: int *p; *p = 10;',
            'correct_reasoning': 'Initialize pointer first: int x; int *p = &x; *p = 10;',
            'interaction_kind': 'code_fix'
        },
            'retrieval': {
            'prompt': 'What does & mean in C++?',
            'answer': 'Address-of operator',
            'alternative': ['gets address'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Write C++ code that passes an array to a function using a pointer.',
            'answer': 'void print(int *arr, int n) {\n    for (int i = 0; i < n; i++) {\n        cout << arr[i];\n    }\n}',
            'explanation': 'Array name decays to pointer. Use pointer arithmetic or indexing.',
            'interaction_kind': 'code_build'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'What does &x return?',
            'answer': 'Address of x',
            'options': ['Value of x', 'Address of x', 'Size of x', 'Type of x'],
            'explanation': '& is the address-of operator.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': 'What is a reference in C++?',
            'answer': 'An alias for another variable',
            'options': ['A pointer', 'An alias for another variable', 'A copy', 'A constant'],
            'explanation': 'A reference is an alternative name for an existing variable.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': 'Write a C++ function that returns the larger of two numbers using references.',
            'answer_format': 'text',
            'correct': 'int& max(int &a, int &b) {\n    return (a > b) ? a : b;\n}',
            'explanation': 'Return the larger reference.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['tcs_pointers', 'tcs_references'],
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS: What is a dangling pointer?',
            'answer_format': 'text',
            'correct': 'Pointer pointing to freed memory',
            'explanation': 'Dangling pointer points to memory that is no longer valid.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'coding_state_trace_error',
            'signature': 'Student thinks a pointer is the value itself instead of the address.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_address_versus_value'
        }, {
            'code': 'coding_state_trace_error',
            'signature': 'Student treats C++ references as pointers.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_synonym_versus_address'
        }],
            'srs_key_points': ['Pointer stores a memory address.', '& gives the address of a variable.', '* dereferences to get the value.', 'Reference is an alias, not a separate address.', 'Always initialize pointers before dereferencing.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'coding',
            'competency_id': 'pointers_and_references',
            'unlocks_next': [],
            'tower_badge': 'coding_pointers_and_references'
        }
        }

SLUG = 'coding.pointers_references'
