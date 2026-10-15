# URL Shortener

A lightweight URL shortening API built with FastAPI and Pydantic. It accepts a long URL, generates a unique 6-character code, and redirects visitors from the short link to the original destination.

## Features

- **URL Shortening**: Generates 6-character base62 codes using Python's `secrets` module, giving roughly 56.8 billion possible codes.
- **Redirects**: Resolves short codes and responds with an HTTP 307 redirect to the original URL. Unknown codes return a 404.
- **Validation**: Request bodies are validated with Pydantic, and URL format is checked with the `validators` library. Invalid URLs return a 400.
- **Duplicate Handling**: Submitting a URL that has already been shortened returns the existing code instead of creating a new one.
- **Collision Handling**: A newly generated code is regenerated until it does not match an existing one.
- **Interactive Documentation**: Swagger UI and ReDoc are generated automatically by FastAPI.

## Project Structure

```text
url-shortener/
│
├── main.py             # Application entry point, routes, and code generation
├── requirements.txt    # Python package dependencies
├── .gitignore          # Files excluded from version control
└── README.md           # Project documentation
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/upYuki/url-shortener.git
cd url-shortener
```

### 2. Set up a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

## API Documentation

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

| Method | Endpoint        | Description                   |
| :----- | :-------------- | :---------------------------- |
| GET    | `/`             | Homepage                      |
| POST   | `/shorten_url`  | Create a short code for a URL |
| GET    | `/{short_code}` | Redirect to the original URL  |

## Example

### Shorten a URL (`POST /shorten_url`)

Request:

```json
{
  "url": "https://github.com"
}
```

Response (`201 Created`):

```json
{
  "short_code": "aB3xZ9",
  "short_url": "http://127.0.0.1:8000/aB3xZ9"
}
```

Opening `http://127.0.0.1:8000/aB3xZ9` in a browser redirects to `https://github.com`.

## Known Limitations

This is a first version. The following are known and planned:

- **In-memory storage**: Links are stored in a Python dictionary and are lost when the server restarts. Persistent storage (SQLite) is planned.
- **Hardcoded base URL**: Short links are built with `http://127.0.0.1:8000`, so the base URL needs to be configurable before deployment.
- **No URL normalization**: `https://example.com` and `https://example.com/` are stored as separate entries.
- **No self-reference check**: A URL pointing at the shortener's own domain is accepted.
- **No click analytics or link expiry**: Planned for a later version.
