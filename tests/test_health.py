import unittest
from unittest.mock import Mock, patch

from sprout.server import Handler


class HealthTests(unittest.TestCase):
    def test_health_does_not_open_plant_storage(self):
        handler = Handler.__new__(Handler)
        handler.path = '/health'
        handler.send_response = Mock()
        handler.end_headers = Mock()
        with patch('sprout.server.load_plants', side_effect=AssertionError('storage was opened')):
            handler.do_GET()
        handler.send_response.assert_called_once_with(204)
        handler.end_headers.assert_called_once_with()
