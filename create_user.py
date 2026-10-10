
from passwords import create_salt, create_hash
from database import get_connection


def create_user(username, password):
    if len(username) < 3:
        raise ValueError("The username must be at least 3 characters long.")

    if len(password) < 12:
        raise ValueError("The password must be at least 12 characters long.")

    salt = create_salt()
    password_hash = create_hash(password, salt)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, salt)
            VALUES (%s, %s, %s)
            """,
            (username, password_hash, salt)
        )
        connection.commit()

    finally:
        cursor.close()
        connection.close()


def create_username():
    while True:
        username = input("Choose a username: ").strip()

        if len(username) < 3:
            print("The username must be at least 3 characters long.")
            continue

        return username


def create_password():
    while True:
        from getpass import getpass

        password = getpass("1. Choose a password: ")

        if len(password) < 12:
            print("Error: The password must be at least 12 characters long.")
            continue

        repeat_password = getpass("2. Confirm your password: ")

        if password == repeat_password:
            return password

        print("Error: The passwords do not match. Please try again.")


if __name__ == "__main__":
    username = create_username()
    password = create_password()

    try:
        create_user(username, password)
        print("User account created successfully!")
    except ValueError as error:
        print(f"Error: {error}")
