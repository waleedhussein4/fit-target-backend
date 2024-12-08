from pydantic import BaseModel, EmailStr
from typing import List, Any

class CheckSync(BaseModel):
    user_id: int
    workoutsPendingUpload: List[int]  # Local workout IDs pending upload
    foodEntriesPendingUpload: List[Any]  # Local food entry identifiers pending upload
    lastLocalSync: str  # ISO 8601 formatted string for the last sync timestamp
