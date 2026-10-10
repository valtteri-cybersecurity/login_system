import os
import subprocess
from pathlib import Path

from dotenv import dotenv_values


# Load configuration only from this project's .env file.
PROJECT_DIR = Path(__file__).resolve().parent
ENV_FILE = PROJECT_DIR / ".env"

config = dotenv_values(ENV_FILE)

DB_NAME = config.get("DB_NAME", "login_system")
DB_USER = config.get("DB_USER", "login_system_app")
DB_PASSWORD = config.get("DB_PASSWORD", "")


def validate_identifier(value):
    """Allow only ASCII letters, digits and underscores."""
    allowed = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789_"
    )

    if not value or value[0] not in (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ):
        raise ValueError("Invalid database identifier")

    if any(char not in allowed for char in value):
        raise ValueError("Invalid database identifier")


def sql_string(value):
    """Escape a value for a MySQL string literal."""
    value = value.replace("\\", "\\\\")
    value = value.replace("'", "\\'")
    return f"'{value}'"


validate_identifier(DB_NAME)
validate_identifier(DB_USER)

if not DB_PASSWORD:
    raise SystemExit(
        "DB_PASSWORD is empty. Set the application password in .env first."
    )

database_identifier = f"`{DB_NAME}`"
user_literal = sql_string(DB_USER)
password_literal = sql_string(DB_PASSWORD)

sql = f"""
CREATE DATABASE IF NOT EXISTS {database_identifier}
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS {user_literal}@'localhost'
    IDENTIFIED BY {password_literal};

GRANT SELECT, INSERT, UPDATE, DELETE
    ON {database_identifier}.*
    TO {user_literal}@'localhost';

USE {database_identifier};

CREATE TABLE IF NOT EXISTS users (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    password_hash VARBINARY(32) NOT NULL,
    salt VARBINARY(16) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_username (username)
);
"""

print(f"Configuration loaded from: {ENV_FILE}")
print(f"Target database: {DB_NAME}")
print(f"Application user: {DB_USER}")

confirmation = input(
    "Create database/user and users table with these settings? (yes/no): "
)

if confirmation != "yes":
    raise SystemExit("Setup cancelled.")

try:
    result = subprocess.run(
        ["sudo", "mysql"],
        input=sql,
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
except subprocess.TimeoutExpired:
    raise SystemExit("MySQL setup timed out.")

if result.returncode != 0:
    print("MySQL setup failed.")
    if result.stderr:
        print(result.stderr)
    raise SystemExit(result.returncode)

print("Database setup completed successfully.")
print(f"Database: {DB_NAME}")
print(f"Application user: {DB_USER}")
print("Table created or already exists: users")
