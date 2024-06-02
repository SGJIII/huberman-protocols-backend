from flask_sqlalchemy import SQLAlchemy
from slugify import slugify

db = SQLAlchemy()

class Transcript(db.Model):
    __tablename__ = 'transcripts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    url = db.Column(db.String(255), unique=True)
    content = db.Column(db.Text)
    summary = db.Column(db.Text)

class Protocol(db.Model):
    __tablename__ = 'protocols'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255))
    protocol = db.Column(db.Text)

def init_db():
    db.create_all()

def save_transcript(title, url, content, summary):
    existing_transcript = Transcript.query.filter_by(url=url).first()
    if existing_transcript is None:
        transcript = Transcript(title=title, url=url, content=content, summary=summary)
        db.session.add(transcript)
        db.session.commit()

def get_all_transcripts():
    transcripts = Transcript.query.all()
    return [{'id': t.id, 'title': t.title, 'url': t.url, 'content': t.content, 'summary': t.summary} for t in transcripts]

def get_transcript_by_id(transcript_id):
    transcript = Transcript.query.get(transcript_id)
    if transcript:
        return {'id': transcript.id, 'title': transcript.title, 'url': transcript.url, 'content': transcript.content, 'summary': transcript.summary}
    else:
        return None

def get_transcript_by_title(slug_title):
    transcripts = Transcript.query.all()
    for transcript in transcripts:
        if slugify(transcript.title) == slug_title:
            return {'id': transcript.id, 'title': transcript.title, 'url': transcript.url, 'content': transcript.content, 'summary': transcript.summary}
    return None

def search_transcripts(query):
    results = Transcript.query.filter((Transcript.title.ilike(f'%{query}%')) | (Transcript.content.ilike(f'%{query}%'))).all()
    return [{'id': r.id, 'title': r.title, 'url': r.url, 'content': r.content, 'summary': r.summary} for r in results]

def save_protocol(user_id, protocol):
    new_protocol = Protocol(user_id=user_id, protocol=protocol)
    db.session.add(new_protocol)
    db.session.commit()

def get_user_protocols(user_id):
    protocols = Protocol.query.filter_by(user_id=user_id).all()
    return [{'id': p.id, 'protocol': p.protocol} for p in protocols]