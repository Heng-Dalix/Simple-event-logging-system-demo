from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class EventBase(BaseModel):
    type: str
    source: str
    message: str


class Event(EventBase):
    id: str
    timestamp: str


class EventCreate(EventBase):
    pass


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

events: List[Event] = [
    Event(
        id="evt_001",
        timestamp="2024-01-15T14:30:00Z",
        type="user_action",
        source="web_client",
        message="User clicked submit button",
    ),
    Event(
        id="evt_002",
        timestamp="2024-01-15T15:00:00Z",
        type="system",
        source="backend_worker",
        message="Background job started",
    ),
    Event(
        id="evt_003",
        timestamp="2024-01-15T15:05:00Z",
        type="error",
        source="api_server",
        message="Failed to process payment",
    ),
    Event(
        id="evt_004",
        timestamp="2024-01-15T15:10:00Z",
        type="info",
        source="monitoring_service",
        message="Daily health check OK",
    ),
]


@app.get("/events", response_model=List[Event])
def get_events(type: Optional[str] = Query(default=None)) -> List[Event]:
    if type:
        return [event for event in events if event.type == type]
    return events


@app.post("/events", response_model=Event)
def create_event(event_in: EventCreate) -> Event:
    event = Event(
        id=str(uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
        type=event_in.type,
        source=event_in.source,
        message=event_in.message,
    )
    events.append(event)
    return event
