import os
import re
import uuid

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver

from tools import search_restaurants, calculate_dining_cost
from guardrails import (
    validate_input,
    validate_guest_count,
    detect_pii,
    redact_pii,
    is_restaurant_related,
    is_contextual_followup,
    process_output
)


# Load the Groq API key
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Please add your GROQ_API_KEY to the .env file.")


# Set up the AI model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# Tools the agent can use
tools = [search_restaurants, calculate_dining_cost]


# Store conversation history
memory = InMemorySaver()
thread_id = str(uuid.uuid4())
has_conversation = False


# Instructions given to the AI agent
SYSTEM_PROMPT = """
You are a helpful AI Restaurant Reservation Assistant.

You can help users:
- Search for restaurants.
- Find restaurants by name or cuisine.
- Calculate estimated dining costs.
- Continue conversations using previous context.

Follow these rules:
- Only answer restaurant-related questions.
- Always use the available tools for restaurant information.
- Never make up restaurant names, prices or available seats.
- Use the restaurant ID returned by the search tool.
- Remember the restaurant and guest count discussed earlier.
- If the user changes the guest count, use the previously
  selected restaurant when it is clear.
- Ask for clarification if the restaurant is not clear.
- Guest count must be between 1 and 20.
- Do not make actual bookings or accept payments.
- Only provide estimated costs in Indian Rupees (INR).
- Mention if the requested group is larger than the
  available seats.

Be friendly and keep your answers simple.
"""


# Create the agent with conversation memory
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=memory
)


def display_tool_calls(messages):
    """Show which tools the agent used."""

    for message in messages:
        for tool_call in getattr(message, "tool_calls", []):
            print("\n[TOOL USED]")
            print("Name:", tool_call["name"])
            print("Arguments:", tool_call["args"])


def extract_guest_count(text):
    """Find the guest count mentioned in a message."""

    patterns = [
        r"\b(\d+)\s*(?:people|persons|person|guests)\b",
        r"\bfor\s+(\d+)\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text.lower())

        if match:
            return int(match.group(1))

    return None


def process_user_message(user_input):
    global has_conversation

    # Check whether the input is valid
    valid, error_message = validate_input(user_input)

    if not valid:
        print("\nGuardrail:", error_message)
        return

    # Check for email addresses or phone numbers
    if detect_pii(user_input):
        print("\n[GUARDRAIL] Personal information detected.")

        user_input = redact_pii(user_input)

        print("[GUARDRAIL] Personal information was redacted.")

        if not is_restaurant_related(user_input):
            print(
                "\nAgent: Your personal information was redacted. "
                "Please ask me a restaurant-related question."
            )
            return

    # Allow restaurant questions and relevant follow-ups
    restaurant_related = is_restaurant_related(user_input)

    followup = (
        has_conversation
        and is_contextual_followup(user_input)
    )

    if not restaurant_related and not followup:
        print(
            "\nAgent: I can only help with restaurant searches "
            "and estimated dining costs."
        )
        return

    # Check the number of guests before calling the agent
    guests = extract_guest_count(user_input)

    if guests is not None:
        valid, error_message = validate_guest_count(guests)

        if not valid:
            print("\n[GUARDRAIL] Guest count validation failed.")
            print("Agent:", error_message)
            return

    # Make sure no personal information reaches the model
    safe_input = redact_pii(user_input)

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:
        print("\nAgent is thinking...")

        # Check how many messages are already in memory
        previous_state = agent.get_state(config)

        previous_count = len(
            previous_state.values.get("messages", [])
        ) if previous_state.values else 0

        # Send the user's message to the agent
        result = agent.invoke(
            {
                "messages": [
                    {"role": "user", "content": safe_input}
                ]
            },
            config=config
        )

        # Display only the tools used in this turn
        new_messages = result["messages"][previous_count:]
        display_tool_calls(new_messages)

        # Get the agent's answer
        final_response = result["messages"][-1].content

        # Remove any personal information from the answer
        final_response = process_output(final_response)

        print("\nRestaurant AI Agent:")
        print(final_response)

        has_conversation = True

    except Exception as error:
        print("\nSomething went wrong:", error)


def main():
    global thread_id, has_conversation

    print("\n================================")
    print("      RESTAURANT AI ASSISTANT")
    print("================================")

    print("Powered by LangChain + Groq")
    print("\nAvailable commands:")
    print("/new  - Start a new conversation")
    print("/exit - Close the application")

    print("\nAsk me about restaurants and dining costs.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "/exit":
            print("\nThank you for using the Restaurant AI Assistant!")
            break

        elif user_input.lower() == "/new":
            thread_id = str(uuid.uuid4())
            has_conversation = False

            print("\n[MEMORY RESET] Started a new conversation.")
            continue

        process_user_message(user_input)


if __name__ == "__main__":
    main()
