const STORAGE_KEY = "mom_meetings";

export const getMeetings = () => {
  const meetings = localStorage.getItem(STORAGE_KEY);

  return meetings ? JSON.parse(meetings) : [];
};

export const saveMeeting = (meeting) => {
  const meetings = getMeetings();

  const existingIndex = meetings.findIndex(
    (item) => item.id === meeting.id
  );

  if (existingIndex >= 0) {
    meetings[existingIndex] = {
      ...meetings[existingIndex],
      ...meeting,
    };
  } else {
    meetings.push(meeting);
  }

  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(meetings)
  );
};

export const getMeetingById = (meetingId) => {
  return getMeetings().find(
    (meeting) => meeting.id === meetingId
  );
};