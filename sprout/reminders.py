"""Watering dates and reminders, independent of HTTP."""
from datetime import date, timedelta
import json
from pathlib import Path


def load_settings(path=Path('settings.json')):
    return json.loads(path.read_text())


def load_plants(path=Path('plants.json')):
    return json.loads(path.read_text())['plants']


def due_plants(plants, today, settings):
    interval = timedelta(days=settings['watering_interval_days'])
    return [plant for plant in plants
            if date.fromisoformat(plant['watered_at']) + interval <= today]
