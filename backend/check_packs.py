import sys, json
sys.path.insert(0, 'backend')
from pathlib import Path
from app.models.mission_pack import MissionPack

packs_dir = Path('backend/app/content/mission_packs')
for path in sorted(packs_dir.glob('*.json')):
    pack_id = path.stem
    try:
        raw = json.loads(path.read_text(encoding='utf-8'))
        pack = MissionPack(**raw)
        print('OK', pack_id)
    except Exception as e:
        print('FAIL', pack_id, str(e)[:120])
