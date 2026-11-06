import re

# -------------------------------------------------
# GUARDRAIL 1: Input Validation
# -------------------------------------------------

def validate_input(user_input: str) -> tuple[bool, str]:

    if not user_input or not user_input.strip():
        return False, "Your question cannot be empty."

    if len(user_input) > 500:
        return False, "Your question is too long. Maximum length is 500 characters."

    return True, ""


# -------------------------------------------------
# GUARDRAIL 2: PII Detection
# -------------------------------------------------

def detect_pii(text: str) -> bool:

    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    phone_pattern = r'(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)'

    email_found = re.search(email_pattern, text)
    phone_found = re.search(phone_pattern, text)

    return bool(email_found or phone_found)


# -------------------------------------------------
# GUARDRAIL 3: PII Redaction
# -------------------------------------------------

def redact_pii(text: str) -> str:

    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    phone_pattern = r'(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)'

    text = re.sub(email_pattern, "[EMAIL REDACTED]", text)

    text = re.sub(phone_pattern, "[PHONE REDACTED]", text)

    return text


# -------------------------------------------------
# GUARDRAIL 4: Guest Count Validation
# -------------------------------------------------

def validate_guest_count(guests: int) -> tuple[bool, str]:

    if guests < 1:
        return False, "Guest count must be at least 1."

    if guests > 20:
        return False, "Guest count cannot exceed 20."

    return True, ""


# -------------------------------------------------
# GUARDRAIL 5: Domain Restriction
# -------------------------------------------------

def is_restaurant_related(user_input: str) -> bool:

    restaurant_keywords = [
        "restaurant",
        "restaurants",
        "food",
        "cuisine",
        "indian",
        "italian",
        "chinese",
        "mexican",
        "seafood",
        "dining",
        "dinner",
        "lunch",
        "breakfast",
        "reservation",
        "reserve",
        "booking",
        "book",
        "table",
        "guest",
        "guests",
        "people",
        "person",
        "cost",
        "price",
        "prices",
        "cheap",
        "expensive",
        "menu",
        "spice garden",
        "olive bistro",
        "dragon palace",
        "coastal catch",
        "taco fiesta",
        "r101",
        "r102",
        "r103",
        "r104",
        "r105"
    ]

    text = user_input.lower()

    return any(keyword in text for keyword in restaurant_keywords)


# -------------------------------------------------
# GUARDRAIL 6: Contextual Follow-up Handling
# -------------------------------------------------

def is_contextual_followup(user_input: str) -> bool:

    followup_messages = [
        "yes",
        "no",
        "okay",
        "ok",
        "sure",
        "that one",
        "same restaurant",
        "same",
        "what about that",
        "make that",
        "change it",
        "increase it",
        "decrease it",
        "more people",
        "fewer people"
    ]

    text = user_input.lower().strip()

    # Short numerical follow-ups, e.g. "6 people"
    if re.fullmatch(r"\d+\s*(people|person|guests)?", text):
        return True

    return text in followup_messages


# -------------------------------------------------
# GUARDRAIL 7: Combined Output Processing
# -------------------------------------------------

def process_output(response: str) -> str:

    return redact_pii(response)
