from datetime import datetime, timedelta
from flask import Flask, jsonify, request, send_from_directory, jsonify, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

from workers import make_celery, cache
from flask_mail import Mail, Message # type: ignore
from celery.schedules import crontab # type: ignore



app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': 'http://localhost:5173'}})
CORS(app, resources={r'/books': {'origins': 'http://localhost:5173'}, r'/sections': {'origins': 'http://localhost:5173'}})


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secret key of your choice
app.config['CACHE_TYPE'] = "RedisCache"


app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] ="viratprem4321@gmail.com"
app.config['MAIL_PASSWORD'] ="puqnxaaxoicstoiw"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = "viratprem4321@gmail.com"

cache.init_app(app)
celery = make_celery(app)
mail = Mail(app)


db = SQLAlchemy(app)
jwt = JWTManager(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

class RegistrationForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    email = StringField('Email')
    submit = SubmitField('Register')

# Define User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(10), nullable=False, default='user')
    books_requested = db.relationship('BookRequest', backref='user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    books = db.relationship('Book', backref='section', lazy=True)

# Define Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    author = db.Column(db.String(100))
    image = db.Column(db.String())  # New column for storing image filename
    requests = db.relationship('BookRequest', backref='book', lazy=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))

# Define BookRequest model
class BookRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.String(50), nullable=False, default='pending')  # Default status is 'pending'

# Define Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_name = db.Column(db.String(100), nullable=False)  # Changed to store book name
    rating = db.Column(db.Integer, nullable=False)  # Changed to accept ratings up to 10
    comment = db.Column(db.Text)

    
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    
#######################################################
@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=17, minute=45), send_monthly_report.s())
    sender.add_periodic_task(crontab(hour=17, minute=45), visit_reminder.s())

@celery.task()
def visit_reminder():
    users_to_remind = User.query.all()

    for user in users_to_remind:
        send_reminder(user)
    return f"Sent {len(users_to_remind)} reminders"

def send_reminder(user):
    with mail.connect() as conn:
        msg = Message(
            subject="Visit the site",
            recipients=[user.email],
            sender="viratprem4321@gmail.com"  
        )
        msg.body = f"Hello {user.username},\n\nDon't forget to visit our site and read some books."
        conn.send(msg)
        



def monthly_report(user):
    # Gather relevant data for the user
    username = user.username
    books_requested = user.books_requested
    feedbacks = user.feedbacks

    
    # Calculate the start and end date for the monthly report
    today = datetime.now()
    start_date = today.replace(day=1) - timedelta(days=1)
    end_date = today.replace(day=1)
    
    # Construct HTML content for the report
    html_content = f"""
    <html>
    <head>
        <title>Monthly Report for {username}</title>
    </head>
    <body>
        <h1>Monthly Report for {username}</h1>
        <h2>Period: {start_date.strftime('%B %Y')}</h2>
        
        <h3>Books Requested:</h3>
        <ul>
    """
    for request in books_requested:
        html_content += f"<li>{request.book.name}</li>"
    
    html_content += """
        </ul>
        
        <h3>Feedbacks Given:</h3>
        <ul>
    """
    for feedback in feedbacks:
        html_content += f"<li>{feedback.book_name} - Rating: {feedback.rating}, Comment: {feedback.comment}</li>"
    
    html_content += """
        </ul>
    </body>
    </html>
    """
    
    return html_content

@celery.task()
def send_monthly_report():
    users = User.query.all()
    for user in users:
        html_content = monthly_report(user)
        with mail.connect() as conn:
            msg = Message(
                subject="Monthly Report",
                recipients=[user.email],
                sender="viratprem4321@gmail.com",
                html=html_content
            )
            conn.send(msg)
    return f"Sent {len(users)} monthly reports"

