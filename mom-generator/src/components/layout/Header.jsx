import { useLocation } from "react-router-dom";

import {
  Search,
  Bell,
  ChevronDown,
} from "lucide-react";

function Header() {
  const location = useLocation();

  const pageTitles = {
    "/": "Dashboard",
    "/meetings": "Meetings",
    "/create-meeting": "Create Meeting",
    "/minutes-history": "Minutes History",
    "/settings": "Settings",
    "/help": "Help & Support",
  };

  const currentPage =
    pageTitles[location.pathname] || "Meeting Details";

  return (
    <header className="header">
      <div className="header-left">
        <div className="breadcrumb">
          <span>Workspace</span>
          <span className="breadcrumb-separator">/</span>
          <strong>{currentPage}</strong>
        </div>
      </div>

      <div className="header-right">
        <div className="header-search">
          <Search size={18} />

          <input
            type="text"
            placeholder="Search meetings..."
          />

          <span className="search-shortcut">⌘ K</span>
        </div>

        <button
          type="button"
          className="icon-button"
          aria-label="Notifications"
        >
          <Bell size={20} />
          <span className="notification-dot"></span>
        </button>

        <div className="header-profile">
          <div className="profile-avatar">MK</div>

          <div className="profile-details">
            <strong>My Account</strong>
            <span>Administrator</span>
          </div>

          <ChevronDown size={16} />
        </div>
      </div>
    </header>
  );
}

export default Header;