"""Verbal-ability MCQ intake candidates, written by hand (not computed).

Verbal ability has no executable ground truth, so these 100 items are chosen to
be unambiguous: standard vocabulary, textbook grammar rules and common idioms,
with one clearly correct option. They are written as trust_status "unverified"
and must go through human review before being served; a reviewer should reject
any item they find arguable rather than fix it silently.

Subtypes (20 each): synonyms, antonyms, sentence correction, fill in the blank
(prepositions, tenses, articles), one-word substitution and idioms.

Usage: python scripts/gen_verbal_items.py [--seed 2026]
"""
import argparse
import json
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "app", "data", "intake", "verbal_generated_v2.json")
COMPANIES = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]

# (question, correct, [three wrong])
SYN = [
    ("ABUNDANT", "plentiful", ["scarce", "tiny", "rare"]),
    ("CANDID", "frank", ["secretive", "rude", "shy"]),
    ("BRIEF", "short", ["lengthy", "heavy", "loud"]),
    ("DILIGENT", "hardworking", ["lazy", "careless", "slow"]),
    ("OBSOLETE", "outdated", ["modern", "useful", "fragile"]),
    ("PRUDENT", "cautious", ["careless", "wasteful", "hasty"]),
    ("MITIGATE", "reduce", ["worsen", "ignore", "delay"]),
    ("VERBOSE", "wordy", ["silent", "polite", "clear"]),
    ("EPHEMERAL", "short-lived", ["lasting", "ancient", "solid"]),
    ("CONCUR", "agree", ["disagree", "argue", "refuse"]),
    ("BENEVOLENT", "kind", ["cruel", "selfish", "strict"]),
    ("SCARCE", "rare", ["plentiful", "cheap", "bulky"]),
    ("FRUGAL", "thrifty", ["generous", "lavish", "greedy"]),
    ("AUTHENTIC", "genuine", ["fake", "rare", "old"]),
    ("HINDER", "obstruct", ["help", "guide", "allow"]),
    ("AMBIGUOUS", "unclear", ["certain", "loud", "simple"]),
    ("RELUCTANT", "unwilling", ["eager", "ready", "quick"]),
    ("VIVID", "striking", ["dull", "faint", "vague"]),
    ("ENORMOUS", "huge", ["tiny", "average", "narrow"]),
    ("TRANQUIL", "calm", ["noisy", "stormy", "crowded"]),
]
ANT = [
    ("EXPAND", "contract", ["grow", "stretch", "widen"]),
    ("ANCIENT", "modern", ["old", "historic", "aged"]),
    ("GENEROUS", "stingy", ["kind", "rich", "noble"]),
    ("VICTORY", "defeat", ["triumph", "success", "win"]),
    ("ACCEPT", "reject", ["receive", "take", "agree"]),
    ("TEMPORARY", "permanent", ["brief", "short", "passing"]),
    ("OPTIMISTIC", "pessimistic", ["hopeful", "cheerful", "bright"]),
    ("INCREASE", "decrease", ["rise", "grow", "expand"]),
    ("TRANSPARENT", "opaque", ["clear", "thin", "bright"]),
    ("COURAGEOUS", "timid", ["bold", "brave", "fearless"]),
    ("ARTIFICIAL", "natural", ["false", "fake", "forged"]),
    ("SCARCE", "abundant", ["rare", "few", "limited"]),
    ("HUMBLE", "arrogant", ["modest", "meek", "polite"]),
    ("DEPART", "arrive", ["leave", "go", "exit"]),
    ("ENCOURAGE", "discourage", ["support", "inspire", "urge"]),
    ("SIMPLE", "complex", ["easy", "plain", "clear"]),
    ("VICE", "virtue", ["sin", "crime", "fault"]),
    ("MAJORITY", "minority", ["bulk", "most", "mass"]),
    ("FRAGILE", "sturdy", ["delicate", "thin", "weak"]),
    ("ASCEND", "descend", ["climb", "rise", "mount"]),
]
SENT = [
    ("She doesn't like coffee.", ["She don't like coffee.", "She not like coffee.", "She doesn't likes coffee."]),
    ("Each of the students has submitted the form.", ["Each of the students have submitted the form.", "Each of the student have submitted the form.", "Each of the students are submitted the form."]),
    ("Neither of the answers is correct.", ["Neither of the answers are correct.", "Neither of the answer are correct.", "Neither of the answers were correct."]),
    ("He has been working here for five years.", ["He has been working here since five years.", "He is working here since five years.", "He has been working here from five years."]),
    ("I have gone to the market.", ["I have went to the market.", "I have go to the market.", "I has gone to the market."]),
    ("The children are playing in the garden.", ["The children is playing in the garden.", "The childrens are playing in the garden.", "The children plays in the garden."]),
    ("If it rains tomorrow, we will cancel the trip.", ["If it will rain tomorrow, we will cancel the trip.", "If it rained tomorrow, we will cancel the trip.", "If it rains tomorrow, we would cancelled the trip."]),
    ("He is better than his brother.", ["He is more better than his brother.", "He is much more good than his brother.", "He is better than to his brother."]),
    ("I am looking forward to meeting you.", ["I am looking forward to meet you.", "I am looking forward for meeting you.", "I am looking forward to met you."]),
    ("Every boy in the class has a book.", ["Every boy in the class have a book.", "Every boys in the class has a book.", "Every boy in the class are having a book."]),
    ("She advised me to take rest.", ["She suggested me to take rest.", "She advised me taking rest.", "She advise me to take rest."]),
    ("He is senior to me.", ["He is senior than me.", "He is more senior than me.", "He is senior from me."]),
    ("The news is good.", ["The news are good.", "The news were good.", "The newses are good."]),
    ("My brother is an engineer.", ["My brother is a engineer.", "My brother is engineer.", "My brother are an engineer."]),
    ("She has fewer friends than her sister.", ["She has less friends than her sister.", "She has few friends than her sister.", "She has fewer friend than her sister."]),
    ("Hardly had he arrived when the meeting started.", ["Hardly he had arrived when the meeting started.", "Hardly had he arrived then the meeting started.", "Hardly he arrived when the meeting started."]),
    ("The teacher, along with the students, was present.", ["The teacher, along with the students, were present.", "The teacher, along with the students, are present.", "The teacher, along with the students, have present."]),
    ("I prefer tea to coffee.", ["I prefer tea than coffee.", "I prefer tea from coffee.", "I prefer more tea to coffee."]),
    ("He did not know where the station was.", ["He did not know where was the station.", "He did not knew where the station was.", "He did not know where the station is was."]),
    ("He explained the problem to me.", ["He explained me the problem.", "He explained to me the problem about.", "He explain the problem to me."]),
]
FILL = [
    ("She is good ___ mathematics.", "at", ["in", "on", "with"]),
    ("He has been absent ___ Monday.", "since", ["for", "from", "by"]),
    ("The meeting starts ___ 9 a.m.", "at", ["in", "on", "by"]),
    ("I have lived in Hyderabad ___ 2015.", "since", ["for", "from", "at"]),
    ("We are looking forward ___ the holidays.", "to", ["for", "at", "on"]),
    ("He is afraid ___ dogs.", "of", ["from", "at", "with"]),
    ("She apologised ___ being late.", "for", ["of", "on", "to"]),
    ("This book is different ___ that one.", "from", ["than", "with", "by"]),
    ("He insisted ___ paying the bill.", "on", ["for", "at", "to"]),
    ("The thief was caught ___ the police.", "by", ["with", "from", "at"]),
    ("By next year, she ___ her degree.", "will have completed", ["will complete", "has completed", "completed"]),
    ("If I ___ you, I would accept the offer.", "were", ["was", "am", "be"]),
    ("He ___ to the gym every morning.", "goes", ["go", "going", "gone"]),
    ("The train ___ before we reached the station.", "had left", ["has left", "leaves", "leaving"]),
    ("She is ___ honest girl.", "an", ["a", "the", "no article"]),
    ("He bought ___ umbrella yesterday.", "an", ["a", "the", "no article"]),
    ("Neither Ravi nor his friends ___ present.", "were", ["was", "is", "has been"]),
    ("I wish I ___ more time.", "had", ["have", "has", "having"]),
    ("The sun ___ in the east.", "rises", ["rise", "rose", "rising"]),
    ("He as well as his sisters ___ coming.", "is", ["are", "were", "have"]),
]
ONEWORD = [
    ("A person who loves books", "bibliophile", ["bibliographer", "librarian", "author"]),
    ("Government by the people", "democracy", ["autocracy", "monarchy", "aristocracy"]),
    ("One who knows everything", "omniscient", ["omnipotent", "omnipresent", "optimist"]),
    ("A person who travels on foot", "pedestrian", ["passenger", "commuter", "tourist"]),
    ("Fear of heights", "acrophobia", ["claustrophobia", "hydrophobia", "xenophobia"]),
    ("A speech delivered without preparation", "extempore", ["oration", "monologue", "soliloquy"]),
    ("The study of birds", "ornithology", ["entomology", "zoology", "ecology"]),
    ("That which cannot be read", "illegible", ["audible", "eligible", "legible"]),
    ("One who walks in sleep", "somnambulist", ["somniloquist", "hypnotist", "dreamer"]),
    ("A place where birds are kept", "aviary", ["apiary", "aquarium", "zoo"]),
    ("A person who is present everywhere at once", "omnipresent", ["omniscient", "omnipotent", "omnivorous"]),
    ("A word that has the same meaning as another", "synonym", ["antonym", "homonym", "acronym"]),
    ("A person who eats both plants and animals", "omnivore", ["herbivore", "carnivore", "insectivore"]),
    ("Fear of closed spaces", "claustrophobia", ["acrophobia", "agoraphobia", "hydrophobia"]),
    ("The killing of one's own brother", "fratricide", ["homicide", "patricide", "suicide"]),
    ("A person who does not believe in God", "atheist", ["theist", "pagan", "devotee"]),
    ("A government run by one person with absolute power", "autocracy", ["democracy", "republic", "bureaucracy"]),
    ("A list of books referred to in a work", "bibliography", ["biography", "glossary", "index of names"]),
    ("A person who can use both hands equally well", "ambidextrous", ["ambiguous", "amphibious", "ambitious"]),
    ("That which can be eaten", "edible", ["eligible", "legible", "audible"]),
]
IDIOM = [
    ("Break the ice", "to start a conversation in an awkward situation", ["to break something frozen", "to end a friendship", "to lose one's temper"]),
    ("A piece of cake", "a very easy task", ["a small dessert", "a difficult job", "a cheap gift"]),
    ("Once in a blue moon", "very rarely", ["every month", "at night", "very often"]),
    ("Burn the midnight oil", "to work late into the night", ["to waste fuel", "to start a fire", "to sleep early"]),
    ("Hit the nail on the head", "to say or do exactly the right thing", ["to hurt oneself", "to build a house", "to make a mistake"]),
    ("Spill the beans", "to reveal a secret", ["to cook a meal", "to make a mess", "to lose money"]),
    ("Under the weather", "feeling unwell", ["standing in the rain", "very happy", "in a cold place"]),
    ("Cost an arm and a leg", "to be very expensive", ["to cause an injury", "to be very cheap", "to be a bargain"]),
    ("The ball is in your court", "it is your turn to decide or act", ["you are good at sports", "you must leave", "you have lost the game"]),
    ("Call it a day", "to stop working for the day", ["to name a date", "to start a new job", "to wait until morning"]),
    ("Bite the bullet", "to face a difficult situation bravely", ["to eat quickly", "to give up", "to get angry"]),
    ("Let the cat out of the bag", "to reveal a secret by mistake", ["to adopt a pet", "to lose an animal", "to tell a lie"]),
    ("Beat around the bush", "to avoid the main point", ["to hunt animals", "to clean a garden", "to speak very loudly"]),
    ("On cloud nine", "extremely happy", ["very sad", "flying a plane", "feeling ill"]),
    ("Pull someone's leg", "to joke with someone", ["to injure someone", "to help someone walk", "to argue with someone"]),
    ("A blessing in disguise", "something good that seemed bad at first", ["a hidden gift box", "a religious ritual", "a clever costume"]),
    ("Cut corners", "to do something cheaply or carelessly", ["to build a house", "to draw a square", "to save time by driving"]),
    ("Get cold feet", "to become nervous and back out", ["to have a cold", "to feel the winter", "to walk barefoot"]),
    ("Back to square one", "to start again from the beginning", ["to win a game", "to go home early", "to reach the end"]),
    ("Miss the boat", "to lose an opportunity", ["to arrive on time", "to travel by sea", "to go fishing"]),
]


