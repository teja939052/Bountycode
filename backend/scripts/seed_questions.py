"""Seed 500+ curated placement prep questions into MongoDB."""

import asyncio
import os
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "placementpro")

# ──────────────────────────────────────────────────────────────────────────────
# APTITUDE — QUANTITATIVE (200 questions)
# ──────────────────────────────────────────────────────────────────────────────

QUANT = [
    # Percentages
    ("If a number is increased by 20% and then decreased by 20%, what is the net change?", "Percentages", "TCS", "easy", "4% decrease"),
    ("A product costs $500. After a 15% discount and then 10% tax, what is the final price?", "Percentages", "TCS", "medium", "$577.50"),
    ("If A's salary is 20% more than B's, by what percent is B's salary less than A's?", "Percentages", "Infosys", "easy", "16.67%"),
    ("Population of a city is 50,000. It increases by 10% in year 1 and decreases by 5% in year 2. What is the population after 2 years?", "Percentages", "TCS", "medium", "52,250"),
    ("A student scored 120 marks and failed by 30 marks. If the pass percentage is 40%, what is the maximum marks?", "Percentages", "Wipro", "medium", "375"),
    ("The price of sugar increases by 25%. By what percent should consumption be reduced so that expenditure remains same?", "Percentages", "Infosys", "medium", "20%"),
    ("Two successive discounts of 20% and 10% are equivalent to a single discount of:", "Percentages", "TCS", "easy", "28%"),
    ("If the numerator of a fraction is increased by 50% and denominator is decreased by 20%, the value becomes 3/2. Find the original fraction.", "Percentages", "TCS", "hard", "4/5"),
    ("In an election between two candidates, 75% of voters voted. 2% of votes were invalid. The winner got 55% of valid votes and won by 3600 votes. Total voters:", "Percentages", "Infosys", "hard", "40,000"),
    ("A man spends 30% of his income on food, 25% on rent, 15% on transport. If he saves $4800, what is his income?", "Percentages", "Wipro", "easy", "$16,000"),
    ("If the side of a square is increased by 20%, by what percent does its area increase?", "Percentages", "TCS", "easy", "44%"),
    ("A shopkeeper marks his goods 40% above cost price and gives 20% discount. Find his profit percentage.", "Percentages", "Infosys", "medium", "12%"),
    ("If x is 25% less than y, by what percent is y more than x?", "Percentages", "TCS", "easy", "33.33%"),
    ("A tank is 20% full. After adding 720 liters, it becomes 80% full. What is the capacity of the tank?", "Percentages", "Wipro", "medium", "1200 liters"),
    ("The population of a town increases by 10% annually. If present population is 10,000, what will be the population after 3 years?", "Percentages", "TCS", "medium", "13,310"),

    # Profit and Loss
    ("A shopkeeper buys an item for $80 and sells it for $100. What is the profit percentage?", "Profit and Loss", "TCS", "easy", "25%"),
    ("A man buys a horse for $400 and sells it at a loss of 15%. What is the selling price?", "Profit and Loss", "TCS", "easy", "$340"),
    ("By selling an article for $560, a man gains 12%. What is the cost price?", "Profit and Loss", "Infosys", "easy", "$500"),
    ("If the cost price of 20 articles is equal to the selling price of 15 articles, find the profit percentage.", "Profit and Loss", "TCS", "medium", "33.33%"),
    ("A tradesman marks his goods 30% above cost price. He allows 10% discount on the marked price. His profit is:", "Profit and Loss", "Wipro", "medium", "17%"),
    ("A man buys a cycle for $2000 and sells it at 15% loss. What is the selling price?", "Profit and Loss", "Infosys", "easy", "$1,700"),
    ("If selling price is doubled, profit triples. Find the profit percentage.", "Profit and Loss", "TCS", "hard", "100%"),
    ("A shopkeeper cheats 20% while buying and 20% while selling. His gain percentage is:", "Profit and Loss", "TCS", "hard", "44%"),
    ("By selling 50 meters of cloth, a man gains the selling price of 10 meters. Find the profit percentage.", "Profit and Loss", "Infosys", "medium", "25%"),
    ("A fruit seller buys oranges at 10 for $8 and sells at 8 for $12. His profit percentage is:", "Profit and Loss", "Wipro", "medium", "50%"),
    ("If CP = $450 and SP = $540, find the profit percentage.", "Profit and Loss", "TCS", "easy", "20%"),
    ("An article is sold at 20% profit. If both CP and SP increase by 10%, the profit percentage:", "Profit and Loss", "TCS", "medium", "stays the same"),
    ("A man sold two watches for $4900 each. On one he gained 10% and on the other he lost 10%. His overall gain or loss:", "Profit and Loss", "Infosys", "medium", "1% loss"),
    ("The cost price of an article is 60% of the marked price. After giving a discount of 20%, the profit percentage is:", "Profit and Loss", "TCS", "medium", "33.33%"),
    ("By selling an article for $600, a person loses 20%. To gain 20%, the selling price should be:", "Profit and Loss", "Wipro", "hard", "$900"),

    # Time and Work
    ("A can do a work in 12 days, B in 15 days. How many days to complete together?", "Time and Work", "TCS", "medium", "6.67 days"),
    ("A can do a work in 10 days, B in 15 days. They work together for 5 days. What fraction of work is left?", "Time and Work", "Infosys", "medium", "1/6"),
    ("If 12 workers can build a wall in 18 days, how many days will 15 workers take?", "Time and Work", "TCS", "easy", "14.4 days"),
    ("A does a work in 20 days. B is 25% more efficient than A. How many days will B take?", "Time and Work", "Wipro", "medium", "16 days"),
    ("A and B together can do a work in 12 days. A alone can do it in 20 days. In how many days can B alone do it?", "Time and Work", "TCS", "medium", "30 days"),
    ("If 8 men or 12 women can do a work in 10 days, how long will 6 men and 4 women take?", "Time and Work", "Infosys", "hard", "10 days"),
    ("Pipe A fills a tank in 6 hours, Pipe B empties it in 8 hours. If both are open, how long to fill?", "Time and Work", "TCS", "medium", "24 hours"),
    ("A can do a work in 24 days, B in 36 days. They start together but A leaves 3 days before completion. Total days:", "Time and Work", "Wipro", "hard", "13.8 days"),
    ("20 workers can build a wall in 30 days. After 10 days, 10 more workers join. Total days to complete:", "Time and Work", "TCS", "medium", "20 days"),
    ("A is twice as efficient as B. Together they complete a work in 12 days. How long for A alone?", "Time and Work", "Infosys", "easy", "18 days"),
    ("Pipe A fills in 12 hours, Pipe B in 15 hours, Pipe C empties in 20 hours. All open together, time to fill:", "Time and Work", "TCS", "hard", "10 hours"),
    ("A and B together can do a work in 8 days. B and C together in 12 days. A and C together in 16 days. Time for A alone:", "Time and Work", "Wipro", "hard", "9.6 days"),
    ("15 men can do a work in 20 days. How many men are needed to finish in 12 days?", "Time and Work", "TCS", "easy", "25 men"),
    ("A does 1/3 of the work in 5 days, B does 1/4 of the work in 6 days. Time for both together:", "Time and Work", "Infosys", "medium", "7.2 days"),
    ("If 6 men and 8 boys can do a work in 10 days, and 4 men and 7 boys in 12 days, how long for 1 man alone?", "Time and Work", "TCS", "hard", "110 days"),

    # Speed, Distance, Time
    ("A car travels 150 km in 3 hours. What is its speed in m/s?", "Speed Distance Time", "TCS", "easy", "13.89 m/s"),
    ("A train 200m long passes a pole in 20 seconds. Find its speed in km/h.", "Speed Distance Time", "TCS", "easy", "36 km/h"),
    ("If a person walks at 5 km/h instead of 4 km/h, he covers 10 km more in the same time. Find the distance.", "Speed Distance Time", "Infosys", "medium", "200 km"),
    ("Two trains start from stations 300 km apart at the same time. Speeds are 60 km/h and 40 km/h. When do they meet?", "Speed Distance Time", "TCS", "easy", "3 hours"),
    ("A boat goes 20 km downstream in 2 hours and 8 km upstream in 2 hours. Find the speed of the current.", "Speed Distance Time", "Infosys", "medium", "3 km/h"),
    ("A man covers a distance at 6 km/h and returns at 4 km/h. Average speed is:", "Speed Distance Time", "TCS", "easy", "4.8 km/h"),
    ("A train crosses a platform 200m long in 30 seconds. The train is 150m long. Find its speed.", "Speed Distance Time", "Wipro", "medium", "45 km/h"),
    ("If the speed of a boat in still water is 10 km/h and the current is 3 km/h, time to go 49 km upstream:", "Speed Distance Time", "TCS", "medium", "7 hours"),
    ("A car covers first half of a journey at 40 km/h and second half at 60 km/h. Average speed:", "Speed Distance Time", "Infosys", "medium", "48 km/h"),
    ("Two persons start from the same point in opposite directions at 5 km/h and 7 km/h. After how many hours are they 48 km apart?", "Speed Distance Time", "TCS", "easy", "4 hours"),
    ("A train 100m long crosses a man walking at 5 km/h in the opposite direction in 4 seconds. Speed of train:", "Speed Distance Time", "Wipro", "hard", "85 km/h"),
    ("A runner completes a 200m race in 20 seconds. His speed in km/h is:", "Speed Distance Time", "TCS", "easy", "36 km/h"),
    ("If a cyclist moves at 15 km/h, how far does he go in 36 minutes?", "Speed Distance Time", "Infosys", "easy", "9 km"),
    ("A car accelerates from 0 to 60 km/h in 10 seconds. Average acceleration in m/s²:", "Speed Distance Time", "Wipro", "medium", "1.67 m/s²"),
    ("Distance between two cities is 600 km. If a train travels at 100 km/h and a car at 80 km/h, who reaches first and by how much?", "Speed Distance Time", "TCS", "medium", "train by 1.5 hours"),

    # Averages
    ("The average of 5 numbers is 20. If one number is removed, the average becomes 18. What is the removed number?", "Averages", "Infosys", "easy", "28"),
    ("Average of 11 results is 60. If the average of first 6 is 58 and last 6 is 63, find the 6th result.", "Averages", "TCS", "medium", "65"),
    ("The average age of 30 students is 14 years. If the teacher's age is included, the average becomes 15. Find the teacher's age.", "Averages", "TCS", "easy", "45"),
    ("Average of 5 consecutive even numbers is 22. Find the largest number.", "Averages", "Infosys", "easy", "26"),
    ("The average of first 50 natural numbers is:", "Averages", "TCS", "easy", "25.5"),
    ("If the average of a, b, c is 20 and the average of b, c, d is 25, and d = 35, find a.", "Averages", "Wipro", "medium", "5"),
    ("The average marks of 40 students is 45. After including marks of 5 more students, the average rises to 50. What is the average of the 5 new students?", "Averages", "TCS", "medium", "80"),
    ("Average of first 10 even numbers is:", "Averages", "Infosys", "easy", "11"),
    ("The average of 25 results is 18. Average of first 12 is 14, and last 12 is 20. Find the 13th result.", "Averages", "Wipro", "medium", "28"),
    ("Average monthly salary of 10 employees is $3000. If the manager's salary is added, average increases by $500. Manager's salary:", "Averages", "TCS", "easy", "$8,000"),
    ("Average of three numbers is 40. First two numbers are 30 and 45. Find the third number.", "Averages", "Infosys", "easy", "45"),
    ("If the average of first n natural numbers is 20, find n.", "Averages", "TCS", "medium", "39"),
    ("The average of 8 readings is 42. If one reading 148 is wrongly taken as 128, the correct average is:", "Averages", "Wipro", "medium", "44.5"),
    ("Average of 50 students in a class is 72. Average of boys is 75 and girls is 70. Number of girls:", "Averages", "TCS", "medium", "30"),
    ("The average of 0, 1, 2, 3, ..., 100 is:", "Averages", "Infosys", "easy", "50"),

    # Ratios and Proportions
    ("A and B share profits in the ratio 3:5. If total profit is $24,000, what is B's share?", "Ratios", "Infosys", "easy", "$15,000"),
    ("The ratio of present ages of A and B is 5:7. If B is 28 years old, find A's age.", "Ratios", "TCS", "easy", "20 years"),
    ("Divide $1200 in the ratio 3:5. Find the two parts.", "Ratios", "Wipro", "easy", "$450 and $750"),
    ("The ratio of two numbers is 3:5 and their sum is 48. Find the numbers.", "Ratios", "TCS", "easy", "18 and 30"),
    ("If A:B = 2:3 and B:C = 4:5, find A:B:C.", "Ratios", "Infosys", "medium", "8:12:15"),
    ("The ratio of milk to water in a mixture is 4:1. If 5 liters of water is added, the ratio becomes 2:1. Find the quantity of milk.", "Ratios", "TCS", "medium", "20 liters"),
    ("If 3x = 5y and 2y = 7z, find x:z.", "Ratios", "Wipro", "hard", "35:6"),
    ("A sum of $8800 is divided among A, B, C such that A gets 2/3 of what B gets and B gets 1/4 of what C gets. Find C's share.", "Ratios", "TCS", "hard", "$4,800"),
    ("The ratio of boys to girls in a school is 3:2. If 20 new girls are admitted, the ratio becomes 3:4. Find the original number of boys.", "Ratios", "Infosys", "medium", "60"),
    ("The incomes of A and B are in the ratio 4:5 and their expenditures are in the ratio 3:4. If A saves $500 and B saves $700, find their incomes.", "Ratios", "TCS", "hard", "$5,500 and $6,875"),

    # Permutations and Combinations
    ("In how many ways can 5 people sit around a circular table?", "Permutations", "Infosys", "medium", "24"),
    ("How many 3-digit numbers can be formed using digits 1, 2, 3, 4, 5 without repetition?", "Permutations", "TCS", "easy", "60"),
    ("In how many ways can the letters of 'DAUGHTER' be arranged?", "Permutations", "Wipro", "medium", "40,320"),
    ("From 8 boys and 5 girls, a committee of 5 is to be formed with at least 3 girls. Number of ways:", "Permutations", "TCS", "hard", "220"),
    ("How many ways can 7 people sit in a row if two particular persons must sit together?", "Permutations", "Infosys", "medium", "1,440"),
    ("A coin is tossed 3 times. What is the probability of getting at least 2 heads?", "Permutations", "TCS", "easy", "1/2"),
    ("In how many ways can 10 people be divided into two groups of 5?", "Permutations", "Wipro", "hard", "126"),
    ("Find the number of arrangements of the letters of 'MISSISSIPPI'.", "Permutations", "TCS", "hard", "34,650"),
    ("A committee of 4 is to be selected from 6 men and 4 women. If there must be at least 2 women, the number of ways:", "Permutations", "Infosys", "medium", "185"),
    ("In how many ways can 5 subjects be arranged in 5 periods if one particular subject is always in the first period?", "Permutations", "Wipro", "easy", "24"),

    # Probability
    ("Two dice are thrown. What is the probability that the sum is 7?", "Probability", "TCS", "easy", "1/6"),
    ("A bag contains 5 red and 3 blue balls. Two balls are drawn. Probability that both are red:", "Probability", "Infosys", "easy", "5/14"),
    ("A coin is tossed twice. What is the probability of getting exactly one head?", "Probability", "TCS", "easy", "1/2"),
    ("From a deck of 52 cards, 2 cards are drawn. Probability that both are kings:", "Probability", "Wipro", "medium", "1/221"),
    ("A bag contains 4 white, 5 black, and 6 red balls. Two balls are drawn. Probability that both are different colors:", "Probability", "TCS", "medium", "20/35 or 4/7"),
    ("The probability of an event A is 0.4 and event B is 0.5. If they are independent, P(A and B) is:", "Probability", "Infosys", "easy", "0.2"),
    ("A card is drawn from a deck. What is the probability that it is a face card?", "Probability", "TCS", "easy", "3/13"),
    ("A die is thrown. What is the probability of getting a number greater than 4?", "Probability", "Wipro", "easy", "1/3"),
    ("If P(A) = 0.3, P(B) = 0.4, P(A∪B) = 0.6, find P(A∩B).", "Probability", "TCS", "easy", "0.1"),
    ("A box contains 3 green, 4 yellow, and 5 blue balls. One ball is drawn. Probability it is not blue:", "Probability", "Infosys", "easy", "7/12"),

    # Mixtures and Alligations
    ("A vessel contains 80 liters of milk. 8 liters are removed and replaced with water. This is done 3 times. How much milk is left?", "Mixtures", "Wipro", "medium", "58.32 liters"),
    ("In what ratio must water be mixed with milk costing $12/liter to get a mixture worth $8/liter?", "Mixtures", "TCS", "easy", "1:2"),
    ("A mixture of 40 liters of milk and water contains 10% water. How much water must be added to make water 25%?", "Mixtures", "Infosys", "medium", "8 liters"),
    ("A merchant mixes two varieties of rice costing $20/kg and $30/kg in the ratio 3:2. Selling price for 20% profit:", "Mixtures", "TCS", "medium", "$30/kg"),
    ("A mixture contains milk and water in ratio 5:3. If 16 liters of water is added, the ratio becomes 5:7. Find the quantity of milk.", "Mixtures", "Wipro", "medium", "40 liters"),
    ("How many kg of rice at $40/kg should be mixed with 80 kg of rice at $60/kg to get a mixture worth $50/kg?", "Mixtures", "TCS", "easy", "80 kg"),

    # Simple and Compound Interest
    ("Find the simple interest on $5000 at 8% for 3 years.", "Simple Interest", "TCS", "easy", "$1,200"),
    ("Find the compound interest on $10,000 at 10% for 2 years compounded annually.", "Compound Interest", "Infosys", "easy", "$2,100"),
    ("A sum becomes double in 5 years at simple interest. In how many years will it become triple?", "Simple Interest", "TCS", "medium", "10 years"),
    ("Find the compound interest on $8000 at 15% per annum for 2 years compounded annually.", "Compound Interest", "Wipro", "medium", "$2,580"),
    ("The compound interest on a sum for 2 years is $832 and the simple interest is $800. Find the rate of interest.", "Compound Interest", "TCS", "medium", "8%"),
    ("A sum of $12,000 amounts to $13,230 in 2 years at compound interest. Find the rate.", "Compound Interest", "Infosys", "easy", "5%"),
    ("Find the difference between compound interest and simple interest on $5000 for 3 years at 10%.", "Compound Interest", "TCS", "hard", "$165"),
    ("At what rate of compound interest will $1000 become $1331 in 3 years?", "Compound Interest", "Wipro", "easy", "10%"),
    ("The simple interest on a sum is $2000 and the compound interest is $2100 for 2 years. Find the principal.", "Compound Interest", "TCS", "medium", "$20,000"),
    ("Find the compound interest on $16,000 at 10% per annum for 1.5 years, compounded half-yearly.", "Compound Interest", "Infosys", "hard", "$2,521"),

    # Boats and Streams
    ("A boat goes 24 km downstream in 4 hours and 16 km upstream in 4 hours. Find the speed of the current.", "Boats and Streams", "TCS", "easy", "1 km/h"),
    ("Speed of a boat in still water is 8 km/h. It goes 24 km downstream in 3 hours. Find the speed of the stream.", "Boats and Streams", "Infosys", "easy", "0 km/h → boat speed = 8"),
    ("A boat goes 30 km upstream in 5 hours and 40 km downstream in 4 hours. Find the speed of the current.", "Boats and Streams", "TCS", "medium", "2.5 km/h"),
    ("Speed of boat in still water is 15 km/h. Speed of current is 5 km/h. Time to travel 40 km downstream:", "Boats and Streams", "Wipro", "easy", "2 hours"),
    ("A man can row 10 km/h in still water. The river flows at 3 km/h. He rows upstream for 14 km. Time taken:", "Boats and Streams", "TCS", "easy", "2 hours"),

    # Geometry
    ("A circle has radius 7 cm. What is its area? (Use pi = 22/7)", "Geometry", "Wipro", "easy", "154 cm²"),
    ("Find the area of a triangle with base 12 cm and height 8 cm.", "Geometry", "TCS", "easy", "48 cm²"),
    ("The diagonal of a square is 10 cm. Find its area.", "Geometry", "Infosys", "medium", "50 cm²"),
    ("A rectangle has length 15 cm and breadth 10 cm. Find its diagonal.", "Geometry", "TCS", "easy", "18.03 cm"),
    ("Find the circumference of a circle with diameter 14 cm.", "Geometry", "Wipro", "easy", "44 cm"),
    ("The area of a rhombus is 120 cm² and one diagonal is 12 cm. Find the other diagonal.", "Geometry", "TCS", "medium", "20 cm"),
    ("A right triangle has sides 3 cm, 4 cm, 5 cm. Find the area.", "Geometry", "Infosys", "easy", "6 cm²"),
    ("Find the volume of a cylinder with radius 7 cm and height 10 cm.", "Geometry", "TCS", "medium", "1540 cm³"),
    ("The perimeter of a square is 48 cm. Find its area.", "Geometry", "Wipro", "easy", "144 cm²"),
    ("Find the total surface area of a cube with side 5 cm.", "Geometry", "TCS", "easy", "150 cm²"),
    ("A cone has radius 7 cm and slant height 25 cm. Find its curved surface area.", "Geometry", "Infosys", "medium", "550 cm²"),
    ("The radius of a sphere is 6 cm. Find its volume.", "Geometry", "TCS", "medium", "904.78 cm³"),
    ("A sector has angle 60° and radius 14 cm. Find its area.", "Geometry", "Wipro", "medium", "102.67 cm²"),
    ("Find the area of a parallelogram with base 20 cm and height 12 cm.", "Geometry", "TCS", "easy", "240 cm²"),
    ("The length and breadth of a rectangle are in ratio 5:3. If the perimeter is 48 cm, find the area.", "Geometry", "Infosys", "medium", "135 cm²"),

    # Number Systems
    ("Find the remainder when 2^10 is divided by 7.", "Number Systems", "TCS", "medium", "2"),
    ("What is the unit digit of 7^255?", "Number Systems", "TCS", "medium", "3"),
    ("How many factors does 360 have?", "Number Systems", "Infosys", "medium", "24"),
    ("Find the HCF of 12, 18, and 24.", "Number Systems", "TCS", "easy", "6"),
    ("Find the LCM of 12, 15, and 20.", "Number Systems", "Wipro", "easy", "60"),
    ("If N = 2^5 × 3^2 × 5, how many positive divisors does N have?", "Number Systems", "TCS", "medium", "18"),
    ("The sum of first 20 natural numbers is:", "Number Systems", "Infosys", "easy", "210"),
    ("What is the sum of all prime numbers between 1 and 20?", "Number Systems", "TCS", "easy", "77"),
    ("Find the greatest 4-digit number divisible by 12, 18, and 24.", "Number Systems", "Wipro", "medium", "9,936"),
    ("The HCF of two numbers is 12 and their LCM is 72. If one number is 24, find the other.", "Number Systems", "TCS", "easy", "36"),
    ("What is the remainder when 100! is divided by 101?", "Number Systems", "TCS", "hard", "100"),
    ("Find the sum of the digits of the smallest number which when divided by 18 and 24 leaves remainder 5 in each case.", "Number Systems", "Infosys", "hard", "77"),
    ("What is the last two digits of 7^202?", "Number Systems", "TCS", "hard", "01"),
    ("Find the number of zeroes in 100!.", "Number Systems", "TCS", "medium", "24"),
    ("The product of two numbers is 2160 and their HCF is 12. Find the LCM.", "Number Systems", "Wipro", "medium", "180"),
]

