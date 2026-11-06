
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
  getMeetingById,
  updateMeeting,
} from "../services/meetingService";

import "../styles/MeetingNotes.css";

// Split notes into meaningful non-empty lines.
const getLines = (notes) => {
  return notes
    .split(/\n+/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => line.replace(/^[-*•]\s*/, ""));
};

// Rule-based MoM generation.
// This organizes the supplied notes; it does not use AI.
const generateMinutesFromNotes = (notes) => {
  const lines = getLines(notes);

  const decisionPattern =
    /\b(decided|decision|agreed|approved|confirmed|finalized|resolved)\b/i;

  const actionPattern =
    /\b(action item|will |must |should |need to|assigned to|responsible for|follow up|follow-up|todo|to-do)\b/i;

  const nextStepPattern =
    /\b(next step|next meeting|follow up|follow-up|by next|deadline)\b/i;

  const decisions = [];
  const actionItems = [];
  const nextSteps = [];
  const discussionPoints = [];

  lines.forEach((line) => {
    if (decisionPattern.test(line)) {
      decisions.push(line);
    } else if (actionPattern.test(line)) {
      actionItems.push(line);
    } else if (nextStepPattern.test(line)) {
      nextSteps.push(line);
    } else {
      discussionPoints.push(line);
    }
  });

  // Keep the summary simple and grounded in the original notes.
  const summary = lines.slice(0, 3).join(" ");

  return {
    summary: summary || "No summary available.",
    discussion_points: discussionPoints,
    decisions,
    action_items: actionItems,
    next_steps: nextSteps,
  };
};

function Minutes() {
  const { meetingId } = useParams();
  const navigate = useNavigate();

  const [meeting, setMeeting] = useState(null);
  const [minutes, setMinutes] = useState(null);

  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState("");

  // Load meeting details and previously saved minutes.
  useEffect(() => {
    const fetchMeeting = async () => {
      try {
        setIsLoading(true);
        setError("");

        const data = await getMeetingById(meetingId);

        setMeeting(data);
        setMinutes(data.minutes || null);
      } catch (err) {
        console.error("Failed to load meeting:", err);

        const detail = err.response?.data?.detail;

        setError(
          typeof detail === "string"
            ? detail
            : "Unable to load this meeting."
        );
      } finally {
        setIsLoading(false);
      }
    };

    fetchMeeting();
  }, [meetingId]);

  // Generate MoM and save it to PostgreSQL.
  const handleGenerateMinutes = async () => {
    if (!meeting?.notes?.trim()) {
      setError("Please save meeting notes before generating minutes.");
      return;
    }

    try {
      setIsGenerating(true);
      setError("");

      const generatedMinutes = generateMinutesFromNotes(
        meeting.notes
      );

      const updatedMeeting = await updateMeeting(meetingId, {
        minutes: generatedMinutes,
      });

      setMeeting(updatedMeeting);
      setMinutes(updatedMeeting.minutes || generatedMinutes);
    } catch (err) {
      console.error(
        "Failed to generate or save minutes:",
        err.response?.data || err
      );

      const detail = err.response?.data?.detail;

      setError(
        typeof detail === "string"
          ? detail
          : "Unable to save the generated minutes."
      );
    } finally {
      setIsGenerating(false);
    }
  };

  if (isLoading) {
    return (
      <div className="page-container">
        <p>Loading meeting minutes...</p>
      </div>
    );
  }

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
          <h1>Minutes of Meeting</h1>
          <p>
            Review and save the minutes generated from your notes.
          </p>
        </div>

        <button
          className="secondary-button"
          onClick={() => navigate("/meetings")}
        >
          Back to Meetings
        </button>
      </div>

      {/* Meeting information */}
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

      {/* Source notes */}
      <div className="notes-card">
        <h2>Original Meeting Notes</h2>

        <p style={{ whiteSpace: "pre-wrap" }}>
          {meeting.notes || "No notes have been saved."}
        </p>

        <button
          className="secondary-button"
          onClick={() =>
            navigate(`/meetings/${meetingId}/notes`)
          }
        >
          Edit Meeting Notes
        </button>
      </div>

      {/* Generate button */}
      <div className="notes-card">
        <h2>Generate Minutes</h2>

        <p>
          Organize the saved notes into a summary, discussion
          points, decisions, action items, and next steps.
        </p>

        <button
          className="primary-button"
          onClick={handleGenerateMinutes}
          disabled={isGenerating || !meeting.notes?.trim()}
        >
          {isGenerating
            ? "Generating Minutes..."
            : minutes
              ? "Regenerate Minutes"
              : "Generate MoM"}
        </button>

        {error && (
          <p className="field-error">
            {error}
          </p>
        )}
      </div>

      {/* Generated MoM */}
      {minutes && (
        <div className="notes-card">
          <h2>Generated Minutes of Meeting</h2>

          <section>
            <h3>Summary</h3>
            <p>{minutes.summary}</p>
          </section>

          <section>
            <h3>Discussion Points</h3>

            {minutes.discussion_points?.length > 0 ? (
              <ul>
                {minutes.discussion_points.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            ) : (
              <p>No separate discussion points identified.</p>
            )}
          </section>

          <section>
            <h3>Decisions</h3>

            {minutes.decisions?.length > 0 ? (
              <ul>
                {minutes.decisions.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            ) : (
              <p>No decisions identified in the notes.</p>
            )}
          </section>

          <section>
            <h3>Action Items</h3>

            {minutes.action_items?.length > 0 ? (
              <ul>
                {minutes.action_items.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            ) : (
              <p>No action items identified in the notes.</p>
            )}
          </section>

          <section>
            <h3>Next Steps</h3>

            {minutes.next_steps?.length > 0 ? (
              <ul>
                {minutes.next_steps.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            ) : (
              <p>No next steps identified in the notes.</p>
            )}
          </section>

          <p>
            <strong>Status:</strong> Minutes saved successfully.
          </p>
        </div>
      )}
    </div>
  );
}

export default Minutes;
