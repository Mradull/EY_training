
from langgraph.graph import StateGraph, START, END

from models.state import NewsState
from agents.research_agent import research_news
from agents.analysis_agent import analyze_news
from agents.notifier_agent import create_notification


def check_research(state: NewsState) -> str:
    """Decide whether research results can be analyzed."""

    if state.get("error") or not state.get("research_results"):
        return "stop"

    return "continue"


def check_analysis(state: NewsState) -> str:
    """Decide whether a notification can be generated."""

    if state.get("error") or not state.get("summary"):
        return "stop"

    return "continue"


def build_workflow():
    """Create and compile the AI News Assistant workflow."""

    workflow = StateGraph(NewsState)

    # Register the three agents as workflow nodes
    workflow.add_node("research", research_news)
    workflow.add_node("analysis", analyze_news)
    workflow.add_node("notifier", create_notification)

    # Starting point
    workflow.add_edge(START, "research")

    # Research -> Analysis, or stop if research failed
    workflow.add_conditional_edges(
        "research",
        check_research,
        {
            "continue": "analysis",
            "stop": END
        }
    )

    # Analysis -> Notifier, or stop if analysis failed
    workflow.add_conditional_edges(
        "analysis",
        check_analysis,
        {
            "continue": "notifier",
            "stop": END
        }
    )

    # Finish after notification
    workflow.add_edge("notifier", END)

    return workflow.compile()


# Create the compiled application
news_workflow = build_workflow()
