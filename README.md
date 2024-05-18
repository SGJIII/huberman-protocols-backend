# huberman_protocols

## Project Overview:

I have built a Flask web application that acts as a chatbot to help users create personalized protocols based on Andrew Huberman's podcast transcripts. The application scrapes transcripts from a website, stores them in a SQLite database, and uses OpenAI's GPT-3.5-turbo model to generate responses and protocols based on user input.

## Current Functionality:

### Scraping Transcripts:

The application scrapes full transcripts of Andrew Huberman's podcasts and saves them in a SQLite database.

### Chatbot Interface:
Users interact with the chatbot through a web interface. They can specify what they want to improve (e.g., "I want to improve my sleep").
The chatbot searches the database for relevant transcripts and generates a protocol based on the excerpts from these transcripts.

### Emailing Protocols:
The chatbot can generate a PDF of the protocol and email it to the user.
## Issues:

### Transcript Storage:
Currently, the full transcripts are stored in the database. This makes responses verbose and less focused. We need to store concise summaries instead of full transcripts.

### Search Functionality:
The current search functionality is too literal and doesn't effectively find relevant transcripts based on user queries. For example, it fails to find episodes related to "sleep" when a user types "I want to improve my sleep".
Required Improvements:

### Store Summaries:
Modify the scraper to extract and store summaries of the podcasts instead of full transcripts.

### Improve Search:
Enhance the search functionality to be more flexible and context-aware. It should understand user intent and find relevant episodes even if the query isn't a direct match to the transcript text.
Current Code Overview:

### app.py:
```
from flask import Flask
from models import init_db
from routes import configure_routes
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Initialize database
init_db()

# Configure routes
configure_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
```

### chatbot.py:
```
import os
from openai import OpenAI
from dotenv import load_dotenv
from models import search_transcripts
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_protocol(user_input):
    transcripts = search_transcripts(user_input)
    if not transcripts:
        return "No relevant transcripts found."

    # Extract excerpts from the found transcripts
    excerpts = []
    for transcript in transcripts:
        excerpts.append(transcript[3][:1000])  # Taking the first 1000 characters as an excerpt

    # Combine all excerpts into one large string
    combined_excerpts = ' '.join(excerpts)
    
    # Use the combined excerpts to generate a response
    prompt = f"The user wants to: {user_input}. Based on the following transcript excerpts, provide a Huberman protocol: {combined_excerpts}"

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo",
    )
    
    return response.choices[0].message.content.strip()

def update_protocol(user_input, protocol_text):
    prompt = f"The current protocol is: {protocol_text}. The user wants to make the following changes: {user_input}. Update the protocol accordingly."

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo",
    )
    
    return response.choices[0].message.content.strip()

def send_protocol_via_email(protocol_text, user_email):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, protocol_text)

    pdf_output = f"protocol_{user_email}.pdf"
    pdf.output(pdf_output)

    # Email configuration
    sender_email = "your-email@example.com"
    sender_password = "your-password"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = "Your Huberman Protocol"

    body = "Please find attached your personalized Huberman protocol."
    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_output, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=pdf_output)
        part['Content-Disposition'] = f'attachment; filename="{pdf_output}"'
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return "Email sent successfully."
    except Exception as e:
        return f"Failed to send email: {str(e)}"
```
### routes.py:
```
from flask import jsonify, request, render_template
from scraper import scrape_transcripts  # Importing scrape_transcripts
from models import get_all_transcripts, get_transcript_by_id
from chatbot import generate_protocol, update_protocol, send_protocol_via_email

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
```
### models.py:
``` 
import sqlite3
import re

DATABASE = 'transcripts.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            content TEXT,
            summary TEXT  -- Added summary field
        )
    ''')
    conn.commit()
    conn.close()

def save_transcript(title, url, content, summary):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT OR REPLACE INTO transcripts (title, url, content, summary)
            VALUES (?, ?, ?, ?)
            ''', (title, url, content, summary))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Failed to insert or replace transcript at {url}: {e}")
    finally:
        conn.close()

def get_all_transcripts():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM transcripts')
    transcripts = c.fetchall()
    conn.close()
    return transcripts

def get_transcript_by_id(transcript_id):```
