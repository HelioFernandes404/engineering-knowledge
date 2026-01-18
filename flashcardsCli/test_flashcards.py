import unittest
from unittest.mock import patch, MagicMock
import wave
import io

# import your functions here
from flashcards import tts_bytes, play_wav_bytes

class TestTTS(unittest.TestCase):

    @patch("flashcards.requests.get")
    def test_tts_bytes_returns_data(self, mock_get):
        fake_wav_data = b"RIFF....WAVEfmt " + b"\x00" * 100  # fake header
        mock_resp = MagicMock()
        mock_resp.content = fake_wav_data
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        result = tts_bytes("test", speaker_id="p376")
        self.assertEqual(result, fake_wav_data)
        mock_get.assert_called_once()
    
    @patch("flashcards.sa.play_buffer")
    def test_play_wav_bytes_runs(self, mock_play):
        # Generate a very basic valid WAV in memory
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(22050)
            wf.writeframes(b"\x00\x00" * 2205)  # 0.1 second of silence

        buffer.seek(0)
        wav_bytes = buffer.read()

        mock_obj = MagicMock()
        mock_play.return_value = mock_obj

        # Call the function
        play_wav_bytes(wav_bytes)

        mock_play.assert_called_once()
        mock_obj.wait_done.assert_called_once()

if __name__ == "__main__":
    unittest.main()
