from config.redis_config import redis_client
import json

QUEUE_NAME = "apicall_queue"

def push_api_call(session_id, question):
    msg = {"session_id": session_id, "question": question}
    redis_client.rpush(QUEUE_NAME, json.dumps(msg))

def pop_api_call():
    result = redis_client.blpop(QUEUE_NAME)
    if result:
        return json.loads(result[1])
    return None