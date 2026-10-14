import json, re, pathlib

packs_dir = pathlib.Path('backend/app/content/mission_packs')
for path in packs_dir.glob('*.json'):
    text = path.read_text(encoding='utf-8')
    new_text = text.replace(': True', ': true').replace(': False', ': false')
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('fixed', path.name)
    else:
        print('ok', path.name)
