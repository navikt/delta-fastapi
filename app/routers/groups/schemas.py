from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import time, datetime

class GroupBase(BaseModel):
    name: str
    announcement: Optional[str] = None
    description: Optional[str] = None
    group_type: str
    is_regular_meeting: bool
    meeting_frequency: Optional[str] = None
    default_meeting_start: Optional[time] = None
    default_meeting_end: Optional[time] = None
    has_private_slack: bool = False
    slack_channel_name: Optional[str] = None
    slack_channel_url: Optional[str] = None
    is_active: bool = True

class GroupCreate(GroupBase):
    pass

class Owner(BaseModel):
    email: str
    name: str
    role: str

    class Config:
        from_attributes = True

class Group(GroupBase):
    group_id: uuid.UUID
    created_at: datetime
    owners: List[Owner] = []

    class Config:
        from_attributes = True
        json_encoders = {
            time: lambda v: v.strftime('%H:%M:%S') if v else None,
            datetime: lambda v: v.isoformat() if v else None,
        }