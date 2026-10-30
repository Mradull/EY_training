
import { useRegistrations } from "../context/RegistrationContext";

import events from "../data/events";

function Registrations() {
  const {
    registrations,
    cancelRegistration,
  } = useRegistrations();

  const getEventDetails = (eventId) => {
    return events.find(
      (event) => String(event.id) === String(eventId)
    );
  };

  const sortedRegistrations = [...registrations].sort(
    (a, b) =>
      new Date(a.registeredAt) -
      new Date(b.registeredAt)
  );

  return (
    <div className="registrations-page">
      <section className="page-heading">
        <span className="hero-label">
          YOUR COMMUNITY JOURNEY
        </span>

        <h1>My Registrations</h1>

        <p>
          Manage your upcoming events and reservations.
        </p>
      </section>

      {sortedRegistrations.length > 0 ? (
        <div className="registrations-list">
          {sortedRegistrations.map(
            (registration) => {
              const event = getEventDetails(
                registration.eventId
              );

              if (!event) {
  return (
    <article
      className="registration-card"
      key={registration.id}
    >
      <div className="registration-info">
        <h3>Event details unavailable</h3>

        <p>
          Registration ID: {registration.id}
        </p>

        <p>
          Event ID: {String(registration.eventId)}
        </p>

        <button
          className="btn btn-danger"
          onClick={() => {
            const confirmed = window.confirm(
              "Are you sure you want to cancel this registration?"
            );

            if (confirmed) {
              cancelRegistration(registration.id);
            }
          }}
        >
          Cancel Registration
        </button>
      </div>
    </article>
  );
}

              const formattedDate = new Date(
                `${event.date}T00:00:00`
              ).toLocaleDateString("en-IN", {
                day: "numeric",
                month: "short",
                year: "numeric",
              });

              return (
                <article
                  className="registration-card"
                  key={registration.id}
                >
                  <img
                    src={event.image}
                    alt={event.title}
                    className="registration-image"
                  />

                  <div className="registration-info">
                    <span className="event-category">
                      {event.category}
                    </span>

                    <h3>{event.title}</h3>

                    <p>
                      📅 {formattedDate} · {event.time}
                    </p>

                    <p>
                      📍 {event.location}
                    </p>

                    <p>
                      <strong>Attendee:</strong>{" "}
                      {registration.name}
                    </p>

                    <p>
                      <strong>Email:</strong>{" "}
                      {registration.email}
                    </p>

                    <button
                      className="btn btn-danger"
                      onClick={() => {
                        const confirmed =
                          window.confirm(
                            "Are you sure you want to cancel this registration?"
                          );

                        if (confirmed) {
                          cancelRegistration(
                            registration.id
                          );
                        }
                      }}
                    >
                      Cancel Registration
                    </button>
                  </div>
                </article>
              );
            }
          )}
        </div>
      ) : (
        <div className="empty-state">
          <h2>No registrations yet</h2>

          <p>
            You haven't registered for any events.
            Explore events and reserve your spot!
          </p>
        </div>
      )}
    </div>
  );
}

export default Registrations;
