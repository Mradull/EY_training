
import re
from difflib import SequenceMatcher


def get_sentences(text):
    """Split article descriptions into individual sentences."""

    sentences = re.split(r"(?<=[.!?])\s+", text)

    return [
        sentence.strip()
        for sentence in sentences
        if len(sentence.split()) >= 8
    ]


def similarity(text1, text2):
    """Calculate basic textual similarity."""

    return SequenceMatcher(
        None,
        text1.lower(),
        text2.lower()
    ).ratio()


def analyze_news(state: dict) -> dict:
    """
    Analyze collected news using basic Python logic.
    No paid LLM API is required.
    """

    articles = state.get("research_results", [])

    if not articles:
        return {
            "summary": [],
            "verification_notes": [
                "No articles available for analysis."
            ],
            "error": "Research Agent returned no articles."
        }

    candidates = []

    for article in articles:
        description = article.get("description", "")

        for sentence in get_sentences(description):
            candidates.append({
                "sentence": sentence,
                "source": article.get("source", "Unknown"),
                "url": article.get("url", "")
            })

    # Remove duplicate sentences
    unique_candidates = []

    for candidate in candidates:
        duplicate = any(
            similarity(
                candidate["sentence"],
                existing["sentence"]
            ) > 0.90
            for existing in unique_candidates
        )

        if not duplicate:
            unique_candidates.append(candidate)

    # Give higher priority to sentences containing important terms
    priority_keywords = [
        "launch", "announced", "released", "security",
        "vulnerability", "breach", "update", "investment",
        "artificial intelligence", "ai", "technology",
        "acquisition", "research", "regulation"
    ]

    def calculate_priority(sentence):
        sentence_lower = sentence.lower()

        score = sum(
            1 for keyword in priority_keywords
            if keyword in sentence_lower
        )

        return score

    unique_candidates.sort(
        key=lambda item: calculate_priority(item["sentence"]),
        reverse=True
    )

    # Select up to five important points
    selected = unique_candidates[:5]

    summary = []

    for item in selected:
        sentence = item["sentence"]

        # Basic similarity check against other sources.
        supporting_sources = []

        for other in unique_candidates:
            if other["url"] == item["url"]:
                continue

            if similarity(sentence, other["sentence"]) >= 0.65:
                supporting_sources.append(other["source"])

        if supporting_sources:
            confidence = "medium"
            status = "potentially corroborated"
        else:
            confidence = "low"
            status = "needs verification"

        priority = (
            "high"
            if calculate_priority(sentence) >= 2
            else "medium"
            if calculate_priority(sentence) == 1
            else "normal"
        )

        summary.append({
            "point": sentence,
            "status": status,
            "confidence": confidence,
            "priority": priority,
            "sources": [item["url"]]
            + list(set(
                other["url"]
                for other in unique_candidates
                if other["source"] in supporting_sources
                and other["url"] != item["url"]
            ))
        })

    notes = [
        "Analysis performed using rule-based Python processing.",
        "No external language model was used.",
        "Text similarity is only an initial comparison, not proof.",
        "All claims should be checked against their original articles."
    ]

    if len(summary) < 5:
        notes.append(
            f"Only {len(summary)} distinct points were found. "
            "More research may be required."
        )

    print(f"[Analysis Agent] Generated {len(summary)} key points.")

    return {
        "summary": summary,
        "verification_notes": notes,
        "error": None
    }
