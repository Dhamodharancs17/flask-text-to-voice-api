from flask import jsonify

def validate_text_input(text):
    if not isinstance(text, str) or not text.strip():
        return False, "Invalid input: Text must be a non-empty string."
    return True, ""

def format_response(audio_file_path):
    return jsonify({
        "message": "Audio generated successfully.",
        "audio_file": audio_file_path
    })