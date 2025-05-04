
import os
import hashlib
import io
from functools import wraps
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from redis import Redis
from dia.model import Dia
from dotenv import load_dotenv
from pyngrok import ngrok

model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype="float16")

ngrok.set_auth_token("API_KEY")


# Load environment variables (optional)
load_dotenv()

# Hardcoded API key for authorization
API_KEY = "APP_API_KEY"

# Redis configuration
# REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
# EXPIRE_SEC = 10 * 24 * 3600  # 10 days

app = Flask(__name__)
CORS(app)
# redis_client = Redis.from_url(REDIS_URL)


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if key != API_KEY:
            return jsonify({"error": "Invalid or missing API Key"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/generate-text-to-voice/en", methods=["POST"])
@require_api_key
def generate_tts():
    data = request.get_json(force=True)
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Create a unique cache key for this text
    # key = "tts:" + hashlib.sha256(text.encode("utf-8")).hexdigest()

    # Try to fetch from Redis
    # audio_bytes = redis_client.get(key)
    audio_bytes = None
    if audio_bytes is None:
        print("Generating audio for ", text)
        # Generate audio
        output = model.generate(text, use_torch_compile=True, verbose=False)
        tmp_file = "temp.mp3"
        model.save_audio(tmp_file, output)
        with open(tmp_file, "rb") as f:
            audio_bytes = f.read()
        os.remove(tmp_file)
        # Cache in Redis
        # redis_client.set(key, audio_bytes, ex=EXPIRE_SEC)
        print("Audio generated!")

    return send_file(
        io.BytesIO(audio_bytes),
        mimetype="audio/mpeg",
        as_attachment=False,
        download_name="speech.mp3"
    )

if __name__ == "__main__":
    # Open a ngrok tunnel to the Flask app
    public_url = ngrok.connect(addr=8000, domain="DOMAIN_NAME")
    print(f" * ngrok tunnel is running at: {public_url}")
    app.run(host="0.0.0.0", port=8000)
