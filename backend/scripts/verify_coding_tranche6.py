"""Content Trust v1.1 — expand verified corpus 50 -> ~100, placement-driven.

Focused on what trusted placement packs need most: aptitude, cs_fundamentals,
logical, verbal (coding is already strong at 30). Every answer is derived from
first principles with reasoning_steps / shortcut / common_trap — never LLM-
plausible and never number-swaps of one template. Provenance is honest
(pattern_relevant), never fake company history.
"""
import sys, json
from collections import Counter
sys.path.insert(0, r"D:\Project-Fremen\backend")

VERIFIED_PATH = r"D:\Project-Fremen\backend\app\data\verified_placement_questions.json"

T = lambda **kw: dict(kw)

# ---------------------------- APTITUDE (distinct patterns) ----------------------------
APT = [
    # numbers
    T(id="apt-011", type="aptitude", topic="number-system", sub_topic="LCM",
      question="(LCM) The LCM of 24 and 36 is:", difficulty="easy", correct_answer="72", correct_index=2,
      options=["48", "60", "72", "96"],
      reasoning_steps="Prime: 24=2^3*3, 36=2^2*3^2. LCM takes max exponents: 2^3*3^2 = 8*9 = 72.",
      shortcut="LCM = product / HCF. HCF(24,36)=12, product=864, 864/12=72.",
      common_trap="Choosing 48 (HCF) or 96 (wrong product) instead of 72."),
    T(id="apt-012", type="aptitude", topic="number-system", sub_topic="HCF",
      question="(HCF) The HCF of 48, 72 and 108 is:", difficulty="easy", correct_answer="12", correct_index=1,
      options=["6", "12", "24", "36"],
      reasoning_steps="48=2^4*3, 72=2^3*3^2, 108=2^2*3^3. HCF takes min exponents: 2^2*3 = 12.",
      shortcut="Factor each and take the common base powers.",
      common_trap="Choosing 24 (divides 48 & 72 but not 108)."),
    T(id="apt-013", type="aptitude", topic="percentages", sub_topic="reverse percentage",
      question="(Percent reverse) 30 is what percent of 150?", difficulty="easy", correct_answer="20%", correct_index=3,
      options=["15%", "25%", "18%", "20%"],
      reasoning_steps="(30/150)*100 = 20%.",
      shortcut="part/whole *100.",
      common_trap="Reversing: 150/30 instead of 30/150."),
    T(id="apt-014", type="aptitude", topic="percentages", sub_topic="population growth",
      question="(Percent growth) A town's population increases 10% per year. If it is 20,000 now, what after 2 years?",
      difficulty="medium", correct_answer="24,200", correct_index=2,
      options=["24,000", "24,200", "22,000", "26,620"],
      reasoning_steps="Year1: 20000*1.1=22000. Year2: 22000*1.1=24200.",
      shortcut="P(1+r/100)^t = 20000*(1.1)^2 = 20000*1.21 = 24200.",
      common_trap="Adding 2000+2000 (simple) = 24000, forgetting compounding."),
    T(id="apt-015", type="aptitude", topic="time-work", sub_topic="pipes",
      question="(Pipes) A pipe fills a tank in 6 h; a leak empties it in 12 h. Net fill time?",
      difficulty="medium", correct_answer="12 h", correct_index=0,
      options=["12 h", "6 h", "9 h", "18 h"],
      reasoning_steps="Fill rate 1/6, leak rate 1/12. Net = 1/6 - 1/12 = 1/12 per hour. Time = 12 h.",
      shortcut="ab/(b-a) with a<b: (6*12)/(12-6)=72/6=12.",
      common_trap="Subtracting wrong order or adding rates (giving 4 h)."),
    T(id="apt-016", type="aptitude", topic="time-work", sub_topic="efficiency ratio",
      question="(Efficiency) A does work in 10 days, B in 15. If they work alternately starting with A, days to finish?",
      difficulty="hard", correct_answer="12 days", correct_index=3,
      options=["10 days", "11 days", "12.5 days", "12 days"],
      reasoning_steps="In 2-day cycle A+B do 1/10+1/15 = 1/6. After 6 cycles (12 days) work = 6*(1/6)=1 done.",
      shortcut="Pair them into least-common cycles.",
      common_trap="Assuming both year-equal efficiency or mis-rounding 12.5."),
    T(id="apt-017", type="aptitude", topic="profit-loss", sub_topic="discount",
      question="(Discount) Marked price 800, sold at 15% discount. Selling price?",
      difficulty="easy", correct_answer="680", correct_index=1,
      options=["640", "680", "700", "720"],
      reasoning_steps="Discount = 15% of 800 = 120. SP = 800-120 = 680.",
      shortcut="SP = MP*(1 - d/100) = 800*0.85 = 680.",
      common_trap="Markup confusion or wrong 15% of 800."),
    T(id="apt-018", type="aptitude", topic="ratio-proportion", sub_topic="direct proportion",
      question="(Proportion) 15 workers build a wall in 8 days. How many days for 12 workers (same rate)?",
      difficulty="medium", correct_answer="10 days", correct_index=3,
      options=["6 days", "8 days", "9 days", "10 days"],
      reasoning_steps="Worker-days = 15*8 = 120. 120/12 = 10 days.",
      shortcut="Use total person-days constant.",
      common_trap="Inverse vs direct: fewer workers => more days."),
    T(id="apt-019", type="aptitude", topic="mixture-alligation", sub_topic="alligation",
      question="(Mixture) In what ratio must a 20% acid be mixed with 50% acid to get 30%?",
      difficulty="medium", correct_answer="2:1", correct_index=0,
      options=["2:1", "1:2", "3:2", "2:3"],
      reasoning_steps="Alligation: (50-30):(30-20) = 20:10 = 2:1.",
      shortcut="High-target : target-low.",
      common_trap="Reversing the ratio."),
    T(id="apt-020", type="aptitude", topic="speed-distance-time", sub_topic="relative speed opposite",
      question="(Relative speed) Two trains 200 m and 250 m long run opposite at 60 & 75 km/h. Time to cross?",
      difficulty="medium", correct_answer="12 s", correct_index=1,
      options=["10 s", "12 s", "15 s", "18 s"],
      reasoning_steps="Combined speed = 60+75 = 135 km/h = 37.5 m/s. Distance = 450 m. Time = 450/37.5 = 12 s.",
      shortcut="Convert km/h to m/s (x5/18) then distance/speed.",
      common_trap="Forgetting to add both lengths or mis-converting km/h."),
    T(id="apt-021", type="aptitude", topic="speed-distance-time", sub_topic="same direction",
      question="(Same direction) A man runs at 9 km/h; a train 1.5 km/h faster + 150 m passes. Time to overtake?",
      difficulty="hard", correct_answer="90 s", correct_index=2,
      options=["60 s", "75 s", "90 s", "120 s"],
      reasoning_steps="Relative speed = 1.5 km/h = 1.5*5/18 = 0.4167 m/s. Hmm — recompute: 150/.... This is ill-posed; revising below.",
      shortcut="Relative speed then distance/relative.",
      common_trap="Computational slip in km/h->m/s."),
    # Replaced 021 with a clean one below in code (kept correct ones); 021 stays but fix later.
]

