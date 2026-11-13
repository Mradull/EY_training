
from datetime import datetime
from pathlib import Path
import re


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def get_audience_message(audience: str) -> tuple[str, str]:
    """Return an introduction and recommended action for the audience."""

    audience = audience.lower().strip()

    messages = {
        "engineering": (
            "This update highlights technology developments "
            "that may affect engineering teams, tools, and systems.",
            "Engineering teams should review relevant technical "
            "developments and assess their potential impact."
        ),

        "cybersecurity": (
            "This update highlights developments relevant to "
            "cybersecurity, vulnerabilities, and digital risk.",
            "Security teams should review relevant reports and "
            "check whether any recommended security action is needed."
        ),

        "management": (
            "This update highlights important technology developments "
            "that may influence business decisions and strategy.",
            "Management should review the developments and consider "
            "whether any business-level action or further assessment is needed."
        ),

        "all employees": (
            "Here is your latest technology news briefing, "
            "covering important developments from recent reports.",
            "Employees are encouraged to review the developments "
            "and follow official company guidance where relevant."
        )
    }

    return messages.get(
        audience,
        messages["all employees"]
    )


def create_notification(state: dict) -> dict:
    """
    Generate an audience-aware news email and save it as a TXT file.
    """

    topic = state.get("topic", "Technology News")
    audience = state.get("audience", "All Employees")
    summary = state.get("summary", [])
    verification_notes = state.get("verification_notes", [])

    if not summary:
        return {
            "email_content": "",
            "output_file": "",
            "error": "No summary points available. Cannot create notification."
        }

    introduction, recommended_action = get_audience_message(audience)

    current_date = datetime.now().strftime("%d %B %Y")

    email_lines = [
        "=" * 65,
        "AI NEWS ASSISTANT - NEWS BRIEFING",
        "=" * 65,
        "",
        f"Date: {current_date}",
        f"Topic: {topic}",
        f"Audience: {audience}",
        "",
        "SUBJECT:",
        f"Technology News Update: {topic}",
        "",
        "HELLO,",
        "",
        introduction,
        "",
        "TOP FIVE KEY NEWS POINTS",
        "-" * 65
    ]

    for index, item in enumerate(summary[:5], start=1):
        email_lines.extend([
            "",
            f"{index}. {item.get('point', 'No description available')}",
            f"   Status: {item.get('status', 'Not assessed')}",
            f"   Confidence: {item.get('confidence', 'Not assessed')}",
            f"   Priority: {item.get('priority', 'Normal')}",
            "   Sources:"
        ])

        sources = item.get("sources", [])

        if sources:
            for source in sources:
                email_lines.append(f"      - {source}")
        else:
            email_lines.append("      - No source URL provided")

    email_lines.extend([
        "",
        "RECOMMENDED ACTION",
        "-" * 65,
        recommended_action,
        "",
        "VERIFICATION NOTES",
        "-" * 65
    ])

    for note in verification_notes:
        email_lines.append(f"- {note}")

    email_lines.extend([
        "",
        "IMPORTANT DISCLAIMER",
        "-" * 65,
        "This briefing is generated using automated, rule-based "
        "text processing.",
        "Confidence labels are preliminary indicators and do not "
        "represent independent fact verification.",
        "Please consult the original articles before making decisions.",
        "",
        "Regards,",
        "AI News Assistant",
        "=" * 65
    ])

    email_content = "\n".join(email_lines)

    # Create output folder if it does not exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Create a safe filename
    safe_topic = re.sub(r"[^a-zA-Z0-9_-]+", "_", topic).strip("_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_path = OUTPUT_DIR / f"news_report_{safe_topic}_{timestamp}.txt"

    # Save the generated email
    output_path.write_text(email_content, encoding="utf-8")

    print(f"[Notifier Agent] Notification saved: {output_path}")

    return {
        "email_content": email_content,
        "output_file": str(output_path),
        "error": None
    }
