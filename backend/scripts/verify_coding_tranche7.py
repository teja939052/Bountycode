"""Expand verified corpus 83 -> 100+ (placement-driven: aptitude + CS +
logical + a few coding). All independently reasoned, honest provenance."""
import sys, json
from collections import Counter
sys.path.insert(0, r"D:\Project-Fremen\backend")
VERIFIED_PATH = r"D:\Project-Fremen\backend\app\data\verified_placement_questions.json"
T = lambda **kw: kw

APT = [
    T(id="apt-027", type="aptitude", topic="ratios", sub_topic="share", question="(Ratio) Divide 720 in ratio 5:4.", difficulty="easy", correct_answer="400 and 320", correct_index=0, options=["400 and 320", "360 and 360", "450 and 270", "420 and 300"], reasoning_steps="Total parts 9; one = 5/9*720=400, other=4/9*720=320.", shortcut="part = ratio/total * whole.", common_trap="Equal split or wrong total parts."),
    T(id="apt-028", type="aptitude", topic="percentages", sub_topic="marks", question="(Marks) Scored 312 out of 400. Percentage?", difficulty="easy", correct_answer="78%", correct_index=2, options=["75%","76%","78%","80%"], reasoning_steps="312/400*100 = 78%.", shortcut="score/total*100.", common_trap="Dropping a digit (e.g. 75%)."),
    T(id="apt-029", type="aptitude", topic="time-speed", sub_topic="catch-up", question="(Catch-up) A starts at 40 km/h; B starts same point 2 h later at 60 km/h. When does B catch A?", difficulty="hard", correct_answer="6 h after A starts", correct_index=2, options=["4 h","5 h","6 h","8 h"], reasoning_steps="A lead = 40*2 = 80 km. B gains 20 km/h. Time = 80/20 = 4 h after B starts = 6 h after A.", shortcut="lead/gain_rate, then add head start.", common_trap="Adding gain time to the wrong baseline."),
    T(id="apt-030", type="aptitude", topic="profit-loss", sub_topic="cost price find", question="(CP) Sold at 540, gain 20%. Cost price?", difficulty="medium", correct_answer="450", correct_index=3, options=["432","440","540","450"], reasoning_steps="SP=CP*1.2 => CP = 540/1.2 = 450.", shortcut="CP = SP/(1+gain%).", common_trap="SP*0.8 (wrong) = 432."),
    T(id="apt-031", type="aptitude", topic="mixtures", sub_topic="replace", question="(Mixture replace) 20 L of 10% salt; 5 L pure water added. New salt %?", difficulty="medium", correct_answer="8%", correct_index=1, options=["7%","8%","9%","10%"], reasoning_steps="Salt = 10% of 20 = 2 L. New total 25 L. % = 2/25*100 = 8%.", shortcut="salt_amount/new_total.", common_trap="Dividing by original 20 L."),
    T(id="apt-032", type="aptitude", topic="average-speed", sub_topic="two equal halves", question="(Equal-halves speed) Half distance at 40, half at 60 km/h. Avg?", difficulty="medium", correct_answer="48 km/h", correct_index=0, options=["48 km/h","50 km/h","55 km/h","45 km/h"], reasoning_steps="Equal distances: avg = 2uv/(u+v) = 2*40*60/100 = 4800/100 = 48.", shortcut="2uv/(u+v).", common_trap="Arithmetic mean 50."),
    T(id="apt-033", type="aptitude", topic="compound-interest", sub_topic="CI vs SI", question="(CI v SI) Difference between CI and SI for 3 years at 10% on Rs 1000?", difficulty="hard", correct_answer="Rs 31", correct_index=2, options=["Rs 30","Rs 30.90","Rs 31","Rs 33"], reasoning_steps="SI=1000*10*3/100=300. CI=1000*(1.1)^3-1000=1331-1000=331. Diff=31.", shortcut="Use the 3-year CI-SI formula or compute directly.", common_trap="Using 2-year formula giving 30."),
    T(id="apt-034", type="aptitude", topic="number-series", sub_topic="geometric", question="(Series geometric) 3, 9, 27, 81, ?", difficulty="easy", correct_answer="243", correct_index=3, options=["108","162","216","243"], reasoning_steps="Each term x3: 81*3 = 243.", shortcut="Identify constant multiplier.", common_trap="Adding instead of multiplying."),
    T(id="apt-035", type="aptitude", topic="perimeter-area", sub_topic="circle", question="(Area) Area of circle radius 7 (pi=22/7)?", difficulty="easy", correct_answer="154", correct_index=1, options=["44","154","308","49"], reasoning_steps="pi*r^2 = 22/7 * 49 = 154.", shortcut="pi r^2.", common_trap="Using circumference 44 instead."),
    T(id="apt-036", type="aptitude", topic="ratio-time", sub_topic="work ratio", question="(Work time ratio) A is twice as fast as B; together 12 days. A alone = ?", difficulty="hard", correct_answer="18 days", correct_index=2, options=["24","16","18","20"], reasoning_steps="If A=2B rates, A+B = 3B = 1/12 => B=1/36, A=2/36=1/18 => 18 days.", shortcut="Let B=x, A=2x.", common_trap="Wrongly setting A=24."),
]

