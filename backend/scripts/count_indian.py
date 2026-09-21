import re
with open('D:\\Project-Fremen\\backend\\app\\data\\indian_companies.py', 'r', encoding='utf-8') as f:
    content = f.read()
companies = re.findall(r'"([a-z_]+)":\s*\{', content)
print(f"Total company sections: {len(companies)}")
print(f"Companies: {companies}")
print(f"hr_questions fields: {content.count('hr_questions')}")
print(f"coding_patterns fields: {content.count('coding_patterns')}")
