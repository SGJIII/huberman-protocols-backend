from flask import jsonify, request, render_template
from scraper import scrape_transcripts  # Importing scrape_transcripts
from models import get_all_transcripts, get_transcript_by_id
from chatbot import generate_protocol

def configure_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/scrape', methods=['POST'])
    def scrape_and_save():
        try:
            scrape_transcripts()
            return jsonify({'status': 'success', 'message': 'Data scraped and saved successfully'}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @app.route('/transcripts', methods=['GET'])
    def list_transcripts():
        try:
            transcripts = get_all_transcripts()
            return jsonify({'status': 'success', 'data': transcripts}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @app.route('/transcript/<int:transcript_id>', methods=['GET'])
    def get_transcript(transcript_id):
        try:
            transcript = get_transcript_by_id(transcript_id)
            if transcript:
                return jsonify({'status': 'success', 'data': transcript}), 200
            else:
                return jsonify({'status': 'error', 'message': 'Transcript not found'}), 404
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @app.route('/chat', methods=['POST'])
    def chat():
        try:
            user_input = request.json.get('message')
            response = generate_protocol(user_input)
            return jsonify({'status': 'success', 'response': response}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
