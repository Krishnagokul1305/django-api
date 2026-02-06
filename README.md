# Liture API

A Django REST Framework API for managing users, webinars, internships, memberships, and generic feedback, with JWT authentication and PostgreSQL.

## Features

- JWT-based authentication (login, refresh)
- Custom user model with profile fields
- User CRUD with staff/superuser permissions
- Password reset flow via reset token
- PostgreSQL database support
- **Webinars**: manage events, registrations, attendance, and feedback
- **Internships**: manage postings and applications with status tracking
- **Memberships**: subscriptions, renewals, and payment metadata
- **Generic Feedback**: content-type based feedback for multiple modules
- Filtering and pagination across list endpoints
- Media uploads for webinar/internship images
- Mailgun email support via Anymail

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
   pip install django-filter
   pip install Pillow
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

## API Endpoints

All API endpoints are prefixed with `/api/v1/`

### API Structure

The API is organized into the following modules:

- **Users** (`/api/v1/users/`) - User management and profile operations
- **Authentication** (`/api/v1/auth/`) - User registration, login, and password reset
- **Webinars** (`/api/v1/webinars/`) - Webinar management and registrations
- **Internships** (`/api/v1/internships/`) - Internship management and applications
- **Memberships** (`/api/v1/memberships/`) - Membership subscriptions and registrations
- **Feedback** (`/api/v1/feedbacks/`) - Generic feedback system for all modules
- **Dashboard Stats** (`/api/v1/stats/`) - Dashboard statistics and analytics

### Dashboard Stats Routes

- `GET /api/v1/stats/dashboard/` - Get basic dashboard counts (active internships, webinars, memberships)
- `GET /api/v1/stats/past_registrations/` - Get registration statistics for past 10 days grouped by date
- `GET /api/v1/stats/recent_registrations/?limit=5` - Get recent registrations across webinars and internships (customizable limit)
- `GET /api/v1/stats/comprehensive/` - Get comprehensive statistics with detailed breakdowns

### Authentication Routes

- `POST /api/v1/auth/register/` - Register new user
- `POST /api/v1/auth/login/` - Login and obtain JWT token pair
- `POST /api/v1/auth/token/refresh/` - Refresh access token
- `POST /api/v1/auth/<id>/change-password/` - Change password
- `POST /api/v1/auth/forgot-password/` - Request password reset
- `POST /api/v1/auth/reset-password/` - Reset password with token

### User Management Routes

- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/<id>/` - Get user details
- `GET /api/v1/users/me/` - Get current user profile
- `POST /api/v1/users/` - Create user
- `PATCH /api/v1/users/<id>/` - Update user

### Webinar Routes

- `GET /api/v1/webinars/` - List all webinars
- `GET /api/v1/webinars/<id>/` - Get webinar details
- `POST /api/v1/webinars/` - Create webinar (Staff only)

### Webinar Registration Routes

- `GET /api/v1/webinars/registrations/` - List user's registrations
- `POST /api/v1/webinars/registrations/` - Register for webinar
- `GET /api/v1/webinars/registrations/<id>/` - Get registration details
- `POST /api/v1/webinars/registrations/<id>/mark_attendance/` - Mark attendance (Staff only)
- `POST /api/v1/webinars/registrations/<id>/submit_feedback/` - Submit feedback
- `PATCH /api/v1/webinars/registrations/<id>/change_status/` - Change registration status (Staff only)
- `POST /api/v1/webinars/registrations/<id>/reject/` - Reject registration (Staff only)

### Internship Routes

- `GET /api/v1/internships/` - List all internships
- `GET /api/v1/internships/<id>/` - Get internship details
- `POST /api/v1/internships/` - Create internship (Staff only)

### Internship Registration Routes

- `GET /api/v1/internships/registrations/` - List applications
- `POST /api/v1/internships/registrations/` - Apply for internship
- `GET /api/v1/internships/registrations/<id>/` - Get application details
- `PATCH /api/v1/internships/registrations/<id>/change_status/` - Change application status (Staff only)
- `GET /api/v1/internships/registrations/pending_applications/` - Get pending applications (Staff only)

### Membership Routes

- `GET /api/v1/memberships/` - List all memberships
- `GET /api/v1/memberships/<id>/` - Get membership details
- `POST /api/v1/memberships/` - Create membership (Staff only)

### Membership Registration Routes

- `GET /api/v1/memberships/registrations/` - List membership registrations
- `POST /api/v1/memberships/registrations/` - Register for membership
- `GET /api/v1/memberships/registrations/<id>/` - Get registration details
- `PATCH /api/v1/memberships/registrations/<id>/change_status/` - Change registration status (Staff only)
- `PATCH /api/v1/memberships/registrations/<id>/` - Update payment status (Staff only)

### Feedback Routes

- `GET /api/v1/feedbacks/` - List feedback
- `POST /api/v1/feedbacks/` - Submit feedback (Authenticated users)
- `GET /api/v1/feedbacks/<id>/` - Get feedback details
- `PATCH /api/v1/feedbacks/<id>/` - Update feedback (Own feedback only)
- `DELETE /api/v1/feedbacks/<id>/` - Delete feedback (Own feedback only)

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

## Registration Models

### Webinar Registration

- `status`: pending, accepted, rejected, cancelled
- `rejection_reason`: Reason for rejection/cancellation
- `attended`: Attendance status
- `attendance_marked_at`: When attendance was marked
- `rating`: User rating (1-5)
- `feedback`: User feedback text
- `feedback_given_at`: When feedback was submitted

### Internship Registration

- `status`: pending, accepted, rejected
- `rejection_reason`: Reason for rejection
- `resume`: Uploaded resume file
- `reason`: User's reason for applying
- `applied_at`: Application submission timestamp
- `status_updated_at`: When status was updated

### Membership Registration

- `status`: pending, accepted, rejected
- `rejection_reason`: Reason for rejection
- `payment_status`: pending, completed, failed, refunded
- `payment_amount`: Amount paid
- `payment_method`: Payment method used
- `transaction_id`: Payment transaction ID
- `payment_date`: When payment was made
- `reason`: User's reason for joining
- `created_at`: Creation timestamp
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
