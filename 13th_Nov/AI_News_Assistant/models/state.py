from typing import TypedDict, Optional


class NewsState(TypedDict, total=False):
    # User input
    topic: str
    audience: str

    # Research Agent
    research_results: list[dict]

    # Analysis Agent
    summary: list[dict]
    verification_notes: list[str]

    # Notifier Agent
    email_content: str
    output_file: str

    # Workflow control
    research_attempts: int
    research_sufficient: bool
    error: Optional[str]