from collections import defaultdict
import time

user_requests = defaultdict(list)

LIMIT = 10  # requests per minute


def allow_user(user_id: int) -> bool:
    now = time.time()

    user_requests[user_id] = [
        t for t in user_requests[user_id] if now - t < 60
    ]

    if len(user_requests[user_id]) >= LIMIT:
        return False

    user_requests[user_id].append(now)
    return True