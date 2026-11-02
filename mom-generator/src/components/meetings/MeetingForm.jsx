
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  CalendarDays,
  Clock,
  MapPin,
  User,
  FileText,
  ArrowLeft,
  ArrowRight,
} from "lucide-react";

import AttendeesSection from "./AttendeesSection";
import AgendaSection from "./AgendaSection";

import { createMeeting } from "../../services/meetingService";

function MeetingForm() {
  const navigate = useNavigate();

  // Meeting form fields
  const [formData, setFormData] = useState({
    title: "",
    date: "",
    startTime: "",
    endTime: "",
    location: "",
    organizer: "",
  });

  // Attendees and agenda
  const [attendees, setAttendees] = useState([]);
  const [agenda, setAgenda] = useState([]);

  // Form validation and submission errors
  const [errors, setErrors] = useState({});

  // Loading state
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Handle changes to meeting fields
  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));

    setErrors((previous) => ({
      ...previous,
      [name]: "",
      submit: "",
    }));
  };

  // Validate meeting form
  const validateForm = () => {
    const newErrors = {};

    if (!formData.title.trim()) {
      newErrors.title = "Meeting title is required.";
    }

    if (!formData.date) {
      newErrors.date = "Meeting date is required.";
    }

    if (!formData.startTime) {
      newErrors.startTime = "Start time is required.";
    }

    if (!formData.endTime) {
      newErrors.endTime = "End time is required.";
    }

    if (
      formData.startTime &&
      formData.endTime &&
      formData.endTime <= formData.startTime
    ) {
      newErrors.endTime = "End time must be after start time.";
    }

    if (!formData.organizer.trim()) {
      newErrors.organizer = "Organizer is required.";
    }

    if (attendees.length === 0) {
      newErrors.attendees = "Add at least one attendee.";
    }

    if (agenda.length === 0) {
      newErrors.agenda = "Add at least one agenda item.";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  // Submit meeting
  const handleSubmit = async (event) => {
    event.preventDefault();

    // Stop if validation fails
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    setErrors({});

    try {
      // Prepare meeting data for FastAPI
      const meetingData = {
        title: formData.title.trim(),
        date: formData.date,
        start_time: formData.startTime,
        end_time: formData.endTime,
        location: formData.location.trim(),
        organizer: formData.organizer.trim(),
        attendees: attendees.map((attendee) => attendee.name),

        // Convert agenda objects to strings
        agenda: agenda.map((item) => item.title),
        notes: "",
        minutes: null,
      };

      console.log("Sending meeting data:", meetingData);

      // Save meeting in PostgreSQL through FastAPI
      const savedMeeting = await createMeeting(meetingData);

      console.log("Meeting saved successfully:", savedMeeting);

      // Navigate to Meeting Notes page using generated ID
      navigate(`/meetings/${savedMeeting.id}/notes`);
    } catch (err) {
      console.error(
        "Failed to save meeting:",
        JSON.stringify(err.response?.data, null, 2)
      );

      const detail = err.response?.data?.detail;

      if (Array.isArray(detail)) {
        const messages = detail.map((item) => {
          const field =
            item.loc?.[item.loc.length - 1] || "field";

          return `${field}: ${item.msg}`;
        });

        setErrors((previous) => ({
          ...previous,
          submit: messages.join(", "),
        }));
      } else if (typeof detail === "string") {
        setErrors((previous) => ({
          ...previous,
          submit: detail,
        }));
      } else {
        setErrors((previous) => ({
          ...previous,
          submit: "Failed to save meeting. Please try again.",
        }));
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form
      className="meeting-form"
      onSubmit={handleSubmit}
    >
      <div className="form-card">
        {/* Meeting Information */}
        <section className="form-section">
          <div className="form-section-heading">
            <div className="section-icon">
              <FileText size={19} />
            </div>

            <div>
              <h3>Meeting Information</h3>
              <p>
                Enter the basic details of your meeting.
              </p>
            </div>
          </div>

          <div className="form-grid">
            {/* Meeting Title */}
            <div className="form-field full-width">
              <label htmlFor="title">
                Meeting Title <span>*</span>
              </label>

              <input
                id="title"
                name="title"
                type="text"
                placeholder="e.g. Sprint Planning Meeting"
                value={formData.title}
                onChange={handleChange}
              />

              {errors.title && (
                <p className="field-error">
                  {errors.title}
                </p>
              )}
            </div>

            {/* Meeting Date */}
            <div className="form-field">
              <label htmlFor="date">
                <CalendarDays size={15} />
                Meeting Date <span>*</span>
              </label>

              <input
                id="date"
                name="date"
                type="date"
                value={formData.date}
                onChange={handleChange}
              />

              {errors.date && (
                <p className="field-error">
                  {errors.date}
                </p>
              )}
            </div>

            {/* Organizer */}
            <div className="form-field">
              <label htmlFor="organizer">
                <User size={15} />
                Organizer <span>*</span>
              </label>

              <input
                id="organizer"
                name="organizer"
                type="text"
                placeholder="Enter organizer name"
                value={formData.organizer}
                onChange={handleChange}
              />

              {errors.organizer && (
                <p className="field-error">
                  {errors.organizer}
                </p>
              )}
            </div>

            {/* Start Time */}
            <div className="form-field">
              <label htmlFor="startTime">
                <Clock size={15} />
                Start Time <span>*</span>
              </label>

              <input
                id="startTime"
                name="startTime"
                type="time"
                value={formData.startTime}
                onChange={handleChange}
              />

              {errors.startTime && (
                <p className="field-error">
                  {errors.startTime}
                </p>
              )}
            </div>

            {/* End Time */}
            <div className="form-field">
              <label htmlFor="endTime">
                <Clock size={15} />
                End Time <span>*</span>
              </label>

              <input
                id="endTime"
                name="endTime"
                type="time"
                value={formData.endTime}
                onChange={handleChange}
              />

              {errors.endTime && (
                <p className="field-error">
                  {errors.endTime}
                </p>
              )}
            </div>

            {/* Location */}
            <div className="form-field full-width">
              <label htmlFor="location">
                <MapPin size={15} />
                Meeting Location
              </label>

              <input
                id="location"
                name="location"
                type="text"
                placeholder="e.g. Conference Room A or Google Meet"
                value={formData.location}
                onChange={handleChange}
              />
            </div>
          </div>
        </section>

        <div className="form-divider"></div>

        {/* Attendees */}
        <AttendeesSection
          attendees={attendees}
          setAttendees={setAttendees}
        />

        {errors.attendees && (
          <p className="field-error section-error">
            {errors.attendees}
          </p>
        )}

        <div className="form-divider"></div>

        {/* Agenda */}
        <AgendaSection
          agenda={agenda}
          setAgenda={setAgenda}
        />

        {errors.agenda && (
          <p className="field-error section-error">
            {errors.agenda}
          </p>
        )}

        {/* Backend submission error */}
        {errors.submit && (
          <p className="field-error section-error">
            {errors.submit}
          </p>
        )}
      </div>

      {/* Form Actions */}
      <div className="form-actions">
        <button
          type="button"
          className="back-button"
          onClick={() => navigate("/")}
          disabled={isSubmitting}
        >
          <ArrowLeft size={17} />
          Cancel
        </button>

        <button
          type="submit"
          className="primary-button"
          disabled={isSubmitting}
        >
          {isSubmitting
            ? "Saving Meeting..."
            : "Continue to Meeting Notes"}

          {!isSubmitting && (
            <ArrowRight size={17} />
          )}
        </button>
      </div>
    </form>
  );
}

export default MeetingForm;
