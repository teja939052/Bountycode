"""
Concept Clarity Slice: Trie / Prefix Tree
==========================================

A trie is a tree where each edge is a character and each path from root to
node spells a word. It answers "does this prefix exist?" in O(prefix length)
instead of scanning every word.

Misconceptions attacked:
  1. "Tries need a node per character" — yes, but nodes are shared across words
  2. "Trie is the same as BST" — no; tries compare by prefix, not by value
  3. "Trie search is O(log n)" — no; it is O(L) where L is word length
"""
from typing import Dict, Any

TRIE_SLICE: Dict[str, Any] = {
    "lesson_id": "trie_prefix_tree",
    "module_id": "dsa:trie",
    "title": "The Prefix Router",
    "description": "Learn how tries store shared prefixes and answer prefix queries in O(L).",
    "difficulty": "medium",
    "est_minutes": 15,
    "xp_reward": 250,
    "skills_taught": ["trie", "prefix", "strings", "search"],
    "srs_concept_tag": "dsa:trie",
    "story_context": {
        "title": "The Prefix Router",
        "narration": (
            "In the city of Lexica, every street name shares a common signpost. "
            "Instead of writing every name in full, the signs branch only where names "
            "diverge. That branching structure is exactly a trie."
        ),
        "setting": "lexica_signposts",
        "character": "Signkeeper Miri",
        "intro_text": (
            "Welcome. Every word here is a path through shared signposts. "
            "Follow the letters; when the path ends, the word exists."
        ),
    },
    "discovery": {
        "title": "Shared Branches",
        "steps": [
            {
                "action": "inspect_signpost",
                "narration": (
                    "Three words share the first two letters: 'cat', 'car', 'card'. "
                    "The trie reuses the 'c' → 'a' path, then branches at 't' vs 'r'."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "words = ['cat', 'car', 'card']\n# Shared prefix: ca\nprint('Shared:', words[0][:2])",
                    "expected_output": "Shared: ca",
                    "hint": "Look at the first two characters of every word.",
                },
            },
            {
                "action": "insert_word",
                "narration": (
                    "Inserting 'cat' creates nodes for c → a → t. Inserting 'car' reuses "
                    "c → a and adds r. No duplicate c or a nodes."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nroot = TrieNode()\nfor ch in 'cat':\n    root.children.setdefault(ch, TrieNode())\nprint('Nodes after cat:', len(root.children) + sum(len(n.children) for n in root.children.values()))",
                    "expected_output": "Nodes after cat: 3",
                    "hint": "Each new character can create one new node.",
                },
            },
        ],
    },
    "manipulation": {
        "title": "Build a Mini Trie",
        "steps": [
            {
                "action": "insert",
                "narration": "Insert 'do' and 'dot'. They share 'do', then branch on 't'.",
                "interaction": {
                    "type": "code",
                    "starter_code": "root = {}\n\n# Insert 'do'\n",
                    "solution": "root = {}\n\n# Insert 'do'\nnode = root\nfor ch in 'do':\n    node = node.setdefault(ch, {})\nnode['end'] = True\n\n# Insert 'dot'\nnode = root\nfor ch in 'dot':\n    node = node.setdefault(ch, {})\nnode['end'] = True\n",
                    "expected_output": None,
                    "hint": "Use setdefault to reuse existing branches.",
                },
            },
        ],
    },
    "code": {
        "title": "Trie Insert and Search",
        "starter_code": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n\n    def insert(self, word: str) -> None:\n        # TODO: walk/create nodes for each character\n        pass\n\n    def search(self, word: str) -> bool:\n        # TODO: return True only if the full word exists\n        pass\n",
        "solution": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n\n    def insert(self, word: str) -> None:\n        node = self.root\n        for ch in word:\n            node = node.children.setdefault(ch, TrieNode())\n        node.is_end = True\n\n    def search(self, word: str) -> bool:\n        node = self.root\n        for ch in word:\n            if ch not in node.children:\n                return False\n            node = node.children[ch]\n        return node.is_end\n",
        "expected_output": None,
    },
    "checks": [
        r"def insert\(",
        r"def search\(",
        r"setdefault\(",
        r"is_end",
    ],
    "success": {
        "before": "Empty signpost city — nobody can find anything.",
        "after": "Shared-prefix city — every lookup walks only the letters it needs.",
        "title": "Prefix Router — you can store and query words by shared prefix.",
        "lesson": "A trie turns many string comparisons into one short path walk.",
        "next": "Try prefix counting or autocomplete next.",
    },
}
