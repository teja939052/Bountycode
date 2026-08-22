"""Career RPG service -- the core game loop for PlacementPro."""
import math
from datetime import datetime, timezone
from app.database import gamification_collection, skill_graph_collection

CAREER_RANKS = [
    {"min_level": 1,   "max_level": 5,   "title": "Code Seed",       "icon": "\U0001f331", "color": "#22C55E", "tier": "beginner",    "description": "Planting the first lines of code"},
    {"min_level": 6,   "max_level": 10,  "title": "Code Apprentice",  "icon": "\U0001f527", "color": "#3B82F6", "tier": "beginner",    "description": "Learning the tools of the trade"},
    {"min_level": 11,  "max_level": 20,  "title": "Problem Solver",   "icon": "\u2694\ufe0f", "color": "#8B5CF6", "tier": "intermediate", "description": "Breaking through coding challenges"},
    {"min_level": 21,  "max_level": 30,  "title": "Algorithm Adept",  "icon": "\U0001f9e0", "color": "#F59E0B", "tier": "intermediate", "description": "Mastering algorithmic thinking"},
    {"min_level": 31,  "max_level": 40,  "title": "Software Builder", "icon": "\U0001f4bb", "color": "#EF4444", "tier": "advanced",     "description": "Building real software systems"},
    {"min_level": 41,  "max_level": 50,  "title": "Engineer",         "icon": "\U0001f680", "color": "#EC4899", "tier": "advanced",     "description": "Engineering solutions at scale"},
    {"min_level": 51,  "max_level": 65,  "title": "Interview Ready",  "icon": "\U0001f3c6", "color": "#F97316", "tier": "expert",       "description": "Ready to face any interview"},
    {"min_level": 66,  "max_level": 80,  "title": "Placement Ready",  "icon": "\U0001f48e", "color": "#06B6D4", "tier": "expert",       "description": "Polished and placement-ready"},
    {"min_level": 81,  "max_level": 100, "title": "Elite Candidate",  "icon": "\U0001f451", "color": "#A855F7", "tier": "legend",       "description": "Top-tier candidate, ready for FAANG"},
]


def get_career_rank(level):
    for rank in CAREER_RANKS:
        if rank["min_level"] <= level <= rank["max_level"]:
            span = max(1, rank["max_level"] - rank["min_level"])
            return {
                **rank,
                "progress_in_rank": (level - rank["min_level"]) / span,
                "xp_to_next_rank": ((rank["max_level"] + 1) ** 2) * 50 - (level ** 2) * 50 if rank["max_level"] < 100 else 0,
            }
    return {**CAREER_RANKS[0], "progress_in_rank": 0, "xp_to_next_rank": 50}


def get_rank_ladder():
    return CAREER_RANKS


