# VehiTrackDjango

This repository contains a Django project created for educational purposes.

## Getting Started

### Prerequisites

Make sure you have the following prerequisites installed on your machine:

- [Python](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/)
- [npm](https://www.npmjs.com/get-npm/)

### Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your_username/your_project_name.git
   cd your_project_name
   ```
1. **Create a Virtual Environment (Optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # (On Windows, use `venv\Scripts\activate`)
   ```
1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   npm install
   ```
1. **Create an Environment File:**
   Create a .env file in the project root and add the following variables:
   ```bash
   SECRET_KEY=your_generated_secret_key
   ```
   You can generate file with key by using following command:
   ```bash
   echo "SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" >> .env
   ```
1. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```
1. **Create a Superuser:**
   ```bash
   python manage.py createsuperuser
   ```
1. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
1. **Access the Django Admin Interface:**
   If you created a superuser, visit http://localhost:8000/admin.

### Environment Configuration
- DEBUG: Set to `True` for development, and `False` for production.
- SECRET_KEY: Replace with your Django secret key. Use the command mentioned above to generate a new key.

### Stopping the Development Server
To stop the development server, press `Ctrl+C` in the terminal.

### Scripts
- Seed data
  You can seed data using following script:
  ```bash
  python manage.py runscript scripts.seed_data
  ```
