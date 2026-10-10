import pymysql
import os

def get_connection():
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    pass

def get_user_by_username(username):
    #1. Luo tietokantayhteys
    #2. Luo kursori
    #3. HAe käyttäjä parametrisoidulla SQL-kyselyllä
    #4. Palauta käyttäjän tiedot tai None, jos käyttäjää ei löydy.
    #5. Sulje kursori ja yhteys myös virhetilanteissa.
    pass