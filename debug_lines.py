with open('D:\\Project-Fremen\\backend\\app\\services\\question_store.py', 'r') as f:
    content = f.read()
# Print the exact bytes around line 583
idx = content.find('def _audit_trust_integrity')
print(repr(content[idx:idx+1200]))