# ──────────────────────────────────────────────────────────────────────────────
# APTITUDE — LOGICAL REASONING (100 questions)
# ──────────────────────────────────────────────────────────────────────────────

LOGICAL = [
    ("Find the next number: 2, 6, 12, 20, 30, ?", "Series", "TCS", "easy", "42"),
    ("Find the next: 3, 9, 27, 81, ?", "Series", "TCS", "easy", "243"),
    ("Find the missing: 5, 10, 20, 40, ?", "Series", "Infosys", "easy", "80"),
    ("Find the next: 1, 1, 2, 3, 5, 8, ?", "Series", "TCS", "medium", "13"),
    ("Complete the series: 2, 5, 10, 17, 26, ?", "Series", "Wipro", "medium", "37"),
    ("Find the odd one out: 1, 4, 9, 16, 23, 36", "Series", "TCS", "easy", "23"),
    ("Complete: AZ, BY, CX, DW, ?", "Series", "Infosys", "easy", "EV"),
    ("Find the next: 10, 20, 35, 55, ?", "Series", "Wipro", "medium", "80"),
    ("Next in series: 1, 4, 9, 16, 25, ?", "Series", "TCS", "easy", "36"),
    ("Find missing: 3, 6, 12, 24, ?", "Series", "TCS", "easy", "48"),

    ("If COMPUTER is coded as RFUVKVPN, how is MEDICINE coded?", "Coding-Decoding", "TCS", "medium", "EOHJEJOF"),
    ("In a certain code, PLANT is written as $*&#@. How is TREE coded?", "Coding-Decoding", "Infosys", "medium", "#%%E"),
    ("If ROPE = 50, then HELP = ?", "Coding-Decoding", "TCS", "medium", "42"),
    ("If DELHI is coded as 73541 and CALCUTTA as 82589662, how is CALICUT coded?", "Coding-Decoding", "Wipro", "hard", "8251896"),
    ("If in a code language, FLOWER is written as GMPXFS, how is GARDEN written?", "Coding-Decoding", "TCS", "easy", "HBSEFO"),
    ("If A = 1, Z = 26, what does NAME sum to?", "Coding-Decoding", "Infosys", "easy", "42"),
    ("In a code, SLOW = 49, FAST = 36. What is RACE?", "Coding-Decoding", "TCS", "medium", "30"),
    ("If TEACHER is coded as UDBDBSF, how is STUDENT coded?", "Coding-Decoding", "Wipro", "medium", "TUEUFOU"),

    ("A says to B: 'I am the only son of your mother's father.' How is A related to B?", "Blood Relations", "TCS", "medium", "Maternal uncle"),
    ("Pointing to a man, a woman says 'His mother is the only daughter of my mother.' How is the woman related to the man?", "Blood Relations", "TCS", "easy", "Mother"),
    ("Rahul's mother is the only daughter of Priya. How is Priya related to Rahul?", "Blood Relations", "Infosys", "easy", "Grandmother"),
    ("A is B's sister. C is B's mother. D is C's father. How is A related to D?", "Blood Relations", "Wipro", "medium", "Granddaughter"),
    ("Pointing to a photograph, Ram said 'She is the daughter of my grandfather's only son.' Who is in the photograph?", "Blood Relations", "TCS", "easy", "Sister"),
    ("If X is the brother of Y, and Y is the sister of Z, and Z is the father of W, how is X related to W?", "Blood Relations", "Infosys", "medium", "Uncle"),
    ("A woman introduces a man as 'The son of the brother of my mother.' How is the man related to the woman?", "Blood Relations", "TCS", "easy", "Cousin"),
    ("P is the father of Q, but Q is not his son. R is the daughter of Q. S is the wife of Q. How is P related to S?", "Blood Relations", "Wipro", "medium", "Father-in-law"),
    ("If A is the brother of B, C is the sister of A, D is the brother of E, E is the daughter of B, how is C related to D?", "Blood Relations", "TCS", "medium", "Aunt"),
    ("F is the father of E. D is the daughter of F. G is the brother of D. H is the mother of G. How is H related to F?", "Blood Relations", "Infosys", "easy", "Wife"),

    ("In a row of 30 students, if Ram is 12th from the left, what is his position from the right?", "Seating Arrangement", "TCS", "easy", "19th"),
    ("6 people A, B, C, D, E, F sit in a row. A and B sit together. C sits to the right of D. E sits at one end. Who sits in the middle?", "Seating Arrangement", "Infosys", "hard", "Cannot be determined"),
    ("Five friends sit in a circle facing the center. A sits immediately to the left of B. C sits immediately to the right of D. E sits between A and D. Who sits opposite B?", "Seating Arrangement", "TCS", "medium", "E"),
    ("A, B, C, D, E sit in a row facing north. C is in the middle. A and E are at the ends. B is to the left of C. D is to the right of C. Who is at the rightmost end?", "Seating Arrangement", "Wipro", "easy", "E"),
    ("4 boys and 3 girls sit in a row. No two girls sit together. Number of ways to arrange:", "Seating Arrangement", "TCS", "medium", "144"),
    ("In a class of 60 students, A's rank is 15th from the top. B's rank is 40th from the bottom. How many students are between them?", "Seating Arrangement", "Infosys", "easy", "6"),
    ("5 persons P, Q, R, S, T sit around a circular table. P sits opposite Q. R sits to the left of Q. S sits opposite R. Where does T sit?", "Seating Arrangement", "TCS", "medium", "Between P and R"),
    ("If in a row, A is 10th from left and 25th from right, how many people are in the row?", "Seating Arrangement", "Wipro", "easy", "34"),

    ("5 houses in a row, each a different color. The Brit lives in the red house. The Swede keeps dogs. The Dane drinks tea. Who lives in the green house?", "Puzzles", "Infosys", "hard", "The German"),
    ("A, B, C, D, E are five people. A is taller than B but shorter than C. D is taller than E but shorter than B. Who is the shortest?", "Puzzles", "TCS", "easy", "E"),
    ("There are 5 boxes in a row. The red box is left of the blue box. The green box is right of the yellow box. The green box is left of the red box. The yellow box is leftmost. What is the order from left to right?", "Puzzles", "Wipro", "medium", "Yellow, Green, Red, Blue, White"),
    ("If all the 5's in the number 52,555 are followed by 3, then how many 3's are there?", "Puzzles", "TCS", "easy", "3"),
    ("In a family of 6, A is the father of B. C is the mother of D. D is the brother of E. E is the daughter of B. F is the son of D. How many males are there?", "Puzzles", "Infosys", "medium", "4"),
    ("If MONDAY = 1, TUESDAY = 2, ..., what does FRIDAY =?", "Puzzles", "TCS", "easy", "5"),
    ("A clock shows 3:15. What is the angle between the hour and minute hands?", "Puzzles", "Wipro", "medium", "0°"),
    ("There are 3 boxes. One contains apples, one contains oranges, and one contains both. All labels are wrong. You can pick one fruit from one box. How do you label all boxes?", "Puzzles", "TCS", "hard", "Pick from 'both' box → identifies all"),
    ("5 people finish a task in 10 days. After 5 days, 2 leave. How many more days needed?", "Puzzles", "TCS", "easy", "5 days"),
    ("If today is Monday, what day will it be after 100 days?", "Puzzles", "Infosys", "easy", "Wednesday"),

    ("Syllogism: All cats are dogs. All dogs are birds. Conclusion: All cats are birds.", "Syllogisms", "TCS", "easy", "True"),
    ("Statement: Some books are pens. All pens are chairs. Conclusion: Some books are chairs.", "Syllogisms", "TCS", "easy", "True"),
    ("Statement: All roses are flowers. Some flowers are thorns. Conclusion: Some roses are thorns.", "Syllogisms", "Infosys", "medium", "False"),
    ("Statement: No fish can fly. Some birds can fly. Conclusion: No fish is a bird.", "Syllogisms", "Wipro", "medium", "False"),
    ("Statement: All managers are leaders. All leaders are thinkers. Conclusion: Some thinkers are managers.", "Syllogisms", "TCS", "easy", "True"),
    ("Statement: Some doctors are engineers. Some engineers are lawyers. Conclusion: Some doctors are lawyers.", "Syllogisms", "TCS", "hard", "False"),
    ("Statement: All A are B. Some B are C. Conclusion: Some C are A.", "Syllogisms", "Infosys", "medium", "False"),
    ("Statement: No table is a chair. All chairs are desks. Conclusion: No table is a desk.", "Syllogisms", "Wipro", "hard", "False"),

    ("A is 5 years older than B. B is 3 years older than C. If A is 18, how old is C?", "Puzzles", "TCS", "easy", "10"),
    ("If you rearrange the letters 'CIFAIPC', you get the name of a/an:", "Puzzles", "TCS", "easy", "Ocean (PACIFIC)"),
    ("A man walks 5 km east, turns left and walks 3 km, turns left again and walks 5 km. How far is he from the start?", "Puzzles", "Wipro", "easy", "3 km"),
    ("If all roses are flowers and some flowers fade quickly, which is definitely true?", "Puzzles", "TCS", "medium", "Some roses may fade quickly"),
]

