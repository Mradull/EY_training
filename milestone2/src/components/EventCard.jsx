
import { useState } from "react";

import RegistrationForm from "./RegistrationForm";

import { useRegistrations } from "../context/RegistrationContext";

function EventCard({ event }) {
  const [showForm, setShowForm] = useState(false);

  const { getRegistrationCount } = useRegistrations();

  const registeredCount = getRegistrationCount(event.id);

  const availableSeats =
    event.capacity - registeredCount;

  const isFull = availableSeats <= 0;

  const formattedDate = new Date(
    `${event.date}T00:00:00`
  ).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });

  return (
    <article className="event-card">
      <div className="event-image-wrapper">
        <img
          src={event.image}
          alt={event.title}
          className="event-image"
          loading="lazy"
        />

        <span className="event-category">
          {event.category}
        </span>
      </div>

      <div className="event-content">
        <h3>{event.title}</h3>

        <p className="event-description">
          {event.description}
        </p>

        <div className="event-details">
          <p>
            <span>📅</span>
            {formattedDate} · {event.time}
          </p>

          <p>
            <span>📍</span>
            {event.location}
          </p>
        </div>

        <div className="event-footer">
          <div>
            <strong>
              {availableSeats}
            </strong>

            <span>
              {" "}seats left
            </span>
          </div>

          <button
            className="btn btn-primary"
            disabled={isFull}
            onClick={() => setShowForm(!showForm)}
          >
            {isFull
              ? "Fully Booked"
              : showForm
              ? "Close Form"
              : "Register"}
          </button>
        </div>

        {showForm && !isFull && (
          <RegistrationForm
            event={event}
            onClose={() => setShowForm(false)}
          />
        )}
      </div>
    </article>
  );
}

export default EventCard;
