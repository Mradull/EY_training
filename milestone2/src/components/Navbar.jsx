
import { Link, NavLink } from "react-router-dom";

import { useRegistrations } from "../context/RegistrationContext";

function Navbar() {
  const { registrations } = useRegistrations();

  return (
    <header className="navbar">
      <Link to="/" className="brand">
        <span className="brand-icon">E</span>
        <span>Evently</span>
      </Link>

      <nav className="nav-links">
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Explore Events
        </NavLink>

        <NavLink
          to="/registrations"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          My Registrations
          <span className="registration-count">
            {registrations.length}
          </span>
        </NavLink>
      </nav>
    </header>
  );
}

export default Navbar;