SKILL_TREE = {
    "root": {"id": "root", "name": "Software Engineer", "icon": "\U0001f4bb", "category": "root", "x": 400, "y": 40, "prerequisites": [], "mastery_required": 0, "skill_domain": None, "description": "Your journey begins here"},
    "prog_fundamentals": {"id": "prog_fundamentals", "name": "Programming", "icon": "\u2328\ufe0f", "category": "branch", "x": 150, "y": 130, "prerequisites": ["root"], "mastery_required": 0, "skill_domain": ("dsa", "arrays"), "description": "Master the building blocks of code"},
    "variables": {"id": "variables", "name": "Variables", "icon": "\U0001f4e6", "category": "leaf", "x": 60, "y": 220, "prerequisites": ["prog_fundamentals"], "mastery_required": 5, "skill_domain": ("dsa", "arrays"), "description": "Store and retrieve data"},
    "control_flow": {"id": "control_flow", "name": "Control Flow", "icon": "\U0001f500", "category": "leaf", "x": 150, "y": 220, "prerequisites": ["prog_fundamentals"], "mastery_required": 10, "skill_domain": ("dsa", "recursion"), "description": "Branch, loop, and repeat"},
    "functions": {"id": "functions", "name": "Functions", "icon": "\U0001f9e9", "category": "leaf", "x": 240, "y": 220, "prerequisites": ["control_flow"], "mastery_required": 20, "skill_domain": ("dsa", "recursion"), "description": "Encapsulate reusable logic"},
    "dsa_realm": {"id": "dsa_realm", "name": "DSA", "icon": "\u2694\ufe0f", "category": "branch", "x": 400, "y": 130, "prerequisites": ["root"], "mastery_required": 5, "skill_domain": ("dsa", "arrays"), "description": "Data structures and algorithms"},
    "arrays_strings": {"id": "arrays_strings", "name": "Arrays & Strings", "icon": "\U0001f4ca", "category": "leaf", "x": 310, "y": 220, "prerequisites": ["dsa_realm"], "mastery_required": 10, "skill_domain": ("dsa", "arrays"), "description": "Master linear data structures"},
    "linked_lists": {"id": "linked_lists", "name": "Linked Lists", "icon": "\U0001f517", "category": "leaf", "x": 400, "y": 220, "prerequisites": ["arrays_strings"], "mastery_required": 15, "skill_domain": ("dsa", "linked_lists"), "description": "Connect nodes in sequence"},
    "trees_graphs": {"id": "trees_graphs", "name": "Trees & Graphs", "icon": "\U0001f333", "category": "leaf", "x": 490, "y": 220, "prerequisites": ["linked_lists"], "mastery_required": 30, "skill_domain": ("dsa", "trees"), "description": "Navigate hierarchical data"},
    "sorting_searching": {"id": "sorting_searching", "name": "Sorting & Searching", "icon": "\U0001f50d", "category": "leaf", "x": 310, "y": 310, "prerequisites": ["arrays_strings"], "mastery_required": 20, "skill_domain": ("dsa", "sorting"), "description": "Order and find efficiently"},
    "greedy_recursion": {"id": "greedy_recursion", "name": "Greedy & Recursion", "icon": "\U0001f504", "category": "leaf", "x": 490, "y": 310, "prerequisites": ["trees_graphs"], "mastery_required": 35, "skill_domain": ("dsa", "greedy"), "description": "Think recursively and greedily"},
    "dynamic_programming": {"id": "dynamic_programming", "name": "Dynamic Programming", "icon": "\U0001f9ee", "category": "leaf", "x": 400, "y": 310, "prerequisites": ["trees_graphs", "functions"], "mastery_required": 45, "skill_domain": ("dsa", "dynamic_programming"), "description": "Optimize with memoization"},
    "cs_fundamentals": {"id": "cs_fundamentals", "name": "CS Fundamentals", "icon": "\U0001f4da", "category": "branch", "x": 650, "y": 130, "prerequisites": ["root"], "mastery_required": 5, "skill_domain": ("aptitude", "quantitative"), "description": "Core computer science knowledge"},
    "dbms": {"id": "dbms", "name": "DBMS", "icon": "\U0001f5c4\ufe0f", "category": "leaf", "x": 560, "y": 220, "prerequisites": ["cs_fundamentals"], "mastery_required": 15, "skill_domain": ("system_design", "databases"), "description": "Relational and NoSQL databases"},
    "os": {"id": "os", "name": "Operating Systems", "icon": "\U0001f5a5\ufe0f", "category": "leaf", "x": 650, "y": 220, "prerequisites": ["cs_fundamentals"], "mastery_required": 15, "skill_domain": ("system_design", "scaling"), "description": "Processes, threads, and memory"},
    "networks": {"id": "networks", "name": "Computer Networks", "icon": "\U0001f310", "category": "leaf", "x": 740, "y": 220, "prerequisites": ["cs_fundamentals"], "mastery_required": 15, "skill_domain": ("system_design", "load_balancing"), "description": "TCP/IP, HTTP, and protocols"},
    "system_design": {"id": "system_design", "name": "System Design", "icon": "\U0001f3d7\ufe0f", "category": "leaf", "x": 650, "y": 310, "prerequisites": ["dbms", "os", "networks"], "mastery_required": 50, "skill_domain": ("system_design", "high_level_design"), "description": "Design scalable systems"},
    "interview_mastery": {"id": "interview_mastery", "name": "Interview", "icon": "\U0001f3af", "category": "branch", "x": 400, "y": 420, "prerequisites": ["dynamic_programming", "system_design"], "mastery_required": 55, "skill_domain": ("behavioral", "communication"), "description": "Ace the interview process"},
    "behavioral": {"id": "behavioral", "name": "Behavioral", "icon": "\U0001f5e3\ufe0f", "category": "leaf", "x": 310, "y": 510, "prerequisites": ["interview_mastery"], "mastery_required": 60, "skill_domain": ("behavioral", "leadership"), "description": "STAR method and leadership"},
    "aptitude": {"id": "aptitude", "name": "Aptitude", "icon": "\U0001f9ee", "category": "leaf", "x": 490, "y": 510, "prerequisites": ["interview_mastery"], "mastery_required": 60, "skill_domain": ("aptitude", "quantitative"), "description": "Quant, logic, and verbal"},
    "placement_ready": {"id": "placement_ready", "name": "Placement Ready", "icon": "\U0001f451", "category": "mastery", "x": 400, "y": 600, "prerequisites": ["behavioral", "aptitude"], "mastery_required": 80, "skill_domain": None, "description": "You are ready for placement"},
}


