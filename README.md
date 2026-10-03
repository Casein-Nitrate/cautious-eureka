# Division 1 - Session Service

Backend service for PS 26241 AI-Enabled Career Counselling Platform. This service manages counselling session lifecycle, concern tracking, evidence history, and counsellor case queue functionality.

## Technology Stack

- **Python 3.10+**
- **FastAPI** - Modern async web framework
- **SQLAlchemy (async)** - ORM with async support
- **aiosqlite** - Async SQLite driver
- **Pydantic v2** - Data validation
- **SQLite with WAL mode** - Database with concurrent access

## Features

- Session creation with family context
- Hierarchical concern state calculation
- Evidence history tracking
- Counsellor case queue with filtering
- Async database operations
- CASCADE DELETE relationships
- Session ID generation ('S' + 8 alphanumeric)

## Project Structure

```
division-1-session-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database engine and session management
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API route handlers
│   └── services/            # Business logic
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variable template
└── README.md               # This file
```

## Setup Instructions

### 1. Clone or Navigate to Project Directory

```bash
cd division-1-session-service
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env if needed (defaults are usually fine for development)
```

**Environment Variables:**
- `DATABASE_URL`: SQLite database path (default: `sqlite+aiosqlite:///./session_service.db`)
- `CORS_ORIGINS`: Comma-separated list of allowed origins (default: `http://localhost:5173,http://localhost:3000`)
- `APP_NAME`: Application name
- `APP_VERSION`: Application version

### 5. Run the Application

```bash
# Start the development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the main.py directly
python app/main.py
```

The service will be available at:
- API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

## Database

The application uses SQLite with WAL (Write-Ahead Logging) mode enabled for improved concurrency. The database file (`session_service.db`) is created automatically on first run.

### WAL Mode Benefits
- Multiple readers can access the database while a writer is active
- Improved performance for concurrent operations
- Better suited for web applications

## API Endpoints

### Health Check
- `GET /api/health` - Check service and database health

More endpoints will be added in subsequent tasks.

## Development

### Database Initialization
The database tables and indexes are created automatically on application startup. No manual migration is needed for initial setup.

### Logging
The application uses Python's built-in logging module. Logs are printed to stdout with timestamps and log levels.

### CORS Configuration
The application is configured to accept requests from:
- `http://localhost:5173` (Vite default)
- `http://localhost:3000` (React default)

Additional origins can be added via the `CORS_ORIGINS` environment variable.

## Testing

Testing will be implemented in subsequent tasks.

## API Contract

This service implements endpoints from the PS 26241 API Contract v1.2:
- Session creation and retrieval
- Concern state calculation
- Evidence history
- Counsellor case queue management

For detailed API specifications, refer to `PS_26241_API_Contract_v1.2.md`.

## License

Part of PS 26241 hackathon project.