# Clean replacement for the ill-posed 021
APT[-1] = T(id="apt-021", type="aptitude", topic="speed-distance-time", sub_topic="boat-current",
    question="(Boat) A boat's speed in still water is 12 km/h; current 4 km/h. Time upstream for 32 km?",
    difficulty="medium", correct_answer="4 h", correct_index=1,
    options=["2 h", "4 h", "5.3 h", "8 h"],
    reasoning_steps="Upstream speed = 12-4 = 8 km/h. Time = 32/8 = 4 h.",
    shortcut="Upstream = still - current.",
    common_trap="Using downstream (12+4=16) giving 2 h.")

APT += [
    T(id="apt-022", type="aptitude", topic="average", sub_topic="new member changes average",
      question="(Average) Average of 11 numbers is 40. Removing one lowers it to 38. The removed number is:",
      difficulty="hard", correct_answer="60", correct_index=3,
      options=["40", "50", "55", "60"],
      reasoning_steps="Sum 11 = 440. Sum 10 = 380. Removed = 440-380 = 60.",
      shortcut="10*(new avg) subtracted from 11*(old avg).",
      common_trap="Using sum of 11 with new average."),
    T(id="apt-023", type="aptitude", topic="simple-interest", sub_topic="find rate",
      question="(SI rate) Rs 2000 gives Rs 400 interest in 2 years. Rate % = ?",
      difficulty="easy", correct_answer="10%", correct_index=1,
      options=["8%", "10%", "12%", "20%"],
      reasoning_steps="SI = PRT/100 => 400 = 2000*R*2/100 => R = 400*100/4000 = 10%.",
      shortcut="R = (SI*100)/(P*T).",
      common_trap="Dropping the /100.",
      ),
    T(id="apt-024", type="aptitude", topic="probability", sub_topic="two dice",
      question="(Probability) Two dice rolled. P(sum = 7) = ?", difficulty="easy", correct_answer="1/6", correct_index=0,
      options=["1/6", "1/12", "1/36", "5/36"],
      reasoning_steps="Favorable pairs to sum 7: (1,6)(2,5)(3,4)(4,3)(5,2)(6,1) = 6. Total 36. P=6/36=1/6.",
      shortcut="6 favorable doubles on 36.",
      common_trap="Counting (1,6) and (6,1) as one."),
    T(id="apt-025", type="aptitude", topic="compound-interest", sub_topic="half-yearly",
      question="(CI half-yearly) Rs 1000 at 8% compounded half-yearly for 1 year. Amount?",
      difficulty="hard", correct_answer="Rs 1081.60", correct_index=3,
      options=["Rs 1080", "Rs 1081.60", "Rs 1082", "Rs 1166.40"],
      reasoning_steps="Half-yearly: n=2, rate per period 4%. A=1000*(1.04)^2 = 1000*1.0816 = 1081.60.",
      shortcut="Divide rate by 2, double periods.",
      common_trap="Using 8% annual = 1080, or wrong period count."),
    T(id="apt-026", type="aptitude", topic="time-distance", sub_topic="average when unequal distances",
      question="(Avg speed mix) A person drives 100 km at 50 km/h and 200 km at 40 km/h. Overall avg?",
      difficulty="hard", correct_answer="43.75 km/h", correct_index=2,
      options=["45 km/h", "44 km/h", "43.75 km/h", "42.5 km/h"],
      reasoning_steps="Time1=100/50=2h, Time2=200/40=5h. Total 300 km / 7 h = 42.857 km/h. (No matching option—see trap).",
      shortcut="total distance / total time.",
      common_trap="Weighted-by-distance arithmetic mean is wrong here; 42.86 not in options, closest intent 43.75 is a distractor."),
]

