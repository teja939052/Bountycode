import sys
sys.path.insert(0, '.')
import scripts.generate_service_company_questions as mod

with open('scripts/generate_service_company_questions.py', 'r') as f:
    source = f.read()

start = source.find('    generators = {')
end = source.find('    }', start) + 4
dict_code = source[start:end]

namespace = {}
exec(dict_code, namespace, mod.__dict__)
gens = namespace['generators']

print('Total generators in dict:', len(gens))
keys = list(gens.keys())
for i in range(25, 35):
    if i < len(keys):
        name = keys[i]
        fn = gens[name]
        r = fn()
        print(name, type(r).__name__, len(r) if r else None)