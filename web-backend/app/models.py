from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from . import db

class RequestForDocs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    email_text = db.Column(db.Text, nullable=False)
    callback_url = db.Column(db.Text, nullable=False)
    string_id = db.Column(db.String(255), nullable=False)
    doc_types = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)