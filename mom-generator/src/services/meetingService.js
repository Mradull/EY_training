import api from "./api";

// Get all meetings
export const getMeetings = async () => {
  const response = await api.get("/meetings/");
  return response.data;
};

// Get one meeting by ID
export const getMeetingById = async (id) => {
  const response = await api.get(`/meetings/${id}`);
  return response.data;
};

// Create a meeting
export const createMeeting = async (meetingData) => {
  const response = await api.post("/meetings/", meetingData);
  return response.data;
};

//update a meeting
export const updateMeeting = async (id, meetingData) => {
  const response = await api.put(`/meetings/${id}`, meetingData);
  return response.data;
};