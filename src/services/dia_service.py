from dia.model import Dia
import redis
import tempfile
import os

class DiaService:
    def __init__(self, redis_client):
        self.model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")
        self.redis_client = redis_client

    def generate_audio(self, text):
        output = self.model.generate(text, use_torch_compile=True, verbose=True)
        
        # Create a temporary file to store the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_file_path = temp_file.name
            self.model.save_audio(temp_file_path, output)

        # Store the audio file in Redis with an expiry of 10 days (864000 seconds)
        with open(temp_file_path, 'rb') as audio_file:
            self.redis_client.setex(temp_file_path, 864000, audio_file.read())

        # Return the path of the temporary file
        return temp_file_path

    def get_audio(self, file_path):
        # Check if the audio file exists in Redis
        audio_data = self.redis_client.get(file_path)
        if audio_data:
            return audio_data
        return None

    def cleanup_audio(self, file_path):
        # Remove the temporary file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)