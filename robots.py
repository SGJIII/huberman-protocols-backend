from flask import Blueprint, make_response

robots_blueprint = Blueprint('robots', __name__)

@robots_blueprint.route('/robots.txt')
def robots():
    lines = [
        "User-Agent: *",
        "Disallow: /api/",
        "Allow: /",
        "Sitemap: https://huberman-protocols-9761d2c36844.herokuapp.com/sitemap.xml"
    ]
    response = make_response("\n".join(lines))
    response.headers["Content-Type"] = "text/plain"
    return response
