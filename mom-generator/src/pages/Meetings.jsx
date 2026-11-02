import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getMeetings } from "../services/meetingService";
import "../styles/MeetingNotes.css";

function Meetings() {
  const [meetings, setMeetings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchMeetings = async () => {
      try {
        const data = await getMeetings();
        setMeetings(data);
      } catch (err) {
        console.error("Error fetching meetings:", err);
        setError(
          err.response?.data?.detail ||
            "Unable to load meetings. Please try again."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchMeetings();
  }, []);

  const getMeetingStatus = (meeting) => {
    const hasNotes = Boolean(meeting.notes?.trim());
    const hasMinutes = Boolean(meeting.minutes);

    if (hasMinutes) {
      return "Minutes Saved";
    }

    if (hasNotes) {
      return "Notes Added";
    }

    return "Created";
  };

  return (
    <div className="page-container">
      <div className="page-heading">
        <div>
          <h1>Meetings</h1>
          <p>Manage your meetings and meeting notes.</p>
        </div>

        <Link to="/create-meeting" className="primary-button">
          + Create Meeting
        </Link>
      </div>

      {/* Loading state */}
      {loading && (
        <div className="notes-card">
          <p>Loading meetings...</p>
        </div>
      )}

      {/* Error state */}
      {!loading && error && (
        <div className="notes-card">
          <h2>Unable to load meetings</h2>
          <p>{error}</p>

          <button
            className="primary-button"
            onClick={() => window.location.reload()}
          >
            Try Again
          </button>
        </div>
      )}

      {/* Empty state */}
      {!loading && !error && meetings.length === 0 && (
        <div className="notes-card">
          <h2>No meetings found</h2>

          <p>You haven't created any meetings yet.</p>

          <Link to="/create-meeting">
            Create your first meeting
          </Link>
        </div>
      )}

      {/* Meetings table */}
      {!loading && !error && meetings.length > 0 && (
        <div className="notes-card">
          <table className="history-table">
            <thead>
              <tr>
                <th>Meeting Title</th>
                <th>Date</th>
                <th>Time</th>
                <th>Organizer</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              {meetings.map((meeting) => {
                const hasMinutes = Boolean(meeting.minutes);

                return (
                  <tr key={meeting.id}>
                    <td>{meeting.title}</td>

                    <td>{meeting.date}</td>

                    <td>
                      {meeting.start_time} - {meeting.end_time}
                    </td>

                    <td>
                      {meeting.organizer || "Not specified"}
                    </td>

                    <td>{getMeetingStatus(meeting)}</td>

                    <td>
                      <div className="meeting-actions">
                        <Link
                          to={`/meetings/${meeting.id}/notes`}
                        >
                          Notes
                        </Link>

                        {hasMinutes && (
                          <Link
                            to={`/meetings/${meeting.id}/minutes`}
                          >
                            Minutes
                          </Link>
                        )}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Meetings;