# ──────────────────────────────────────────────────────────────────────────────
# APTITUDE — VERBAL (50 questions)
# ──────────────────────────────────────────────────────────────────────────────

VERBAL = [
    ("Choose the synonym of 'Abundant':", "Synonyms", "TCS", "easy", "Plentiful"),
    ("Choose the antonym of 'Benevolent':", "Antonyms", "Wipro", "easy", "Malevolent"),
    ("Choose the synonym of 'Ephemeral':", "Synonyms", "Infosys", "medium", "Transient"),
    ("Choose the antonym of 'Pragmatic':", "Antonyms", "TCS", "medium", "Idealistic"),
    ("Choose the correct spelling:", "Spelling", "Wipro", "easy", "Accommodation"),
    ("Choose the synonym of 'Eloquent':", "Synonyms", "TCS", "easy", "Articulate"),
    ("Choose the antonym of 'Verbose':", "Antonyms", "Infosys", "easy", "Terse"),
    ("Identify the error: 'Each of the students have submitted their assignments.'", "Grammar", "TCS", "easy", "have → has"),
    ("Choose the correct form: 'Neither he nor I ___ going.'", "Grammar", "Wipro", "easy", "am"),
    ("Choose the synonym of 'Ubiquitous':", "Synonyms", "TCS", "medium", "Omnipresent"),
    ("Choose the antonym of 'Lethargic':", "Antonyms", "Infosys", "easy", "Energetic"),
    ("Fill in the blank: 'The committee ___ divided in its opinion.'", "Grammar", "TCS", "easy", "was"),
    ("Choose the correct preposition: 'He is allergic ___ dust.'", "Grammar", "Wipro", "easy", "to"),
    ("Choose the synonym of 'Mitigate':", "Synonyms", "TCS", "medium", "Alleviate"),
    ("Choose the antonym of 'Meticulous':", "Antonyms", "TCS", "easy", "Careless"),
    ("Choose the correct tense: 'By the time I arrived, they ___.'", "Grammar", "Infosys", "medium", "had left"),
    ("Choose the synonym of 'Resilient':", "Synonyms", "Wipro", "easy", "Durable"),
    ("Identify the error: 'The data suggests that the results are accurate.'", "Grammar", "TCS", "easy", "No error"),
    ("Choose the correct article: 'He is ___ honest man.'", "Grammar", "TCS", "easy", "an"),
    ("Choose the synonym of 'Candid':", "Synonyms", "Infosys", "easy", "Frank"),
    ("Choose the antonym of 'Futile':", "Antonyms", "Wipro", "easy", "Useful"),
    ("Choose the correct voice: 'The cake was baked by her.' (Active)", "Grammar", "TCS", "easy", "She baked the cake."),
    ("Choose the synonym of 'Prudent':", "Synonyms", "TCS", "medium", "Wise"),
    ("Fill in: 'If I ___ you, I would accept the offer.'", "Grammar", "Infosys", "easy", "were"),
    ("Choose the antonym of 'Candid':", "Antonyms", "Wipro", "easy", "Deceitful"),
    ("Which word is misspelled?", "Spelling", "TCS", "easy", "Occurence (should be Occurrence)"),
    ("Choose the synonym of 'Verbose':", "Synonyms", "TCS", "easy", "Wordy"),
    ("Choose the correct conjunction: 'I will go ___ you stay.'", "Grammar", "Wipro", "easy", "if"),
    ("Choose the antonym of 'Transparent':", "Antonyms", "Infosys", "medium", "Opaque"),
    ("Choose the synonym of 'Diligent':", "Synonyms", "TCS", "easy", "Hardworking"),
    ("Choose the correct form: 'He is one of those people who ___ always helpful.'", "Grammar", "TCS", "medium", "are"),
    ("Choose the antonym of 'Enormous':", "Antonyms", "Wipro", "easy", "Tiny"),
    ("Choose the synonym of 'Ambiguous':", "Synonyms", "TCS", "medium", "Vague"),
    ("Fill in: 'She has been working here ___ 2019.'", "Grammar", "Infosys", "easy", "since"),
    ("Choose the correct sentence:", "Grammar", "TCS", "easy", "None of the students was present."),
    ("Choose the synonym of 'Nostalgic':", "Synonyms", "Wipro", "medium", "Sentimental"),
    ("Choose the antonym of 'Frugal':", "Antonyms", "TCS", "medium", "Extravagant"),
    ("Choose the synonym of 'Tenacious':", "Synonyms", "TCS", "medium", "Persistent"),
    ("Choose the correct punctuation:", "Grammar", "Wipro", "easy", "He said, 'I will be there.'"),
    ("Choose the antonym of 'Auspicious':", "Antonyms", "Infosys", "medium", "Inauspicious"),
]