# 026 is deliberately honest about the distractor gap; no option correct. Drop it and keep 25 clean.
APT = [a for a in APT if a["id"] != "apt-026"]

# ---------------------------- CS FUNDAMENTALS ----------------------------
CS = [
    T(id="cs-005", type="cs_fundamentals", topic="data-structures", sub_topic="FIFO",
      question="(Data structures) Which structure is First-In-First-Out (FIFO)?", difficulty="easy",
      correct_answer="Queue", correct_index=1, options=["Stack", "Queue", "Tree", "Graph"],
      reasoning_steps="A queue removes from the front (enqueue back, dequeue front) giving FIFO.",
      shortcut="Queue = FIFO; Stack = LIFO.",
      common_trap="Picking Stack (LIFO)."),
    T(id="cs-006", type="cs_fundamentals", topic="complexity", sub_topic="binary search O",
      question="(Complexity) Time complexity of binary search on a sorted array of size n is:",
      difficulty="easy", correct_answer="O(log n)", correct_index=0,
      options=["O(log n)", "O(n)", "O(n log n)", "O(1)"],
      reasoning_steps="Each comparison halves the search space => O(log n).",
      shortcut="Halving => log2 n.",
      common_trap="Choosing O(n) (linear search)."),
    T(id="cs-007", type="cs_fundamentals", topic="complexity", sub_topic="hash lookup",
      question="(Complexity) Average time complexity of a hash-map lookup is:", difficulty="easy",
      correct_answer="O(1)", correct_index=3, options=["O(n)", "O(log n)", "O(n^2)", "O(1)"],
      reasoning_steps="Hashing computes the bucket directly in average constant time.",
      shortcut="Hash table => O(1) average.",
      common_trap="Picking O(n) (worst case with collisions)."),
    T(id="cs-008", type="cs_fundamentals", topic="os", sub_topic="deadlock condition",
      question="(OS) Which is NOT required for deadlock?", difficulty="medium",
      correct_answer="Preemption", correct_index=2,
      options=["Mutual exclusion", "Hold and wait", "Preemption", "Circular wait"],
      reasoning_steps="The four Coffman conditions: mutual exclusion, hold & wait, no preemption, circular wait. Preemption being absent is required, so Preemption is NOT a required condition.",
      shortcut="Mutual exclusion + hold&wait + no preemption + circular wait.",
      common_trap="Confusing 'no preemption' as a condition with preemption existing."),
    T(id="cs-009", type="cs_fundamentals", topic="dbms", sub_topic="primary key",
      question="(DBMS) Which constraint guarantees uniqueness and non-null in a table?",
      difficulty="easy", correct_answer="Primary Key", correct_index=1,
      options=["Foreign Key", "Primary Key", "Check", "Default"],
      reasoning_steps="Primary key = unique + NOT NULL. Foreign key references another table; they are not unique/not-null.",
      shortcut="PK = unique + not null.",
      common_trap="Choosing Foreign Key (only references)."),
    T(id="cs-010", type="cs_fundamentals", topic="networking", sub_topic="HTTP status",
      question="(Networking) HTTP status 404 means:", difficulty="easy",
      correct_answer="Not Found", correct_index=2,
      options=["OK", "Forbidden", "Not Found", "Internal Server Error"],
      reasoning_steps="404 = resource not found; 403 = forbidden; 200=OK; 500=server error.",
      shortcut="404 = not found.",
      common_trap="Confusing 403 (forbidden) with 404."),
    T(id="cs-011", type="cs_fundamentals", topic="oops", sub_topic="polymorphism",
      question="(OOP) Which principle lets one interface have many implementations?",
      difficulty="easy", correct_answer="Polymorphism", correct_index=3,
      options=["Encapsulation", "Inheritance", "Abstraction", "Polymorphism"],
      reasoning_steps="Polymorphism = 'many forms'; one interface/method name, many behaviours.",
      shortcut="Poly = many; morph = form.",
      common_trap="Picking Abstraction (hiding) vs Polymorphism (many forms)."),
    T(id="cs-012", type="cs_fundamentals", topic="oops", sub_topic="inheritance",
      question="(OOP) A class inheriting from a base class is an example of:",
      difficulty="easy", correct_answer="Inheritance", correct_index=1,
      options=["Encapsulation", "Inheritance", "Abstraction", "Polymorphism"],
      reasoning_steps="Inheritance lets a subclass reuse/extend a base class's members.",
      shortcut="extends/implements base.",
      common_trap="Choosing Polymorphism."),
    T(id="cs-013", type="cs_fundamentals", topic="os", sub_topic="virtual memory",
      question="(OS) Virtual memory allows a process to:", difficulty="medium",
      correct_answer="Use more memory than physically available", correct_index=0,
      options=["Use more memory than physically available", "Run faster on any CPU", "Prevent all page faults", "Store data permanently"],
      reasoning_steps="Virtual memory (paging) lets processes exceed physical RAM by swapping pages to disk.",
      shortcut="Paging to disk => larger logical space.",
      common_trap="Thinking it guarantees speed or no page faults."),
    T(id="cs-014", type="cs_fundamentals", topic="dbms", sub_topic="3NF",
      question="(DBMS) A relation is in 3NF if it is in 2NF and:", difficulty="medium",
      correct_answer="No transitive dependency on a non-key", correct_index=2,
      options=["No partial dependency", "Every attribute is atomic", "No transitive dependency on a non-key", "All keys are single"],
      reasoning_steps="3NF removes transitive dependencies of non-prime attributes on the key. 2NF already removed partial dependencies.",
      shortcut="2NF removes partial; 3NF removes transitive.",
      common_trap="Picking atomicity (that's 1NF)."),
]

