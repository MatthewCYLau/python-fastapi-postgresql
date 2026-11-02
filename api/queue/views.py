from fastapi import APIRouter
from pydantic import BaseModel
import heapq
import threading

from api.config.logging import get_logger

# In-memory priority queue and a lock for thread safety
priority_queue = []
queue_lock = threading.Lock()


class QueueItem(BaseModel):
    priority: int
    name: str
    description: str | None = None


logger = get_logger(__name__)


router = APIRouter(prefix="/api/v1/queue", tags=["queue"])


@router.post("/", status_code=201)
def add_item(item: QueueItem):
    """
    Add an item to the priority queue.
    Lower priority number = higher priority (standard min-heap behavior).
    """
    with queue_lock:
        # Store as a tuple: (priority, dictionary of item data)
        heapq.heappush(priority_queue, (item.priority, item.model_dump()))

    return {"message": "Item added successfully", "item": item}


@router.get("/", status_code=200)
def get_queue():
    """
    Get all items in the priority queue ordered by priority.
    """
    with queue_lock:
        # Sort a copy of the heap elements so they appear in correct priority order
        # without altering the internal heap structure.
        sorted_items = [item_data for priority, item_data in sorted(priority_queue)]

    return {"total_items": len(sorted_items), "queue": sorted_items}
