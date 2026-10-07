"""Upgrade sample plant storage with a backup and an atomic replacement."""
import json
from pathlib import Path


def migrate(path=Path('plants.json')):
    original = path.read_bytes()
    data = json.loads(original)
    if data.get('schema_version') == 2:
        return False
    if data.get('schema_version', 1) != 1:
        raise ValueError('Unsupported plant schema')
    for plant in data['plants']:
        plant['last_watered'] = plant.pop('watered_at')
    data['schema_version'] = 2
    backup = path.with_suffix('.json.bak')
    with backup.open('xb') as stream:
        stream.write(original)
    temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(data, indent=2) + '\n')
    temporary.replace(path)
    return True


if __name__ == '__main__':
    migrate()
