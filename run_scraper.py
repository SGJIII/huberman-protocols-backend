# run_scraper.py
from app import app
from scraper import scrape_transcripts

if __name__ == '__main__':
    with app.app_context():
        scrape_transcripts()

