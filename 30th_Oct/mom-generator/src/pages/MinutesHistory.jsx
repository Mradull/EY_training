import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getMeetings } from "../data/mockMeetings";

function MinutesHistory() {
  const [meetings, setMeetings] = useState([]);

  useEffect(() => {
    setMeetings(getMeetings());
  }, []);

  return (
    <div className="page-container">
      <div className="page-heading">
        <div>
          <h1>Minutes History</h1>
          <p>View and manage your saved meeting minutes.</p>
        </div>
      </div>

      {meetings.length === 0 ? (
        <div className="notes-card">
          <h2>No meeting minutes yet</h2>

          <p>
            Create a meeting, enter your notes, and save the
            generated minutes to see them here.
          </p>

          <Link to="/create-meeting">
            Create Your First Meeting
          </Link>
        </div>
      ) : (
        <div className="notes-card">
          <table className="history-table">
            <thead>
              <tr>
                <th>Meeting</th>
                <th>Date</th>
                <th>Organizer</th>
                <th>Minutes</th>
              </tr>
            </thead>

            <tbody>
              {meetings.map((meeting) => (
                <tr key={meeting.id}>
                  <td>{meeting.title}</td>
                  <td>{meeting.date}</td>
                  <td>
                    {meeting.organizer || "Not specified"}
                  </td>
                  <td>
                    <Link
                      to={`/meetings/${meeting.id}/minutes`}
                    >
                      View Minutes
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default MinutesHistory;