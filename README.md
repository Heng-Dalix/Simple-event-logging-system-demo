# Simple Event Logging System

A minimal event logging system built with **FastAPI** (backend) and **Streamlit** (frontend).

It is designed as a small demo that shows how a web UI can talk to a Python API to:

- Create new events
- List all events
- Filter events by type

All data is stored **in memory only** – there is no database.

---

## Tech Stack

- **Backend:** FastAPI
- **Frontend:** Streamlit
- **HTTP client (frontend → backend):** `requests`

---

## Features

- **In-memory event store**
  - Keeps events in a Python list (no external database required).
  - Seeds a few example events at startup for quick testing.

- **Backend API (FastAPI)**
  - `GET /health`
    - Simple health check returning `{ "status": "ok" }`.
  - `GET /events`
    - Returns all events in memory.
    - Supports optional query parameter `?type=` to filter by event type.
  - `POST /events`
    - Creates a new event in memory.
    - Automatically generates `id` (e.g. `evt_004`) and `timestamp` (current UTC time).

- **Frontend UI (Streamlit)**
  - Shows backend status in the sidebar using `GET /health`.
  - **Create Event form**:
    - Select event type (`user_action | system | error | info`).
    - Enter `source` and `message`.
    - Submits to `POST /events` and shows success or error feedback.
  - **Event list view**:
    - Dropdown filter by event type (`all`, `user_action`, `system`, `error`, `info`).
    - Calls `GET /events` or `GET /events?type=...` depending on the selected filter.
    - Displays events in a table (including `timestamp`, `type`, `source`, `message`, `id`).

---

## Data Model

The backend uses the following event structure:

```js
const eventExample = {
  id: "evt_001",
  timestamp: "2024-01-15T14:30:00Z",
  type: "user_action", // user_action | system | error | info
  source: "web_client",
  message: "User clicked submit button"
};
```

On creation, the client only needs to send `type`, `source`, and `message`. The backend fills in `id` and `timestamp`.

---

## Install Dependencies

From the project root:

```bash
pip install -r requirements.txt
```

This installs FastAPI, Uvicorn, Streamlit, and `requests` with pinned versions.

---

## Run Backend

From the project root:

```bash
uvicorn backend.main:app --reload --port 8000
```

- The API will be available at: `http://127.0.0.1:8000`
- `--reload` enables auto-reload on code changes (useful for local development).

---

## Run Frontend

From the project root:

```bash
streamlit run frontend/app.py
```

By default Streamlit will start on:

- Local URL: `http://localhost:8501`

The frontend expects the backend to be running at `http://127.0.0.1:8000` (configured as `BACKEND_URL` in `frontend/app.py`).

---

## Typical Workflow

1. Start FastAPI backend with Uvicorn.
2. Start the Streamlit frontend.
3. Open `http://localhost:8501` in your browser.
4. Check the **Backend status** in the sidebar.
5. Use **Create Event** to add new events.
6. Use **Filter by type** to explore different event types.

---

## Limitations & Possible Extensions

Current limitations:

- Events are stored **in memory only**.
- No authentication or authorization.
- No pagination or persistent storage.

Ideas for future improvements:

- Persist events to a real database (e.g. SQLite, PostgreSQL).
- Add pagination and sorting on the event list.
- Add authentication / API keys for the backend.
- Add more metadata to events (e.g. user ID, request ID, tags).
- Export events as CSV/JSON from the Streamlit UI.
