from flask import Flask, redirect, request
from models import init_db, db
from routes import configure_routes
from dotenv import load_dotenv
import os
from sitemap import sitemap_blueprint
from robots import robots_blueprint

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Initialize database
with app.app_context():
    init_db()

# Redirect www to root domain
@app.before_request
def redirect_www():
    if request.host.startswith('www.'):
        return redirect(request.url.replace('www.', ''), code=301)

# Configure routes
configure_routes(app)
app.register_blueprint(sitemap_blueprint)
app.register_blueprint(robots_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
