# excel_processor
 
# Django Project Setup

Follow these steps to set up and run the Django project.

## Prerequisites
- Python installed (>= 3.8 recommended)
- PostgreSQL installed and running
- Virtual environment setup

## Setup Steps

### 1. Create and Activate Virtual Environment
```sh
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Create PostgreSQL Database
- Open PostgreSQL and create a new database:

### 4. Configure Database in Django
Update the `DATABASES` settings in `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Run Migrations
```sh
python manage.py migrate
```

### 6. Run the Server
```sh
python manage.py runserver
```

### 7. Access the Project
Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## API Testing with Postman

I have provided a **Postman collection** to help you test the API easily.

### Steps to Import Postman Collection:
1. Download [Postman](https://www.postman.com/downloads/).
2. Open Postman and go to **File → Import**.
3. Select the file: `postman/postman_collection.json`.
4. The API endpoints will be available in your **Collections** tab.

## Sample Input File
For testing, I have added a sample input file in the project directory. You can use this file to test the API functionality.

You can now test the API directly in Postman!

## Additional Commands
- Create a superuser:
```sh
python manage.py createsuperuser
```
- Collect static files:
```sh
python manage.py collectstatic
```
- Run Django shell:
```sh
python manage.py shell
```