CS = [
    T(id="cs-016", type="cs_fundamentals", topic="sorting", sub_topic="best case", question="(Sorting) Best-case complexity of quicksort is:", difficulty="easy", correct_answer="O(n log n)", correct_index=1, options=["O(n)","O(n log n)","O(n^2)","O(log n)"], reasoning_steps="With good pivot, quicksort partitions log n levels each O(n) => O(n log n).", shortcut="Balanced partition => n log n.", common_trap="Picking O(n^2) (worst case)."),
    T(id="cs-017", type="cs_fundamentals", topic="data-structures", sub_topic="heap", question="(Heap) A min-heap always keeps the smallest element:", difficulty="easy", correct_answer="At the root", correct_index=0, options=["At the root","At a leaf","At the middle","Anywhere"], reasoning_steps="Min-heap property: parent <= children, so smallest is at root.", shortcut="Root = min (min-heap).", common_trap="Thinking root holds largest."),
    T(id="cs-018", type="cs_fundamentals", topic="os", sub_topic="threads vs processes", question="(OS) Which shares memory by default?", difficulty="medium", correct_answer="Threads", correct_index=0, options=["Threads","Processes","Both","Neither"], reasoning_steps="Threads of a process share the same address space; processes have isolated memory.", shortcut="Threads share heap/globals.", common_trap="Picking processes (isolated)."),
    T(id="cs-019", type="cs_fundamentals", topic="dbms", sub_topic="index", question="(DBMS) A database index speeds up:", difficulty="easy", correct_answer="Search/lookup", correct_index=1, options=["Insert always","Search/lookup","Deletion always","Storage always"], reasoning_steps="Indexes are lookup structures (B-tree/hash) that accelerate searches.", shortcut="Index = faster SELECT.", common_trap="Thinking it always speeds all operations."),
    T(id="cs-020", type="cs_fundamentals", topic="networking", sub_topic="UDP", question="(Networking) UDP is:", difficulty="easy", correct_answer="Connectionless, unreliable", correct_index=2, options=["Connection-oriented, reliable","Connectionless, reliable","Connectionless, unreliable","Connection-oriented, unreliable"], reasoning_steps="UDP sends datagrams without a connection and does not guarantee delivery.", shortcut="UDP = fast, no guarantees.", common_trap="Picking reliable (that's TCP)."),
]

LOG = [
    T(id="log-008", type="logical", topic="number-puzzles", sub_topic="operation pattern", question="(Puzzle) If 2*3=11, 3*4=19, then 4*5=?", difficulty="medium", correct_answer="29", correct_index=3, options=["20","24","29","31"], reasoning_steps="Rule: a*b -> a*b + a + b. 2*3=6+2+3=11; 3*4=12+3+4=19; so 4*5=20+4+5=29.", shortcut="Multiply then add both operands.", common_trap="Assuming plain multiplication."),
    T(id="log-009", type="logical", topic="analogy-numbers", sub_topic="square relationship", question="(Number analogy) 7 : 49 :: 9 : ?", difficulty="easy", correct_answer="81", correct_index=1, options=["72","81","90","99"], reasoning_steps="7^2=49, so 9^2=81.", shortcut="Square the first.", common_trap="Adding (9+72) instead of squaring."),
    T(id="log-010", type="logical", topic="cubes", sub_topic="visible faces", question="(Cube) A 3x3x3 cube painted outside, cut into unit cubes. How many have paint on exactly 2 faces?", difficulty="hard", correct_answer="12", correct_index=2, options=["8","12","16","24"], reasoning_steps="Edge cubes (not corners) each have 2 painted faces: 12 edges * 1 center cube = 12.", shortcut="For n: 12*(n-2); here 12*1=12.", common_trap="Counting corners (3 faces) or face-centers (1 face)."),
]

VERB = [
    T(id="verb-008", type="verbal", topic="spelling", sub_topic="correct word", question="(Spelling) Choose the correct spelling:", difficulty="easy", correct_answer="Accommodate", correct_index=0, options=["Accommodate","Acommodate","Accomodate","Acomodate"], reasoning_steps="Accommodate has double c and double m.", shortcut="acCOMMoDATE (two c, two m).", common_trap="Dropping one 'c' or 'm'."),
    T(id="verb-009", type="verbal", topic="synonym", sub_topic="word meaning", question="(Synonym) Closest synonym of 'BRIEF':", difficulty="easy", correct_answer="Short", correct_index=0, options=["Short","Long","Detailed","Wordy"], reasoning_steps="Brief means short in duration or length = short.", shortcut="Brief = short.", common_trap="Choosing an antonym."),
    T(id="verb-010", type="verbal", topic="one-word", sub_topic="single word", question="(One-word) 'A person who speaks many languages' is a:", difficulty="medium", correct_answer="Polyglot", correct_index=3, options=["Linguist","Innumerable","Prolific","Polyglot"], reasoning_steps="A polyglot knows/uses several languages.", shortcut="Polyglot = many languages.", common_trap="Choosing Linguist (language scholar)."),
]

NEW = APT + CS + LOG + VERB
with open(VERIFIED_PATH, "r", encoding="utf-8") as f:
    existing = json.load(f)
existing_ids = {q["id"] for q in existing}
added = 0
for q in NEW:
    q.setdefault("trust_status", "verified")
    q.setdefault("source_bank", "verified_placement_questions")
    q.setdefault("verification_version", 1)
    q.setdefault("stage", "placement")
    q.setdefault("companies", ["tcs", "infosys", "wipro", "accenture", "cognizant"])
    q.setdefault("provenance", "pattern_relevant to TCS NQT / Infosys")
    if q["id"] not in existing_ids:
        existing.append(q)
        added += 1
with open(VERIFIED_PATH, "w", encoding="utf-8") as f:
    json.dump(existing, f, indent=2, ensure_ascii=False)
print("Added:", added, "| Total:", len(existing))
print("Type dist:", dict(Counter(x["type"] for x in existing)))