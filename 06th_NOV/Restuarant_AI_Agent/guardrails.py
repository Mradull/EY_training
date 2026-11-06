
import re


# Patterns used to find email addresses and phone numbers
EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
PHONE_PATTERN = r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)"


def validate_input(user_input: str) -> tuple[bool, str]:
    """Check that the user's message is valid."""

    if not user_input or not user_input.strip():
        return False, "Your question cannot be empty."

    if len(user_input) > 500:
        return False, "Your question is too long. Maximum length is 500 characters."

    return True, ""


def detect_pii(text: str) -> bool:
    """Check whether the message contains an email or phone number."""

    email_found = re.search(EMAIL_PATTERN, text)
    phone_found = re.search(PHONE_PATTERN, text)

    return email_found is not None or phone_found is not None


def redact_pii(text: str) -> str:
    """Hide email addresses and phone numbers."""

    text = re.sub(EMAIL_PATTERN, "[EMAIL REDACTED]", text)
    text = re.sub(PHONE_PATTERN, "[PHONE REDACTED]", text)

    return text


def validate_guest_count(guests: int) -> tuple[bool, str]:
    """Allow groups of 1 to 20 guests."""

    if guests < 1:
        return False, "Guest count must be at least 1."

    if guests > 20:
        return False, "Guest count cannot exceed 20."

    return True, ""


def is_restaurant_related(user_input: str) -> bool:
    """Check whether the question is about restaurants."""

    restaurant_keywords = [
        "restaurant", "restaurants", "food", "cuisine",
        "indian", "italian", "chinese", "mexican", "seafood",
        "dining", "dinner", "lunch", "breakfast",
        "reservation", "reserve", "booking", "book", "table",
        "guest", "guests", "people", "person",
        "cost", "price", "prices", "cheap", "expensive", "menu",
        "spice garden", "olive bistro", "dragon palace",
        "coastal catch", "taco fiesta",
        "r101", "r102", "r103", "r104", "r105"
    ]

    text = user_input.lower()

    for keyword in restaurant_keywords:
        if keyword in text:
            return True

    return False


def is_contextual_followup(user_input: str) -> bool:
    """Recognize short replies that depend on the previous conversation."""

    followup_messages = [
        "yes", "no", "okay", "ok", "sure",
        "that one", "same restaurant", "same",
        "what about that", "make that", "change it",
        "increase it", "decrease it",
        "more people", "fewer people"
    ]

    text = user_input.lower().strip()

    # Examples: "6", "6 people", "4 guests"
    if re.fullmatch(r"\d+\s*(people|person|guests)?", text):
        return True

    return text in followup_messages


def process_output(response: str) -> str:
    """Remove any personal information from the agent's response."""

    return redact_pii(response)
