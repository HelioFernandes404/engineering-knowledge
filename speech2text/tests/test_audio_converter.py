import unittest
import os
import tempfile
from src.audio_converter import converter_mp3_to_wav, verify_audio


class TestAudioConverter(unittest.TestCase):
    """Tests for audio conversion module"""

    def setUp(self):
        """Setup before each test"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Cleanup after each test"""
        # Clean temporary files
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_converter_nonexistent_file(self):
        """Test conversion with non-existent file"""
        input_file = os.path.join(self.temp_dir, "nonexistent.mp3")
        output_file = os.path.join(self.temp_dir, "output.wav")

        result = converter_mp3_to_wav(input_file, output_file)
        self.assertFalse(result)

    def test_verify_audio_nonexistent_file(self):
        """Test verification with non-existent file"""
        wav_file = os.path.join(self.temp_dir, "nonexistent.wav")

        result = verify_audio(wav_file)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
