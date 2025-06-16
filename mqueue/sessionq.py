from config.redis_config import redis_client

QUEUE_NAME = "session_queue"

def push_monitor(session_id):
    redis_client.rpush(QUEUE_NAME, session_id)    # Push session_id to the right end of the queue : !!!error

def pop_monitor():
    result = redis_client.blpop(QUEUE_NAME)         # Blocking pop from the queue but on left :  !!!error 
    if result:
        return result[1]  # session_id as string
    return None