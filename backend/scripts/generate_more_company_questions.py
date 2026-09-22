#!/usr/bin/env python3
"""
Generate additional company questions for under-represented companies.
Uses the existing _base and _label_options from generate_service_company_questions.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
import random
import math
from pathlib import Path
from typing import Dict, List

from scripts.generate_service_company_questions import _base, _label_options, COMPANIES, _company_relevance

random.seed(42)

OUTPUT_DIR = Path("app/data/generated")


def _wipro_problems(count: int = 100) -> List[Dict]:
    out = []
    idx = 0

    for _ in range(min(20, count - idx)):
        a = random.randint(2, 8)
        b = random.randint(3, 12)
        while b == a:
            b = random.randint(3, 12)
        lcm = (a * b) // math.gcd(a, b)
        work_a = lcm // a
        work_b = lcm // b
        total_work = work_a + work_b
        days = round(lcm / total_work, 2) if total_work > 0 else 0

        opts_raw = [str(round(days, 2)), str(round(days+1, 2)), str(round(days-1, 2)), str(round(days+2, 2))]
        opts = _label_options(opts_raw)
        correct = opts[0]

        q = _base(
            "wipro_work", idx, "wipro_time_work", "Quantitative Aptitude", "easy",
            f"A can complete a task in {a} days and B in {b} days. How long together?",
            opts, correct,
            f"Combined rate: 1/{a} + 1/{b}. Time = {days} days",
            ["Wipro"], _company_relevance(["wipro"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(20, count - idx)):
        cp = random.randint(100, 500)
        profit_pct = random.choice([10, 15, 20, 25, 30])
        sp = int(cp * (1 + profit_pct/100))

        opts_raw = [str(sp), str(cp), str(cp*2), str(cp//2)]
        opts = _label_options(opts_raw)
        correct = opts[0]

        q = _base(
            "wipro_profit", idx, "wipro_profit_loss", "Quantitative Aptitude", "easy",
            f"Cost price is ₹{cp} and profit is {profit_pct}%. What is selling price?",
            opts, correct,
            f"SP = CP × (1 + {profit_pct}/100) = ₹{sp}",
            ["Wipro"], _company_relevance(["wipro"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(20, count - idx)):
        a = random.randint(2, 8)
        b = random.randint(2, 8)
        while b == a:
            b = random.randint(2, 8)
        c = random.randint(2, 8)
        d = round((b * c) / a, 2)

        opts = _label_options([str(d), str(round(d+1,2)), str(round(d-1,2)), str(round(d*2,2))])
        correct = opts.index(str(d))

        q = _base(
            "wipro_ratio", idx, "wipro_ratio", "Quantitative Aptitude", "easy",
            f"If {a}:{b} = {c}:?, what is the fourth proportion?",
            opts, correct,
            f"d = (b×c)/a = ({b}×{c})/{a} = {d}",
            ["Wipro"], _company_relevance(["wipro"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(20, count - idx)):
        n = random.randint(3, 8)
        avg = random.randint(20, 80)
        total = n * avg
        nums = [random.randint(avg-10, avg+10) for _ in range(n-1)]
        last = total - sum(nums)
        if last < 0: last = abs(last)

        opts = _label_options([str(int(last)), str(int(last+5)), str(int(last-5)), str(int(last*2))])
        correct = opts.index(str(int(last)))

        q = _base(
            "wipro_avg", idx, "wipro_average", "Quantitative Aptitude", "easy",
            f"Average of {n} numbers is {avg}. If {n-1} numbers are {', '.join(map(str, nums))}, what is last?",
            opts, correct,
            f"Sum = {total}. Last = {total} - {sum(nums)} = {int(last)}",
            ["Wipro"], _company_relevance(["wipro"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(20, count - idx)):
        value = random.randint(100, 500)
        inc = random.choice([10, 15, 20, 25])
        new_val = int(value * (1 + inc/100))

        opts = _label_options([str(new_val), str(value), str(value*2), str(value//2)])
        correct = opts.index(str(new_val))

        q = _base(
            "wipro_pct", idx, "wipro_percentage", "Quantitative Aptitude", "easy",
            f"What is {value} increased by {inc}%?",
            opts, correct,
            f"New = {value} × (1+{inc}/100) = {new_val}",
            ["Wipro"], _company_relevance(["wipro"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    return out[:count]


def _capgemini_problems(count: int = 100) -> List[Dict]:
    out = []
    idx = 0

    for _ in range(min(20, count - idx)):
        speed = random.randint(30, 120)
        time_hr = random.randint(1, 5)
        dist = speed * time_hr

        opts = _label_options([str(dist), str(dist+10), str(dist-10), str(dist*2)])
        correct = opts.index(str(dist))

        q = _base(
            "cap_speed", idx, "capgemini_speed", "Quantitative Aptitude", "easy",
            f"Car travels at {speed} km/h for {time_hr} hours. Distance?",
            opts, correct,
            f"Distance = {speed} × {time_hr} = {dist} km",
            ["Capgemini"], _company_relevance(["capgemini"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(15, count - idx)):
        sb = random.randint(5, 15)
        ss = random.randint(1, 5)
        downstream = sb + ss

        opts = _label_options([str(downstream), str(sb-ss), str(sb), str(ss)])
        correct = opts.index(str(downstream))

        q = _base(
            "cap_boat", idx, "capgemini_boat", "Quantitative Aptitude", "medium",
            f"Boat speed {sb} km/h, stream {ss} km/h. Downstream speed?",
            opts, correct,
            f"Downstream = {sb} + {ss} = {downstream} km/h",
            ["Capgemini"], _company_relevance(["capgemini"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(15, count - idx)):
        pa = random.randint(2, 6)
        pb = random.randint(3, 8)
        combined = 1/(1/pa + 1/pb)
        combined = round(combined, 2)

        opts = _label_options([str(combined), str(combined+1), str(combined-1), str(combined*2)])
        correct = opts.index(str(combined))

        q = _base(
            "cap_pipes", idx, "capgemini_pipes", "Quantitative Aptitude", "medium",
            f"Pipe A fills in {pa}hrs, Pipe B in {pb}hrs. Together?",
            opts, correct,
            f"Rate = 1/{pa} + 1/{pb} = {combined} hrs",
            ["Capgemini"], _company_relevance(["capgemini"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(15, count - idx)):
        start = random.choice(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        days_after = random.randint(1, 30)
        days_map = {"Monday":0,"Tuesday":1,"Wednesday":2,"Thursday":3,"Friday":4,"Saturday":5,"Sunday":6}
        result_idx = (days_map[start] + days_after) % 7
        result_day = list(days_map.keys())[result_idx]

        opts = _label_options([result_day, "Monday", "Tuesday", "Wednesday"])
        correct = opts.index(result_day)

        q = _base(
            "cap_cal", idx, "capgemini_calendar", "Quantitative Aptitude", "easy",
            f"If today is {start}, what day after {days_after} days?",
            opts, correct,
            f"({days_map[start]}+{days_after})%7 = {result_idx} = {result_day}",
            ["Capgemini"], _company_relevance(["capgemini"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(15, count - idx)):
        hr = random.randint(1, 12)
        mn = random.randint(0, 11) * 5
        ha = (hr % 12) * 30 + mn * 0.5
        ma = mn * 6
        angle = round(min(abs(ha-ma), 360-abs(ha-ma)), 1)

        opts = _label_options([str(angle), str(round(angle+15,1)), str(round(angle-15,1)), str(round(angle+30,1))])
        correct = opts.index(str(angle))

        q = _base(
            "cap_clock", idx, "capgemini_clock", "Quantitative Aptitude", "medium",
            f"Angle between hands at {hr}:{mn:02d}?",
            opts, correct,
            f"Hour: {ha}°, Minute: {ma}°, Angle = {angle}°",
            ["Capgemini"], _company_relevance(["capgemini"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    return out[:count]


def _tech_mahindra_problems(count: int = 100) -> List[Dict]:
    out = []
    idx = 0

    for _ in range(min(20, count - idx)):
        n = random.randint(4, 8)
        r = random.randint(2, n-1)
        npr = math.perm(n, r) if hasattr(math, 'perm') else math.factorial(n)//math.factorial(n-r)

        opts = _label_options([str(npr), str(npr//2), str(npr*2), str(npr+10)])
        correct = opts.index(str(npr))

        q = _base(
            "tm_perm", idx, "techm_perm", "Quantitative Aptitude", "medium",
            f"How many ways to arrange {r} items from {n} distinct?",
            opts, correct,
            f"nPr = {n}!/({n-r})! = {npr}",
            ["Tech Mahindra"], _company_relevance(["tech_mahindra"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(15, count - idx)):
        n = random.randint(4, 8)
        r = random.randint(2, n-1)
        ncr = math.comb(n, r) if hasattr(math, 'comb') else math.factorial(n)//(math.factorial(r)*math.factorial(n-r))

        opts = _label_options([str(ncr), str(ncr//2), str(ncr*2), str(ncr+5)])
        correct = opts.index(str(ncr))

        q = _base(
            "tm_comb", idx, "techm_comb", "Quantitative Aptitude", "medium",
            f"How many ways to choose {r} from {n}?",
            opts, correct,
            f"nCr = {n}!/({r}!×{n-r}!) = {ncr}",
            ["Tech Mahindra"], _company_relevance(["tech_mahindra"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(15, count - idx)):
        coins = random.randint(2, 4)
        total = 2 ** coins
        favorable = coins
        prob = f"{favorable}/{total}"

        opts = _label_options([prob, f"1/{total}", f"{coins-1}/{total}", f"{total-1}/{total}"])
        correct = opts.index(prob)

        q = _base(
            "tm_prob", idx, "techm_prob", "Quantitative Aptitude", "easy",
            f"{coins} coins tossed, exactly 1 head?",
            opts, correct,
            f"P = {favorable}/{total}",
            ["Tech Mahindra"], _company_relevance(["tech_mahindra"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(15, count - idx)):
        a = random.randint(2, 8)
        d = random.randint(2, 5)
        n = random.randint(3, 6)
        nth = a + (n-1)*d

        opts = _label_options([str(nth), str(nth+d), str(nth-d), str(nth*2)])
        correct = opts.index(str(nth))

        q = _base(
            "tm_series", idx, "techm_series", "Quantitative Aptitude", "easy",
            f"In AP {a}, {a+d}, {a+2d}, ..., {n}th term?",
            opts, correct,
            f"nth = {a}+({n-1})×{d} = {nth}",
            ["Tech Mahindra"], _company_relevance(["tech_mahindra"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    return out[:count]


def _cognizant_problems(count: int = 100) -> List[Dict]:
    out = []
    idx = 0

    for _ in range(min(20, count - idx)):
        vals = [random.randint(10, 100) for _ in range(4)]
        max_val = max(vals)
        max_item = f"Product {chr(65+vals.index(max_val))}"

        opts = _label_options([max_item, "Product A", "Product B", "Product C"])
        correct = opts.index(max_item)

        q = _base(
            "cog_di", idx, "cognizant_di", "Quantitative Aptitude", "medium",
            f"Highest sales: A={vals[0]}, B={vals[1]}, C={vals[2]}, D={vals[3]}?",
            opts, correct,
            f"Highest value: {max_val} for {max_item}",
            ["Cognizant"], _company_relevance(["cognizant"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(15, count - idx)):
        answer = "Both statements together are sufficient"
        opts = _label_options([
            "Statement 1 alone is sufficient",
            "Statement 2 alone is sufficient",
            answer,
            "Each statement alone is sufficient"
        ])
        correct = opts.index(answer)

        q = _base(
            "cog_ds", idx, "cognizant_ds", "Quantitative Aptitude", "medium",
            "Is x positive? (1) x²=16 (2) x>0",
            opts, correct,
            "From (1): x=±4 (not sufficient). From (2): x>0 (not alone). Together: x=4.",
            ["Cognizant"], _company_relevance(["cognizant"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(15, count - idx)):
        n = random.randint(4, 8)
        r = random.randint(2, n-1)
        ncr = math.comb(n, r) if hasattr(math, 'comb') else math.factorial(n)//(math.factorial(r)*math.factorial(n-r))

        opts = _label_options([str(ncr), str(ncr//2), str(ncr*2), str(ncr+5)])
        correct = opts.index(str(ncr))

        q = _base(
            "cog_comb", idx, "cognizant_comb", "Quantitative Aptitude", "medium",
            f"How many ways to choose {r} from {n}?",
            opts, correct,
            f"C({n},{r}) = {ncr}",
            ["Cognizant"], _company_relevance(["cognizant"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    return out[:count]


def _hcl_problems(count: int = 100) -> List[Dict]:
    """Generate problems for HCL."""
    out = []
    idx = 0

    for _ in range(min(25, count - idx)):
        # Simple coding logic
        n = random.randint(1, 10)
        total = n * (n+1) // 2
        opts = _label_options([str(total), str(total//2), str(total*2), str(total+10)])
        correct = opts.index(str(total))

        q = _base(
            "hcl_sum", idx, "hcl_loops", "Programming Logic", "easy",
            f"What is sum of 1 to {n}?",
            opts, correct,
            f"Sum = n(n+1)/2 = {n}×{n+1}/2 = {total}",
            ["HCL"], _company_relevance(["hcl"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(25, count - idx)):
        # Array manipulation
        arr = [random.randint(1, 20) for _ in range(5)]
        max_val = max(arr)
        opts = _label_options([str(max_val), str(min(arr)), str(sum(arr)//len(arr)), str(arr[0])])
        correct = opts.index(str(max_val))

        q = _base(
            "hcl_max", idx, "hcl_array", "Programming Logic", "easy",
            f"Given array {arr}, what is the maximum?",
            opts, correct,
            f"Maximum of {arr} = {max_val}",
            ["HCL"], _company_relevance(["hcl"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(25, count - idx)):
        # String length
        words = ["hello", "world", "python", "code", "test"]
        word = random.choice(words)
        length = len(word)
        opts = _label_options([str(length), str(length+1), str(length-1), str(length*2)])
        correct = opts.index(str(length))

        q = _base(
            "hcl_str", idx, "hcl_string", "Programming Logic", "easy",
            f"Length of '{word}'?",
            opts, correct,
            f"'{word}' has {length} characters",
            ["HCL"], _company_relevance(["hcl"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    return out[:count]


def _ibm_problems(count: int = 100) -> List[Dict]:
    """Generate problems for IBM."""
    out = []
    idx = 0

    for _ in range(min(25, count - idx)):
        # Database query result count
        table_size = random.randint(10, 100)
        filter_pct = random.choice([10, 20, 25, 50])
        result = int(table_size * filter_pct / 100)
        opts = _label_options([str(result), str(table_size), str(result//2), str(result*2)])
        correct = opts.index(str(result))

        q = _base(
            "ibm_db", idx, "ibm_database", "CS Fundamentals", "medium",
            f"Table has {table_size} rows. Filter keeps {filter_pct}%. How many rows?",
            opts, correct,
            f"Result = {table_size} × {filter_pct}% = {result}",
            ["IBM"], _company_relevance(["ibm"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(25, count - idx)):
        # SQL aggregation
        values = [random.randint(10, 100) for _ in range(4)]
        avg_val = round(sum(values)/len(values), 1)
        opts = _label_options([str(avg_val), str(sum(values)), str(min(values)), str(max(values))])
        correct = opts.index(str(avg_val))

        q = _base(
            "ibm_sql", idx, "ibm_sql", "CS Fundamentals", "medium",
            f"Values: {values}. What is the average?",
            opts, correct,
            f"Average = ({'+'.join(map(str, values))})/{len(values)} = {avg_val}",
            ["IBM"], _company_relevance(["ibm"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(25, count - idx)):
        # Network routing
        nodes = random.randint(3, 8)
        hops = nodes - 1
        opts = _label_options([str(hops), str(nodes), str(nodes+1), str(hops*2)])
        correct = opts.index(str(hops))

        q = _base(
            "ibm_net", idx, "ibm_network", "CS Fundamentals", "easy",
            f"In a network of {nodes} nodes, minimum hops to connect all?",
            opts, correct,
            f"Minimum hops = nodes - 1 = {hops}",
            ["IBM"], _company_relevance(["ibm"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    return out[:count]


def _deloitte_problems(count: int = 100) -> List[Dict]:
    """Generate problems for Deloitte."""
    out = []
    idx = 0

    for _ in range(min(25, count - idx)):
        # Financial calculations
        revenue = random.randint(1000, 5000)
        cost = random.randint(500, revenue//2)
        profit = revenue - cost
        opts = _label_options([str(profit), str(revenue), str(cost), str(revenue+cost)])
        correct = opts.index(str(profit))

        q = _base(
            "dl_finance", idx, "deloitte_finance", "Quantitative Aptitude", "medium",
            f"Revenue: ₹{revenue}, Cost: ₹{cost}. Profit?",
            opts, correct,
            f"Profit = Revenue - Cost = {revenue} - {cost} = {profit}",
            ["Deloitte"], _company_relevance(["deloitte"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(25, count - idx)):
        # Percentage calculations
        salary = random.randint(30000, 80000)
        tax_pct = random.choice([10, 15, 20, 25])
        tax = int(salary * tax_pct / 100)
        opts = _label_options([str(tax), str(salary), str(tax//2), str(tax*2)])
        correct = opts.index(str(tax))

        q = _base(
            "dl_tax", idx, "deloitte_tax", "Quantitative Aptitude", "easy",
            f"Salary ₹{salary}, tax {tax_pct}%. Tax amount?",
            opts, correct,
            f"Tax = {salary} × {tax_pct}% = {tax}",
            ["Deloitte"], _company_relevance(["deloitte"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    return out[:count]


def _google_problems(count: int = 100) -> List[Dict]:
    """Generate problems for Google."""
    out = []
    idx = 0

    for _ in range(min(25, count - idx)):
        # Algorithm complexity
        n = random.randint(10, 100)
        log_n = round(math.log2(n), 1)
        opts = _label_options([str(log_n), str(n), str(n*n), str(n//2)])
        correct = opts.index(str(log_n))

        q = _base(
            "g_log", idx, "google_complexity", "CS Fundamentals", "medium",
            f"Binary search on {n} elements. How many comparisons?",
            opts, correct,
            f"Binary search: O(log n) = log2({n}) ≈ {log_n}",
            ["Google"], _company_relevance(["google"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(25, count - idx)):
        # Binary tree nodes
        height = random.randint(3, 6)
        max_nodes = 2**height - 1
        opts = _label_options([str(max_nodes), str(height), str(height*2), str(max_nodes//2)])
        correct = opts.index(str(max_nodes))

        q = _base(
            "g_tree", idx, "google_tree", "CS Fundamentals", "medium",
            f"Complete binary tree of height {height}. Max nodes?",
            opts, correct,
            f"Max nodes = 2^h - 1 = 2^{height} - 1 = {max_nodes}",
            ["Google"], _company_relevance(["google"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    for _ in range(min(25, count - idx)):
        # Hash table
        size = random.randint(10, 100)
        load_factor = 0.75
        items = int(size * load_factor)
        opts = _label_options([str(items), str(size), str(size//2), str(items*2)])
        correct = opts.index(str(items))

        q = _base(
            "g_hash", idx, "google_hash", "CS Fundamentals", "medium",
            f"Hash table size {size}, load factor 0.75. Items stored?",
            opts, correct,
            f"Items = size × load_factor = {size} × 0.75 = {items}",
            ["Google"], _company_relevance(["google"], ["tcs", "infosys"])
        )
        out.append(q)
        idx += 1

    return out[:count]


def generate_all():
    """Generate questions for all under-represented companies."""
    all_questions = []

    companies = [
        ("Wipro", _wipro_problems, 100),
        ("Capgemini", _capgemini_problems, 100),
        ("Tech Mahindra", _tech_mahindra_problems, 100),
        ("Cognizant", _cognizant_problems, 100),
        ("HCL", _hcl_problems, 100),
        ("IBM", _ibm_problems, 100),
        ("Deloitte", _deloitte_problems, 100),
        ("Google", _google_problems, 100),
    ]

    for name, generator, count in companies:
        print(f"Generating {name} questions...")
        qs = generator(count)
        all_questions.extend(qs)
        print(f"  Generated {len(qs)} questions")

    return all_questions


def save_questions(questions: List[Dict]):
    """Save questions to files."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    company_questions = {}
    for q in questions:
        tags = q.get("company_tags", [])
        if tags:
            company = tags[0].lower()
        else:
            company = "general"
        if company not in company_questions:
            company_questions[company] = []
        company_questions[company].append(q)

    for company, qs in company_questions.items():
        company_dir = OUTPUT_DIR / company
        company_dir.mkdir(exist_ok=True)

        max_per_file = 50
        for i in range(0, len(qs), max_per_file):
            chunk = qs[i:i+max_per_file]
            filename = company_dir / f"{company}_batch{i//max_per_file+1}.json"
            with open(filename, 'w') as f:
                json.dump(chunk, f, indent=2)
            print(f"Saved {len(chunk)} to {filename}")

    combined_file = OUTPUT_DIR / "more_company_questions.json"
    with open(combined_file, 'w') as f:
        json.dump(questions, f, indent=2)
    print(f"Saved combined: {len(questions)} to {combined_file}")


def main():
    print("Generating additional company questions...")
    questions = generate_all()
    print(f"\nTotal generated: {len(questions)}")

    print("\nSaving questions...")
    save_questions(questions)
    print("\nDone!")


if __name__ == "__main__":
    main()