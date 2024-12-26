from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WordPhrase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    translation = db.Column(db.String(100), nullable=False)
    example_sentence = db.Column(db.String(255), nullable=True)
