import json
from pathlib import Path
import tempfile
import unittest
from sprout.migrate import migrate


class MigrationTests(unittest.TestCase):
    def test_backup_and_repeat_are_safe(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'plants.json'
            original = b'{"plants": [{"name": "Fern", "watered_at": "2026-10-01"}]}'
            path.write_bytes(original)
            self.assertTrue(migrate(path))
            self.assertEqual(path.with_suffix('.json.bak').read_bytes(), original)
            self.assertEqual(json.loads(path.read_text())['plants'][0]['last_watered'], '2026-10-01')
            self.assertFalse(migrate(path))

    def test_existing_backup_prevents_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'plants.json'
            original = b'{"plants": []}'
            path.write_bytes(original)
            path.with_suffix('.json.bak').write_text('keep')
            with self.assertRaises(FileExistsError):
                migrate(path)
            self.assertEqual(path.read_bytes(), original)
