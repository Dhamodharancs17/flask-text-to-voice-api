from flask import Flask, jsonify
import unittest
from unittest.mock import patch, MagicMock
from src.services.dia_service import generate_audio
from src.services.storage_service import store_audio

class TestAudioServices(unittest.TestCase):

    @patch('src.services.dia_service.Dia')
    def test_generate_audio(self, mock_dia):
        mock_model = MagicMock()
        mock_dia.from_pretrained.return_value = mock_model
        mock_model.generate.return_value = b'audio_data'

        text = "Test text for audio generation."
        audio_output = generate_audio(text)

        self.assertEqual(audio_output, b'audio_data')
        mock_dia.from_pretrained.assert_called_once_with("nari-labs/Dia-1.6B", compute_dtype="float16")
        mock_model.generate.assert_called_once_with(text, use_torch_compile=True, verbose=True)

    @patch('src.services.storage_service.redis_client')
    def test_store_audio(self, mock_redis):
        audio_data = b'audio_data'
        key = 'test_audio_key'
        store_audio(key, audio_data)

        mock_redis.set.assert_called_once_with(key, audio_data, ex=864000)  # 10 days in seconds

if __name__ == '__main__':
    unittest.main()