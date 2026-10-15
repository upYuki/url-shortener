from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status
import validators
import secrets
import string
from fastapi.responses import RedirectResponse

app = FastAPI()
url_db = {}


class UrlModel(BaseModel):
    url: str


@app.get("/")
def greetings():
    return "homepage"


def generate_short_code() -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(6))


@app.post("/shorten_url", status_code=status.HTTP_201_CREATED)
def shorten_url(payload: UrlModel):
    if not validators.url(payload.url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid url")

    for key, url in url_db.items():
        if url == payload.url:
            return {"short_code": key, "short_url": f"http://127.0.0.1:8000/{key}"}

    short_code = generate_short_code()
    while short_code in url_db:
        short_code = generate_short_code()

    url_db[short_code] = payload.url
    return {"short_code": short_code, "short_url": f"http://127.0.0.1:8000/{short_code}"}


@app.get("/{short_code}")
def redirect(short_code: str):
    url = url_db.get(short_code)
    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short code not found")
    return RedirectResponse(url, status.HTTP_307_TEMPORARY_REDIRECT)
