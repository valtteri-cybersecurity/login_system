from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_user_by_username
from passwords import create_hash, compare_hash
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from create_user import create_user
from pymysql.err import IntegrityError

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

@app.get("/", response_class=FileResponse)
def home():
    return BASE_DIR / "templates" / "index.html"

@app.post("/login")
def login(data: LoginRequest):
    user = get_user_by_username(data.username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    user_id, username, stored_hash, salt = user
    new_hash = create_hash(data.password, salt)

    if compare_hash(stored_hash, new_hash):
        return {"message": "Login successful!"}

    raise HTTPException(
        status_code=401,
        detail="Invalid username or password"
    )


@app.post("/register")
def register(data: RegisterRequest):
    try:
        create_user(data.username.strip(), data.password)
        return {"message": "Registration successful!"}

    except ValueError as error:
        return {"message": str(error)}

    except IntegrityError:
        return {"message": "Username is already taken."}
