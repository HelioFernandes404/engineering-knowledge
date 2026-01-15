import unittest
from unittest.mock import patch, MagicMock
from src.audio_recorder import find_monitor_device, list_audio_devices


class TestAudioRecorder(unittest.TestCase):
    """Tests for audio recording module"""

    @patch('src.audio_recorder.sd.query_devices')
    def test_find_monitor_device_with_monitor(self, mock_query):
        """Test monitor device detection"""
        # Simulate devices
        mock_query.return_value = [
            {'name': 'Monitor of Built-in Audio', 'max_input_channels': 2, 'index': 0},
            {'name': 'Built-in Microphone', 'max_input_channels': 1, 'index': 1},
        ]

        device_id, device_name = find_monitor_device()

        self.assertEqual(device_id, 0)
        self.assertIn('monitor', device_name.lower())

    @patch('src.audio_recorder.sd.query_devices')
    def test_find_monitor_device_without_monitor(self, mock_query):
        """Test fallback when no monitor device exists"""
        # Simulate absence of monitor
        mock_query.side_effect = [
            [{'name': 'Microphone', 'max_input_channels': 1, 'index': 0}],
            {'name': 'Default Input', 'max_input_channels': 1, 'index': 0}
        ]

        device_id, device_name = find_monitor_device()

        self.assertIsNotNone(device_id)
        self.assertIsNotNone(device_name)


if __name__ == '__main__':
    unittest.main()
