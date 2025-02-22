# Event Management API

This is a Flask-based API for managing events, user authentication, profiles, and event recommendations. It uses MongoDB as the database and includes features like JWT authentication, email verification, rate limiting, and QR code generation for event invitations.

---

## Table of Contents
1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Setup and Installation](#setup-and-installation)
4. [API Endpoints](#api-endpoints)
5. [Environment Variables](#environment-variables)
6. [Running the Application](#running-the-application)
7. [Contributing](#contributing)
8. [License](#license)

---

## Features
- **User Authentication**: Register, login, and email verification with OTP.
- **Event Management**: Create, update, and list events.
- **Profile Management**: Update user profiles.
- **Event Recommendations**: Get personalized event recommendations.
- **Event Joining**: Join events and generate QR codes for invitations.
- **Rate Limiting**: Prevent abuse with rate limiting.
- **Email Notifications**: Send emails for OTP and event invitations.

---

## Technologies Used
- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: Bcrypt
- **Email**: Flask-Mail
- **Rate Limiting**: Flask-Limiter
- **File Storage**: GridFS (for large files)
- **Environment Management**: `python-dotenv`
- **CORS**: Flask-CORS

---

## Setup and Installation

### Prerequisites
- Python 3.x
- MongoDB (running locally or remotely)
- SMTP server (e.g., Gmail for sending emails)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/event-management-api.git
   cd event-management-api