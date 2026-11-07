import io

with io.open('app/data/worlds_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('_level("b-1"')
print(f'b-1 found at index: {idx}')

if idx != -1:
    end_idx = content.find('            _level("b-2"', idx)
    print(f'b-1 ends at index: {end_idx}')
    
    with io.open('b1_context.txt', 'w', encoding='utf-8') as f:
        f.write(content[idx:end_idx])
    print('Context written to b1_context.txt')
