import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  getMeetingById,
  saveMeeting,
} from "../data/mockMeetings";
import { generateMinutes } from "../utils/generateMinutes";

function GeneratedMinutes() {
  const { meetingId } = useParams();
  const navigate = useNavigate();

  const [meeting, setMeeting] = useState(() =>
    getMeetingById(meetingId)
  );

  const [minutes, setMinutes] = useState(() => {
    if (!meeting) return null;

    return meeting.minutes || generateMinutes(meeting.notes || "");
  });

  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const latestMeeting = getMeetingById(meetingId);
    setMeeting(latestMeeting);

    if (latestMeeting) {
      setMinutes(
        latestMeeting.minutes ||
          generateMinutes(latestMeeting.notes || "")
      );
    }
  }, [meetingId]);

  if (!meeting || !minutes) {
    return (
      <div className="page-container">
        <h2>Meeting not found</h2>

        <button onClick={() => navigate("/minutes-history")}>
          Back to History
        </button>
      </div>
    );
  }

  const updateField = (field, value) => {
    setMinutes((previous) => ({
      ...previous,
      [field]: value,
    }));

    setSaved(false);
  };

  const updateActionItem = (index, field, value) => {
    const updatedItems = [...minutes.actionItems];

    updatedItems[index] = {
      ...updatedItems[index],
      [field]: value,
    };

    updateField("actionItems", updatedItems);
  };

  const handleSave = () => {
    const updatedMeeting = {
      ...meeting,
      minutes,
      updatedAt: new Date().toISOString(),
    };

    saveMeeting(updatedMeeting);
    setMeeting(updatedMeeting);
    setSaved(true);
  };

  return (
    <div className="page-container">
      <div className="page-heading">
        <div>
          <h1>Generated Minutes</h1>
          <p>Review and edit the minutes for your meeting.</p>
        </div>

        <button
          className="secondary-button"
          onClick={() =>
            navigate(`/meetings/${meetingId}/notes`)
          }
        >
          Back to Notes
        </button>
      </div>

      <div className="meeting-info-card">
        <h2>{meeting.title}</h2>

        <p>
          <strong>Date:</strong> {meeting.date}
        </p>

        <p>
          <strong>Organizer:</strong>{" "}
          {meeting.organizer || "Not specified"}
        </p>
      </div>

      <div className="notes-card">
        <h2>Meeting Summary</h2>

        <textarea
          rows={5}
          value={minutes.summary}
          onChange={(event) =>
            updateField("summary", event.target.value)
          }
        />
      </div>

      <div className="notes-card">
        <h2>Discussion Points</h2>

        <textarea
          rows={7}
          value={minutes.discussionPoints.join("\n")}
          onChange={(event) =>
            updateField(
              "discussionPoints",
              event.target.value.split("\n")
            )
          }
        />

        <p className="field-hint">
          Enter one discussion point per line.
        </p>
      </div>

      <div className="notes-card">
        <h2>Decisions</h2>

        <textarea
          rows={5}
          value={minutes.decisions.join("\n")}
          onChange={(event) =>
            updateField(
              "decisions",
              event.target.value.split("\n")
            )
          }
        />

        <p className="field-hint">
          Enter one decision per line.
        </p>
      </div>

      <div className="notes-card">
        <h2>Action Items</h2>

        {minutes.actionItems.map((item, index) => (
          <div className="action-item" key={index}>
            <label>Task</label>

            <input
              value={item.task}
              onChange={(event) =>
                updateActionItem(
                  index,
                  "task",
                  event.target.value
                )
              }
            />

            <label>Owner</label>

            <input
              value={item.owner}
              onChange={(event) =>
                updateActionItem(
                  index,
                  "owner",
                  event.target.value
                )
              }
            />

            <label>Deadline</label>

            <input
              value={item.deadline}
              onChange={(event) =>
                updateActionItem(
                  index,
                  "deadline",
                  event.target.value
                )
              }
            />
          </div>
        ))}
      </div>

      <div className="notes-footer">
        <span>
          {saved ? "Minutes saved successfully." : ""}
        </span>

        <button
          className="primary-button"
          onClick={handleSave}
        >
          Save Minutes
        </button>
      </div>
    </div>
  );
}

export default GeneratedMinutes;