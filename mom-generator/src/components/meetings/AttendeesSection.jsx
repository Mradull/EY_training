import { useState } from "react";
import { Plus, Trash2, Users } from "lucide-react";

function AttendeesSection({ attendees, setAttendees }) {
  const [newAttendee, setNewAttendee] = useState("");

  const addAttendee = () => {
    const name = newAttendee.trim();

    if (!name) return;

    setAttendees((previous) => [
      ...previous,
      {
        id: crypto.randomUUID(),
        name,
      },
    ]);

    setNewAttendee("");
  };

  const removeAttendee = (id) => {
    setAttendees((previous) =>
      previous.filter((attendee) => attendee.id !== id)
    );
  };

  return (
    <section className="form-section">
      <div className="form-section-heading">
        <div className="section-icon">
          <Users size={19} />
        </div>

        <div>
          <h3>Attendees</h3>
          <p>Add the people who attended the meeting.</p>
        </div>
      </div>

      <div className="dynamic-input-row">
        <input
          type="text"
          placeholder="Enter attendee name"
          value={newAttendee}
          onChange={(event) =>
            setNewAttendee(event.target.value)
          }
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              event.preventDefault();
              addAttendee();
            }
          }}
        />

        <button
          type="button"
          className="secondary-button"
          onClick={addAttendee}
        >
          <Plus size={17} />
          Add
        </button>
      </div>

      <div className="attendees-list">
        {attendees.map((attendee) => (
          <div
            className="attendee-chip"
            key={attendee.id}
          >
            <div className="attendee-avatar">
              {attendee.name.charAt(0).toUpperCase()}
            </div>

            <span>{attendee.name}</span>

            <button
              type="button"
              aria-label={`Remove ${attendee.name}`}
              onClick={() => removeAttendee(attendee.id)}
            >
              <Trash2 size={15} />
            </button>
          </div>
        ))}
      </div>

      {attendees.length === 0 && (
        <p className="empty-hint">
          No attendees added yet.
        </p>
      )}
    </section>
  );
}

export default AttendeesSection;