import { useState } from "react";

import {
  Plus,
  Trash2,
  ListChecks,
} from "lucide-react";

function AgendaSection({ agenda, setAgenda }) {
  const [newAgendaItem, setNewAgendaItem] = useState("");

  const addAgendaItem = () => {
    const title = newAgendaItem.trim();

    if (!title) return;

    setAgenda((previous) => [
      ...previous,
      {
        id: crypto.randomUUID(),
        title,
      },
    ]);

    setNewAgendaItem("");
  };

  const removeAgendaItem = (id) => {
    setAgenda((previous) =>
      previous.filter((item) => item.id !== id)
    );
  };

  return (
    <section className="form-section">
      <div className="form-section-heading">
        <div className="section-icon">
          <ListChecks size={19} />
        </div>

        <div>
          <h3>Meeting Agenda</h3>
          <p>Define the topics to be discussed.</p>
        </div>
      </div>

      <div className="dynamic-input-row">
        <input
          type="text"
          placeholder="Enter agenda topic"
          value={newAgendaItem}
          onChange={(event) =>
            setNewAgendaItem(event.target.value)
          }
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              event.preventDefault();
              addAgendaItem();
            }
          }}
        />

        <button
          type="button"
          className="secondary-button"
          onClick={addAgendaItem}
        >
          <Plus size={17} />
          Add
        </button>
      </div>

      <div className="agenda-list">
        {agenda.map((item, index) => (
          <div
            className="agenda-item"
            key={item.id}
          >
            <div className="agenda-number">
              {index + 1}
            </div>

            <span>{item.title}</span>

            <button
              type="button"
              aria-label={`Remove agenda item ${index + 1}`}
              onClick={() => removeAgendaItem(item.id)}
            >
              <Trash2 size={15} />
            </button>
          </div>
        ))}
      </div>

      {agenda.length === 0 && (
        <p className="empty-hint">
          No agenda items added yet.
        </p>
      )}
    </section>
  );
}

export default AgendaSection;