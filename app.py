from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Initialize the database outside the app to avoid circular import issues
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configure the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

    # Import models and routes after db is initialized
    with app.app_context():
        from models import Expense
        db.create_all()  # Creates the database tables if they don’t exist

    from routes import expense_routes
    app.register_blueprint(expense_routes, url_prefix='/api')  # Register blueprint with '/api' prefix

    # Root route (home) to serve the HTML page
    @app.route('/')
    def home():
        return render_template('index.html')  # Renders the index.html file

    return app

# To run the app directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
