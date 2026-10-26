c = open('D:\\Project-Fremen\\backend\\seed_questions_mega.py', encoding='utf-8').read()
opens = c.count('[')
closes = c.count(']')
print(f'Open brackets: [{opens}], Close brackets: [{closes}], Net: [{opens - closes}]')

# Find position of last ] and last [
last_open = c.rfind('[')
last_close = c.rfind(']')
print(f'Last [ at position: {last_open}')
print(f'Last ] at position: {last_close}')
print(f'Last 300 chars: ...{c[-300:]}')
