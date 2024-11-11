from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db  # Import db from models.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'  # Replace with your database URI
db.init_app(app)


@app.route('/expenses', methods=['POST'])
def create_expense():
    data = request.get_json()

    # Validate data (optional)
    if not data or not all(field in data for field in ['date', 'amount', 'category', 'description']):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Create and save expense
        new_expense = Expense(
            date=data['date'],
            amount=data['amount'],
            category=data['category'],
            description=data['description'],
        )
        db.session.add(new_expense)
        db.session.commit()

        return jsonify({'message': 'Expense created successfully!', 'expense': new_expense.serialize()}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    try:
        expense = Expense.query.get_or_404(expense_id)
        data = request.get_json()

        expense.date = data.get('date', expense.date)
        expense.amount = data.get('amount', expense.amount)
        expense.category = data.get('category', expense.category)
        expense.description = data.get('description', expense.description)

        db.session.commit()
        return jsonify({'message': 'Expense updated successfully!'})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except NotFoundError:  # Handle expense not found error (optional)
        return jsonify({'error': f'Expense with id {expense_id} not found'}), 404


@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:
        expense = Expense.query.get_or_404(expense_id)
        db.session.delete(expense)
        db.session.commit()
        return jsonify({'message': 'Expense deleted successfully!'})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except NotFoundError:  # Handle expense not found error (optional)
        return jsonify({'error': f'Expense with id {expense_id} not found'}), 404
