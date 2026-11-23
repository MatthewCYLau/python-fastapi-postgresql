from datetime import datetime, timezone
from collections import deque


class RateLimiter:
    def __init__(self, max_requests: int = 5, window_size=60):
        self.user_ids = {}
        self.max_requests = max_requests
        self.window_size = window_size

    def is_allowed(self, user_id: str):
        if user_id not in self.user_ids:
            self.user_ids[user_id] = deque()

        now = datetime.now(timezone.utc).timestamp()

        requests = self.user_ids[user_id]

        while requests and requests[0] < now - self.window_size:
            requests.popleft()

        if len(requests) < self.max_requests:
            requests.append(now)
            return True

        return False
