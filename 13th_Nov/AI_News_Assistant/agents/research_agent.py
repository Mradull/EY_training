
import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def research_news(state: dict) -> dict:
    """
    Search for recent news articles about the user's topic.
    Return structured, deduplicated results for the Analysis Agent.
    """

    topic = state.get("topic", "").strip()

    if not topic:
        return {
            "research_results": [],
            "research_sufficient": False,
            "error": "Please provide a news topic."
        }

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return {
            "research_results": [],
            "research_sufficient": False,
            "error": "TAVILY_API_KEY is missing from the .env file."
        }

    try:
        client = TavilyClient(api_key=api_key)

        print(f"\n[Research Agent] Searching for: {topic}")

        response = client.search(
            query=f"Latest technology news about {topic}",
            topic="news",
            max_results=10,
            time_range="week"
        )

        articles = response.get("results", [])
        research_results = []
        seen_urls = set()

        for article in articles:
            url = article.get("url", "").strip()

            # Skip articles without URLs and duplicate URLs
            if not url or url in seen_urls:
                continue

            seen_urls.add(url)

            research_results.append({
                "title": article.get("title", "Untitled"),
                "description": article.get("content", ""),
                "source": article.get("source", "Unknown"),
                "published_date": article.get("published_date", "Not provided"),
                "url": url
            })

        print(f"[Research Agent] Found {len(research_results)} unique articles.")

        return {
            "research_results": research_results,
            "research_sufficient": len(research_results) >= 3,
            "research_attempts": state.get("research_attempts", 0) + 1,
            "error": None
        }

    except Exception as error:
        print(f"[Research Agent] Error: {error}")

        return {
            "research_results": [],
            "research_sufficient": False,
            "research_attempts": state.get("research_attempts", 0) + 1,
            "error": str(error)
        }