def get_skill_tree(user_level=1):
    nodes = []
    for nid, node in SKILL_TREE.items():
        prereqs_met = all(SKILL_TREE[p]["mastery_required"] <= user_level for p in node["prerequisites"] if p in SKILL_TREE)
        level_met = user_level >= node["mastery_required"]
        nodes.append({**node, "unlocked": prereqs_met and level_met, "prereqs_met": prereqs_met, "level_met": level_met})
    return {"nodes": nodes, "total_nodes": len(nodes), "unlocked_count": sum(1 for n in nodes if n["unlocked"])}


QUEST_CHAINS = [
    {"id": "binary_search_arc", "title": "The Binary Search Arc", "icon": "\U0001f3f9", "description": "Master the art of divide and conquer", "category": "dsa", "reward_xp": 500, "reward_badge": "binary_search_master", "unlock_level": 10, "steps": [
        {"id": "bs_1", "title": "Find the Hidden Number", "type": "solve", "target": 3, "category": "dsa", "skill": "binary_search", "description": "Solve 3 binary search problems"},
        {"id": "bs_2", "title": "Visualize the Search", "type": "visualize", "target": 1, "category": "dsa", "skill": "binary_search", "description": "Complete 1 visualizer challenge"},
        {"id": "bs_3", "title": "Predict the Algorithm", "type": "predict", "target": 5, "category": "dsa", "skill": "binary_search", "description": "Predict 5 algorithm outputs"},
        {"id": "bs_4", "title": "Debug the Broken Search", "type": "debug", "target": 3, "category": "dsa", "skill": "binary_search", "description": "Fix 3 buggy implementations"},
        {"id": "bs_5", "title": "Binary Search Boss", "type": "boss", "target": 1, "category": "dsa", "skill": "binary_search", "description": "Defeat the Binary Search Guardian"},
    ]},
    {"id": "graph_explorer", "title": "The Graph Explorer", "icon": "\U0001f5fa\ufe0f", "description": "Navigate the world of graphs and networks", "category": "dsa", "reward_xp": 600, "reward_badge": "graph_guardian", "unlock_level": 25, "steps": [
        {"id": "ge_1", "title": "Map the Territory", "type": "solve", "target": 5, "category": "dsa", "skill": "graphs", "description": "Solve 5 graph traversal problems"},
        {"id": "ge_2", "title": "Find Shortest Path", "type": "solve", "target": 3, "category": "dsa", "skill": "graphs", "description": "Solve 3 shortest path problems"},
        {"id": "ge_3", "title": "Detect Cycles", "type": "solve", "target": 3, "category": "dsa", "skill": "graphs", "description": "Solve 3 cycle detection problems"},
        {"id": "ge_4", "title": "Graph Boss", "type": "boss", "target": 1, "category": "dsa", "skill": "graphs", "description": "Defeat the Graph Guardian"},
    ]},
    {"id": "dp_master", "title": "The DP Dimension", "icon": "\U0001f9ee", "description": "Unlock the power of dynamic programming", "category": "dsa", "reward_xp": 700, "reward_badge": "dp_slayer", "unlock_level": 35, "steps": [
        {"id": "dp_1", "title": "Fibonacci Fundamentals", "type": "solve", "target": 3, "category": "dsa", "skill": "dynamic_programming", "description": "Solve 3 DP warm-up problems"},
        {"id": "dp_2", "title": "Knapsack Challenges", "type": "solve", "target": 5, "category": "dsa", "skill": "dynamic_programming", "description": "Solve 5 knapsack-family problems"},
        {"id": "dp_3", "title": "String DP", "type": "solve", "target": 3, "category": "dsa", "skill": "dynamic_programming", "description": "Solve 3 string DP problems"},
        {"id": "dp_4", "title": "DP Boss", "type": "boss", "target": 1, "category": "dsa", "skill": "dynamic_programming", "description": "Defeat the DP Wizard"},
    ]},
    {"id": "interview_gauntlet", "title": "The Interview Gauntlet", "icon": "\U0001f3df\ufe0f", "description": "Prove you are ready for any interview", "category": "interview", "reward_xp": 800, "reward_badge": "interview_champion", "unlock_level": 40, "steps": [
        {"id": "ig_1", "title": "Mock Interview", "type": "interview", "target": 1, "category": "behavioral", "skill": "communication", "description": "Complete a mock interview"},
        {"id": "ig_2", "title": "Resume Polish", "type": "resume", "target": 1, "category": "resume", "skill": "content_quality", "description": "Get 80+ ATS score"},
        {"id": "ig_3", "title": "Aptitude Test", "type": "aptitude", "target": 1, "category": "aptitude", "skill": "quantitative", "description": "Score 80%+ on aptitude"},
        {"id": "ig_4", "title": "System Design", "type": "system_design", "target": 1, "category": "system_design", "skill": "high_level_design", "description": "Complete a system design session"},
        {"id": "ig_5", "title": "Final Boss", "type": "boss", "target": 1, "category": "behavioral", "skill": "communication", "description": "Achieve 75%+ readiness"},
    ]},
    {"id": "code_warrior", "title": "Code Warriors Path", "icon": "\U0001f5e1\ufe0f", "description": "From beginner to coding champion", "category": "coding", "reward_xp": 400, "reward_badge": "code_warrior", "unlock_level": 5, "steps": [
        {"id": "cw_1", "title": "First Blood", "type": "solve", "target": 5, "category": "dsa", "skill": "arrays", "description": "Solve your first 5 problems"},
        {"id": "cw_2", "title": "Rising Blade", "type": "solve", "target": 10, "category": "dsa", "skill": "arrays", "description": "Solve 10 total problems"},
        {"id": "cw_3", "title": "Edge Master", "type": "solve", "target": 5, "category": "dsa", "skill": "sorting", "description": "Solve 5 sorting problems"},
        {"id": "cw_4", "title": "Warriors Oath", "type": "streak", "target": 7, "category": "streak", "skill": None, "description": "Maintain a 7-day streak"},
    ]},
]


