import time
import json
from config.redis_config import redis_client
from mqueue.uploadq import pop_upload
from sessiondb.redisdb import get_session

def fake_db_upload(data):
    print(f"[DB] Uploaded: {data}")

def notify_user(session_id):
    print(f"[User Notify] (session {session_id}) Upload successful!")

def delete_session(session_id):
    redis_client.delete(f"session:{session_id}")
    print(f"[Session] Deleted session:{session_id}")

if __name__ == "__main__":
    print("Upload worker started, waiting for jobs...")
    while True:
        job = pop_upload()
        if job:
            session_id = job["session_id"]
            fake_db_upload(job)  # Simulate DB upload
            # Simulate user notification with delay
            print(f"[User Notify] Notifying user in 4s for session {session_id}...")
            time.sleep(4)  # Wait 4000ms
            notify_user(session_id)
            # Remove session data if present
            delete_session(session_id)