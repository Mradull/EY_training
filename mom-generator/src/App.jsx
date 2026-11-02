import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import MainLayout from "./components/layout/MainLayout";

import Dashboard from "./pages/Dashboard";
import Meetings from "./pages/Meetings";
import CreateMeeting from "./pages/CreateMeeting";
import MinutesHistory from "./pages/MinutesHistory";
import MeetingNotes from "./pages/MeetingNotes";
import GeneratedMinutes from "./pages/GeneratedMinutes";
import Minutes from "./pages/MinutesPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/"
          element={
            <MainLayout>
              <Dashboard />
            </MainLayout>
          }
        />

        <Route
          path="/meetings"
          element={
            <MainLayout>
              <Meetings />
            </MainLayout>
          }
        />

        <Route
          path="/create-meeting"
          element={
            <MainLayout>
              <CreateMeeting />
            </MainLayout>
          }
        />

        <Route
          path="/minutes-history"
          element={
            <MainLayout>
              <MinutesHistory />
            </MainLayout>
          }
        />

        {/* Meeting Notes */}
        <Route
          path="/meetings/:meetingId/notes"
          element={
            <MainLayout>
              <MeetingNotes />
            </MainLayout>
          }
        />

        <Route
  path="/meetings/:meetingId/minutes"
  element={
    <MainLayout>
      <Minutes />
    </MainLayout>
  }
/>

      </Routes>
    </BrowserRouter>
  );
}

export default App;