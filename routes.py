from flask import Blueprint, request, jsonify
from app import db
from models import Expense


expense_routes = Blueprint('expense_routes', __name__)

# Route to create a new expense
@expense_routes.route('/expenses', methods=['POST'])
def create_expense():
    data = request.get_json()
    new_expense = Expense(
        date=data['date'],
        amount=data['amount'],
        category=data['category'],
        description=data['description'],
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({'message': 'Expense created successfully!'})

# Route to update an existing expense by ID
@expense_routes.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    data = request.get_json()
    expense.date = data.get('date', expense.date)
    expense.amount = data.get('amount', expense.amount)
    expense.category = data.get('category', expense.category)
    expense.description = data.get('description', expense.description)
    db.session.commit()
    return jsonify({'message': 'Expense updated successfully!'})

# Route to delete an existing expense by ID
@expense_routes.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Expense deleted successfully!'})

# Route to fetch all expenses
@expense_routes.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([{
        'id': expense.id,
        'date': expense.date,
        'amount': expense.amount,
        'category': expense.category,
        'description': expense.description
    } for expense in expenses])