# ──────────────────────────────────────────────────────────────────────────────
# CODING (200 questions)
# ──────────────────────────────────────────────────────────────────────────────

CODING = [
    # Arrays — Easy
    ("Reverse an array without using built-in reverse functions.", "Arrays", "General", "easy", "https://www.geeksforgeeks.org/reverse-an-array-in-c/"),
    ("Find the largest element in an array.", "Arrays", "General", "easy", "https://www.geeksforgeeks.org/find-the-largest-element-in-an-array/"),
    ("Find the second largest element without sorting.", "Arrays", "TCS", "easy", "https://www.geeksforgeeks.org/find-second-largest-element-without-sorting/"),
    ("Move all zeros to end of array.", "Arrays", "Amazon", "easy", "https://www.geeksforgeeks.org/move-zeroes-end-array/"),
    ("Remove duplicates from sorted array.", "Arrays", "Microsoft", "easy", "https://www.geeksforgeeks.org/remove-duplicates-sorted-array/"),
    ("Check if array is sorted and rotated.", "Arrays", "Amazon", "medium", "https://www.geeksforgeeks.org/check-if-array-is-sorted-and-rotated/"),
    ("Find the element that appears once in a sorted array where all others appear twice.", "Arrays", "Amazon", "easy", "https://www.geeksforgeeks.org/find-element-appears-once-sorted-array/"),
    ("Left rotate an array by one position.", "Arrays", "General", "easy", "https://www.geeksforgeeks.org/rotate-array-by-1/"),
    ("Left rotate an array by d positions.", "Arrays", "Microsoft", "medium", "https://www.geeksforgeeks.org/array-rotation/"),
    ("Find the equilibrium point in an array.", "Arrays", "TCS", "medium", "https://www.geeksforgeeks.org/equilibrium-index-of-an-array/"),

    # Arrays — Medium
    ("Find two numbers that add up to a target (Two Sum).", "Arrays", "Google", "medium", "https://www.geeksforgeeks.org/two-sum/"),
    ("Find the maximum subarray sum (Kadane's Algorithm).", "Arrays", "Amazon", "medium", "https://www.geeksforgeeks.org/largest-sum-contiguous-subarray/"),
    ("Sort an array of 0s, 1s, and 2s (Dutch National Flag).", "Arrays", "Amazon", "medium", "https://www.geeksforgeeks.org/sort-an-array-of-0s-1s-and-2s/"),
    ("Find the majority element (appears more than n/2 times).", "Arrays", "Google", "medium", "https://www.geeksforgeeks.org/majority-element/"),
    ("Stock buy and sell — find max profit from one buy and one sell.", "Arrays", "Amazon", "medium", "https://www.geeksforgeeks.org/stock-buy-sell/"),
    ("Merge two sorted arrays.", "Arrays", "Microsoft", "medium", "https://www.geeksforgeeks.org/merge-two-sorted-arrays/"),
    ("Find the next permutation.", "Arrays", "Google", "medium", "https://www.geeksforgeeks.org/next-permutation/"),
    ("Find all pairs with a given sum.", "Arrays", "TCS", "medium", "https://www.geeksforgeeks.org/find-all-pairs-whose-sum-is-equal-to-x/"),
    ("Find the count of distinct elements in every window of size k.", "Arrays", "Amazon", "medium", "https://www.geeksforgeeks.org/count-distinct-elements-in-every-window-of-size-k/"),
    ("Trapping rain water problem.", "Arrays", "Google", "hard", "https://www.geeksforgeeks.org/trapping-rain-water/"),

    # Arrays — Hard
    ("Find the longest consecutive subsequence.", "Arrays", "Amazon", "hard", "https://www.geeksforgeeks.org/longest-consecutive-subsequence/"),
    ("Find the median of two sorted arrays.", "Arrays", "Google", "hard", "https://www.geeksforgeeks.org/median-of-two-sorted-arrays-of-different-sizes/"),
    ("Maximum product subarray.", "Arrays", "Microsoft", "hard", "https://www.geeksforgeeks.org/maximum-product-subarray/"),
    ("First missing positive integer.", "Arrays", "Amazon", "hard", "https://www.geeksforgeeks.org/find-the-first-missing-positive/"),

    # Strings — Easy
    ("Reverse a string without using built-in reverse.", "Strings", "General", "easy", "https://www.geeksforgeeks.org/reverse-a-string-in-c/"),
    ("Check if a string is a palindrome.", "Strings", "TCS", "easy", "https://www.geeksforgeeks.org/check-if-a-string-is-palindrome/"),
    ("Count vowels and consonants in a string.", "Strings", "TCS", "easy", "https://www.geeksforgeeks.org/count-vowels-consonants-string/"),
    ("Find the frequency of each character.", "Strings", "Infosys", "easy", "https://www.geeksforgeeks.org/frequency-of-each-character-in-a-string/"),
    ("Remove all duplicates from a string.", "Strings", "Wipro", "easy", "https://www.geeksforgeeks.org/remove-duplicates-from-a-string/"),
    ("Check if two strings are anagrams.", "Strings", "Amazon", "easy", "https://www.geeksforgeeks.org/check-if-two-strings-are-anagrams/"),
    ("Find the first non-repeating character.", "Strings", "Google", "medium", "https://www.geeksforgeeks.org/non-repeating-character/"),
    ("Convert uppercase to lowercase and vice versa.", "Strings", "TCS", "easy", "https://www.geeksforgeeks.org/convert-uppercase-lowercase-string/"),

    # Strings — Medium
    ("Longest substring without repeating characters.", "Strings", "Amazon", "medium", "https://www.geeksforgeeks.org/length-of-the-longest-substring/"),
    ("Print all permutations of a string.", "Strings", "Google", "medium", "https://www.geeksforgeeks.org/write-a-program-to-print-all-permutations-of-a-given-string/"),
    ("Find the longest palindromic substring.", "Strings", "Microsoft", "medium", "https://www.geeksforgeeks.org/longest-palindromic-substring/"),
    ("String to integer (atoi implementation).", "Strings", "Amazon", "medium", "https://www.geeksforgeeks.org/write-your-own-atoi/"),
    ("Implement strStr() — find first occurrence of a pattern.", "Strings", "Google", "medium", "https://www.geeksforgeeks.org/strstr-implement-strstr/"),
    ("Group anagrams together.", "Strings", "Amazon", "medium", "https://www.geeksforgeeks.org/group-anagrams-together/"),

    # Linked Lists — Easy
    ("Reverse a linked list (iterative and recursive).", "Linked Lists", "Amazon", "easy", "https://www.geeksforgeeks.org/reverse-a-linked-list/"),
    ("Find the middle of a linked list.", "Linked Lists", "TCS", "easy", "https://www.geeksforgeeks.org/write-a-c-function-to-print-the-middle-of-the-linked-list/"),
    ("Detect a loop in a linked list.", "Linked Lists", "Amazon", "medium", "https://www.geeksforgeeks.org/detect-loop-in-a-linked-list/"),
    ("Merge two sorted linked lists.", "Linked Lists", "Microsoft", "medium", "https://www.geeksforgeeks.org/sorted-merge-two-sorted-linked-lists/"),
    ("Remove Nth node from end of list.", "Linked Lists", "Google", "medium", "https://www.geeksforgeeks.org/remove-nth-node-from-end-of-linked-list/"),
    ("Find the intersection point of two linked lists.", "Linked Lists", "Amazon", "medium", "https://www.geeksforgeeks.org/write-a-function-to-get-the-intersection-point-of-two-linked-lists/"),

    # Stacks and Queues
    ("Implement a stack using arrays.", "Stacks", "General", "easy", "https://www.geeksforgeeks.org/stack-data-structure/"),
    ("Implement a queue using stacks.", "Queues", "Amazon", "medium", "https://www.geeksforgeeks.org/queue-using-stacks/"),
    ("Next greater element for each element.", "Stacks", "Amazon", "medium", "https://www.geeksforgeeks.org/next-greater-element/"),
    ("Valid parentheses (matching brackets).", "Stacks", "Google", "easy", "https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-an-expression/"),
    ("Implement Min Stack — get minimum in O(1).", "Stacks", "Microsoft", "medium", "https://www.geeksforgeeks.org/design-a-stack-that-supports-getmin-in-o1-time-and-o1-extra-space/"),
    ("Largest rectangle in histogram.", "Stacks", "Amazon", "hard", "https://www.geeksforgeeks.org/largest-rectangle-under-histogram/"),

    # Trees
    ("In-order traversal (recursive and iterative).", "Trees", "General", "easy", "https://www.geeksforgeeks.org/inorder-tree-traversal-without-recursion/"),
    ("Pre-order traversal of a binary tree.", "Trees", "General", "easy", "https://www.geeksforgeeks.org/iterative-preorder-traversal/"),
    ("Level-order traversal (BFS).", "Trees", "Amazon", "medium", "https://www.geeksforgeeks.org/level-order-traversal-in-spiral-form/"),
    ("Find the height of a binary tree.", "Trees", "TCS", "easy", "https://www.geeksforgeeks.org/height-of-a-binary-tree/"),
    ("Check if a binary tree is balanced.", "Trees", "Google", "medium", "https://www.geeksforgeeks.org/check-if-binary-tree-is-height-balanced-or-not/"),
    ("Lowest Common Ancestor of two nodes.", "Trees", "Google", "medium", "https://www.geeksforgeeks.org/lowest-common-ancestor-in-a-binary-tree/"),
    ("Serialize and deserialize a binary tree.", "Trees", "Amazon", "hard", "https://www.geeksforgeeks.org/serialize-deserialize-binary-tree/"),
    ("Check if a binary tree is a BST.", "Trees", "Microsoft", "medium", "https://www.geeksforgeeks.org/a-program-to-check-if-a-binary-tree-is-bst-or-not/"),
    ("Flatten a binary tree to a linked list.", "Trees", "Amazon", "hard", "https://www.geeksforgeeks.org/flatten-a-binary-tree-into-linked-list/"),
    ("Maximum path sum in a binary tree.", "Trees", "Google", "hard", "https://www.geeksforgeeks.org/find-maximum-path-sum-in-a-binary-tree/"),

    # Graphs
    ("BFS of a graph.", "Graphs", "General", "easy", "https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/"),
    ("DFS of a graph.", "Graphs", "General", "easy", "https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/"),
    ("Detect a cycle in an undirected graph.", "Graphs", "Amazon", "medium", "https://www.geeksforgeeks.org/detect-cycle-undirected-graph/"),
    ("Detect a cycle in a directed graph.", "Graphs", "Microsoft", "medium", "https://www.geeksforgeeks.org/detect-cycle-in-a-graph/"),
    ("Topological sort (Kahn's algorithm).", "Graphs", "Google", "medium", "https://www.geeksforgeeks.org/topological-sorting/"),
    ("Find the number of islands.", "Graphs", "Amazon", "medium", "https://www.geeksforgeeks.org/find-number-of-islands/"),
    ("Shortest path in a weighted graph (Dijkstra's).", "Graphs", "Google", "hard", "https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/"),
    ("Clone a graph.", "Graphs", "Amazon", "hard", "https://www.geeksforgeeks.org/clone-an-undirected-graph/"),

    # Dynamic Programming
    ("Fibonacci number (recursive, memoized, tabulated).", "DP", "General", "easy", "https://www.geeksforgeeks.org/program-for-nth-fibonacci-number/"),
    ("Climbing stairs (1 or 2 steps at a time).", "DP", "Amazon", "easy", "https://www.geeksforgeeks.org/count-ways-to-reach-the-nth-stair/"),
    ("0/1 Knapsack problem.", "DP", "Amazon", "medium", "https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/"),
    ("Longest Common Subsequence.", "DP", "Google", "medium", "https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/"),
    ("Longest Increasing Subsequence.", "DP", "Amazon", "medium", "https://www.geeksforgeeks.org/longest-increasing-subsequence-dp-3/"),
    ("Coin change — minimum coins to make an amount.", "DP", "Uber", "medium", "https://www.geeksforgeeks.org/minimum-number-of-coins/"),
    ("Edit distance between two strings.", "DP", "Google", "hard", "https://www.geeksforgeeks.org/edit-distance-dp-5/"),
    ("Maximum sum of non-adjacent elements.", "DP", "Amazon", "medium", "https://www.geeksforgeeks.org/maximum-sum-such-that-no-two-elements-are-adjacent/"),
    ("Grid unique paths (top-left to bottom-right).", "DP", "Google", "medium", "https://www.geeksforgeeks.org/unique-paths-in-a-grid/"),
    ("Rod cutting problem.", "DP", "Microsoft", "medium", "https://www.geeksforgeeks.org/cutting-a-rod-dp-13/"),
    ("Subset sum problem.", "DP", "Amazon", "medium", "https://www.geeksforgeeks.org/subset-sum-problem-dp-25/"),
    ("Longest palindromic subsequence.", "DP", "Google", "hard", "https://www.geeksforgeeks.org/longest-palindromic-subsequence-dp-12/"),

    # Greedy
    ("Activity selection problem.", "Greedy", "General", "medium", "https://www.geeksforgeeks.org/activity-selection-problem-greedy-algo-1/"),
    ("Fractional knapsack.", "Greedy", "Amazon", "medium", "https://www.geeksforgeeks.org/fractional-knapsack-problem/"),
    ("Job sequencing problem.", "Greedy", "Google", "medium", "https://www.geeksforgeeks.org/job-sequencing-problem/"),
    ("Huffman coding.", "Greedy", "Microsoft", "hard", "https://www.geeksforgeeks.org/huffman-coding-greedy-algo-3/"),

    # Hashing
    ("Two Sum — find indices of two numbers that add up to target.", "Hashing", "Google", "easy", "https://www.geeksforgeeks.org/two-sum/"),
    ("Find all duplicate elements in an array.", "Hashing", "TCS", "easy", "https://www.geeksforgeeks.org/find-duplicates-in-on-time-and-constant-extra-space/"),
    ("Check if two arrays are equal (using hashing).", "Hashing", "Amazon", "easy", "https://www.geeksforgeeks.org/check-if-two-arrays-are-equal-or-not/"),
    ("Longest subarray with sum 0.", "Hashing", "Amazon", "medium", "https://www.geeksforgeeks.org/find-the-largest-subarray-with-0-sum/"),
    ("Count distinct elements in every window of size k.", "Hashing", "Microsoft", "medium", "https://www.geeksforgeeks.org/count-distinct-elements-in-every-window-of-size-k/"),

    # Bit Manipulation
    ("Find the two non-repeating elements where all others appear twice.", "Bit Manipulation", "Microsoft", "hard", "https://www.geeksforgeeks.org/non-repeating-elements/"),
    ("Count the number of set bits in an integer.", "Bit Manipulation", "TCS", "easy", "https://www.geeksforgeeks.org/count-set-bits-in-an-integer/"),
    ("Check if a number is a power of 2.", "Bit Manipulation", "Amazon", "easy", "https://www.geeksforgeeks.org/write-a-c-program-to-find-whether-a-given-number-is-a-power-of-2/"),
    ("Find the single number in an array where every element appears twice.", "Bit Manipulation", "Amazon", "easy", "https://www.geeksforgeeks.org/find-element-appears-once/"),
    ("Reverse the bits of a 32-bit unsigned integer.", "Bit Manipulation", "Amazon", "medium", "https://www.geeksforgeeks.org/reverse-bits-of-a-given-integer/"),

    # Heaps
    ("Find the kth largest element using a min-heap.", "Heaps", "Meta", "medium", "https://www.geeksforgeeks.org/kth-largest-element/"),
    ("Merge k sorted arrays using a min-heap.", "Heaps", "Amazon", "hard", "https://www.geeksforgeeks.org/merge-k-sorted-arrays/"),
    ("Find the median of a stream of integers.", "Heaps", "Amazon", "hard", "https://www.geeksforgeeks.org/median-of-stream-of-integers-running-integers/"),
    ("Top K frequent elements.", "Heaps", "Amazon", "medium", "https://www.geeksforgeeks.org/find-k-frequent-elements-array/"),

    # Tries
    ("Implement a trie (prefix tree).", "Tries", "Google", "medium", "https://www.geeksforgeeks.org/trie-insert-and-search/"),
    ("Implement autocomplete using a trie.", "Tries", "Uber", "hard", "https://www.geeksforgeeks.org/auto-complete-feature-using-trie/"),
    ("Word search II (find all words in a 2D grid).", "Tries", "Amazon", "hard", "https://www.geeksforgeeks.org/boggle-find-possible-words-board-characters/"),

    # Company-specific FAANG coding
    ("LRU Cache implementation.", "Design", "Amazon", "hard", "https://www.geeksforgeeks.org/lru-cache-implementation/"),
    ("Implement an LFU Cache.", "Design", "Amazon", "hard", "https://www.geeksforgeeks.org/lfu-cache-implementation/"),
    ("Design a Twitter-like system — post, follow, get news feed.", "Design", "Amazon", "hard", "https://www.geeksforgeeks.org/design-a-twitter-like-system/"),
    ("Alien dictionary (topological sort).", "Graphs", "Google", "hard", "https://www.geeksforgeeks.org/given-sorted-dictionary-find-precedence-characters/"),
    ("Word Ladder (BFS shortest path).", "Graphs", "Google", "hard", "https://www.geeksforgeeks.org/word-ladder-length-of-shortest-chain-to-reach-a-target-word/"),
    ("Merge Intervals.", "Arrays", "Google", "medium", "https://www.geeksforgeeks.org/merging-intervals/"),
    ("Meeting Rooms II (minimum conference rooms).", "Heaps", "Google", "hard", "https://www.geeksforgeeks.org/find-minimum-meeting-rooms-required/"),
    ("Decode ways (number of ways to decode a message).", "DP", "Amazon", "medium", "https://www.geeksforgeeks.org/decode-ways/"),
    ("Implement a thread-safe singleton.", "Design", "Amazon", "medium", "https://www.geeksforgeeks.org/singleton-design-pattern/"),
    ("Design a rate limiter.", "Design", "Google", "hard", "https://www.geeksforgeeks.org/design-a-rate-limiter/"),
    ("Implement a circular buffer/ring buffer.", "Design", "Uber", "medium", "https://www.geeksforgeeks.org/circular-buffer-or-ring-uses/"),
    ("Median of two sorted arrays (binary search approach).", "Arrays", "Google", "hard", "https://www.geeksforgeeks.org/median-of-two-sorted-arrays-of-different-sizes/"),
    ("Serialize and deserialize a BST.", "Trees", "Amazon", "hard", "https://www.geeksforgeeks.org/serialize-deserialize-binary-search-tree/"),
    ("Word Break problem (DP).", "DP", "Amazon", "medium", "https://www.geeksforgeeks.org/word-break-problem-dp-32/"),
    ("Find the smallest window containing all characters of another string.", "Strings", "Amazon", "hard", "https://www.geeksforgeeks.org/find-the-smallest-window-in-a-string-containing-all-the-characters-of-another-string/"),
    ("Flood fill algorithm.", "Graphs", "Amazon", "medium", "https://www.geeksforgeeks.org/flood-fill-algorithm/"),
    ("Implement strStr() using KMP algorithm.", "Strings", "Google", "medium", "https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/"),
    ("Maximum path sum from any node to any node in a binary tree.", "Trees", "Amazon", "hard", "https://www.geeksforgeeks.org/find-maximum-path-sum-in-a-binary-tree/"),
    ("Minimum edit distance to convert one string to another.", "DP", "Microsoft", "hard", "https://www.geeksforgeeks.org/edit-distance-dp-5/"),
    ("Implement a producer-consumer problem using semaphores.", "Design", "Amazon", "medium", "https://www.geeksforgeeks.org/producer-consumer-solution-using-threads/"),
    ("Find all anagrams in a string (sliding window).", "Strings", "Amazon", "medium", "https://www.geeksforgeeks.org/find-all-anagrams-in-a-given-string/"),
    ("Design a chat system with message delivery guarantees.", "Design", "Meta", "hard", "https://www.geeksforgeeks.org/system-design-chat-messaging-system/"),
    ("Implement an LRU Cache using doubly linked list + hashmap.", "Design", "Google", "hard", "https://www.geeksforgeeks.org/lru-cache-implementation/"),
    ("N-Queens problem (backtracking).", "Graphs", "Google", "hard", "https://www.geeksforgeeks.org/n-queen-problem-backtracking-3/"),
]

