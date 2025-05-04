from flask import Flask, jsonify, request
import requests

def test_generate_text_to_voice(client):
    response = client.post('/generate/text-to-voice/en', json={'text': 'Hello, this is a test.'})
    assert response.status_code == 200
    assert response.content_type == 'audio/mpeg'
    assert 'simple.mp3' in response.data.decode()

def test_generate_text_to_voice_invalid_method(client):
    response = client.get('/generate/text-to-voice/en')
    assert response.status_code == 405

def test_generate_text_to_voice_missing_text(client):
    response = client.post('/generate/text-to-voice/en', json={})
    assert response.status_code == 400
    assert response.json['error'] == 'Text is required.'

def test_generate_text_to_voice_invalid_text(client):
    response = client.post('/generate/text-to-voice/en', json={'text': ''})
    assert response.status_code == 400
    assert response.json['error'] == 'Text cannot be empty.'