########################################

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def homepage():
    return jsonify({'message': 'Welcome to the homepage!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity={'id': user.id})
        return jsonify(access_token=access_token, user={'id': user.id}, message='Login successful'), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'Username already exists'}), 400

        new_user = User(username=username, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id)

        return jsonify(access_token=access_token, message='Registration successful'), 201

    except Exception as e:
        print(f"Error during registration: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500


from sqlalchemy.orm.exc import NoResultFound


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add-book', methods=['POST'])
@jwt_required()
def add_book():
    try:
        data = request.form  # Use request.form for form data
        name = data.get('name')
        author = data.get('author')
        section_id = data.get('sectionId')
        content = data.get('content')

        if not name or not author or not section_id or not content:
            return jsonify({'message': 'Missing required fields'}), 400

        section = Section.query.get(section_id)
        if not section:
            return jsonify({'message': 'Section not found'}), 404

        # Get the image file from the request
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '' and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                return jsonify({'error': 'Invalid file type for image'}), 400
        else:
            filename = None

        new_book = Book(name=name, author=author, section_id=section_id, content=content, image=filename)
        db.session.add(new_book)
        db.session.commit()

        return jsonify({'message': 'Book added successfully'}), 201

    except Exception as e:
        print(f"Error adding book: {str(e)}")
        return jsonify({'message': 'Failed to add book'}), 500



@app.route('/add-section', methods=['POST'])
@jwt_required()
def add_section():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'message': 'Unauthorized'}), 401

    try:
        data = request.get_json()  # Ensure you're getting JSON data
        if not data or 'name' not in data or 'description' not in data:
            return jsonify({'message': 'Invalid request data'}), 400

        name = data['name']
        description = data['description']

        existing_section = Section.query.filter_by(name=name).first()
        if existing_section:
            return jsonify({'message': 'Section with this name already exists'}), 409

        new_section = Section(name=name, description=description)
        db.session.add(new_section)
        db.session.commit()

        return jsonify({'message': 'Section added successfully'}), 201

    except Exception as e:
        print(f"Error adding section: {str(e)}")
        return jsonify({'message': 'Failed to add section'}), 500


@app.route('/sections', methods=['GET'])
# @cache.cached(timeout=500, key_prefix='sections')
def get_sections():
    sections = Section.query.all()
    sections_data = [{'id': section.id, 'name': section.name, 'description': section.description} for section in sections]
    return jsonify(sections_data)



@app.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    books = Book.query.all()
    books_data = []

    for book in books:
        # Get the section associated with the book
        section = Section.query.filter_by(id=book.section_id).first()
        section_name = section.name if section else ''  # Use section name if available

        # Build the URL for the book image if available
        image_url = None
        if book.image:
            image_url = url_for('uploaded_file', filename=book.image, _external=True)

        # Check if the book is requested and approved
        requested_book = BookRequest.query.filter_by(book_id=book.id).first()
        request_approved = requested_book.status == 'approved' if requested_book else False

        book_info = {
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'section': section_name,
            'image_url': image_url if image_url else '',  # Include image URL only if available
            'request_approved': request_approved  # Include the request approval status
        }
        books_data.append(book_info)
    return jsonify(books_data)


@app.route('/get_books', methods=['GET'])
def getbooks():
    books = Book.query.all()
    books_data = []

    for book in books:
        # Get the section associated with the book
        section = Section.query.filter_by(id=book.section_id).first()
        section_name = section.name if section else ''  # Use section name if available

        # Build the URL for the book image
        image_url = None
        if book.image:
            image_url = url_for('uploaded_file', filename=book.image, _external=True)

        book_info = {
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'section': section_name,
            'image_url': image_url  # Include the image URL in the response
        }
        books_data.append(book_info)

    return jsonify(books_data)

@app.route('/feedback', methods=['POST'])
def add_feedback():
    data = request.get_json()
    user_id = data.get('user_id')
    # book_id = data.get('book_id')
    book_name = data.get('book_name')
    rating = data.get('rating')
    comment = data.get('comment')

    if not user_id or not book_name or not rating:
        return jsonify({'error': 'Missing required fields'}), 400

    # Assuming Feedback model is imported and exists
    feedback = Feedback(
        user_id=user_id,
        # book_id=book_id,
        book_name=book_name,
        rating=rating,
        comment=comment
    )
    db.session.add(feedback)
    db.session.commit()

    return jsonify({'message': 'Feedback added successfully'}), 201