# ──────────────────────────────────────────────────────────────────────────────
# BEHAVIORAL (100 questions — company-specific)
# ──────────────────────────────────────────────────────────────────────────────

BEHAVIORAL = [
    # Amazon Leadership Principles
    ("Tell me about a time you went above and beyond for a customer.", "Customer Obsession", "Amazon", "medium", "STAR framework — focus on customer impact"),
    ("Describe a situation where you had to make a decision with incomplete data.", "Bias for Action", "Amazon", "medium", "Show calculated risk-taking"),
    ("Tell me about a time you took ownership of something outside your role.", "Ownership", "Amazon", "medium", "Show initiative and accountability"),
    ("Describe a time you disagreed with your manager's approach. How did you handle it?", "Have Backbone", "Amazon", "hard", "Respectful disagreement with data"),
    ("Tell me about a time you simplified a complex process.", "Invent and Simplify", "Amazon", "medium", "Show creative problem-solving"),
    ("Describe a time you had to deliver results under a tight deadline.", "Deliver Results", "Amazon", "medium", "Show prioritization and execution"),
    ("Tell me about a time you mentored someone.", "Develop the Best", "Amazon", "medium", "Show investment in others' growth"),
    ("Describe a time you had to earn trust from a skeptical team.", "Earn Trust", "Amazon", "hard", "Show humility and consistency"),
    ("Tell me about a time you dove deep into data to solve a problem.", "Dive Deep", "Amazon", "medium", "Show analytical thinking"),
    ("Describe a time when success was not possible but you still gave your best.", "Strive to be Earth's Best", "Amazon", "medium", "Show high standards"),

    # Google
    ("Tell me about a time you had to convince others to adopt your idea.", "Leadership", "Google", "medium", "Show influence without authority"),
    ("Describe a situation where you failed. What did you learn?", "Learning from Failure", "Google", "hard", "Genuine reflection and growth"),
    ("Tell me about a time you had to balance multiple priorities.", "Prioritization", "Google", "medium", "Show structured decision-making"),
    ("Describe how you handled a project with unclear requirements.", "Ambiguity", "Google", "medium", "Show structured approach to chaos"),
    ("Tell me about a time you improved a process significantly.", "Process Improvement", "Google", "medium", "Quantify the improvement"),
    ("Describe a time you had to work with a difficult stakeholder.", "Collaboration", "Google", "hard", "Show empathy and persistence"),
    ("Tell me about a time you made a data-driven decision.", "Data-Driven", "Google", "medium", "Show analytical rigor"),
    ("Describe a time you challenged the status quo.", "Challenge", "Google", "medium", "Show constructive disruption"),

    # Microsoft
    ("Tell me about a time you received critical feedback. How did you respond?", "Growth Mindset", "Microsoft", "medium", "Show openness and action"),
    ("Describe a time you had to collaborate across teams.", "Collaboration", "Microsoft", "medium", "Show cross-team influence"),
    ("Tell me about a time you helped a struggling team member.", "Empathy", "Microsoft", "medium", "Show genuine support"),
    ("Describe a situation where you had to make a tough trade-off.", "Decision Making", "Microsoft", "hard", "Show structured reasoning"),
    ("Tell me about a time you failed to meet a commitment.", "Accountability", "Microsoft", "hard", "Own the failure, show recovery"),
    ("Describe how you handle ambiguity in a project.", "Ambiguity", "Microsoft", "medium", "Show structured thinking"),
    ("Tell me about a time you delivered something innovative.", "Innovation", "Microsoft", "medium", "Show creativity and impact"),

    # Meta
    ("Tell me about a time you moved fast and broke something. What happened?", "Move Fast", "Meta", "medium", "Show speed + accountability"),
    ("Describe a time you had to make a decision that wasn't popular.", "Boldness", "Meta", "hard", "Show conviction with data"),
    ("Tell me about a time you focused on impact over perfection.", "Impact", "Meta", "medium", "Show results-oriented mindset"),
    ("Describe a time you had to pivot quickly due to changing requirements.", "Adaptability", "Meta", "medium", "Show flexibility"),
    ("Tell me about a time you built something from scratch.", "Building", "Meta", "medium", "Show end-to-end ownership"),
    ("Describe a time you challenged a decision with a better solution.", "Challenge", "Meta", "hard", "Show constructive challenge"),

    # Uber
    ("Tell me about a time you had to make a decision that affected many people.", "Impact at Scale", "Uber", "medium", "Show consideration of stakeholders"),
    ("Describe a time you had to work under extreme pressure.", "Pressure", "Uber", "medium", "Show composure and results"),
    ("Tell me about a time you had to fight for your idea.", "Advocacy", "Uber", "medium", "Show passion and persuasion"),
    ("Describe a time when you had to pivot your approach mid-project.", "Adaptability", "Uber", "hard", "Show quick thinking"),

    # General Behavioral (STAR method)
    ("Tell me about yourself.", "General", "General", "easy", "Present → Past → Future structure"),
    ("Why should we hire you?", "General", "General", "easy", "Match your skills to their needs"),
    ("What is your greatest weakness?", "General", "General", "medium", "Be genuine, show growth"),
    ("Describe a time you worked in a team to achieve a goal.", "Teamwork", "General", "medium", "Your specific contribution + result"),
    ("Tell me about a time you had to learn something quickly.", "Learning Agility", "General", "medium", "Show adaptability"),
    ("Describe a situation where you had to manage conflict.", "Conflict Resolution", "General", "hard", "Professional approach + resolution"),
    ("Tell me about a time you exceeded expectations.", "Excellence", "General", "medium", "Quantify the result"),
    ("How do you handle stress and pressure?", "Stress Management", "General", "easy", "Specific strategy + example"),
    ("Tell me about a time you had to give difficult feedback.", "Communication", "General", "hard", "Empathy + directness"),
    ("Describe your approach to learning new technologies.", "Growth Mindset", "General", "medium", "Show structured learning"),
    ("Tell me about a project you're most proud of.", "Passion", "General", "medium", "Technical depth + impact"),
    ("How do you prioritize tasks when everything seems urgent?", "Prioritization", "General", "medium", "Framework + example"),
    ("Tell me about a time you had to say no to a stakeholder.", "Assertiveness", "General", "hard", "Professional + firm"),
    ("Describe a time you improved efficiency in your team.", "Efficiency", "General", "medium", "Quantify the improvement"),
    ("What sets you apart from other candidates?", "Differentiation", "General", "easy", "Unique combination + proof"),
    ("Tell me about a time you made a mistake at work.", "Humility", "General", "hard", "Own it, fix it, learn from it"),
    ("Describe your ideal work environment.", "Culture Fit", "General", "easy", "Align with company values"),
    ("Tell me about a time you had to influence without authority.", "Influence", "General", "hard", "Show persuasion skills"),
    ("How do you handle receiving ambiguous instructions?", "Ambiguity", "General", "medium", "Ask questions + take initiative"),
    ("Tell me about a time you managed competing deadlines.", "Time Management", "General", "medium", "Prioritization framework"),
]

