import json
from config.redis_config import redis_client

def create_session(session_id, data):
    """Store session data as a JSON string."""
    redis_client.set(f"session:{session_id}", json.dumps(data))

def get_session(session_id):
    """Fetch session data and convert back to dict."""
    session_json = redis_client.get(f"session:{session_id}")
    if session_json:
        return json.loads(session_json)
    return None