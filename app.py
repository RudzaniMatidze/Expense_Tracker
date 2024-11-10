from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# ... (import models and configure database)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'  # Replace with your database URI
db.init_app(app)

@app.route('/expenses', methods=['POST'])
def create_expense():
  # Get request data (e.g., date, amount, category, description)
  data = request.get_json()

  if not data or not all(field in data for field in ['date', 'amount', 'category', 'description']):
    return jsonify({'error': 'Missing required fields'}), 400  # Bad request

  # Create Expense object with validated data
  new_expense = Expense(
      date=data['date'],
      amount=data['amount'],
      category=data['category'],
      description=data['description'],
  )

  # Add expense to database and commit changes
  db.session.add(new_expense)
  db.session.commit()

  return jsonify({'message': 'Expense created successfully!', 'expense': new_expense.serialize()}), 201  # Created
