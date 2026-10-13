# Login System

A Python, FastAPI, and MySQL learning project for account registration and password verification. It includes a browser interface, JSON API endpoints, and command-line registration and login tools.

**Work in progress.** This project demonstrates authentication fundamentals. It is not a complete authentication service or a production-ready login system.

## Features

- Register accounts through the browser, API, or command line.
- Verify credentials through the API or command line.
- Store password hashes and per-user salts rather than plaintext passwords.
- Hash passwords with PBKDF2-HMAC-SHA256 using 600,000 iterations and a 32-byte derived key.
- Generate a random 16-byte salt with Python's secrets module.
- Compare hashes with hmac.compare_digest.
- Use parameterized SQL for user lookups and inserts.
- Require usernames of at least three characters and passwords of at least twelve characters during registration.
- Enforce unique usernames through a database index.

Successful login currently returns a message only. It does not create a session, issue a token, or grant access to protected pages.

## Requirements

- Python 3 and MySQL.
- Dependencies listed in requirements.txt.
- For setup_database.py: Linux with sudo and the mysql command-line client, and a local MySQL administrative account accessible through sudo mysql.

The main libraries are FastAPI, Uvicorn, PyMySQL, and python-dotenv. Exact package versions are recorded in requirements.txt; compatibility should be checked in the target environment.

## Setup

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/valtteri-cybersecurity/login_system.git
cd login_system
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create a private .env file in the project root:

```dotenv
DB_HOST=localhost
DB_USER=login_system_app
DB_PASSWORD=replace_with_a_private_password
DB_NAME=login_system
```

Use a dedicated application account. Generate a password locally, for example:

```bash
openssl rand -hex 32
```

Replace the placeholder with that password and restrict the file's permissions:

```bash
chmod 600 .env
```

Configuration is loaded directly from this project's .env file with dotenv_values. Shell variables do not replace the explicitly loaded configuration. Restart the server after changing the file.

Create the database, application user, and users table:

```bash
python setup_database.py
```

Review the displayed database and username, then enter yes to proceed. The script invokes sudo mysql and grants SELECT, INSERT, UPDATE, and DELETE on the configured database to the application account at localhost.

The setup script does not change the password of an existing account. If that account already exists, its current password must match .env. DB_HOST is used by the application, while the setup script configures a local MySQL server. Database and username identifiers must start with an ASCII letter and contain only ASCII letters, digits, or underscores.

## Run the web application

Start on the local machine:

```bash
./.venv/bin/python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 in a browser. The interface provides login and account-registration forms. Registration checks password confirmation in the browser.

FastAPI's interactive API documentation is available at http://127.0.0.1:8000/docs.

For an isolated local-network lab:

```bash
./.venv/bin/python -m uvicorn api:app --host 0.0.0.0 --port 8000
```

Access it using the server's LAN address and port 8000. This binds to all interfaces. The application does not configure HTTPS, and credentials sent over plain HTTP are not encrypted in transit. Do not expose this development server directly to the internet or use real account passwords for lab testing.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| GET | / | Browser interface |
| POST | /register | Create an account |
| POST | /login | Verify credentials |

Both POST endpoints accept JSON with username and password fields.

Successful requests return a message. Invalid login credentials return HTTP 401 with the same generic error for an unknown username or an incorrect password. Invalid request bodies are handled by FastAPI validation.

Registration validation errors and duplicate usernames currently return a message with HTTP 200 rather than an appropriate error status. This behavior is a known limitation.

## Command-line tools

Create an account:

```bash
python create_user.py
```

Verify credentials:

```bash
python login.py
```

Command-line password input is hidden with getpass. Account creation also requests password confirmation.

## Database

The users table stores:

| Column | Purpose |
| --- | --- |
| id | Auto-incrementing user identifier |
| username | Unique username, up to 100 characters |
| password_hash | 32-byte password hash |
| salt | 16-byte random salt |
| created_at | Account creation timestamp |

## Project structure

| File or directory | Responsibility |
| --- | --- |
| api.py | FastAPI routes and request models |
| passwords.py | Salt generation, hashing, and comparison |
| database.py | Database connection and username lookup |
| create_user.py | Account creation and CLI registration |
| login.py | CLI credential verification |
| setup_database.py | Interactive local database setup |
| templates/index.html | Browser interface and JavaScript |
| static/style.css | Interface styling |
| requirements.txt | Python dependency versions |

## Known limitations and next steps

- Add sessions or tokens, logout, authorization, and protected endpoints.
- Add rate limiting and brute-force protection.
- Use appropriate HTTP status codes for registration failures.
- Add maximum input lengths and consistent username normalization.
- Improve database-error handling and configuration validation.
- Reduce timing differences between unknown users and incorrect passwords.
- Add automated tests and schema migrations.
- Review database privileges and secure deployment before broader use.
- Standardize interface wording: some current labels use Sign in for registration and one heading is in Finnish.

The setup script assembles administrative SQL using its own string escaping. That implementation depends on MySQL SQL-mode behavior and needs further review before being treated as a portable provisioning tool.

Keep .env, local logs, virtual environments, and credentials out of Git. Password hashing protects stored credentials; it does not replace HTTPS or the other controls required by a complete authentication system.
