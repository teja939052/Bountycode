import json
try:
    print(json.loads('{"a": True, "b": False}'))
except Exception as e:
    print('ERROR:', e)
