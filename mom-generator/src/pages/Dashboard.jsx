import {
  CalendarDays,
  FileText,
  CheckCircle2,
  Clock,
  ArrowUpRight,
  Plus,
  MoreHorizontal,
} from "lucide-react";

import { Link } from "react-router-dom";

const meetings = [
  {
    id: 1,
    title: "Sprint Planning Meeting",
    date: "Oct 30, 2026",
    time: "10:00 AM",
    attendees: 6,
    status: "Completed",
    color: "purple",
  },
  {
    id: 2,
    title: "Product Design Review",
    date: "Oct 29, 2026",
    time: "02:30 PM",
    attendees: 4,
    status: "Completed",
    color: "blue",
  },
  {
    id: 3,
    title: "Weekly Team Sync",
    date: "Oct 28, 2026",
    time: "11:00 AM",
    attendees: 8,
    status: "Pending",
    color: "orange",
  },
];

function Dashboard() {
  const stats = [
    {
      title: "Total Meetings",
      value: "24",
      change: "+12%",
      icon: CalendarDays,
      color: "purple",
    },
    {
      title: "Minutes Generated",
      value: "18",
      change: "+8%",
      icon: FileText,
      color: "blue",
    },
    {
      title: "Action Items",
      value: "32",
      change: "8 pending",
      icon: CheckCircle2,
      color: "green",
    },
    {
      title: "Time Saved",
      value: "6.5 hrs",
      change: "This month",
      icon: Clock,
      color: "orange",
    },
  ];

  return (
    <div className="dashboard-page">

      {/* Page Heading */}

      <div className="page-heading">
        <div>
          <h1>Good morning! 👋</h1>

          <p>
            Here's what's happening with your meetings today.
          </p>
        </div>

        <Link
          to="/create-meeting"
          className="primary-button"
        >
          <Plus size={18} />
          Create Meeting
        </Link>
      </div>

      {/* Statistics */}

      <div className="stats-grid">
        {stats.map((stat) => {
          const Icon = stat.icon;

          return (
            <div className="stat-card" key={stat.title}>
              <div className="stat-card-top">
                <div
                  className={`stat-icon ${stat.color}`}
                >
                  <Icon size={21} />
                </div>

                <span className="stat-change">
                  {stat.change}
                </span>
              </div>

              <h2>{stat.value}</h2>

              <p>{stat.title}</p>
            </div>
          );
        })}
      </div>

      {/* Recent Meetings */}

      <div className="section-heading">
        <div>
          <h2>Recent Meetings</h2>

          <p>
            Your latest meetings and generated minutes.
          </p>
        </div>

        <Link
          to="/meetings"
          className="text-link"
        >
          View all
          <ArrowUpRight size={16} />
        </Link>
      </div>

      <div className="meetings-table-wrapper">
        <table className="meetings-table">

          <thead>
            <tr>
              <th>Meeting</th>
              <th>Date & Time</th>
              <th>Attendees</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>

          <tbody>
            {meetings.map((meeting) => (
              <tr key={meeting.id}>
                <td>
                  <div className="meeting-title-cell">
                    <div
                      className={`meeting-icon ${meeting.color}`}
                    >
                      <CalendarDays size={19} />
                    </div>

                    <strong>{meeting.title}</strong>
                  </div>
                </td>

                <td>
                  <div className="meeting-date">
                    <strong>{meeting.date}</strong>
                    <span>{meeting.time}</span>
                  </div>
                </td>

                <td>
                  <span className="attendee-count">
                    {meeting.attendees} people
                  </span>
                </td>

                <td>
                  <span
                    className={`status-badge ${
                      meeting.status === "Completed"
                        ? "completed"
                        : "pending"
                    }`}
                  >
                    {meeting.status}
                  </span>
                </td>

                <td>
                  <button
                    type="button"
                    className="table-action"
                    aria-label={`More options for ${meeting.title}`}
                  >
                    <MoreHorizontal size={20} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>

        </table>
      </div>

      {/* Bottom Section */}

      <div className="bottom-grid">

        <div className="welcome-card">
          <div className="welcome-content">
            <div className="welcome-icon">
              <FileText size={24} />
            </div>

            <h2>Turn conversations into action</h2>

            <p>
              Generate structured meeting minutes,
              capture important decisions, and track
              action items automatically.
            </p>

            <Link
              to="/create-meeting"
              className="welcome-button"
            >
              Generate Minutes
              <ArrowUpRight size={17} />
            </Link>
          </div>
        </div>

        <div className="activity-card">
          <div className="activity-heading">
            <h2>Upcoming Tasks</h2>

            <button
              type="button"
              className="table-action"
              aria-label="More task options"
            >
              <MoreHorizontal size={20} />
            </button>
          </div>

          <div className="activity-item">
            <div className="activity-indicator purple"></div>

            <div>
              <strong>Complete API documentation</strong>

              <p>Assigned to Rahul</p>
            </div>

            <span>Today</span>
          </div>

          <div className="activity-item">
            <div className="activity-indicator blue"></div>

            <div>
              <strong>Review UI designs</strong>

              <p>Assigned to Priya</p>
            </div>

            <span>Tomorrow</span>
          </div>

          <div className="activity-item">
            <div className="activity-indicator orange"></div>

            <div>
              <strong>Prepare sprint report</strong>

              <p>Assigned to Amit</p>
            </div>

            <span>Nov 2</span>
          </div>
        </div>

      </div>

    </div>
  );
}

export default Dashboard;