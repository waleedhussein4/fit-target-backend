from pydantic import BaseModel, EmailStr
from typing import List, Any

class CheckSync(BaseModel):
    user_email: EmailStr
    workouts_pending_upload: List[int]  # Local workout IDs pending upload
    food_entries_pending_upload: List[Any]  # Local food entry identifiers pending upload
    last_local_sync: str  # ISO 8601 formatted string for the last sync timestamp