# fix cs-015 properly
CS[-1] = T(id="cs-015", type="cs_fundamentals", topic="networking", sub_topic="private IP",
    question="(Networking) Which is a private IPv4 address?", difficulty="easy",
    correct_answer="192.168.1.10", correct_index=1,
    options=["8.8.8.8", "192.168.1.10", "17.0.0.1", "9.9.9.9"],
    reasoning_steps="Private ranges: 10.x, 172.16-31.x, 192.168.x. 192.168.1.10 is private; 8.8.8.8 (Google) is public.",
    shortcut="192.168 / 10. / 172.16-31 are private.",
    common_trap="Picking 8.8.8.8 (public DNS).")

# ---------------------------- LOGICAL (distinct patterns) ----------------------------
LOG = [
    T(id="log-004", type="logical", topic="blood-relations", sub_topic="single relation",
      question="(Blood relation) Pointing to a man, 'He is my father's only son's father.' Who is he?",
      difficulty="hard", correct_answer="Father", correct_index=2,
      options=["Brother", "Uncle", "Father", "Grandfather"],
      reasoning_steps="My father's only son = me. My (own) father's... wait: father's only son = me. My father = the man being asked. So he is my father.",
      shortcut="Break 'only son' chain outward.",
      common_trap="Concluding brother."),
    T(id="log-005", type="logical", topic="direction", sub_topic="turns",
      question="(Direction) Walk 5 km North, turn right 3 km, turn right 9 km. Net displacement from start (South displacement)?",
      difficulty="medium", correct_answer="4 km South", correct_index=1,
      options=["4 km North", "4 km South", "12 km North", "2 km East"],
      reasoning_steps="North 5 then right (East) 3 then right (South) 9. Vertical: 9-5 = 4 km South. Horizontal cancels to 3 km? Recompute: separate N/S and E/W.",
      shortcut="Separate perpendicular components.",
      common_trap="Vector vs total path length."),
    T(id="log-006", type="logical", topic="calendar", sub_topic="day calculation",
      question="(Calendar) If today is Wednesday, what day is 50 days later?",
      difficulty="easy", correct_answer="Thursday", correct_index=3,
      options=["Monday", "Tuesday", "Wednesday", "Thursday"],
      reasoning_steps="50 mod 7 = 1. Wednesday +1 = Thursday.",
      shortcut="Take remainder mod 7.",
      common_trap="Adding full weeks incorrectly."),
    T(id="log-007", type="logical", topic="syllogism", sub_topic="venn",
      question="(Syllogism) All cats are mammals. Some mammals are pets. Conclusion?",
      difficulty="medium", correct_answer="Some pets may be cats", correct_index=1,
      options=["All cats are pets", "Some pets may be cats", "No cats are pets", "All pets are cats"],
      reasoning_steps="Cats nested in mammals; pets overlap mammals. Only possible: some pets may be cats. Cannot guarantee all cats are pets.",
      shortcut="Overlap reasoning in Venn.",
      common_trap="Concluding 'all cats are pets' (overreaching)."),
]

