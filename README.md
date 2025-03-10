# GoogleForm API Project (Back-End)

This project is a Django-based RESTful API that replicates the basic functionality of a Google Forms-like system. It allows users to create forms, add questions of various types, and submit answers. The API is built using Django REST Framework (DRF), with Swagger and ReDoc integrated for interactive API documentation.

---

## Features
- **Form Management:** Create, retrieve, update, and delete forms.
- **Question Management:** Add questions with different types (e.g., short text, long text, number, email) to forms.
- **Validation:** Enforce validation on inputs like maximum lengths, number ranges, and required fields.
- **Answer Submission:** Submit answers for the questions in a form.
- **Interactive API Documentation:** Swagger UI and ReDoc support for easy testing.
- **Testing:** Pytest-based unit tests for API endpoints.

---
## Technologies Used
- Python 3.12
- Django 5.1.4
- Django REST Framework (DRF)
- PostgreSQL
- Docker & Docker Compose
- pytest
- Swagger UI (drf-yasg)
- ReDoc for API Documentation

---

## Installation and Setup
Follow these steps to set up the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/asriamir/GoogleForm-BackEnd-.git
cd GoogleForm
```

### 2. Set up a Virtual Environment
It's recommended to use a virtual environment for project dependencies.

```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate    # For Windows
```

### 3. Install Dependencies
Install the required Python packages from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Migrate the Database
Run the database migrations to set up the SQLite database.

```bash
python manage.py migrate
```

### 5. Create a Superuser (Optional)
Create a superuser to access the Django admin panel.

```bash
python manage.py createsuperuser
```
Follow the prompts to set the username, email, and password.

## Running the Application

### 6. Start the Development Server
Run the development server locally.

```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`.

### Using Docker
The easiest way to run the application is using Docker Compose:

1. **Build and Run Containers**:
   ```bash
   docker-compose up --build
   ```
2. The app will be available at `http://localhost:8000/`.

   - **Admin Interface**: `http://localhost:8000/admin/`
   - **Swagger UI**: `http://localhost:8000/swagger/`
   - **ReDoc**: `http://localhost:8000/redoc/`

3. Stop the application:
   ```bash
   docker-compose down
   ```

### 7. API Documentation
You can access the interactive API documentation here:

- **Swagger UI:** [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **ReDoc:** [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

---

## Endpoints

| Endpoint                        | Method | Description                       |
|---------------------------------|--------|-----------------------------------|
| `/api/forms/`                   | GET    | List all forms                   |
| `/api/forms/`                   | POST   | Create a new form                |
| `/api/forms/{id}/`              | GET    | Retrieve a form by ID            |
| `/api/forms/{id}/questions/`    | GET    | Retrieve questions for a form    |
| `/api/questions/`               | POST   | Create a question                |
| `/api/answers/`                 | POST   | Submit an answer                 |

Refer to the Swagger or ReDoc documentation for a complete list of endpoints and request formats.

---

## Running Tests
Tests are written using **pytest** and Django's test client.

### 1. Install Pytest
If not already installed:

```bash
pip install pytest pytest-django
```

### 2. Run Tests
Run the tests using the following command:

```bash
pytest -v -s
```

Pytest will execute all test cases from the `tests.py` file and display the results.

---

## Project Structure
Here is a breakdown of the project structure:

```
GoogleForm/
│
├── forms/                         # App directory
│   ├── migrations/                # Database migrations
│   ├── admin.py                   # Admin configurations
│   ├── models.py                  # Data models
│   ├── serializers.py             # DRF serializers
│   ├── views.py                   # API views
│   ├── urls.py                    # App-level URLs
│   ├── tests.py                   # API tests (pytest)
│
├── GoogleForm/                    # Project configuration
│   ├── settings.py                # Django project settings
│   ├── urls.py                    # Project-level URLs
│
├── requirements.txt               # Project dependencies
├── manage.py                      # Django management script
└── README.md                      # Project documentation
```

---

## Notes
- This project uses SQLite as the default database. For production, configure a more robust database like PostgreSQL.
- The `swagger/` and `redoc/` endpoints are helpful for testing and understanding the API quickly.

---

## License
This project is licensed under the **MIT License**.

---

## Contact
For questions or suggestions, contact:
- **Email:** asri.amir75@gmail.com
