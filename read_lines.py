with open('D:\\Project-Fremen\\backend\\app\\services\\question_store.py', 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines[564:618], start=565):
        print(f'{i}:{repr(line)}')