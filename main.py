from typing import List, Literal, Optional

from datetime import datetime
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class Event(BaseModel):
    id: str
    timestamp: str
    type: Literal["user_action", "system", "error", "info"]
    source: str
    message: str


class EventCreate(BaseModel):
    type: Literal["user_action", "system", "error", "info"]
    source: str
    message: str


app = FastAPI(title="Event Logger API")

# Allow local Streamlit app to call this backend
origins = [
    "http://localhost:8501",
    "http://127.0.0.1:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# In-memory storage for events
EVENTS: List[Event] = []


def seed_events() -> None:
    """Seed a single example event so the list isn't empty at first."""
    if EVENTS:
        return

    example1 = Event(
        id="evt_001",
        timestamp="2024-01-15T14:30:00Z",
        type="user_action",
        source="web_client",
        message="User clicked submit button",
    )

    example2 = Event(
        id="evt_002",
        timestamp="2024-01-15T15:00:00Z",
        type="system",
        source="backend_service",
        message="Scheduled job completed successfully",
    )

    example3 = Event(
        id="evt_003",
        timestamp="2024-01-15T15:05:00Z",
        type="error",
        source="web_client",
        message="Failed to submit form due to validation error",
    )

    EVENTS.extend([example1, example2, example3])


seed_events()


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


@app.get("/events", response_model=List[Event])
async def list_events(
    type: Optional[Literal["user_action", "system", "error", "info"]] = Query(default=None),
) -> List[Event]:
    if type is None:
        return EVENTS

    return [event for event in EVENTS if event.type == type]


@app.post("/events", response_model=Event)
async def create_event(payload: EventCreate) -> Event:
    new_id = f"evt_{len(EVENTS) + 1:03d}"
    timestamp = datetime.utcnow().isoformat() + "Z"

    event = Event(
        id=new_id,
        timestamp=timestamp,
        type=payload.type,
        source=payload.source,
        message=payload.message,
    )

    EVENTS.append(event)
    return event
