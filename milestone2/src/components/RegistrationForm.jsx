
import { useState } from "react";

import { useRegistrations } from "../context/RegistrationContext";

function RegistrationForm({ event, onClose }) {
  const { registerForEvent } = useRegistrations();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [isSuccess, setIsSuccess] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    setMessage("");
    setIsSuccess(false);

    const trimmedName = name.trim();
    const trimmedEmail = email.trim();

    if (!trimmedName || !trimmedEmail) {
      setMessage("Please fill in all fields.");
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(trimmedEmail)) {
      setMessage("Please enter a valid email address.");
      return;
    }

    const result = registerForEvent(
      event.id,
      trimmedName,
      trimmedEmail
    );

    setMessage(result.message);
    setIsSuccess(result.success);

    if (result.success) {
      setName("");
      setEmail("");
    }
  };

  return (
    <div className="registration-form">
      <div className="form-header">
        <h3>Register for this event</h3>

        <button
          type="button"
          className="close-button"
          onClick={onClose}
          aria-label="Close registration form"
        >
          ×
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor={`name-${event.id}`}>
            Full Name
          </label>

          <input
            id={`name-${event.id}`}
            type="text"
            placeholder="Enter your full name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor={`email-${event.id}`}>
            Email Address
          </label>

          <input
            id={`email-${event.id}`}
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        {message && (
          <p
            className={
              isSuccess ? "form-message success" : "form-message error"
            }
            role="status"
          >
            {message}
          </p>
        )}

        <button
          type="submit"
          className="btn btn-primary"
        >
          Confirm Registration
        </button>
      </form>
    </div>
  );
}

export default RegistrationForm;
