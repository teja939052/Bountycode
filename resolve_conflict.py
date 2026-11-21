import sys

with open('backend/app/services/content_loader.py', 'r') as f:
    content = f.read()

old_block = '''<<<<<<< HEAD
            "trust_status": item.get("trust_status") or data.get("trust_status") or "human_reviewed",
            "provenance": item.get("provenance") or data.get("provenance"),
            "source": item.get("source") or data.get("source") or "bountycode_original",
            "type": item.get("type") or "mcq",
=======
            "trust_status": trust_status,
            "source": item.get("source") or data.get("source") or "unspecified",
            "provenance": item.get("provenance") or data.get("provenance"),
            "review_evidence": _evidence(data, item, "review_evidence"),
            "verification_evidence": _evidence(data, item, "verification_evidence"),
            "type": "mcq",
>>>>>>> 2513abbf5afd49040fd2f2c6b74d8f92c90e1901'''

new_block = '''            "trust_status": item.get("trust_status") or data.get("trust_status") or "human_reviewed",
            "provenance": item.get("provenance") or data.get("provenance"),
            "source": item.get("source") or data.get("source") or "bountycode_original",
            "type": item.get("type") or "mcq",
'''

if old_block in content:
    content = content.replace(old_block, new_block, 1)
    with open('backend/app/services/content_loader.py', 'w') as f:
        f.write(content)
    print('SUCCESS: content_loader.py resolved')
else:
    print('FAILED: Could not find exact old_block')
    print('Looking for:')
    print(repr(old_block[:200]))