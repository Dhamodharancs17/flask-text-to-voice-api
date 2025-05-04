from flask import Blueprint, request, send_file, jsonify
from src.services.dia_service import generate_audio
from src.services.storage_service import store_audio
from src.api.auth import api_key_required

api = Blueprint('api', __name__)

@api.route('/generate/text-to-voice/en', methods=['POST'])
@api_key_required
def text_to_voice():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        audio_output = generate_audio(text)
        audio_file_path = store_audio(audio_output)

        return send_file(audio_file_path, mimetype='audio/mpeg', as_attachment=True, download_name='output.mp3')
    except Exception as e:
        return jsonify({"error": str(e)}), 500