# E-Library

**Welcome to E-Library**, a digital platform designed for book enthusiasts and knowledge seekers. E-Library allows you to explore a vast collection of books, delve into various genres, and enjoy both e-books and audiobooks. This app ensures a convenient and enjoyable reading experience with easy access to digital resources.

## Features
- **Vast Collection**: Explore a wide range of books across various genres.
- **Personalized Reading Lists**: Create custom reading lists based on your interests.
- **User Authentication**: Secure login and registration using Flask-Security.
- **Book Management**: Admin can manage books and sections with CRUD operations.
- **Search Functionality**: Efficient search bar to find books and sections.
- **Monthly Reports**: Automatic monthly reports sent using Celery.

## Technologies Used

### Backend
- **Flask**: Web framework for backend development.
- **Flask-Security**: User authentication.
- **Flask-SQLAlchemy**: Database management.
- **Flask-RESTful**: API development.
- **Flask-Caching**: Caching with Redis.
- **Flask-Mail**: Email sending.
- **Flask-CORS**: Handling cross-origin resource sharing.
- **Redis**: Caching and batch job handling.
- **Celery**: Task management.
- **Requests**: HTTP requests management.

### Frontend
- **Vue.js**: Frontend framework.
- **Bootstrap**: Responsive design.
- **Vue-router**: Smooth navigation.
- **Pinia**: State management.

## API Design
Our E-Library app's API architecture is built on Flask with blueprints for streamlined functionality. It includes multiple endpoints for various tasks:

- **Book Data API**: Handles book operations like creation, editing, and searching.
- **User Data API**: Manages user tasks such as authentication, registration, and role modification.
- **Section API**: Manages book sections for organized navigation and allows users to create and manage personalized sections.

## Database Schema Design
The database schema for the E-Library app includes the following tables:

- **User**: Contains details like username, email, and role.
- **Book**: Contains information such as name, content, author, and image.
- **Section**: Categorizes books for easier navigation.
- **BookRequest**: Tracks user requests for books.
- **Feedback**: Stores user ratings and comments about books.

## Architecture and Files
### Root Folder Contains:
- **app.py**: Controller for the app, defining routes, database models, and managing API endpoints.
- **workers.py**: Manages caching using Redis.
- **models.py**: Defines the database models.
- **resources.py**: Manages API resources.
- **readme.md**: This readme file.
- **requirements.txt**: Lists the dependencies.
- **instance folder**: Contains the SQLite database file.
- **component folder**: Contains the Vue templates.
- **static folder**: Contains images and static files.

### Detailed Files:
- **app.py**: Acts as the controller, containing routes to different pages, defining database models using SQLAlchemy and Flask-Login, and managing API endpoints. Sends monthly reports using Celery.
- **workers.py**: Manages caching using Redis.

## Installation and Setup
1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd e-library
   ```
2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up the database**:
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```
5. **Run the development server**:
   ```bash
   flask run
   ```

---

This README file provides an overview of the E-Library app, its features, technologies, database schema, architecture, and instructions for setup and contribution. It is designed to help users and collaborators understand the project's structure and functionality.
