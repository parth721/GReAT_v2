from config.redis_config import redis_client
import json

QUEUE_NAME = "upload_queue"

def push_upload(session_id, name, age, city):
    msg = {
        "session_id": session_id,
        "name": name,
        "age": age,
        "city": city
    }
    redis_client.rpush(QUEUE_NAME, json.dumps(msg))

def pop_upload():
    result = redis_client.blpop(QUEUE_NAME)
    if result:
        return json.loads(result[1])
    return None 