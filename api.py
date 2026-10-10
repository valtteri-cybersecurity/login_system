from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def home():
    return {"message": "API is running..."}

@app.post("/login")
def login(data: LoginRequest):
    #1. Hae käyttäjä tietokannasta käyttäjätunnuksella
    #2. Tarkista löytyikö käyttäjä
    #3. Tarkista salasana salasanatiivistettä vasten
    #4. Palauta kirjautumisen tulos
    pass


