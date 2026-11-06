import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
  getMeetingById,
  updateMeeting,
} from "../services/meetingService";

import "../styles/MeetingNotes.css";

function MeetingNotes() {
  const { meetingId } = useParams();
  const navigate = useNavigate();

  const [meeting, setMeeting] = useState(null);
  const [notes, setNotes] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");

  // Load the selected meeting from the backend
  useEffect(() => {
    const fetchMeeting = async () => {
      try {
        setIsLoading(true);
        setError("");

        const data = await getMeetingById(meetingId);

        setMeeting(data);
        setNotes(data.notes || "");
      } catch (err) {
        console.error("Failed to load meeting:", err);

        setError(
          err.response?.data?.detail ||
            "Unable to load this meeting. Please try again."
        );
      } finally {
        setIsLoading(false);
      }
    };

    fetchMeeting();
  }, [meetingId]);

  // Save notes to PostgreSQL
  const handleSaveNotes = async () => {
    if (!notes.trim()) {
      setError("Please enter meeting notes before continuing.");
      return;
    }

    try {
      setIsSaving(true);
      setError("");

      const updatedMeeting = await updateMeeting(meetingId, {
        notes: notes,
      });

      setMeeting(updatedMeeting);

      navigate(`/meetings/${meetingId}/minutes`);
    } catch (err) {
      console.error("Failed to save meeting notes:", err);

      setError(
        err.response?.data?.detail ||
          "Unable to save the notes. Please try again."
      );
    } finally {
      setIsSaving(false);
    }
  };

  // Loading state
  if (isLoading) {
    return (
      <div className="page-container">
        <p>Loading meeting details...</p>
      </div>
    );
  }

  // Meeting not found or API error
  if (error && !meeting) {
    return (
      <div className="page-container">
        <h2>Unable to load meeting</h2>
        <p>{error}</p>

        <button
          className="secondary-button"
          onClick={() => navigate("/meetings")}
        >
          Back to Meetings
        </button>
      </div>
    );
  }

  if (!meeting) {
    return (
      <div className="page-container">
        <h2>Meeting not found</h2>
        <p>The meeting may have been deleted or the link is invalid.</p>

        <button
          className="secondary-button"
          onClick={() => navigate("/meetings")}
        >
          Back to Meetings
        </button>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-heading">
        <div>
          <h1>Meeting Notes</h1>
          <p>Enter the transcript or notes from your meeting.</p>
        </div>

        <button
          className="secondary-button"
          onClick={() => navigate("/meetings")}
        >
          Back to Meetings
        </button>
      </div>

      <div className="meeting-info-card">
        <h2>{meeting.title}</h2>

        <div className="meeting-info-grid">
          <div>
            <span>Date</span>
            <strong>{meeting.date}</strong>
          </div>

          <div>
            <span>Organizer</span>
            <strong>{meeting.organizer || "Not specified"}</strong>
          </div>

          <div>
            <span>Location</span>
            <strong>{meeting.location || "Not specified"}</strong>
          </div>
        </div>
      </div>

      <div className="notes-card">
        <label htmlFor="meeting-notes">
          Transcript / Meeting Notes
        </label>

        <textarea
          id="meeting-notes"
          value={notes}
          onChange={(event) => setNotes(event.target.value)}
          placeholder="Paste the meeting transcript or type your notes here..."
          rows={16}
        />

        {error && (
          <p className="field-error">
            {error}
          </p>
        )}

        <div className="notes-footer">
          <span>{notes.trim().length} characters</span>

          <button
            className="primary-button"
            onClick={handleSaveNotes}
            disabled={!notes.trim() || isSaving}
          >
            {isSaving ? "Saving..." : "Save & Continue"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default MeetingNotes;