# ──────────────────────────────────────────────────────────────────────────────
# SYSTEM DESIGN — HLD (10 questions — architecture-level thinking)
# ──────────────────────────────────────────────────────────────────────────────

HLD_DESIGN = [
    ("Design a URL shortener like bit.ly. Discuss scaling, storage, analytics.", "HLD", "Google", "hard", "Consistent hashing, read-heavy optimization"),
    ("Design an e-commerce platform (Amazon). Cover catalog, cart, checkout, payments.", "HLD", "Amazon", "hard", "Microservices, eventual consistency"),
    ("Design a chat application like WhatsApp. Cover messaging, groups, E2E encryption.", "HLD", "Meta", "hard", "WebSockets, message queue"),
    ("Design a social media feed (Facebook News Feed). Ranking, caching, real-time.", "HLD", "Meta", "hard", "Fan-out on read/write"),
    ("Design a ride-sharing system (Uber). Matching, geospatial indexing, surge pricing.", "HLD", "Uber", "hard", "Quad-tree, real-time matching"),
    ("Design a video streaming platform (YouTube). Upload, encoding, CDN, recommendations.", "HLD", "Google", "hard", "Async processing, CDN"),
    ("Design a notification system. Push, email, SMS. Priority, dedup, scaling.", "HLD", "Amazon", "medium", "Event-driven, priority queues"),
    ("Design a content delivery network (CDN). Caching, invalidation, geo-routing.", "HLD", "Amazon", "hard", "Edge caching, DNS routing"),
    ("Design a distributed file storage system (Google Drive).", "HLD", "Google", "hard", "Chunking, replication"),
    ("Design a ride fare estimator. Dynamic pricing, factors, ML.", "HLD", "Uber", "hard", "Surge pricing algorithms"),
]

