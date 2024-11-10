from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db  # Import db from models.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'  # Replace with your database URI
db.init_app(app)

@app.route('/expenses', methods=['POST'])
def create_expense():

@app.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    data = request.get_json()
   
    expense.date = data.get('date', expense.date)
    expense.amount = data.get('amount', expense.amount)
    expense.category = data.get('category', expense.category)
    expense.description = data.get('description', expense.description)

    db.session.commit()
    return jsonify({'message': 'Expense updated successfully!'})

@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    
