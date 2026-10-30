
import { useMemo, useState } from "react";

import events from "../data/events";

import EventCard from "../components/EventCard";

function Events() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] =
    useState("All");

  const categories = [
    "All",
    ...new Set(events.map((event) => event.category)),
  ];

  const filteredEvents = useMemo(() => {
    return events.filter((event) => {
      const matchesSearch = event.title
        .toLowerCase()
        .includes(searchTerm.trim().toLowerCase());

      const matchesCategory =
        selectedCategory === "All" ||
        event.category === selectedCategory;

      return matchesSearch && matchesCategory;
    });
  }, [searchTerm, selectedCategory]);

  return (
    <div className="events-page">
      

      <section className="events-section">
        <div className="section-header">
          <div>
            <h2>Upcoming Events</h2>

            <p>
              Explore what's happening around you.
            </p>
          </div>

          <span className="event-total">
            {filteredEvents.length} events
          </span>
        </div>

        <div className="event-filters">
          <div className="search-box">
            <span>⌕</span>

            <input
              type="text"
              placeholder="Search events..."
              value={searchTerm}
              onChange={(e) =>
                setSearchTerm(e.target.value)
              }
            />
          </div>

          <select
            value={selectedCategory}
            onChange={(e) =>
              setSelectedCategory(e.target.value)
            }
            aria-label="Filter by category"
          >
            {categories.map((category) => (
              <option
                key={category}
                value={category}
              >
                {category === "All"
                  ? "All Categories"
                  : category}
              </option>
            ))}
          </select>
        </div>

        {filteredEvents.length > 0 ? (
          <div className="events-grid">
            {filteredEvents.map((event) => (
              <EventCard
                key={event.id}
                event={event}
              />
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <h3>No events found</h3>

            <p>
              Try changing your search or category filter.
            </p>

            <button
              className="btn btn-secondary"
              onClick={() => {
                setSearchTerm("");
                setSelectedCategory("All");
              }}
            >
              Clear Filters
            </button>
          </div>
        )}
      </section>
    </div>
  );
}

export default Events;
