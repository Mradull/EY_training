
from workflow.graph import news_workflow


def main():

    print("=" * 60)
    print("              AI NEWS ASSISTANT")
    print("          Multi-Agent News System")
    print("=" * 60)

    topic = input("\nEnter a technology news topic: ").strip()

    if not topic:
        print("Please enter a valid topic.")
        return

    print("\nSelect your target audience:")
    print("1. Engineering")
    print("2. Cybersecurity")
    print("3. Management")
    print("4. All Employees")

    audience_options = {
        "1": "Engineering",
        "2": "Cybersecurity",
        "3": "Management",
        "4": "All Employees"
    }

    choice = input("\nEnter your choice (1-4): ").strip()
    audience = audience_options.get(choice, "All Employees")

    # Initial shared state
    initial_state = {
        "topic": topic,
        "audience": audience,
        "research_attempts": 0
    }

    print("\nStarting LangGraph workflow...")
    print("-" * 60)

    # Execute the complete workflow
    try:
        result = news_workflow.invoke(initial_state)

        if result.get("error"):
            print("\nWorkflow stopped:", result["error"])
            return

        if not result.get("output_file"):
            print("\nWorkflow finished without generating a report.")
            return

        print("\n" + "=" * 60)
        print("             WORKFLOW COMPLETED")
        print("=" * 60)

        print("\nTopic:", result.get("topic"))
        print("Audience:", result.get("audience"))

        print(
            "Articles researched:",
            len(result.get("research_results", []))
        )

        print(
            "Key points generated:",
            len(result.get("summary", []))
        )

        print("\nGenerated report:")
        print(result["output_file"])

        print("\n" + "-" * 60)
        print("NEWS BRIEFING PREVIEW")
        print("-" * 60)

        print(result.get("email_content", "")[:2000])

    except Exception as error:
        print("\nAn unexpected workflow error occurred:")
        print(error)


if __name__ == "__main__":
    main()
