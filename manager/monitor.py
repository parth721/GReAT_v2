import time
from queues.monitor_queue import pop_monitor
from sessions.session_store import get_session
from queues.api_call_queue import push_api_call
from queues.upload_queue import push_upload

# Define the fields and the questions to ask if missing
REQUIRED_FIELDS = [
    ("name", "What is your name?"),
    ("age", "What is your age?"),
    ("city", "Which city do you live in?")
]

def is_nil(value):
    # Nil: None, empty string, or missing
    return value is None or value == ""

def monitor_worker():
    print("Monitor worker started, waiting for sessions...")
    while True:
        session_id = pop_monitor()
        if not session_id:
            # No job, sleep a bit (shouldn't happen with brpop)
            time.sleep(1)
            continue

        # Fetch session details from Redis DB
        session = get_session(session_id)
        if not session:
            print(f"Session {session_id} not found in DB.")
            continue

        # Check for missing fields
        for field, question in REQUIRED_FIELDS:
            if field not in session or is_nil(session[field]):
                print(f"Session {session_id} missing '{field}'. Asking user: {question}")
                # Push session_id and pre-written question to api_call_queue
                push_api_call(session_id, question)
                break  # Only ask one question at a time, wait for user response
        else:
            # All fields are filled, push to upload_queue
            print(f"All info present for session {session_id}. Sending to upload queue.")
            push_upload(
                session_id,
                session.get("name"),
                session.get("age"),
                session.get("city")
            )

if __name__ == "__main__":
    monitor_worker()