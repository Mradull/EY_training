import asyncio
import os
from dotenv import load_dotenv
from agent_framework import AgentResponseUpdate
from agent_framework.orchestrations import SequentialBuilder
from agents import create_agents

load_dotenv()

def build_workflow():
    (
        client,
        inventory_agent,
        pricing_agent,
        recommendation_agent
    ) = create_agents()

    workflow = SequentialBuilder(
        participants=[
            inventory_agent,
            pricing_agent,
            recommendation_agent
        ],

        intermediate_output_from=[
            inventory_agent,
            pricing_agent
        ]
    ).build()

    return client, workflow

async def run_shopping_assistant(customer_request: str):

    client, workflow = build_workflow()

    try:

        print("\n" + "=" * 65)
        print("       E-COMMERCE MULTI-AGENT SHOPPING ASSISTANT")
        print("=" * 65)
        print("\nCustomer Request:")
        print(customer_request)
        print("\n" + "=" * 65)
        print("AGENT EXECUTION STARTED")
        print("=" * 65)
        last_author = None

        async for event in workflow.run(
            customer_request,
            stream=True
        ):

            if (
                event.type in ("intermediate", "output")
                and isinstance(event.data, AgentResponseUpdate)
            ):
                update = event.data
                author = update.author_name or "AI Agent"
                if author != last_author:
                    if last_author is not None:
                        print("\n")
                    print("\n" + "-" * 65)
                    if event.type == "output":
                        print("RECOMMENDATION AGENT - FINAL OUTPUT")
                    else:
                        print(f"{author.upper()} - INTERMEDIATE OUTPUT")

                    print("-" * 65)

                    last_author = author

                print(update.text, end="", flush=True)

        print("\n\n" + "=" * 65)
        print("       SHOPPING ASSISTANT EXECUTION COMPLETED")
        print("=" * 65)

    finally:
        await client.close()

async def main():
    if not os.getenv("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY is missing from your .env file.")
        return
    print("\nWelcome to the E-commerce AI Shopping Assistant!")
    while True:
        print("\nEnter your shopping request.")
        print("Type 'exit' to quit.")
        customer_request = input("\nYou: ").strip()
        if customer_request.lower() in ["exit", "quit"]:
            print("\nThank you for using the Shopping Assistant!")
            break
        if not customer_request:
            print("Please enter a valid shopping request.")
            continue
        try:
            await run_shopping_assistant(customer_request)
        except Exception as error:
            print(f"\nAn error occurred: {error}")


if __name__ == "__main__":
    asyncio.run(main())