# Define the search-books endpoint
@app.route('/search-books', methods=['GET'])
@jwt_required()
def search_books():
    query = request.args.get('query')  # Get the search query from the URL parameter
    if not query:
        return jsonify({'message': 'Missing search query'}), 400

    # Use ilike for case-insensitive search
    books = Book.query.filter(
        (Book.name.ilike(f'%{query}%')) |  # Search by book name
        (Book.section.has(Section.name.ilike(f'%{query}%')))  # Search by section name
    ).all()

    books_data = []

    for book in books:
        # Get the section associated with the book
        section_name = book.section.name if book.section else ''  # Use section name if available

        # Build the URL for the book image
        image_url = None
        if book.image:
            image_url = url_for('uploaded_file', filename=book.image, _external=True)

        book_info = {
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'section': section_name,
            'image_url': image_url  # Include the image URL in the response
        }
        books_data.append(book_info)

    return jsonify(books_data)


@app.route('/admin/register', methods=['POST'])
def admin_register():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if Admin.query.filter_by(username=username).first():
            return jsonify({'message': 'Username already exists'}), 400

        new_admin = Admin(username=username, email=email, password=generate_password_hash(password))
        db.session.add(new_admin)
        db.session.commit()

        return jsonify({'message': 'Admin registration successful'}), 201

    except Exception as e:
        print(f"Error during admin registration: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500


@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    admin = Admin.query.filter_by(username=username).first()

    if admin and check_password_hash(admin.password, password):
        access_token = create_access_token(identity={'id': admin.id, 'username': admin.username})
        return jsonify(access_token=access_token, message='Admin login successful'), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/admin/dashboard')
@jwt_required()
def admin_dashboard():
    admin_id = get_jwt_identity()
    admin = Admin.query.get(admin_id)

    if not admin:
        return jsonify({'message': 'Admin not found'}), 404

    # Here you can fetch data specific to the admin dashboard
    # For example, you might fetch statistics, recent activities, etc.

    return jsonify({
        'message': 'Admin dashboard',
        'admin_id': admin.id,
        'username': admin.username,
        'dashboard_data': {...}  # Provide relevant dashboard data here
    })



@app.route('/edit_book/<int:book_id>', methods=['PUT'])
def edit_book(book_id):
    try:
        data = request.json  # Use request.json for JSON data
        name = data.get('name')
        author = data.get('author')
        section_id = data.get('section_id')  # Update to match frontend naming
        content = data.get('content')

        if not name or not author or not section_id or not content:
            return jsonify({'message': 'Missing required fields'}), 400

        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book not found'}), 404

        section = Section.query.get(section_id)
        if not section:
            return jsonify({'message': 'Section not found'}), 404

        book.name = name
        book.author = author
        book.section_id = section_id
        book.content = content
        db.session.commit()

        return jsonify({'message': 'Book updated successfully'}), 200

    except Exception as e:
        print(f"Error editing book: {str(e)}")
        return jsonify({'message': 'Failed to edit book'}), 500


@app.route('/delete_book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book not found'}), 404

        # Delete related book requests before deleting the book
        BookRequest.query.filter_by(book_id=book_id).delete()
        db.session.delete(book)
        db.session.commit()

        return jsonify({'message': 'Book deleted successfully'}), 200

    except Exception as e:
        print(f"Error deleting book: {str(e)}")
        return jsonify({'message': 'Failed to delete book'}), 500
    
