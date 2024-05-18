from flask import Flask
from models import init_db
from routes import configure_routes
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Initialize database
init_db()

# Configure routes
configure_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
