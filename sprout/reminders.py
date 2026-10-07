"""Watering dates and reminders, independent of HTTP."""
from datetime import date, timedelta
import json
import yaml
from pathlib import Path


def load_settings(path=Path('settings.yaml')):
    return yaml.safe_load(path.read_text())


def load_plants(path=Path('plants.json')):
    data = json.loads(path.read_text())
    if data.get('schema_version') != 2:
        raise ValueError('Run python -m sprout.migrate before starting')
    return data['plants']


def due_plants(plants, today, settings):
    interval = timedelta(days=settings['watering_interval_days'])
    return [plant for plant in plants
            if date.fromisoformat(plant['last_watered']) + interval <= today]
