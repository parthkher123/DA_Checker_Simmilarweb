# Domain DA/PA Checker & SimilarWeb Traffic API

A FastAPI-based service to check Domain Authority (DA), Page Authority (PA), and SimilarWeb traffic data for domains, with results cached in MySQL database.

## Features
- Check DA/PA for multiple domains using the Moz RapidAPI service
- Fetch SimilarWeb traffic data for domains
- Caches results in MySQL database to avoid redundant API calls
- Refresh endpoints to force update cached data from API
- Manual update endpoint for custom data modifications
- Credentials and configuration managed via `.env` file

## Setup

### 1. Clone the repository and install dependencies
```bash
pip install -r requirements.txt
```

Or using Make:
```bash
make install
```

### 2. Configure environment variables
Create a `.env` file in the project root:

```env
# Moz DA/PA API Configuration
RAPIDAPI_KEY=your_rapidapi_key
RAPIDAPI_HOST=moz-da-pa1.p.rapidapi.com
SIMILARWEB_API_HOST=similarweb-traffic.p.rapidapi.com

# MySQL Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=da_padata
```

> **Replace the credentials above with your own values. Never commit real credentials to public repositories.**

#### Example for Remote MySQL:
```env
DB_HOST=sql12.freesqldatabase.com
DB_PORT=3306
DB_USER=sql12807072
DB_PASSWORD=czWvibrE9c
DB_NAME=sql12807072
```

### 3. Ensure MySQL database exists
Make sure the database specified in `DB_NAME` exists in your MySQL server:
```sql
CREATE DATABASE da_padata;
```

### 4. Run the API

Using Make (recommended):
```bash
make run
```

Or directly with uvicorn:
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **Base URL:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

### 1. Check DA/PA (with cache)
**`POST /check_domains`**

Checks Domain Authority and Page Authority. Returns cached data if available.

**Request:**
```json
{
  "urls": ["https://example.com", "https://google.com"]
}
```

**Response:**
```json
{
  "count": 2,
  "results": [
    {"url": "https://example.com", "da": 78.5, "pa": 82.3, "cached": false},
    {"url": "https://google.com", "da": 96.2, "pa": 98.1, "cached": true}
  ]
}
```

---

### 2. Refresh DA/PA (force API fetch)
**`POST /check_domains/refresh`**

Forces fresh data fetch from Moz API and updates database, ignoring cache.

**Request:**
```json
{
  "urls": ["https://example.com", "https://google.com"]
}
```

**Response:**
```json
{
  "count": 2,
  "results": [
    {
      "url": "https://example.com",
      "da": 78.5,
      "pa": 82.3,
      "refreshed": true,
      "cached": false,
      "message": "Data fetched from API and updated in database"
    }
  ]
}
```

---

### 3. Check SimilarWeb Traffic (with cache)
**`POST /similarweb`**

Fetches SimilarWeb traffic data. Returns cached data if available.

**Request:**
```json
{
  "domains": ["x.com", "facebook.com"]
}
```

**Response:**
```json
{
  "count": 2,
  "results": [
    {
      "domain": "x.com",
      "data": {
        "visits": 2500000,
        "pageviews": 12000000,
        "bounce_rate": 45.5
      },
      "cached": false
    },
    {
      "domain": "facebook.com",
      "data": { ... },
      "cached": true,
      "cached_at": "2025-11-14T10:30:00"
    }
  ]
}
```

---

### 4. Refresh SimilarWeb Traffic (force API fetch)
**`POST /similarweb/refresh`**

Forces fresh data fetch from SimilarWeb API and updates database.

**Request:**
```json
{
  "domains": ["x.com", "facebook.com"]
}
```

**Response:**
```json
{
  "count": 2,
  "results": [
    {
      "domain": "x.com",
      "data": { ... },
      "refreshed": true,
      "message": "Data fetched from API and updated in database"
    }
  ]
}
```

---

### 5. Update SimilarWeb Data (manual)
**`PUT /similarweb`**

Manually update SimilarWeb data in database with custom values.

**Request:**
```json
{
  "domain": "example.com",
  "data": {
    "visits": 1000000,
    "custom_field": "any value",
    "notes": "Manual update"
  }
}
```

**Response:**
```json
{
  "domain": "example.com",
  "message": "Data updated successfully",
  "data": { ... }
}
```

---

## Docker Deployment

### 1. Build the Docker image
```bash
docker build -t da-pa-checker .
```

### 2. Run the Docker container
```bash
docker run --env-file .env -p 8000:8000 da-pa-checker
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Database Schema

### `domain_stats` table
Stores DA/PA data from Moz API.

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Auto-increment primary key |
| url | VARCHAR(255) | Domain URL (unique) |
| da | FLOAT | Domain Authority |
| pa | FLOAT | Page Authority |
| created_at | VARCHAR(255) | Timestamp |

### `similarweb_stats` table
Stores SimilarWeb traffic data as JSON.

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Auto-increment primary key |
| domain | VARCHAR(255) | Domain name (unique) |
| data | TEXT | JSON traffic data |
| created_at | VARCHAR(255) | Timestamp |

---

## Makefile Commands

```bash
make help      # Show available commands
make env       # Create Python virtual environment
make install   # Install dependencies
make run       # Run the FastAPI app
make clean     # Remove virtual environment
```

---

## Notes
- The first request for a domain fetches from the API and caches the result
- Subsequent requests return cached data (use `/refresh` endpoints to update)
- MySQL database is required - SQLite is no longer supported
- All JSON data is stored as TEXT in MySQL for compatibility
- Make sure your MySQL server is running and accessible

## License
MIT

# DA_Checker_Simmilarweb
