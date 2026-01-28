# CRUD API with Authentication

A Django REST Framework API with JWT-based authentication and user management system.

## Features

- JWT Token-based Authentication
- User CRUD Operations
- Role-based Access Control (USER, ADMIN, SUPERADMIN)
- Password Reset Functionality
- User Profile Management
- PostgreSQL Database Support

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Krishnagokul1305/django-api.git

   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**

   Create a `.env` file in the root directory with the following variables:

   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgres://username:password@localhost:5432/dbname
   ALLOWED_HOSTS=localhost,127.0.0.1
   CORS_ORIGIN_ALLOWED_ALL=True
   TIME_ZONE=UTC
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Run migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## User API Endpoints

### Authentication

- `POST /api/token/` - Obtain JWT token pair (access & refresh)
- `POST /api/token/refresh/` - Refresh access token

### User Management

#### List All Users (SUPERADMIN only)

```
GET /users/
Authorization: Bearer <access_token>
```

#### Create User (SUPERADMIN only)

```
POST /users/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "role": "USER"
}
```

#### Get User Details (Owner only)

```
GET /users/<id>/
Authorization: Bearer <access_token>
```

#### Update User (Owner only)

```
PATCH /users/<id>/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Updated Name"
}
```

#### Delete User (Owner only)

```
DELETE /users/<id>/
Authorization: Bearer <access_token>
```

#### Get Current User Profile

```
GET /users/me/
Authorization: Bearer <access_token>
```

#### Change Password

```
POST /users/<id>/change-password/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "old_password": "currentpassword",
  "new_password": "newpassword123",
  "confirm_new_password": "newpassword123"
}
```

#### Forgot Password

```
POST /users/forgot-password/
Content-Type: application/json

{
  "email": "user@example.com"
}
```

#### Reset Password

```
POST /users/reset-password/
Content-Type: application/json

{
  "token": "reset-token",
  "new_password": "newpassword123",
  "confirm_new_password": "newpassword123"
}
```

## User Roles

- **USER**: Basic user with limited permissions
- **ADMIN**: Administrative user with elevated permissions
- **SUPERADMIN**: Full system access

## User Model Fields

- `id`: Unique identifier
- `name`: User's full name
- `email`: User's email (used for authentication)
- `role`: User role (USER, ADMIN, SUPERADMIN)
- `is_active`: Account status
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

## Permissions

- **IsSuperAdmin**: Only SUPERADMIN users can access
- **IsOwner**: Only the resource owner can access

## Technologies Used

- Django 4.2.27
- Django REST Framework 3.15.2
- djangorestframework-simplejwt 5.3.1
- PostgreSQL (psycopg2 2.9.10)
- django-cors-headers 4.4.0
- python-dotenv 1.0.1

## Database

This project uses PostgreSQL as the database. Make sure PostgreSQL is installed and running on your system before starting the application.

## Development

To activate the virtual environment:

```bash
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

To deactivate:

```bash
deactivate
```

## License

This project is open source and available under the MIT License.
