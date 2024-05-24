from app import app
from scraper import scrape_transcripts

with app.app_context():
    scrape_transcripts()
