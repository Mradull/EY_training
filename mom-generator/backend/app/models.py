from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func

from app.database import Base


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    title = Column(String(255), nullable=False)
    date = Column(String(20), nullable=False)

    start_time = Column(String(20), nullable=True)
    end_time = Column(String(20), nullable=True)

    location = Column(String(255), nullable=True)
    organizer = Column(String(255), nullable=True)

    attendees = Column(JSON, nullable=True)
    agenda = Column(JSON, nullable=True)

    notes = Column(JSON, nullable=True)
    minutes = Column(JSON, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )