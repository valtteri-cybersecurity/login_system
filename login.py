
from getpass import getpass
from passwords import compare_hash, create_hash
from database import get_connection


def login_username():
    username = input("Username: ")
    return username or None


def login_password():
    password = getpass("Password: ")
    return password or None


def get_credentials(username):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT salt, password_hash FROM users
            WHERE username = %s
            """,
            (username,)
        )

        result = cursor.fetchone()

        if result is None:
            return None

        salt, stored_hash = result
        return salt, stored_hash

    finally:
        cursor.close()
        connection.close()


def main():
    username = login_username()
    password = login_password()

    if not username or not password:
        print("Error: Username and password are required.")
        return

    credentials = get_credentials(username)

    if credentials is None:
        print("Login failed: Invalid username or password.")
        return

    salt, stored_hash = credentials

    new_hash = create_hash(password, salt)

    if compare_hash(stored_hash, new_hash):
        print("Login successful!")
    else:
        print("Login failed: Invalid username or password.")


if __name__ == "__main__":
    main()
