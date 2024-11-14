const expenseForm = document.getElementById('expense-form');
const expenseTable = document.getElementById('expense-table').getElementsByTagName('tbody')[0];
const monthlyTotalSpan = document.getElementById('monthly-total');

// Fetch total monthly expense from the API
function fetchTotalMonthlyExpense() {
    fetch('/api/expenses/total-monthly')
        .then(response => response.json())
        .then(data => {
            monthlyTotalSpan.textContent = data.total_expense.toFixed(2);
        });
}

// Fetch expenses from the API
function fetchExpenses() {
    fetch('/api/expenses')
        .then(response => response.json())
        .then(data => {
            expenseTable.innerHTML = '';
            data.forEach(expense => {
                const row = expenseTable.insertRow();
                row.innerHTML = `
                    <td>${expense.id}</td>
                    <td>${expense.date}</td>
                    <td>${expense.amount}</td>
                    <td>${expense.category}</td>
                    <td>${expense.description}</td>
                    <td>
                        <button onclick="deleteExpense(${expense.id})">Delete</button>
                        <button onclick="editExpense(${expense.id})">Edit</button>
                    </td>
                `;
            });
        });
}

// Add a new expense
expenseForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const date = document.getElementById('expense-date').value;
    const amount = document.getElementById('expense-amount').value;
    const category = document.getElementById('expense-category').value;
    const description = document.getElementById('expense-description').value;

    const newExpense = { date, amount, category, description };

    const expenseId = document.getElementById('expense-id').value;

    const method = expenseId ? 'PUT' : 'POST';
    const url = expenseId ? `/api/expenses/${expenseId}` : '/api/expenses';

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newExpense)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchExpenses();
        fetchTotalMonthlyExpense();
        resetForm();
    });
});

// Delete an expense
function deleteExpense(expenseId) {
    fetch(`/api/expenses/${expenseId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchExpenses();
        fetchTotalMonthlyExpense();
    });
}

// Edit an expense
function editExpense(expenseId) {
    fetch(`/api/expenses/${expenseId}`)
        .then(response => response.json())
        .then(expense => {
            document.getElementById('expense-id').value = expense.id;
            document.getElementById('expense-date').value = expense.date;
            document.getElementById('expense-amount').value = expense.amount;
            document.getElementById('expense-category').value = expense.category;
            document.getElementById('expense-description').value = expense.description;

            const submitButton = document.getElementById('submit-button');
            submitButton.textContent = "Update Expense";
        });
}

// Reset the form and button to default (Add Expense)
function resetForm() {
    document.getElementById('expense-form').reset();
    const submitButton = document.getElementById('submit-button');
    submitButton.textContent = "Add Expense";
}

// Fetch expenses and total monthly expense when the page loads
window.onload = function() {
    fetchExpenses();
    fetchTotalMonthlyExpense();
};