def get_quest_chains(user_level=1, user_progress=None):
    user_progress = user_progress or {}
    completed_steps = set(user_progress.get("completed_steps", []))
    chains = []
    for chain in QUEST_CHAINS:
        unlocked = user_level >= chain["unlock_level"]
        done = sum(1 for s in chain["steps"] if f"{chain['id']}_{s['id']}" in completed_steps)
        total = len(chain["steps"])
        chains.append({**chain, "unlocked": unlocked, "completed_steps": done, "total_steps": total, "progress_pct": round(done / total * 100) if total > 0 else 0, "is_complete": done >= total})
    return chains


SKILL_BOSSES = {
    "arrays": {"id": "arrays_boss", "name": "The Array Sentinel", "icon": "\U0001f6e1\ufe0f", "skill_domain": ("dsa", "arrays"), "unlock_level": 10, "recommended_readiness": 30, "challenges": [{"type": "solve", "title": "Two Sum Variant", "difficulty": "easy", "xp": 30}, {"type": "solve", "title": "Sliding Window Max", "difficulty": "medium", "xp": 50}, {"type": "debug", "title": "Fix Array Merge", "difficulty": "medium", "xp": 40}, {"type": "predict", "title": "Trace the Output", "difficulty": "easy", "xp": 25}, {"type": "timed", "title": "Array Rotation", "difficulty": "hard", "xp": 60}], "pass_score": 70, "reward_xp": 200, "reward_badge": "array_sentinel"},
    "trees": {"id": "trees_boss", "name": "The Tree Keeper", "icon": "\U0001f333", "skill_domain": ("dsa", "trees"), "unlock_level": 25, "recommended_readiness": 45, "challenges": [{"type": "solve", "title": "BST Insert/Search", "difficulty": "medium", "xp": 40}, {"type": "solve", "title": "Tree Traversal", "difficulty": "medium", "xp": 45}, {"type": "predict", "title": "Trace Inorder", "difficulty": "medium", "xp": 35}, {"type": "debug", "title": "Fix Height Calc", "difficulty": "hard", "xp": 50}, {"type": "timed", "title": "Lowest Common Ancestor", "difficulty": "hard", "xp": 60}], "pass_score": 70, "reward_xp": 300, "reward_badge": "tree_keeper"},
    "graphs": {"id": "graphs_boss", "name": "The Graph Guardian", "icon": "\U0001f30f", "skill_domain": ("dsa", "graphs"), "unlock_level": 30, "recommended_readiness": 55, "challenges": [{"type": "solve", "title": "BFS Level Order", "difficulty": "medium", "xp": 45}, {"type": "solve", "title": "DFS Pathfinding", "difficulty": "hard", "xp": 55}, {"type": "debug", "title": "Fix Cycle Detection", "difficulty": "hard", "xp": 50}, {"type": "predict", "title": "Trace Dijkstra", "difficulty": "hard", "xp": 50}, {"type": "timed", "title": "Topological Sort", "difficulty": "expert", "xp": 70}], "pass_score": 75, "reward_xp": 400, "reward_badge": "graph_guardian"},
    "dynamic_programming": {"id": "dp_boss", "name": "The DP Wizard", "icon": "\U0001f9d9", "skill_domain": ("dsa", "dynamic_programming"), "unlock_level": 35, "recommended_readiness": 60, "challenges": [{"type": "solve", "title": "Fibonacci Memoization", "difficulty": "medium", "xp": 40}, {"type": "solve", "title": "0/1 Knapsack", "difficulty": "hard", "xp": 60}, {"type": "solve", "title": "Longest Common Subseq", "difficulty": "hard", "xp": 55}, {"type": "predict", "title": "Trace DP Table", "difficulty": "hard", "xp": 45}, {"type": "timed", "title": "Edit Distance", "difficulty": "expert", "xp": 75}], "pass_score": 75, "reward_xp": 500, "reward_badge": "dp_wizard"},
    "sorting": {"id": "sorting_boss", "name": "The Sort Master", "icon": "\U0001f503", "skill_domain": ("dsa", "sorting"), "unlock_level": 15, "recommended_readiness": 35, "challenges": [{"type": "solve", "title": "Quick Sort Impl", "difficulty": "medium", "xp": 40}, {"type": "solve", "title": "Merge Intervals", "difficulty": "hard", "xp": 50}, {"type": "debug", "title": "Fix Heap Sort", "difficulty": "medium", "xp": 40}, {"type": "predict", "title": "Trace Partition", "difficulty": "medium", "xp": 35}, {"type": "timed", "title": "Kth Largest Element", "difficulty": "hard", "xp": 55}], "pass_score": 70, "reward_xp": 250, "reward_badge": "sort_master"},
}


