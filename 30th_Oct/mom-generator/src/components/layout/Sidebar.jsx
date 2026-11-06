import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  CalendarDays,
  PlusCircle,
  FileText,
  Clock,
  Settings,
  HelpCircle,
  ChevronLeft,
  Sparkles,
} from "lucide-react";

function Sidebar() {
  const menuItems = [
    {
      title: "Dashboard",
      path: "/",
      icon: LayoutDashboard,
    },
    {
      title: "Meetings",
      path: "/meetings",
      icon: CalendarDays,
    },
    {
      title: "Create Meeting",
      path: "/create-meeting",
      icon: PlusCircle,
    },
    {
      title: "Minutes History",
      path: "/minutes-history",
      icon: FileText,
    },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">
          <Sparkles size={22} />
        </div>

        <div className="logo-text">
          <h2>MeetFlow</h2>
          <span>Minutes Generator</span>
        </div>
      </div>

      <div className="sidebar-section">
        <p className="sidebar-label">WORKSPACE</p>

        <nav className="sidebar-nav">
          {menuItems.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === "/"}
                className={({ isActive }) =>
                  isActive ? "nav-item active" : "nav-item"
                }
              >
                <Icon size={19} />
                <span>{item.title}</span>
              </NavLink>
            );
          })}
        </nav>
      </div>

      <div className="sidebar-bottom">
        <NavLink to="/settings" className="nav-item">
          <Settings size={19} />
          <span>Settings</span>
        </NavLink>

        <NavLink to="/help" className="nav-item">
          <HelpCircle size={19} />
          <span>Help & Support</span>
        </NavLink>

        <div className="sidebar-user">
          <div className="user-avatar">MK</div>

          <div className="user-info">
            <strong>My Workspace</strong>
            <span>Free Plan</span>
          </div>

          <ChevronLeft size={18} />
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;