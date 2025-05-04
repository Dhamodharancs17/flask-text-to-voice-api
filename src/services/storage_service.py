from redis import Redis
import os
import tempfile

class StorageService:
    def __init__(self):
        self.redis_client = Redis(host=os.getenv('REDIS_HOST', 'localhost'), 
                                  port=int(os.getenv('REDIS_PORT', 6379)), 
                                  db=0)

    def store_audio(self, audio_data, audio_id):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        self.redis_client.set(audio_id, temp_file_path, ex=864000)  # 10 days in seconds
        return audio_id

    def retrieve_audio(self, audio_id):
        audio_path = self.redis_client.get(audio_id)
        if audio_path:
            return audio_path.decode('utf-8')
        return None

    def delete_audio(self, audio_id):
        self.redis_client.delete(audio_id)