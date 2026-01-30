import requests
import streamlit as st

API_BASE = "http://localhost:8000"
EVENT_TYPES = ["user_action", "system", "error", "info"]

if "reset_after_submit" not in st.session_state:
    st.session_state["reset_after_submit"] = False

if st.session_state["reset_after_submit"]:
    st.session_state["event_message"] = ""
    st.session_state["event_source"] = "web_client"
    st.session_state["event_type"] = EVENT_TYPES[0]
    st.session_state["filter_type"] = "all"
    st.session_state["reset_after_submit"] = False


def fetch_events(selected_type: str | None = None) -> list[dict]:
    params: dict[str, str] = {}
    if selected_type and selected_type != "all":
        params["type"] = selected_type
    try:
        response = requests.get(f"{API_BASE}/events", params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Failed to fetch events: {exc}")
        return []


def create_event(event_type: str, source: str, message: str) -> dict | None:
    payload = {"type": event_type, "source": source, "message": message}
    try:
        response = requests.post(f"{API_BASE}/events", json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Failed to create event: {exc}")
        return None


st.set_page_config(page_title="Event Logger", layout="wide")

st.title("Event Logger")

st.header("Create Event")
with st.form("create_event_form"):
    type_value = st.selectbox("Type", EVENT_TYPES, key="event_type")
    source_value = st.text_input("Source", value="web_client", key="event_source")
    message_value = st.text_area("Message", key="event_message")
    submitted = st.form_submit_button("Submit")

if submitted:
    if not message_value.strip():
        st.warning("Message cannot be empty")
    else:
        created = create_event(type_value, source_value, message_value)
        if created is not None:
            st.success("Event created")
            st.session_state["reset_after_submit"] = True
            st.experimental_rerun()

st.header("Filters")
filter_type = st.selectbox("Filter by type", ["all"] + EVENT_TYPES, index=0, key="filter_type")


events = fetch_events(filter_type)

st.subheader("Events")

if events:
    rows = [
        {
            "timestamp": e.get("timestamp", ""),
            "type": e.get("type", ""),
            "source": e.get("source", ""),
            "message": e.get("message", ""),
            "id": e.get("id", ""),
        }
        for e in events
    ]
    st.dataframe(rows)
else:
    st.info("No events to display")
