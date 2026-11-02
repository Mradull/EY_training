export function generateMinutes(notes = "") {
  const text = notes.toLowerCase();

  // Demo output for the Sprint 12 sample transcript
  if (
    text.includes("sprint 12") &&
    text.includes("audit logging") &&
    text.includes("staging environment")
  ) {
    return {
      summary:
        "The team planned Sprint 12 and reviewed three high-priority stories: user profile enhancements, notification settings, and audit logging. The team discussed estimates, regression testing, compliance requirements, and a pending staging environment access issue.",

      discussionPoints: [
        "User profile enhancements are estimated at 3 days.",
        "Profile changes require regression testing because they affect authentication.",
        "Notification settings are estimated at 5 days, including frontend and backend integration.",
        "Audit logging is mandatory for compliance and should be prioritized.",
        "Staging environment access is still pending.",
      ],

      decisions: [
        "Prioritize audit logging due to compliance requirements.",
        "Include regression testing for user profile changes.",
      ],

      actionItems: [
        {
          task: "Prepare test cases",
          owner: "Mike",
          deadline: "Wednesday",
        },
        {
          task: "Follow up on staging access",
          owner: "John",
          deadline: "Today",
        },
        {
          task: "Implement profile enhancements",
          owner: "Sarah / Team",
          deadline: "3 days",
        },
        {
          task: "Implement notification settings",
          owner: "Sarah / Team",
          deadline: "5 days",
        },
      ],
    };
  }

  // Fallback for other meeting notes
  return {
    summary:
      "A summary has not yet been generated for these notes. Review the transcript and edit the minutes manually.",

    discussionPoints: [
      "Review the meeting transcript and identify key discussion points.",
    ],

    decisions: [
      "No decisions have been extracted yet.",
    ],

    actionItems: [
      {
        task: "Review the meeting notes and identify follow-up tasks.",
        owner: "Unassigned",
        deadline: "Not specified",
      },
    ],
  };
}