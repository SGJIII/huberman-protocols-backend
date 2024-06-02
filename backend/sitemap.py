from flask import Blueprint, make_response, render_template
from models import get_all_transcripts
from datetime import datetime, timedelta
from slugify import slugify

sitemap_blueprint = Blueprint('sitemap', __name__)

@sitemap_blueprint.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages = []

    # Static pages
    ten_days_ago = (datetime.now() - timedelta(days=10)).date().isoformat()
    pages.append(["https://huberman-protocols-9761d2c36844.herokuapp.com/", ten_days_ago])
    pages.append(["https://huberman-protocols-9761d2c36844.herokuapp.com/blog", ten_days_ago])

    # Blog posts
    transcripts = get_all_transcripts()
    for transcript in transcripts:
        url = "https://huberman-protocols-9761d2c36844.herokuapp.com/blog/" + slugify(transcript['title'])
        modified_time = datetime.now().date().isoformat()
        pages.append([url, modified_time])

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response