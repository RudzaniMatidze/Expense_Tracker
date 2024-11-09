from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    amount = db.Column(db.Float)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