def get_skill_bosses(user_level=1, skill_graph=None):
    """Return bosses with unlock status based on BOTH level AND skill readiness.
    
    Bosses unlock when:
    1. User level >= unlock_level, AND
    2. Relevant skill category score >= recommended_readiness
    
    If skill_graph is provided, both conditions are checked.
    Otherwise, only level is checked (backward-compatible).
    """
    result = []
    for boss in SKILL_BOSSES.values():
        level_unlocked = user_level >= boss["unlock_level"]
        
        if skill_graph and boss.get("skill_domain"):
            cat, _skill = boss["skill_domain"]
            cat_data = skill_graph.get("categories", {}).get(cat, {})
            skill_score = cat_data.get("score", 0)
            readiness_unlocked = skill_score >= boss["recommended_readiness"]
        else:
            skill_score = 0
            readiness_unlocked = True  # No graph = don't gate on readiness
        
        result.append({
            **boss,
            "level_unlocked": level_unlocked,
            "readiness_unlocked": readiness_unlocked,
            "unlocked": level_unlocked and readiness_unlocked,
            "current_skill_score": round(skill_score, 1),
            "readiness_progress": round(min(100, (skill_score / boss["recommended_readiness"]) * 100), 1) if boss["recommended_readiness"] > 0 else 100,
        })
    return result


