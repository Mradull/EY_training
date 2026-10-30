
import { Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import Events from "./pages/Events";
import Registrations from "./pages/Registrations";

import { RegistrationProvider } from "./context/RegistrationContext";

function App() {
  return (
    <RegistrationProvider>
      <div className="app">
        <Navbar />

        <main className="main-content">
          <Routes>
            <Route
              path="/"
              element={<Events />}
            />

            <Route
              path="/registrations"
              element={<Registrations />}
            />

            <Route
              path="*"
              element={
                <div className="empty-state">
                  <h1>404 - Page Not Found</h1>

                  <p>
                    The page you are looking for does not exist.
                  </p>
                </div>
              }
            />
          </Routes>
        </main>

      </div>
    </RegistrationProvider>
  );
}

export default App;
