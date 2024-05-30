from flask import jsonify, request, render_template, url_for, redirect
from scraper import scrape_transcripts
from models import get_all_transcripts, get_transcript_by_id, get_transcript_by_title
from chatbot import generate_protocol, update_protocol, send_protocol_via_email
import logging
from slugify import slugify

def configure_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/scrape', methods=['GET'])
    def scrape_and_save():
        try:
            app.logger.info('Scrape route called')
            scrape_transcripts()
            app.logger.info('Scraping completed successfully')
            return jsonify({'status': 'success', 'message': 'Data scraped and saved successfully'}), 200
        except Exception as e:
            app.logger.error(f'Error during scraping: {e}')
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

    @app.route('/episodes', methods=['GET'])
    def get_episodes():
        try:
            transcripts = get_all_transcripts()
            episodes = [{"id": t['id'], "title": t['title']} for t in transcripts]
            return jsonify({"status": "success", "episodes": episodes}), 200
        except Exception as e:
            return jsonify({"status": 'error', 'message': str(e)}), 500

    @app.route('/chat', methods=['POST'])
    def chat():
        try:
            episode_id = request.json.get('episode_id')
            response = generate_protocol(episode_id)
            return jsonify({'status': 'success', 'response': response}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @app.route('/update_protocol', methods=['POST'])
    def update_chat_protocol():
        try:
            user_input = request.json.get('message')
            current_protocol = request.json.get('protocol')
            response = update_protocol(user_input, current_protocol)
            return jsonify({'status': 'success', 'response': response}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @app.route('/send_protocol', methods=['POST'])
    def send_protocol():
        try:
            protocol_text = request.json.get('protocol')
            user_email = request.json.get('email')
            response = send_protocol_via_email(protocol_text, user_email)
            return jsonify({'status': 'success', 'message': response}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @app.route('/blog', methods=['GET'])
    def blog():
        try:
            transcripts = get_all_transcripts()
            return render_template('blog.html', transcripts=transcripts)
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @app.route('/blog/<title>', methods=['GET'])
    def blog_post(title):
        try:
            transcript = get_transcript_by_title(title)
            if transcript:
                return render_template('blog_post.html', transcript=transcript)
            else:
                return jsonify({'status': 'error', 'message': 'Transcript not found'}), 404
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @app.route('/redirect_blog/<int:transcript_id>', methods=['GET'])
    def redirect_blog(transcript_id):
        transcript = get_transcript_by_id(transcript_id)
        if transcript:
            title_slug = slugify(transcript['title'])
            return redirect(url_for('blog_post', title=title_slug))
        else:
            return jsonify({'status': 'error', 'message': 'Transcript not found'}), 404
    
    @app.route('/privacy_policy', methods=['GET'])
    def privacy_policy():
        return render_template('privacy_policy.html')