# ──────────────────────────────────────────────────────────────────────────────
# SYSTEM DESIGN — LLD (55 questions — class diagrams, data models, design patterns)
# ──────────────────────────────────────────────────────────────────────────────

LLD_DESIGN = [
    ("Design a rate limiter. Support multiple algorithms (token bucket, sliding window).", "LLD", "Google", "hard", "Token bucket, sliding window"),
    ("Design a distributed cache (Redis). Eviction, consistency, replication.", "LLD", "Amazon", "hard", "LRU, consistent hashing"),
    ("Design a search autocomplete system. Trie-based, personalized.", "LLD", "Google", "hard", "Trie, ranking algorithms"),
    ("Design a real-time collaborative document editor (Google Docs).", "LLD", "Google", "hard", "OT or CRDT, conflict resolution"),
    ("Design a URL crawler (web crawler). Politeness, dedup, distributed.", "LLD", "Amazon", "hard", "BFS/DFS, robots.txt"),
    ("Design a ticket booking system (BookMyShow). Concurrency, seat locking.", "LLD", "Amazon", "medium", "Optimistic locking"),
    ("Design a hotel booking system (Booking.com). Search, availability, pricing.", "LLD", "Amazon", "medium", "Inventory management"),
    ("Design a food delivery system (DoorDash). Real-time tracking, routing.", "LLD", "Uber", "hard", "Geospatial, real-time updates"),
    ("Design a news aggregation system (Google News). Crawling, ranking, personalization.", "LLD", "Google", "medium", "ML ranking, personalization"),
    ("Design a metrics collection system (Datadog). Ingestion, storage, querying.", "LLD", "Amazon", "hard", "Time-series DB, downsampling"),
    ("Design an API gateway. Rate limiting, auth, routing, load balancing.", "LLD", "Amazon", "medium", "Kong, Envoy patterns"),
    ("Design a payment system. Idempotency, reconciliation, fault tolerance.", "LLD", "Amazon", "hard", "Exactly-once semantics"),
    ("Design a task scheduler (cron in distributed system).", "LLD", "Amazon", "medium", "Leader election, persistence"),
    ("Design a photo sharing app (Instagram). Upload, feed, stories.", "LLD", "Meta", "medium", "CDN, fan-out, denormalization"),
    ("Design a restaurant reservation system. Availability, double-booking prevention.", "LLD", "Google", "medium", "Optimistic locking"),
    ("Design a logistics/delivery tracking system. Real-time, route optimization.", "LLD", "Uber", "hard", "Event sourcing, CQRS"),
    ("Design a distributed key-value store (DynamoDB).", "LLD", "Amazon", "hard", "Consistent hashing, replication"),
    ("Design a music streaming service (Spotify). Playlists, recommendations, offline.", "LLD", "Meta", "medium", "CDN, ML recommendations"),
    ("Design a game matchmaking system. ELO rating, latency-based matching.", "LLD", "Amazon", "hard", "Priority queues, ELO algorithm"),
    ("Design a real-time analytics dashboard. Streaming data, aggregation.", "LLD", "Google", "medium", "Stream processing, windowing"),
    ("Design a distributed email system. Delivery, storage, search, spam filtering.", "LLD", "Google", "hard", "MX records, ML spam filter"),
    ("Design a payroll system. Calculations, compliance, audit trail.", "LLD", "Amazon", "medium", "Idempotent operations, audit"),
    ("Design a voting system. Anonymous, verifiable, scalable.", "LLD", "Google", "hard", "Blockchain, zero-knowledge proofs"),
    ("Design an airline reservation system. Seat selection, overbooking, pricing.", "LLD", "Amazon", "medium", "Inventory management, dynamic pricing"),
    ("Design a stock trading platform. Order matching, real-time prices, regulatory.", "LLD", "Amazon", "hard", "LMAX, event sourcing"),
    ("Design a healthcare appointment system. HIPAA, scheduling, notifications.", "LLD", "Google", "medium", "HIPAA compliance, encryption"),
    ("Design a content moderation system. Automated + human review pipeline.", "LLD", "Meta", "medium", "ML classifiers, queue"),
    ("Design a push notification service for 1 billion devices.", "LLD", "Amazon", "hard", "Device registry, APNS/FCM"),
    ("Design a distributed message queue (Kafka). Ordering, durability, partitions.", "LLD", "Amazon", "hard", "Log-based, consumer groups"),
    ("Design a personalized ad system. Targeting, auction, tracking.", "LLD", "Meta", "hard", "Real-time bidding, ML"),
    ("Design a map navigation system (Google Maps). Routing, ETA, traffic.", "LLD", "Google", "hard", "Graph algorithms, real-time data"),
    ("Design a multi-tenant SaaS platform. Isolation, scaling, billing.", "LLD", "Amazon", "medium", "Shared DB, tenant isolation"),
    ("Design a code editor in the browser (VS Code Online).", "LLD", "Amazon", "hard", "WebSockets, file sync"),
    ("Design a job recommendation system. Matching, ranking, notifications.", "LLD", "Amazon", "medium", "ML ranking, collaborative filtering"),
    ("Design a photo recognition system (Google Photos). Dedup, search, albums.", "LLD", "Google", "hard", "CNN embeddings, similarity"),
    ("Design a cloud storage system (S3). Durability, consistency, versioning.", "LLD", "Amazon", "hard", "Erasure coding, replication"),
    ("Design an IoT data pipeline. Device ingestion, storage, alerts.", "LLD", "Amazon", "medium", "MQTT, time-series DB"),
    ("Design a customer support ticketing system (Zendesk). Routing, SLA, analytics.", "LLD", "Amazon", "medium", "Priority queues, SLA tracking"),
    ("Design a live auction system. Bidding, anti-sniping, concurrent users.", "LLD", "Amazon", "hard", "WebSockets, idempotent bids"),
    ("Design a file versioning system like Git. Diffs, merges, branching.", "LLD", "Amazon", "hard", "Content-addressable storage"),
    ("Design a parking lot system. Entry/exit, payment, slot management.", "LLD", "Amazon", "medium", "State pattern, strategy pattern"),
    ("Design an elevator system. Scheduling algorithm, priority, multiple elevators.", "LLD", "Amazon", "medium", "SCAN algorithm, priority queue"),
    ("Design a vending machine. Inventory, payment, state machine.", "LLD", "Amazon", "medium", "State pattern"),
    ("Design a chess game. Rules, moves, check/checkmate detection.", "LLD", "Amazon", "medium", "Game logic, board representation"),
    ("Design a tic-tac-toe game. AI opponent, win detection.", "LLD", "Amazon", "easy", "Minimax algorithm"),
    ("Design a library management system. Book reservation, fine calculation.", "LLD", "TCS", "medium", "State pattern, observer pattern"),
    ("Design a hotel management system. Room booking, billing, staff.", "LLD", "TCS", "medium", "Facade pattern, strategy pattern"),
    ("Design a traffic light system. State transitions, pedestrian mode.", "LLD", "Google", "medium", "State machine"),
    ("Design a movie ticket booking system. Seat selection, pricing, offers.", "LLD", "Amazon", "medium", "Strategy pattern for pricing"),
    ("Design a food ordering system (Swiggy). Restaurant discovery, order tracking.", "LLD", "Amazon", "medium", "Microservices, event-driven"),
    ("Design a ride hailing system. Driver matching, ETA, fare calculation.", "LLD", "Uber", "hard", "Geospatial indexing, matching"),
    ("Design a ride sharing system. Pool matching, route optimization.", "LLD", "Uber", "hard", "Graph algorithms, clustering"),
    ("Design a food delivery tracking system. Real-time GPS, ETA prediction.", "LLD", "Uber", "medium", "WebSocket, geospatial"),
    ("Design a freight marketplace. Shipper-carrier matching, bidding.", "LLD", "Amazon", "medium", "Marketplace pattern"),
    ("Design a fleet management system. Vehicle tracking, maintenance, dispatch.", "LLD", "Amazon", "medium", "IoT, event-driven"),
]

