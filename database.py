from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config  # Import configurations

app = Flask(__name__)
app.config.from_object(Config)  # Load config settings

db = SQLAlchemy(app)

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, default=0)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("📊 Database and tables created successfully!")
