# LMS Platform

A Learning Management System built with Django and Channels for real-time features.

## Overview

This is a full-featured LMS platform that supports:
- User registration and authentication
- Course browsing and enrollment
- Real-time chat functionality using WebSockets (Channels)
- AI-powered chat assistant
- User achievements system

## Tech Stack

- **Backend**: Django 5.x with Django Channels (Daphne ASGI server)
- **Database**: PostgreSQL (via DATABASE_URL)
- **WebSockets**: Django Channels with in-memory channel layer
- **Frontend**: Django templates with CSS
- **AI Integration**: OpenAI API

## Project Structure

```
.
├── Lms_project/        # Main Django project settings
├── lms/                # Core LMS app (courses, users, achievements)
├── accounts/           # User authentication and profiles
├── chat/               # Real-time chat with AI bot
├── static/             # Static CSS files
├── staticfiles/        # Collected static files for production
└── manage.py           # Django management script
```

## Running the Application

The application runs on port 5000 using Daphne (ASGI server) to support WebSocket connections.

Development: `python manage.py runserver 0.0.0.0:5000`
Production: `daphne -b 0.0.0.0 -p 5000 Lms_project.asgi:application`

## Database

The application uses PostgreSQL via the DATABASE_URL environment variable. Migrations are managed via Django's ORM.

## Admin User

- Username: admin
- Password: admin123

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (auto-configured by Replit)
- `DJANGO_SECRET_KEY`: Django secret key (has default for development)
- `DJANGO_DEBUG`: Debug mode (default: True)

## Recent Changes

- 2025-12-30: Initial import and Replit environment setup
  - Configured for Replit PostgreSQL database
  - Updated ALLOWED_HOSTS and CSRF settings for Replit proxy
  - Installed all Python dependencies
  - Created admin superuser
  - Loaded sample course data