@app.route('/edit-section/<int:section_id>', methods=['PUT'])
def edit_section(section_id):
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if not name or not description:
            return jsonify({'message': 'Missing required fields'}), 400

        section = Section.query.get(section_id)
        if not section:
            return jsonify({'message': 'Section not found'}), 404

        section.name = name
        section.description = description
        db.session.commit()

        return jsonify({'message': 'Section updated successfully'}), 200

    except Exception as e:
        print(f"Error editing section: {str(e)}")
        return jsonify({'message': 'Failed to update section'}), 500

    
    
@app.route('/delete-section/<int:section_id>', methods=['DELETE'])
def delete_section(section_id):
    try:
        section = Section.query.get(section_id)
        if not section:
            return jsonify({'message': 'Section not found'}), 404
        Book.query.filter_by(section_id=section_id).delete()
        db.session.delete(section)
        db.session.commit()

        return jsonify({'message': 'Section deleted successfully'}), 200

    except Exception as e:
        print(f"Error deleting section: {str(e)}")
        return jsonify({'message': 'Failed to delete section'}), 500

from datetime import datetime, timedelta
from flask import jsonify

# Assuming you have the BookRequest model defined

from sqlalchemy.exc import SQLAlchemyError

@app.route('/add-book-request/<int:book_id>', methods=['POST'])
@jwt_required()
def add_book_request(book_id):
    try:
        user = get_jwt_identity()
        user_id = user['id']
        # Check if book exists
        print(user_id)
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book not found'}), 404
        # Check if user already requested this book
        existing_request = BookRequest.query.filter_by(user_id=user_id, book_id=book_id).first()
        if existing_request:
            return jsonify({'message': 'Book already requested'}), 400
        
        # Create a new book request
        new_request = BookRequest(user_id=user_id, book_id=book.id)
        db.session.add(new_request)
        db.session.commit()

        return jsonify({'message': 'Book request successful'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error adding book request: {str(e)}")
        return jsonify({'message': 'Failed to add book request'}), 500

@app.route('/return-book/<int:book_id>', methods=['POST'])
# @jwt_required()
def return_book(book_id):
    try:
        # user_id = get_jwt_identity()

        issuance_date = datetime.utcnow() - timedelta(days=7)
        issued_book = BookRequest.query.filter_by(
            # user_id=user_id,
            book_id=book_id
        ).filter(
            BookRequest.request_date >= issuance_date
        ).first()

        if not issued_book:
            return jsonify({'message': 'Book cannot be returned yet'}), 400

        db.session.delete(issued_book)
        db.session.commit()

        return jsonify({'message': 'Book returned successfully'}), 200

    except Exception as e:
        print(f"Error returning book: {str(e)}")
        return jsonify({'message': 'Failed to return book'}), 500

@app.route('/admin/book-requests', methods=['GET'])
def get_book_requests():
    requests = BookRequest.query.all()
    requests_data = []

    for request in requests:
        user = User.query.get(request.user_id)
        book = Book.query.get(request.book_id)

        if user and book:
            request_data = {
                'id': request.id,
                'user_name': user.username,
                'book_name': book.name,
                'request_date': request.request_date,
                'status': request.status
            }
            requests_data.append(request_data)

    return jsonify({'requests': requests_data})

# Route to approve a book request
@app.route('/admin/approve-request/<int:request_id>', methods=['PUT'])
def approve_request(request_id):
    request = BookRequest.query.get(request_id)
    if not request:
        return jsonify({'message': 'Request not found'}), 404
    
    # Update the request status to 'accepted' (you may need to adjust this based on your data model)
    request.status = 'accepted'
    db.session.commit()

    return jsonify({'message': 'Request approved successfully'}), 200

# Route to reject a book request
@app.route('/admin/reject-request/<int:request_id>', methods=['PUT'])
def reject_request(request_id):
    request = BookRequest.query.get(request_id)
    if not request:
        return jsonify({'message': 'Request not found'}), 404
    
    # Update the request status to 'rejected' (you may need to adjust this based on your data model)
    request.status = 'rejected'
    db.session.commit()

    return jsonify({'message': 'Request rejected successfully'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True, port=5000)
