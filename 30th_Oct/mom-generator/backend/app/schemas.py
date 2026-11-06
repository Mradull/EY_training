from pydantic import BaseModel
from typing import Optional


class MeetingCreate(BaseModel):
    title: str
    date: str
    start_time: str
    end_time: str
    location: str
    organizer: str
    attendees: list[str]
    agenda: list[str]
    notes: str = ""
    minutes: Optional[dict] = None


class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    organizer: Optional[str] = None
    attendees: Optional[list[str]] = None
    agenda: Optional[list[str]] = None
    notes: Optional[str] = None
    minutes: Optional[dict] = None


class MeetingResponse(BaseModel):
    id: int
    title: str
    date: str
    start_time: str
    end_time: str
    location: str
    organizer: str
    attendees: list[str]
    agenda: list[str]
    notes: str
    minutes: Optional[dict] = None

    class Config:
        from_attributes = True