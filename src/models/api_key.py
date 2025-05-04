from datetime import datetime, timedelta
import uuid

class APIKey:
    def __init__(self, key=None, created_at=None, expires_at=None):
        self.key = key or str(uuid.uuid4())
        self.created_at = created_at or datetime.utcnow()
        self.expires_at = expires_at or self.created_at + timedelta(days=10)

    def is_valid(self):
        return datetime.utcnow() < self.expires_at

    @classmethod
    def generate_key(cls):
        return cls()