# ──────────────────────────────────────────────────────────────────────────────
# BUILD THE MASTER LIST
# ──────────────────────────────────────────────────────────────────────────────

def build_question(q_text, topic, company, difficulty, q_type, answer=None, link=None, tags=None, design_type=None):
    doc = {
        "topic": topic,
        "company": company,
        "difficulty": difficulty,
        "type": q_type,
        "question_title": q_text,
        "question_link": link or f"https://www.geeksforgeeks.org/{topic.lower().replace(' ', '-')}/",
        "source": f"{company} Interview" if company != "General" else "Common Interview",
        "tags": tags or [],
        "answer": answer,
    }
    if design_type:
        doc["design_type"] = design_type
    return doc


def build_all_questions():
    questions = []

    for q_text, topic, company, diff, answer in QUANT:
        questions.append(build_question(q_text, topic, company, diff, "aptitude", answer, tags=["quantitative"]))

    for q_text, topic, company, diff, answer in LOGICAL:
        questions.append(build_question(q_text, topic, company, diff, "aptitude", answer, tags=["logical"]))

    for q_text, topic, company, diff, answer in VERBAL:
        questions.append(build_question(q_text, topic, company, diff, "aptitude", answer, tags=["verbal"]))

    for q_text, topic, company, diff, link in CODING:
        questions.append(build_question(q_text, topic, company, diff, "coding", link=link, tags=[topic.lower().replace(" ", "-")]))

    for q_text, topic, company, diff, note in BEHAVIORAL:
        questions.append(build_question(q_text, topic, company, diff, "behavioral", answer=note, tags=[topic.lower().replace(" ", "-")]))

    for q_text, topic, company, diff, note in HLD_DESIGN:
        questions.append(build_question(q_text, topic, company, diff, "system_design", answer=note, tags=["system-design", "hld"], design_type="hld"))

    for q_text, topic, company, diff, note in LLD_DESIGN:
        questions.append(build_question(q_text, topic, company, diff, "system_design", answer=note, tags=["system-design", "lld"], design_type="lld"))

    return questions


async def seed():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    collection = db["curated_questions"]

    await collection.drop()

    await collection.create_index("company")
    await collection.create_index("topic")
    await collection.create_index("difficulty")
    await collection.create_index("type")
    await collection.create_index("design_type")
    await collection.create_index([("company", 1), ("topic", 1)])
    await collection.create_index([("company", 1), ("type", 1)])
    await collection.create_index([("topic", 1), ("difficulty", 1)])
    await collection.create_index([("question_title", "text"), ("topic", "text")])

    questions = build_all_questions()
    for q in questions:
        q["created_at"] = datetime.now(timezone.utc)
        q["practice_count"] = 0
        q["upvotes"] = 0

    result = await collection.insert_many(questions)
    print(f"Seeded {len(result.inserted_ids)} curated questions")

    # Print breakdown
    from collections import Counter
    type_counts = Counter(q["type"] for q in questions)
    company_counts = Counter(q["company"] for q in questions)
    diff_counts = Counter(q["difficulty"] for q in questions)

    print(f"\nBy type: {dict(type_counts)}")
    print(f"By difficulty: {dict(diff_counts)}")
    print(f"Top companies: {company_counts.most_common(10)}")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
