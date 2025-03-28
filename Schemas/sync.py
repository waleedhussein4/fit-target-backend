from pydantic import BaseModel
from typing import List, Dict

class CheckSync(BaseModel):
    userId: str  # Adjusted to match `userId` as a string (UUID or unique identifier)
    workoutsPendingUpload: List[Dict[str, str]]  # List of workout data with UUID and CREATED_AT
    foodEntriesPendingUpload: List[Dict[str, str]]  # Placeholder for food entries with similar structure
    lastLocalSync: str  # ISO 8601 formatted string for the last sync timestamp

class SyncRequest(BaseModel):
    userId: int
    workoutsPendingUpload: List[dict]  # Accept raw workout objects as dictionaries
    exercisesPendingUpload: List[dict]  # Accept raw exercise objects as dictionaries
    setsPendingUpload: List[dict]  # Accept raw set objects as dictionaries
    lastLocalSync: str  # ISO 8601 formatted string