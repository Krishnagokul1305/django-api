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

### Authentication Endpoints

#### Register User

```
POST /api/v1/auth/register/
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "role": "USER"
}
```

#### Login (Obtain JWT Token Pair)

```
POST /api/v1/auth/login/
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}

Response:
{
  "access": "access_token_here",
  "refresh": "refresh_token_here"
}
```

#### Refresh Access Token

```
POST /api/v1/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "refresh_token_here"
}
```

#### Change Password

```
POST /api/v1/auth/<id>/change-password/
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
POST /api/v1/auth/forgot-password/
Content-Type: application/json

{
  "email": "user@example.com"
}
```

#### Reset Password

```
POST /api/v1/auth/reset-password/
Content-Type: application/json

{
  "token": "reset-token",
  "new_password": "newpassword123",
  "confirm_new_password": "newpassword123"
}
```

### User Management Endpoints

#### List All Users

```
GET /api/v1/users/
Authorization: Bearer <access_token>
```

#### Get User Details

```
GET /api/v1/users/<id>/
Authorization: Bearer <access_token>
```

#### Get Current User Profile

```
GET /api/v1/users/me/
Authorization: Bearer <access_token>
```

#### Create User

```
POST /api/v1/users/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "role": "USER"
}
```

#### Update User

```
PATCH /api/v1/users/<id>/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Updated Name"
}
```

## Webinar Endpoints

#### List All Webinars

```
GET /api/v1/webinars/
```

#### Get Webinar Details

```
GET /api/v1/webinars/<id>/
```

#### Create Webinar (Staff Only)

```
POST /api/v1/webinars/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Advanced Django",
  "description": "Learn advanced Django concepts",
  "image": <image_file>,
  "event_date": "2026-03-15T10:00:00Z",
  "is_active": true
}
```

## Webinar Registration Endpoints

#### List User's Webinar Registrations

```
GET /api/v1/webinars/registrations/
Authorization: Bearer <access_token>
```

#### Register for a Webinar

```
POST /api/v1/webinars/registrations/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "webinar_id": 1
}
```

#### Get Webinar Registration Details

```
GET /api/v1/webinars/registrations/<id>/
Authorization: Bearer <access_token>
```

#### Mark Attendance (Staff Only)

```
POST /api/v1/webinars/registrations/<id>/mark_attendance/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "attended": true
}
```

#### Submit Feedback (Users - One Time Only)

```
POST /api/v1/webinars/registrations/<id>/submit_feedback/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "rating": 5,
  "feedback": "Great webinar, very informative!"
}
```

#### Change Registration Status (Staff Only)

```
PATCH /api/v1/webinars/registrations/<id>/change_status/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "accepted",
  "notes": "Approved"
}

// For rejection (rejection_reason is required)
{
  "status": "rejected",
  "rejection_reason": "Does not meet eligibility criteria",
  "notes": "Optional notes"
}
```

Valid statuses: `accepted`, `rejected`, `cancelled`, `pending`

#### Reject Registration (Staff Only - Alternative)

```
POST /api/v1/webinars/registrations/<id>/reject/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "rejection_reason": "User cancelled"
}
```

## Internship Endpoints

#### List All Internships

```
GET /api/v1/internships/
```

#### Get Internship Details

```
GET /api/v1/internships/<id>/
```

#### Create Internship (Staff Only)

```
POST /api/v1/internships/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Backend Developer Internship",
  "description": "Join our backend team",
  "image": <image_file>,
  "is_active": true
}
```

## Internship Registration Endpoints

#### List Internship Applications

```
GET /api/v1/internships/registrations/
Authorization: Bearer <access_token>
```

#### Apply for Internship

```
POST /api/v1/internships/registrations/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "internship_id": 1,
  "resume_link": "https://link-to-resume.com"
}
```

#### Get Application Details

```
GET /api/v1/internships/registrations/<id>/
Authorization: Bearer <access_token>
```

#### Update Application Status (Staff Only)

```
PATCH /api/v1/internships/registrations/<id>/update_status/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "accepted"
}

// For rejection
{
  "status": "rejected",
  "rejection_reason": "Not meeting requirements"
}
```

#### Get Pending Applications (Staff Only)

```
GET /api/v1/internships/registrations/pending_applications/
Authorization: Bearer <access_token>
```

Application statuses: `pending`, `accepted`, `rejected`

## Membership Registration Endpoints

## Membership Endpoints

#### List All Memberships

```
GET /api/v1/memberships/
```

#### Get Membership Details

```
GET /api/v1/memberships/<id>/
```