def build(rng, subtype, qtext, correct, wrong, diff, explanation):
    opts = [correct] + wrong
    assert len(set(opts)) == 4, (qtext, opts)
    order = list(range(4))
    rng.shuffle(order)
    shuffled = [opts[i] for i in order]
    return {
        "type": "verbal", "topic": subtype, "sub_topic": subtype, "difficulty": diff,
        "question": qtext, "options": shuffled, "correct_index": shuffled.index(correct), "correct_answer": correct,
        "explanation": explanation, "companies": COMPANIES, "role": ["student"], "stage": "placement",
        "trust_status": "unverified", "source_bank": "handwritten_verbal_v2", "verification_version": 0,
        "provenance": "hand-written standard vocabulary/grammar/idiom item; unambiguous by design; "
                      "needs human review before it is served",
    }


def run(seed):
    rng = random.Random(seed)
    items = []
    for w, c, wr in SYN:
        items.append(build(rng, "synonyms", f"Choose the word closest in meaning to {w}.", c, wr, "easy",
                           f"{w.title()} means {c}."))
    for w, c, wr in ANT:
        items.append(build(rng, "antonyms", f"Choose the word opposite in meaning to {w}.", c, wr, "easy",
                           f"The opposite of {w.lower()} is {c}."))
    for c, wr in SENT:
        items.append(build(rng, "sentence_correction", "Choose the grammatically correct sentence.", c, wr, "medium",
                           f"Correct form: \"{c}\""))
    for q, c, wr in FILL:
        items.append(build(rng, "fill_in_the_blank", f"Fill in the blank: {q}", c, wr, "easy",
                           f"\"{q.replace('___', c)}\" is the standard usage."))
    for q, c, wr in ONEWORD:
        items.append(build(rng, "one_word_substitution", f"One word for: {q}", c, wr, "medium",
                           f"{q} = {c}."))
    for idiom, c, wr in IDIOM:
        items.append(build(rng, "idioms", f"What does the idiom \"{idiom}\" mean?", c, wr, "easy",
                           f"\"{idiom}\" means {c}."))
    seen = set()
    for n, it in enumerate(items, 1):
        key = (it["question"], tuple(sorted(it["options"])))
        assert key not in seen, it["question"]
        seen.add(key)
        it["id"] = f"gen2-verbal-{it['topic']}-{n:03d}"
    return items


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=2026)
    a = ap.parse_args()
    items = run(a.seed)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {len(items)} items -> {OUT}")
