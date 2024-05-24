from flask import Flask
from models import init_db, db
from routes import configure_routes
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)
with app.app_context():
    init_db()

# Configure routes
configure_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