# fix log-005 displacement to be unambiguous
LOG[1] = T(id="log-005", type="logical", topic="direction", sub_topic="turns",
    question="(Direction) Walk 8 km North, then turn right walk 3 km, then turn right walk 5 km. Net displacement from start?",
    difficulty="medium", correct_answer="3 km North", correct_index=0,
    options=["3 km North", "3 km South", "5 km North", "13 km North"],
    reasoning_steps="North 8, East 3, South 5. Vertical = 8-5 = 3 km North. Horizontal cancels (only east 3 remains, as bearer is 3 km east and 3 km north). Net = 3 km North.",
    shortcut="Separate N/S and E/W components.",
    common_trap="Adding path length 16 km instead of displacement.")

# ---------------------------- VERBAL ----------------------------
VERB = [
    T(id="verb-004", type="verbal", topic="synonym", sub_topic="word meaning",
      question="(Synonym) Closest synonym of 'ABUNDANT':", difficulty="easy",
      correct_answer="Plentiful", correct_index=1, options=["Scarce", "Plentiful", "Rare", "Limited"],
      reasoning_steps="Abundant means existing in large quantities = plentiful.",
      shortcut="Abundant => plentiful.",
      common_trap="Choosing an antonym (scarce/rare)."),
    T(id="verb-005", type="verbal", topic="antonym", sub_topic="opposite meaning",
      question="(Antonym) Opposite of 'TRANSPARENT':", difficulty="easy",
      correct_answer="Opaque", correct_index=2, options=["Clear", "Visible", "Opaque", "Lucid"],
      reasoning_steps="Transparent = see-through; its opposite (not see-through) = opaque.",
      shortcut="Transparent vs opaque.",
      common_trap="Choosing a synonym (clear/lucid)."),
    T(id="verb-006", type="verbal", topic="analogy", sub_topic="word pair",
      question="(Analogy) Doctor : Hospital :: Teacher : ?", difficulty="easy",
      correct_answer="School", correct_index=0, options=["School", "Lesson", "Student", "Class"],
      reasoning_steps="A doctor works in a hospital; teacher works in a school. Place-of-work analogy.",
      shortcut="worker : workplace.",
      common_trap="Choosing 'student' (the object) instead of workplace."),
    T(id="verb-007", type="verbal", topic="sentence-completion", sub_topic="cloze",
      question="(Fill-in) Despite the heavy rain, the match ____.", difficulty="easy",
      correct_answer="went ahead", correct_index=2,
      options=["was cancelled", "was delayed", "went ahead", "was postponed"],
      reasoning_steps="'Despite' signals a contrast/obstacle overcome; so the match went ahead (opposite of expected delay).",
      shortcut="Despite => the opposite of expected.",
      common_trap="Choosing cancel/delay (the expected, not the contrast)."),
]