COMPANY_DUNGEONS = {
    "tcs": {"id": "tcs_dungeon", "name": "TCS SDE Dungeon", "icon": "\U0001f3ef", "company": "TCS", "min_readiness": 50, "reward_badge": "tcs_challenger", "gates": [
        {"id": "tcs_apt", "name": "Aptitude Gate", "icon": "\U0001f4dd", "type": "aptitude", "required_score": 65, "xp_reward": 80},
        {"id": "tcs_code", "name": "Coding Chamber", "icon": "\U0001f4bb", "type": "coding", "required_score": 70, "xp_reward": 100},
        {"id": "tcs_cs", "name": "CS Fundamentals", "icon": "\U0001f4da", "type": "system_design", "required_score": 60, "xp_reward": 70},
        {"id": "tcs_behave", "name": "Behavioral Hall", "icon": "\U0001f5e3\ufe0f", "type": "behavioral", "required_score": 65, "xp_reward": 60},
    ], "final_boss": {"id": "tcs_final", "name": "TCS OA Boss", "icon": "\U0001f479", "required_score": 70, "xp_reward": 150}},
    "infosys": {"id": "infosys_dungeon", "name": "Infosys SDE Dungeon", "icon": "\U0001f3e2", "company": "Infosys", "min_readiness": 55, "reward_badge": "infosys_challenger", "gates": [
        {"id": "inf_apt", "name": "Aptitude Gate", "icon": "\U0001f4dd", "type": "aptitude", "required_score": 70, "xp_reward": 80},
        {"id": "inf_code", "name": "Coding Chamber", "icon": "\U0001f4bb", "type": "coding", "required_score": 70, "xp_reward": 100},
        {"id": "inf_cs", "name": "CS Fundamentals", "icon": "\U0001f4da", "type": "system_design", "required_score": 65, "xp_reward": 70},
        {"id": "inf_behave", "name": "Behavioral Hall", "icon": "\U0001f5e3\ufe0f", "type": "behavioral", "required_score": 65, "xp_reward": 60},
    ], "final_boss": {"id": "inf_final", "name": "Infosys OA Boss", "icon": "\U0001f479", "required_score": 72, "xp_reward": 160}},
    "amazon": {"id": "amazon_dungeon", "name": "Amazon SDE Dungeon", "icon": "\U0001f3d4\ufe0f", "company": "Amazon", "min_readiness": 75, "reward_badge": "amazon_challenger", "gates": [
        {"id": "amz_apt", "name": "Aptitude Gate", "icon": "\U0001f4dd", "type": "aptitude", "required_score": 75, "xp_reward": 100},
        {"id": "amz_code", "name": "Coding Chamber", "icon": "\U0001f4bb", "type": "coding", "required_score": 80, "xp_reward": 120},
        {"id": "amz_cs", "name": "CS Fundamentals", "icon": "\U0001f4da", "type": "system_design", "required_score": 75, "xp_reward": 90},
        {"id": "amz_sd", "name": "System Design", "icon": "\U0001f3d7\ufe0f", "type": "system_design", "required_score": 80, "xp_reward": 110},
        {"id": "amz_behave", "name": "Leadership Principles", "icon": "\U0001f5e3\ufe0f", "type": "behavioral", "required_score": 80, "xp_reward": 100},
    ], "final_boss": {"id": "amz_final", "name": "Amazon Loop Boss", "icon": "\U0001f479", "required_score": 80, "xp_reward": 200}},
    "microsoft": {"id": "microsoft_dungeon", "name": "Microsoft SDE Dungeon", "icon": "\U0001f310", "company": "Microsoft", "min_readiness": 80, "reward_badge": "microsoft_challenger", "gates": [
        {"id": "ms_code", "name": "Coding Chamber", "icon": "\U0001f4bb", "type": "coding", "required_score": 85, "xp_reward": 130},
        {"id": "ms_sd", "name": "System Design", "icon": "\U0001f3d7\ufe0f", "type": "system_design", "required_score": 85, "xp_reward": 120},
        {"id": "ms_cs", "name": "CS Fundamentals", "icon": "\U0001f4da", "type": "system_design", "required_score": 80, "xp_reward": 100},
        {"id": "ms_behave", "name": "Behavioral Hall", "icon": "\U0001f5e3\ufe0f", "type": "behavioral", "required_score": 80, "xp_reward": 100},
    ], "final_boss": {"id": "ms_final", "name": "Microsoft Loop Boss", "icon": "\U0001f479", "required_score": 85, "xp_reward": 220}},
    "google": {"id": "google_dungeon", "name": "Google SDE Dungeon", "icon": "\U0001f30d", "company": "Google", "min_readiness": 85, "reward_badge": "google_challenger", "gates": [
        {"id": "goog_code", "name": "Coding Chamber", "icon": "\U0001f4bb", "type": "coding", "required_score": 90, "xp_reward": 150},
        {"id": "goog_sd", "name": "System Design", "icon": "\U0001f3d7\ufe0f", "type": "system_design", "required_score": 90, "xp_reward": 140},
        {"id": "goog_cs", "name": "CS Fundamentals", "icon": "\U0001f4da", "type": "system_design", "required_score": 85, "xp_reward": 110},
        {"id": "goog_behave", "name": "Googleyness", "icon": "\U0001f5e3\ufe0f", "type": "behavioral", "required_score": 85, "xp_reward": 110},
        {"id": "goog_algo", "name": "Algorithm Arena", "icon": "\u2694\ufe0f", "type": "coding", "required_score": 90, "xp_reward": 130},
    ], "final_boss": {"id": "goog_final", "name": "Google Panel Boss", "icon": "\U0001f479", "required_score": 90, "xp_reward": 250}},
}


