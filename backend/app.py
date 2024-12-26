from flask import Flask, render_template, request, redirect, url_for
from models import db, WordPhrase
from database_setup import load_initial_data
import os

app = Flask(__name__)

# Create absolute path for the database
basedir = os.path.abspath(os.path.dirname(__file__))  # Get the absolute directory path for the current file
data_dir = os.path.join(basedir, 'data')  # Join the base directory to create the data directory path
os.makedirs(data_dir, exist_ok=True)  # Ensure data directory exists, create it if it doesn't
db_path = os.path.join(data_dir, 'words_phrases.db')  # Join the data directory with the database file name

# Configure the Flask app with database settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/berkanberk/Desktop/cms_project/data/words_phrases.db'  # Database URI for SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
app.config['SQLALCHEMY_ECHO'] = True  # Enable SQLAlchemy logging to echo SQL statements

db.init_app(app)  # Initialize the SQLAlchemy app

@app.route('/')
def index():
    """Homepage showing a paginated list of words and phrases."""
    page = request.args.get('page', 1, type=int)  # Get the page number from query parameters, default to 1
    per_page = 10  # Number of items per page
    words = WordPhrase.query.paginate(page=page, per_page=per_page)  # Paginate the query results
    return render_template('index.html', words=words, page=page)  # Pass the page number to the template

@app.route('/edit/<int:word_id>', methods=['GET', 'POST'])
def edit_word(word_id):
    """Edit a specific word or phrase."""
    word = WordPhrase.query.get_or_404(word_id)  # Get the word by ID or return 404 if not found
    page = request.args.get('page', 1, type=int)  # Get the current page number from the query parameters
    if request.method == 'POST':  # If the request method is POST, update the word details
        word.word = request.form['word']  # Get the updated word from the form
        word.translation = request.form['translation']  # Get the updated translation from the form
        word.example_sentence = request.form['example_sentence']  # Get the updated example sentence from the form
        db.session.commit()  # Commit the changes to the database
        return redirect(url_for('index', page=page))  # Redirect to the homepage with the current page number
    return render_template('edit.html', word=word, page=page)  # Render the 'edit.html' template with the word details and page number

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all database tables
        load_initial_data()  # Populate the database with initial data
    app.run(debug=True)  # Run the Flask app in debug mode
