from sqlalchemy import Column, String, Boolean, Time, DateTime, UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class Group(Base):
    __tablename__ = "groups"

    group_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    announcement = Column(String)
    description = Column(String)
    group_type = Column(String, nullable=False)
    is_regular_meeting = Column(Boolean, default=False, nullable=False)
    meeting_frequency = Column(String, nullable=False)
    default_meeting_start = Column(Time)
    default_meeting_end = Column(Time)
    has_private_slack = Column(Boolean, default=False)
    slack_channel_name = Column(String)
    slack_channel_url = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "group_id": str(self.group_id),
            "name": self.name,
            "announcement": self.announcement,
            "description": self.description,
            "group_type": self.group_type,
            "is_regular_meeting": self.is_regular_meeting,
            "meeting_frequency": self.meeting_frequency,
            "default_meeting_start": self.default_meeting_start.strftime("%H:%M:%S") if self.default_meeting_start else None,
            "default_meeting_end": self.default_meeting_end.strftime("%H:%M:%S") if self.default_meeting_end else None,
            "has_private_slack": self.has_private_slack,
            "slack_channel_name": self.slack_channel_name,
            "slack_channel_url": self.slack_channel_url,
            "is_active": self.is_active,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }

class Member(Base):
    __tablename__ = "members"

    member_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(UUID(as_uuid=True), nullable=False)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, default="member", nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)

class GroupUpdate(Base):
    __tablename__ = "group_updates"

    update_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(UUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(UUID(as_uuid=True), nullable=False)
    update_details = Column(String, nullable=False)
