import json
from mqueue.apicallq import pop_api_call

def fake_api_call(session_id, question):
    print(f"[API CALL] To session {session_id}: {question}")

if __name__ == "__main__":
    print("API call worker started, waiting for jobs...")
    while True:
        job = pop_api_call()
        if job:
            session_id = job["session_id"]
            question = job["question"]
            fake_api_call(session_id, question)