import json
from filters.g_filter import text_filter
from filters.issue_type_filter import is_supported_issue_type
from sessions.s_store import create_session
from queues.monitor_queue import push_monitor

# --- Simulated slot extraction using a simple keyword match ---
def basic_slot_extraction(text):
    # Example: simple keyword mapping
    supported_issues = [
        "login", "payment", "technical error", "account", "reset password"
    ]
    for issue in supported_issues:
        if issue in text.lower():
            return {"issue_type": issue}
    return {"issue_type": None}

def handle_incoming_request(json_data):
    # 1. Parse JSON and extract fields
    try:
        data = json.loads(json_data)
        phone_no = data["phone_no"]
        text_body = data["text_body"]
    except (KeyError, json.JSONDecodeError):
        print("Invalid input format.")
        return

    # 2. Check for gibberish
    if not text_filter(text_body):
        print("It's gibberish.")
        return

    # 3. Slot extraction (simulate with simple function)
    slots = basic_slot_extraction(text_body)
    issue_type = slots["issue_type"]

    # 4. Check if we support this issue type
    if issue_type and is_supported_issue_type(issue_type):
        # 5. Create session using phone_no as session_id
        session_id = phone_no
        session_data = {
            "phone_no": phone_no,
            "issue_type": issue_type,
            "text_body": text_body
        }
        create_session(session_id, session_data)
        print(f"Session created for {session_id} with issue type: {issue_type}")
        # 6. Pass session_id to queue (monitor_queue)
        push_monitor(session_id)
        print(f"Session ID {session_id} pushed to monitor queue.")
    else:
        print("We don't provide such service.")

# --- Example usage ---
if __name__ == "__main__":
    # Simulate incoming JSON request
    incoming = json.dumps({
        "phone_no": "9876543210",
        "text_body": "I want to reset my password"
    })
    handle_incoming_request(incoming)