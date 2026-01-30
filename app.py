import requests
import streamlit as st
from typing import Optional

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Event Logger", layout="wide")

st.title("Event Logger")
st.caption("Simple event list powered by a FastAPI backend")


def fetch_health() -> str:
    try:
        resp = requests.get(f"{BACKEND_URL}/health", timeout=3)
        resp.raise_for_status()
        data = resp.json()
        return data.get("status", "unknown")
    except Exception:
        return "offline"


def fetch_events(selected_type: Optional[str] = None):
    try:
        params = {}
        if selected_type:
            params["type"] = selected_type

        resp = requests.get(f"{BACKEND_URL}/events", params=params, timeout=5)
        resp.raise_for_status()
        return resp.json(), None
    except Exception as exc:
        return [], str(exc)


def create_event(event_type: str, source: str, message: str):
    try:
        payload = {
            "type": event_type,
            "source": source,
            "message": message,
        }
        resp = requests.post(f"{BACKEND_URL}/events", json=payload, timeout=5)
        resp.raise_for_status()
        return resp.json(), None
    except Exception as exc:
        return None, str(exc)


with st.sidebar:
    st.header("Backend status")
    status = fetch_health()
    if status == "ok":
        st.success("Backend online")
    else:
        st.error(f"Backend status: {status}")


st.subheader("Create Event")

with st.form("create_event_form"):
    new_type = st.selectbox("Type", ["user_action", "system", "error", "info"], index=0)
    new_source = st.text_input("Source", value="web_client")
    new_message = st.text_area("Message")
    submitted = st.form_submit_button("Create")

if submitted:
    if not new_message.strip():
        st.warning("Message cannot be empty.")
    else:
        created, create_error = create_event(new_type, new_source, new_message)
        if create_error:
            st.error(f"Failed to create event: {create_error}")
        else:
            st.success("Event created successfully.")


st.subheader("Events")

event_types = ["all", "user_action", "system", "error", "info"]
selected_type = st.selectbox("Filter by type", event_types, index=0)

effective_type = None if selected_type == "all" else selected_type

events, error = fetch_events(effective_type)

if error:
    st.error(f"Failed to load events: {error}")
elif not events:
    st.info("No events available.")
else:
    # Streamlit can directly render list-of-dicts as a table
    st.table(events)