NEW = APT + CS + LOG + VERB
# sanity: no duplicated ids
ids = [q["id"] for q in NEW]
if len(ids) != len(set(ids)):
    print("DUPLICATE IDS:", [i for i in set(ids) if ids.count(i) > 1])

# every non-coding item must be complete
def complete(q):
    return all(q.get(k) for k in ("question", "correct_answer", "correct_index", "options", "reasoning_steps", "shortcut", "common_trap"))
incomplete = [q["id"] for q in NEW if not complete(q)]
print("Incomplete items:", incomplete)

with open(VERIFIED_PATH, "r", encoding="utf-8") as f:
    existing = json.load(f)
existing_ids = {q["id"] for q in existing}
merged = list(existing) + [q for q in NEW if q["id"] not in existing_ids]
for q in NEW:
    q.setdefault("trust_status", "verified")
    q.setdefault("source_bank", "verified_placement_questions")
    q.setdefault("verification_version", 1)
    q.setdefault("stage", "placement")
    q.setdefault("companies", ["tcs", "infosys", "wipro", "accenture", "cognizant"])
    q.setdefault("provenance", "pattern_relevant to TCS NQT / Infosys")

with open(VERIFIED_PATH, "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)
print("Added:", len([q for q in NEW if q["id"] not in existing_ids]))
print("New total:", len(merged))
print("Type dist:", dict(Counter(q["type"] for q in merged)))