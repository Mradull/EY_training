
import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

import events from "../data/events";

const RegistrationContext = createContext();

const STORAGE_KEY = "event-registrations";

function getStoredRegistrations() {
  try {
    const storedData = localStorage.getItem(STORAGE_KEY);

    if (!storedData) {
      return [];
    }

    const parsedData = JSON.parse(storedData);

    return Array.isArray(parsedData) ? parsedData : [];
  } catch (error) {
    console.error("Unable to load registrations:", error);

    return [];
  }
}

export function RegistrationProvider({ children }) {
  const [registrations, setRegistrations] = useState(
    getStoredRegistrations
  );

  useEffect(() => {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(registrations)
    );
  }, [registrations]);

  const registerForEvent = (eventId, name, email) => {
    const normalizedEmail = email.trim().toLowerCase();
    const normalizedName = name.trim();

    const selectedEvent = events.find(
      (event) => event.id === eventId
    );

    if (!selectedEvent) {
      return {
        success: false,
        message: "Event not found.",
      };
    }

    if (!normalizedName || !normalizedEmail) {
      return {
        success: false,
        message: "Please enter your name and email.",
      };
    }

    const existingRegistration = registrations.find(
      (registration) =>
        registration.eventId === eventId &&
        registration.email.toLowerCase() === normalizedEmail
    );

    if (existingRegistration) {
      return {
        success: false,
        message: "You are already registered for this event.",
      };
    }

    const registeredCount = registrations.filter(
      (registration) =>
        registration.eventId === eventId
    ).length;

    if (registeredCount >= selectedEvent.capacity) {
      return {
        success: false,
        message: "Sorry, this event is fully booked.",
      };
    }

    const newRegistration = {
      id: Date.now(),
      eventId: eventId,
      name: normalizedName,
      email: normalizedEmail,
      registeredAt: new Date().toISOString(),
    };

    setRegistrations((previousRegistrations) => [
      ...previousRegistrations,
      newRegistration,
    ]);

    return {
      success: true,
      message: "Registration successful!",
    };
  };

  const cancelRegistration = (registrationId) => {
    setRegistrations((previousRegistrations) =>
      previousRegistrations.filter(
        (registration) =>
          registration.id !== registrationId
      )
    );
  };

  const getRegistrationCount = (eventId) => {
    return registrations.filter(
      (registration) =>
        registration.eventId === eventId
    ).length;
  };

  return (
    <RegistrationContext.Provider
      value={{
        registrations,
        registerForEvent,
        cancelRegistration,
        getRegistrationCount,
      }}
    >
      {children}
    </RegistrationContext.Provider>
  );
}

export function useRegistrations() {
  const context = useContext(RegistrationContext);

  if (!context) {
    throw new Error(
      "useRegistrations must be used inside RegistrationProvider"
    );
  }

  return context;
}
