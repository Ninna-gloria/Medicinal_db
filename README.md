# Traditional Medicinal Plant Database

## Overview

This project is a web application designed to serve as a database for traditional medicinal plants. It allows users to view, add, and search for plants, as well as manage their accounts securely.

## Features

- User authentication and authorization
- Secure session management
- Input validation and sanitization
- CSRF protection
- Password hashing and security
- Logging and monitoring of user actions
- PostgreSQL database integration

## Project Structure

```
traditional-medicinal-plant-db
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── auth.py
│   ├── utils.py
│   ├── templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── plant_list.html
│   │   └── plant_detail.html
│   └── static
│       ├── css
│       │   └── styles.css
│       └── js
│           └── scripts.js
├── migrations
│   └── README.md
├── requirements.txt
├── config.py
├── run.py
├── README.md
└── .env
```

## Database Structure

- **Users Table**:
  - `id` (primary key)
  - `username`
  - `password_hash`
  - `email`
  - `created_at`
- **Plants Table**:
  - `id` (primary key)
  - `name`
  - `description`
  - `location`
  - `created_at`
- **Uses Table**:
  - `id` (primary key)
  - `plant_id` (foreign key)
  - `use_description`
  - `created_at`
- **AuthLogs Table**:
  - `id` (primary key)
  - `user_id` (foreign key)
  - `action`
  - `timestamp`

## Setup Instructions

1. Clone the repository:

   ```
   git clone <repository-url>
   cd medicinal_db
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Set up the database:

   - Update the `.env` file with your database credentials.
   - Run migrations to create the database tables.

5. Run the application:
   ```
   python run.py
   ```

## Usage

- Navigate to `http://localhost:5000` in your web browser to access the application.
- Users can register, log in, and manage their profiles.
- Explore the database of traditional medicinal plants and their uses.

## Security Practices

This application incorporates various security practices to protect user data and ensure secure interactions, including:

- Password hashing using a secure algorithm.
- CSRF protection for forms.
- Input validation and sanitization to prevent injection attacks.
- Logging user actions for monitoring and auditing.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.
