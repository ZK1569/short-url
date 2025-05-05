# URL Shortener API (v1)

> Language: Python 3.12 • Framework: FastAPI • Database: PostgreSQL • ORM: SQLAlchemy
Objective: Expose a REST service that shortens URLs, handles redirection, and counts clicks.

--- 

## Fonctionnalités
| Action         | Route                   | Description                                                       |
| -------------- | ------------------------| ----------------------------------------------------------------- |
| **Shorten**    | `POST /v1/url/`         | Generate a unique short URL for a given `long_url`.               |
| **Redirect**   | `GET  /v1/url/{short}`  | Redirect to the original long URL and increment click count.      |
| **Analytics**  | `GET  /v1/admin/urls`   | Retrieve all URLs sorted by click count (descending).             |

--- 

## Architecture
```
FastAPI  ─┐
          ├── src/
          │   ├── controllers/
          │   │    └── url.py
          │   ├── errors/
          │   │    └── error.py
          │   ├── services/
          │   │    └── url.py         (business logic)
          │   │    └── service.py     (abstract class)
          │   ├── repositories/
          │   │    └── url.py         (data access)
          │   │    └── repository.py  (abstract class)
          │   ├── models/
          │   │    └── url.py        (SQLAlchemy models)
          │   └── utils/
          │        └── database/
          │             └── postgres.py
          └── main.py              (bootstrap & routing)
```

Each layer (controller → service → repository) is injected via FastAPI Depends, improving testability and decoupling.

--- 

## Installation & Local Run
```
# 1. Clone the repository
git clone https://github.com/ZK1569/short-url.git
cd short-url

# 2. Create and activate a virtual environment
python -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment variables
mv .env.example .env

# 5. Run PostgreSQL (via Docker)
docker run -d \
  --name short_url_postgres_database \
  -p 5432:5432 \
  -e POSTGRES_USER="postgres" \
  -e POSTGRES_PASSWORD="password" \
  -e POSTGRES_DB="short-url" \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:12.20-alpine

# 6. Start the application
python main.py
```
> Note: Ensure DB_HOST=localhost is set in .env if needed.

--- 

## Run with Docker Compose
```
# 1. Clone the repository
git clone https://github.com/ZK1569/short-url.git
cd short-url

# 2. Copy environment variables
mv .env.example .env

# 3. Launch services
docker compose up --build -d
```

## API Endpoints

| Method | Route             | Body / Params                           | Success Response                                                            |
| ------ | ----------------- | --------------------------------------- | ----------------------------------------------------------------------------|
| POST   | `/v1/url/`        | `{ "long_url": "https://example.com" }` | `201 Created` → `{ "shortened_url": "<PREFIX><hash>" }` <br> `409 conflict` |
| GET    | `/v1/url/{short}` | —                                       | `307 Temporary Redirect` to the long URL  <br> `404 Not Found`              |
| GET    | `/v1/health/`     | —                                       | `{ "status": "OK", "env": "development", "version": "0.0.1" }`              |
| GET    | `/v1/admin/`      | —                                       | `200 OK` → list of URLs ordered by click count                              |

The list of interactive API docs is available at `https://localhost:8080/docs`.

**Error codes**:
- `409 Conflict` → URL already shortened
- `404 Not Found` → short code not found

--- 

## Future Improvements

* **Caching with Redis**

  * *TTL (Time To Live)*: store entries with a fixed lifespan, automatically expiring stale data.
  * *LRU (Least Recently Used)*: evict the least recently accessed items when capacity is reached, keeping popular URLs in memory without manual management.
* **Admin Route Authentication**
  Implement JWT or OAuth2-based authentication to secure the `/v1/admin` endpoint. Currently open for speed in development.

---

## Additional Information

* **Why use HTTP 307 instead of 301 or 308?**
  A `307 Temporary Redirect` indicates the redirect is temporary and should not be cached permanently. Using a `301 || 308` can cause browsers to cache the redirect, skewing click metrics.

* **Hexagonal Architecture**
  The application follows a hexagonal (ports & adapters) architecture: the core domain (services, models) is isolated from external layers (HTTP controllers, persistence) via interfaces (ports), enhancing modularity, testability, and maintainability.