#### Create Membership (Staff Only)

```
POST /api/v1/memberships/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Premium Membership",
  "description": "Access to premium features",
  "price": 99.99,
  "duration_days": 30,
  "is_active": true
}
```

## Membership Registration Endpoints

#### List Membership Registrations

```
GET /api/v1/memberships/registrations/
Authorization: Bearer <access_token>
```

#### Register for Membership

```
POST /api/v1/memberships/registrations/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "membership_id": 1,
  "expiry_date": "2026-05-03T00:00:00Z"
}
```

#### Get Membership Registration Details

```
GET /api/v1/memberships/registrations/<id>/
Authorization: Bearer <access_token>
```

#### Update Payment Status (Staff Only)

```
PATCH /api/v1/memberships/registrations/<id>/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "payment_status": "completed",
  "payment_amount": "99.99",
  "payment_method": "credit_card",
  "transaction_id": "txn_12345"
}
```

#### Renew Membership (Staff Only)

```
POST /api/v1/memberships/registrations/<id>/renew/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "duration_days": 30
}
```

Payment statuses: `pending`, `completed`, `failed`, `refunded`

## Feedback Endpoints

Generic feedback system for webinars, internships, memberships, and other entities.

#### List Feedback

```
GET /api/v1/feedbacks/
```

Query parameters:

- `feedback_type`: Filter by type (webinar, internship, membership, event, general)
- `rating`: Filter by rating (1-5)
- `user`: Filter by user ID

#### Submit Feedback (Authenticated Users - One Time Per Object)

```
POST /api/v1/feedbacks/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "content_type": 27,
  "object_id": 1,
  "feedback_type": "webinar",
  "rating": 5,
  "title": "Excellent Webinar",
  "comment": "Very informative and well-structured. Highly recommended!"
}
```

**Notes:**

- `content_type`: Django ContentType ID (27 for Webinar, etc.)
- `object_id`: ID of the object being reviewed
- `rating`: Required, must be 1-5
- `title`: Optional
- `comment`: Required feedback text
- Users can only submit one feedback per object

#### Get Feedback Details

```
GET /api/v1/feedbacks/<id>/
```

#### Update Feedback (Own Feedback Only)

```
PATCH /api/v1/feedbacks/<id>/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "rating": 4,
  "comment": "Updated feedback"
}
```

#### Delete Feedback (Own Feedback Only)

```
DELETE /api/v1/feedbacks/<id>/
Authorization: Bearer <access_token>
```

**Feedback Submission Example (Webinar):**

```
POST /api/v1/feedbacks/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "content_type": 27,
  "object_id": 1,
  "feedback_type": "webinar",
  "rating": 5,
  "title": "Great Learning Experience",
  "comment": "The presenter was very knowledgeable and the content was easy to follow."
}
```

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

### Webinar Registration Model

- `id`: Unique identifier
- `webinar_id`: Foreign key to Webinar
- `user_id`: Foreign key to User
- `registered_at`: Registration timestamp
- `attended`: Boolean (attendance status)
- `attendance_marked_at`: When attendance was marked
- `rating`: User rating (1-5 stars)
- `feedback`: User feedback text
- `feedback_given_at`: When feedback was submitted
- `rejection_reason`: Reason for cancellation/rejection
- `notes`: Admin notes

### Internship Registration Model

- `id`: Unique identifier
- `internship_id`: Foreign key to Internship
- `user_id`: Foreign key to User
- `education_level`: Current degree level
- `current_institution`: Educational institution
- `major_or_field`: Field of study
- `resume_link`: URL to hosted resume
- `portfolio_link`: URL to portfolio/GitHub
- `skill_tags`: Array of skills (JSON)
- `status`: Application status (pending, reviewing, shortlisted, interviewing, accepted, rejected, withdrawn)
- `applied_at`: Application submission timestamp
- `cover_letter`: Cover letter text
- `expected_start_date`: Intended start date
- `available_hours_per_week`: Availability
- `interviewer_notes`: Admin feedback notes
- `rejection_reason`: Reason for rejection

### Membership Registration Model

- `id`: Unique identifier
- `membership_id`: Foreign key to Membership
- `user_id`: Foreign key to User
- `start_date`: Membership start date
- `expiry_date`: Membership expiration date
- `is_active`: Active status
- `renewal_count`: Number of renewals
- `payment_status`: Payment status (pending, completed, failed, refunded)
- `payment_amount`: Amount paid
- `payment_method`: Payment method used
- `transaction_id`: Payment transaction ID
- `payment_date`: When payment was made
- `notes`: Admin notes

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
