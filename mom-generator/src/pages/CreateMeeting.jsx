import { Link } from "react-router-dom";
import { createMeeting } from "../services/meetingService";

import {
  ArrowLeft,
  FileText,
} from "lucide-react";

import MeetingForm from "../components/meetings/MeetingForm";

function CreateMeeting() {
  return (
    <div className="create-meeting-page">

      <Link
        to="/"
        className="back-link"
      >
        <ArrowLeft size={16} />
        Back to Dashboard
      </Link>

      <div className="create-meeting-heading">
        <div className="create-meeting-title">
          <div className="create-meeting-icon">
            <FileText size={24} />
          </div>

          <div>
            <h1>Create New Meeting</h1>

            <p>
              Set up your meeting details before
              generating the minutes.
            </p>
          </div>
        </div>

        <div className="step-indicator">
          <span className="step-active">1</span>
          <span>Meeting Details</span>

          <div className="step-line"></div>

          <span className="step-inactive">2</span>
          <span>Meeting Notes</span>
        </div>
      </div>

      <MeetingForm />

    </div>
  );
}

export default CreateMeeting;