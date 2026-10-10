import pymysql
import os
from dotenv import dotenv_values
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
config = dotenv_values(PROJECT_DIR / ".env")


def get_connection():
    connection = pymysql.connect(
        host=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"]
    )

    return connection

def get_user_by_username(name):
    connection = get_connection()

    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id, username, password_hash, salt FROM users
            WHERE username = %s

            """, (name,)
        )

        result = cursor.fetchone()
        return result

    finally:
        cursor.close()
        connection.close()





    #1. Luo tietokantayhteys
    #2. Luo kursori
    #3. HAe käyttäjä parametrisoidulla SQL-kyselyllä
    #4. Palauta käyttäjän tiedot tai None, jos käyttäjää ei löydy.
    #5. Sulje kursori ja yhteys myös virhetilanteissa.
    pass