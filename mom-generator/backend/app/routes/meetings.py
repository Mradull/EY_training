from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Meeting
from app.schemas import MeetingCreate, MeetingUpdate, MeetingResponse

router = APIRouter(
    prefix="/api/meetings",
    tags=["Meetings"],
)


@router.post("/", response_model=MeetingResponse)
def create_meeting(
    meeting_data: MeetingCreate,
    db: Session = Depends(get_db),
):
    new_meeting = Meeting(
        title=meeting_data.title,
        date=meeting_data.date,
        start_time=meeting_data.start_time,
        end_time=meeting_data.end_time,
        location=meeting_data.location,
        organizer=meeting_data.organizer,
        attendees=meeting_data.attendees,
        agenda=meeting_data.agenda,
        notes=meeting_data.notes,
        minutes=meeting_data.minutes,
    )

    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)

    return new_meeting


@router.get("/", response_model=list[MeetingResponse])
def get_meetings(db: Session = Depends(get_db)):
    return (
        db.query(Meeting)
        .order_by(Meeting.created_at.desc())
        .all()
    )


@router.get("/{meeting_id}", response_model=MeetingResponse)
def get_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
):
    meeting = (
        db.query(Meeting)
        .filter(Meeting.id == meeting_id)
        .first()
    )

    if not meeting:
        raise HTTPException(
            status_code=404,
            detail="Meeting not found",
        )

    return meeting


@router.put("/{meeting_id}", response_model=MeetingResponse)
def update_meeting(
    meeting_id: int,
    meeting_data: MeetingUpdate,
    db: Session = Depends(get_db),
):
    meeting = (
        db.query(Meeting)
        .filter(Meeting.id == meeting_id)
        .first()
    )

    if not meeting:
        raise HTTPException(
            status_code=404,
            detail="Meeting not found",
        )

    update_data = meeting_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(meeting, field, value)

    db.commit()
    db.refresh(meeting)

    return meeting


@router.delete("/{meeting_id}")
def delete_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
):
    meeting = (
        db.query(Meeting)
        .filter(Meeting.id == meeting_id)
        .first()
    )

    if not meeting:
        raise HTTPException(
            status_code=404,
            detail="Meeting not found",
        )

    db.delete(meeting)
    db.commit()

    return {
        "message": "Meeting deleted successfully",
        "meeting_id": meeting_id,
    }