def get_company_dungeons(user_readiness=0.0):
    return [{**d, "unlocked": user_readiness >= d["min_readiness"], "readiness_gap": max(0, d["min_readiness"] - user_readiness)} for d in COMPANY_DUNGEONS.values()]


ACHIEVEMENT_COLLECTIONS = {
    "algorithms": {"id": "algorithms", "name": "Algorithms", "icon": "\u2694\ufe0f", "items": [
        {"id": "array_explorer", "name": "Array Explorer", "icon": "\U0001f4ca", "description": "Master array operations", "rarity": "common"},
        {"id": "binary_search_master", "name": "Binary Search Master", "icon": "\U0001f50d", "description": "Conquer binary search", "rarity": "uncommon"},
        {"id": "graph_guardian", "name": "Graph Guardian", "icon": "\U0001f30f", "description": "Navigate graph algorithms", "rarity": "rare"},
        {"id": "dp_slayer", "name": "DP Slayer", "icon": "\U0001f9ee", "description": "Defeat dynamic programming", "rarity": "epic"},
        {"id": "tree_whisperer", "name": "Tree Whisperer", "icon": "\U0001f333", "description": "Command tree structures", "rarity": "rare"},
    ]},
    "companies": {"id": "companies", "name": "Companies", "icon": "\U0001f3e2", "items": [
        {"id": "tcs_challenger", "name": "TCS Challenger", "icon": "\U0001f3ef", "description": "Complete TCS dungeon", "rarity": "uncommon"},
        {"id": "infosys_challenger", "name": "Infosys Challenger", "icon": "\U0001f3e2", "description": "Complete Infosys dungeon", "rarity": "uncommon"},
        {"id": "amazon_challenger", "name": "Amazon Challenger", "icon": "\U0001f3d4\ufe0f", "description": "Complete Amazon dungeon", "rarity": "epic"},
        {"id": "microsoft_challenger", "name": "Microsoft Challenger", "icon": "\U0001f310", "description": "Complete Microsoft dungeon", "rarity": "epic"},
        {"id": "google_challenger", "name": "Google Challenger", "icon": "\U0001f30d", "description": "Complete Google dungeon", "rarity": "legendary"},
    ]},
    "career": {"id": "career", "name": "Career Milestones", "icon": "\U0001f3c6", "items": [
        {"id": "first_problem", "name": "First Problem", "icon": "\u2705", "description": "Solve your first problem", "rarity": "common"},
        {"id": "first_assessment", "name": "First Assessment", "icon": "\U0001f4dd", "description": "Complete your first assessment", "rarity": "common"},
        {"id": "first_mock", "name": "First Mock Interview", "icon": "\U0001f5e3\ufe0f", "description": "Complete a mock interview", "rarity": "uncommon"},
        {"id": "interview_ready", "name": "Interview Ready", "icon": "\U0001f3c6", "description": "Reach 75% interview readiness", "rarity": "rare"},
        {"id": "placement_ready", "name": "Placement Ready", "icon": "\U0001f451", "description": "Reach 90% overall readiness", "rarity": "legendary"},
    ]},
    "mastery": {"id": "mastery", "name": "Mastery", "icon": "\U0001f48e", "items": [
        {"id": "code_apprentice", "name": "Code Apprentice", "icon": "\U0001f527", "description": "Reach Level 10", "rarity": "common"},
        {"id": "problem_solver", "name": "Problem Solver", "icon": "\u2694\ufe0f", "description": "Reach Level 20", "rarity": "uncommon"},
        {"id": "algorithm_adept", "name": "Algorithm Adept", "icon": "\U0001f9e0", "description": "Reach Level 30", "rarity": "rare"},
        {"id": "software_builder", "name": "Software Builder", "icon": "\U0001f4bb", "description": "Reach Level 40", "rarity": "epic"},
        {"id": "elite_candidate", "name": "Elite Candidate", "icon": "\U0001f451", "description": "Reach Level 100", "rarity": "legendary"},
    ]},
    "social": {"id": "social", "name": "Social", "icon": "\U0001f465", "items": [
        {"id": "guild_founder", "name": "Guild Founder", "icon": "\U0001f3db\ufe0f", "description": "Create a study guild", "rarity": "uncommon"},
        {"id": "battle_champion", "name": "Battle Champion", "icon": "\U0001f3c6", "description": "Win 10 coding battles", "rarity": "rare"},
        {"id": "campus_hero", "name": "Campus Hero", "icon": "\U0001f3f0", "description": "Top your college leaderboard", "rarity": "epic"},
    ]},
}


def get_achievement_collections(user_badges=None):
    user_badges = set(user_badges or [])
    collections = []
    for coll in ACHIEVEMENT_COLLECTIONS.values():
        items = []
        for item in coll["items"]:
            items.append({**item, "earned": item["id"] in user_badges})
        earned = sum(1 for i in items if i["earned"])
        total = len(items)
        collections.append({**coll, "items": items, "earned_count": earned, "total_count": total, "progress_pct": round(earned / total * 100) if total > 0 else 0})
    return collections


async def get_rpg_profile(user_id):
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = {"user_id": user_id, "xp": 0, "level": 1, "streak": 0, "badges": [], "bosses_defeated": []}
    level = profile.get("level", 1)
    xp = profile.get("xp", 0)
    streak = profile.get("streak", 0)
    badges = profile.get("badges", [])
    bosses_defeated = profile.get("bosses_defeated", [])

    readiness = 0.0
    try:
        from app.services.skill_assessment import get_readiness_score
        readiness_data = await get_readiness_score(user_id)
        readiness = readiness_data.get("overall_readiness", 0.0)
    except Exception:
        pass

    active_quest = None
    quest_chains = get_quest_chains(level)
    for chain in quest_chains:
        if chain["unlocked"] and not chain["is_complete"]:
            active_quest = chain
            break

    skill_graph = await skill_graph_collection.find_one({"user_id": user_id}) or {}

    return {
        "rank": get_career_rank(level),
        "level": level,
        "xp": xp,
        "xp_to_next": ((level) ** 2) * 50 if level < 100 else 0,
        "streak": streak,
        "readiness": round(readiness, 1),
        "skill_tree": get_skill_tree(level),
        "quest_chains": quest_chains,
        "active_quest": active_quest,
        "bosses": get_skill_bosses(level, skill_graph),
        "dungeons": get_company_dungeons(readiness),
        "collections": get_achievement_collections(badges),
        "total_badges": len(badges),
        "bosses_defeated_count": len(bosses_defeated),
    }
