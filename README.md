# Event Logger (FastAPI + Streamlit)

A lightweight event logging demo application built with a **FastAPI** backend and a **Streamlit** frontend. It showcases a minimal full‑stack setup with event creation, in‑memory storage, and filtering.

## Features

- **Create events (POST /events)**
  - Create new events from the Streamlit form
  - Backend automatically generates `id` and `timestamp`
  - Events are stored in an in‑memory list (no persistence)

- **List events (GET /events)**
  - Return all events
  - Support filtering by `type` via the `?type=` query parameter

- **Frontend UI (Streamlit)**
  - Event table with columns: `timestamp`, `type`, `source`, `message`, `id`
  - Dropdown filter by type: `all` / `user_action` / `system` / `error` / `info`
  - Form to create events: `type`, `source`, `message`
  - After a successful submission: inputs are cleared and filter is reset to `all`

- **Initial sample data**
  - Backend pre‑populates several events of different types on startup for quick testing of list/filter behavior.

## Data Model

Example event object returned by the backend:

```json
{
  "id": "evt_001",
  "timestamp": "2024-01-15T14:30:00Z",
  "type": "user_action",           // user_action | system | error | info
  "source": "web_client",
  "message": "User clicked submit button"
}
```

When creating an event from the frontend (or via API), you only need to send:

```json
{
  "type": "user_action",
  "source": "web_client",
  "message": "User clicked submit button"
}
```

The backend will generate `id` and `timestamp` automatically.

## Project Structure

```text
.
├─ main.py          # FastAPI backend: /events API and in‑memory event store
├─ app.py           # Streamlit frontend: event list, filters, and create form
├─ requirements.txt # Python dependencies
└─ README.md        # Project documentation
```

## Requirements

- Python 3.10+ (developed and tested on Python 3.11)
- `pip` or a compatible package manager

## Installation

From the project root directory, install dependencies:

```bash
pip install -r requirements.txt
```

This will install:

- `fastapi`
- `uvicorn[standard]`
- `streamlit`
- `requests`

## Run the Backend (FastAPI)

From the project root:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API base URL: `http://localhost:8000`
- Useful endpoints:
  - `http://localhost:8000/events`  – List events (JSON)
  - `http://localhost:8000/docs`    – Swagger UI for testing the API

> Note: events are held **in memory** in the `events` list. Restarting the backend clears runtime events (except for the initial sample data).

## Run the Frontend (Streamlit)

In a new terminal window, still at the project root:

```bash
streamlit run app.py
```

- Default UI: `http://localhost:8501`
- You will see:
  - Page title: `Event Logger`
  - **Create Event** form: Type / Source / Message / Submit
  - **Filters** dropdown: filter events by type
  - **Events** table: display all (or filtered) events

## Usage

1. **View initial sample events**
   - Start the backend and frontend
   - Open the Streamlit page
   - With `Filter by type = all`, you should see the pre‑populated sample events

2. **Filter events by type**
   - Choose `user_action`, `system`, `error`, or `info` from `Filter by type`
   - The frontend sends `GET /events?type=<selected_type>`
   - The table shows only events matching the selected type

3. **Create a new event**
   - In the **Create Event** form:
     - Select `Type`
     - Enter `Source` (default is `web_client`)
     - Enter `Message`
     - Click **Submit**
   - If `Message` is empty, you will see a warning and the event is not created
   - On successful creation:
     - A `Event created` message is shown
     - Form inputs are reset to default values
     - `Filter by type` is reset to `all`
     - The event list refreshes to include the new event

4. **Test the backend API directly**

   - Get **all** events:

     ```bash
     curl "http://localhost:8000/events"
     ```

   - Get events of a specific type (e.g. `error`):

     ```bash
     curl "http://localhost:8000/events?type=error"
     ```

   - Create an event via `POST`:

     ```bash
     curl -X POST "http://localhost:8000/events" \
          -H "Content-Type: application/json" \
          -d '{
                "type": "user_action",
                "source": "cli_test",
                "message": "Created from curl"
              }'
     ```

## Extreme / Stress Testing Ideas

The app is intentionally simple but already supports a variety of edge‑case and stress tests:

- **Very long messages**
  - Paste thousands of characters into the `Message` field (long logs, repeated text, etc.)
  - Observe backend response and frontend rendering performance

- **Special characters**
  - Include `"`, `\\`, `\n`, emojis, and multi‑language text
  - Verify JSON encoding/decoding works and the UI renders correctly

- **Multi‑line messages**
  - Use messages with multiple lines to see how they are stored and displayed

- **Many events**
  - Write a small script that repeatedly calls `POST /events` to create hundreds or thousands of events
  - In the UI, switch filters frequently and watch for performance or memory issues

These tests are useful for demonstrating how to validate the robustness of a small system (e.g. in teaching or interview settings).

## Technical Details

- **Backend (`main.py`)**
  - Built with `FastAPI`
  - Uses `CORSMiddleware` to allow cross‑origin requests (`allow_origins=["*"]`)
  - Models defined with `pydantic.BaseModel`:
    - `EventBase`: base fields `type`, `source`, `message`
    - `Event`: extends `EventBase` with `id` and `timestamp`
    - `EventCreate`: same as `EventBase`, used for incoming requests
  - In‑memory storage: `events: List[Event]`
    - Sample events are pre‑populated on startup
    - `POST /events` appends new `Event` objects to the list

- **Frontend (`app.py`)**
  - Uses `requests` to call the FastAPI backend
  - Uses `streamlit` for an interactive, reactive UI
  - Uses `st.session_state` to reset form fields and filters after a successful submission
  - Displays events using `st.dataframe`

## Possible Extensions

If you want to evolve this project further, consider:

- **Persistent storage**
  - Use SQLite / PostgreSQL / MongoDB to store events
  - Replace the in‑memory `events` list with a real database layer

- **User/session information**
  - Record user IDs, session IDs, or request metadata inside events
  - Improve auditing and debugging capabilities

- **Richer filtering**
  - Filter by time range (`from` / `to`)
  - Filter by `source` or search by keywords in `message`

- **Deployment**
  - Package backend + frontend into Docker images
  - Deploy to cloud platforms (e.g. Render, Railway, Fly.io, etc.)


