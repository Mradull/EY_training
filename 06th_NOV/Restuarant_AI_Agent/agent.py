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


# =================================================
# 1. LOAD ENVIRONMENT VARIABLES
# =================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Please configure your .env file."
    )


# =================================================
# 2. INITIALIZE OPENAI MODEL
# =================================================

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# =================================================
# 3. REGISTER TOOLS
# =================================================

tools = [
    search_restaurants,
    calculate_dining_cost
]


# =================================================
# 4. CONVERSATION MEMORY
# =================================================

memory = InMemorySaver()

# Each conversation gets its own thread ID
thread_id = str(uuid.uuid4())

has_conversation = False


# =================================================
# 5. SYSTEM PROMPT
# =================================================

SYSTEM_PROMPT = """
You are a helpful AI Restaurant Reservation Assistant.

Your responsibilities:

1. Help users explore available restaurants.
2. Search restaurants using the search_restaurants tool.
3. Calculate dining costs using calculate_dining_cost.
4. Remember previously selected restaurants.
5. Remember the previously discussed guest count.
6. Handle contextual follow-up questions.

IMPORTANT RULES:

- Only answer restaurant-related questions.
- Never invent restaurant names.
- Never invent restaurant prices.
- Never invent restaurant availability.
- Always use the provided tools for restaurant information.
- Use the restaurant ID from the actual search results.
- Use the calculator tool for dining cost calculations.
- Remember the restaurant selected earlier in the conversation.
- If the user says "make that 6 people", use the previously
  selected restaurant if one is available in conversation history.
- If the restaurant is unclear, ask the user to clarify.
- Guest count must be between 1 and 20.
- Do not perform actual restaurant bookings.
- Do not process payments.
- Only provide estimated dining costs.
- All prices are in Indian Rupees (INR).

If a restaurant has fewer available seats than the requested
guest count, clearly explain that limitation. Do not claim a
reservation has been made.

Be friendly, concise and helpful.
"""


# =================================================
# 6. CREATE LANGCHAIN AGENT
# =================================================

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=memory
)


# =================================================
# 7. HELPER: DISPLAY TOOL EXECUTION
# =================================================

def display_tool_calls(messages):

    for message in messages:

        tool_calls = getattr(message, "tool_calls", [])

        for tool_call in tool_calls:

            print("\n[TOOL EXECUTION]")
            print("Tool Name:", tool_call["name"])
            print("Arguments:", tool_call["args"])
            print("------------------------------")


# =================================================
# 8. HELPER: EXTRACT GUEST COUNT
# =================================================

def extract_guest_count(text):

    patterns = [
        r"\b(\d+)\s*(?:people|persons|person|guests)\b",
        r"\bfor\s+(\d+)\b"
    ]

    for pattern in patterns:

        match = re.search(pattern, text.lower())

        if match:
            return int(match.group(1))

    return None


# =================================================
# 9. PROCESS USER MESSAGE
# =================================================

def process_user_message(user_input):

    global has_conversation

    # ---------------------------------------------
    # INPUT VALIDATION
    # ---------------------------------------------

    valid, error_message = validate_input(user_input)

    if not valid:
        print("\nGuardrail:", error_message)
        return

    # ---------------------------------------------
    # PII DETECTION
    # ---------------------------------------------

    pii_found = detect_pii(user_input)

    if pii_found:

        print("\n[GUARDRAIL] Personal information detected.")

        # Remove PII before sending anything to the model
        user_input = redact_pii(user_input)

        print("[GUARDRAIL] Sensitive information redacted.")

        # If the message has no restaurant-related intent,
        # do not send it to the AI model.
        if not is_restaurant_related(user_input):
            print(
                "\nAgent: I detected and redacted personal "
                "information. Please ask me a restaurant-related "
                "question instead."
            )
            return

    # ---------------------------------------------
    # DOMAIN RESTRICTION
    # ---------------------------------------------

    restaurant_related = is_restaurant_related(user_input)

    contextual_followup = (
        has_conversation
        and is_contextual_followup(user_input)
    )

    if not restaurant_related and not contextual_followup:

        print(
            "\nAgent: Sorry! I can only help with "
            "restaurant-related questions, restaurant searches "
            "and estimated dining costs."
        )
        return

    # ---------------------------------------------
    # GUEST COUNT VALIDATION
    # ---------------------------------------------

    guests = extract_guest_count(user_input)

    if guests is not None:

        valid, error_message = validate_guest_count(guests)

        if not valid:
            print("\n[GUARDRAIL] Guest validation failed.")
            print("Agent:", error_message)
            return

    # ---------------------------------------------
    # REDACT PII BEFORE MODEL PROCESSING
    # ---------------------------------------------

    safe_input = redact_pii(user_input)

    # ---------------------------------------------
    # INVOKE LANGCHAIN AGENT
    # ---------------------------------------------

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:

        print("\nAgent is thinking...")

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": safe_input
                    }
                ]
            },
            config=config
        )

        # -----------------------------------------
        # DISPLAY TOOL EXECUTION
        # -----------------------------------------

        display_tool_calls(result["messages"])

        # -----------------------------------------
        # GET FINAL AI RESPONSE
        # -----------------------------------------

        final_response = result["messages"][-1].content

        # -----------------------------------------
        # OUTPUT GUARDRAIL
        # -----------------------------------------

        final_response = process_output(final_response)

        print("\nRestaurant AI Agent:")
        print(final_response)

        has_conversation = True

    except Exception as error:

        print("\nAn error occurred:", error)


# =================================================
# 10. MAIN INTERACTIVE CHAT LOOP
# =================================================

def main():

    global thread_id, has_conversation

    print("\n========================================")
    print("       RESTAURANT AI ASSISTANT")
    print("========================================")

    print("Powered by LangChain + GPT-4o-mini")

    print("\nAvailable commands:")
    print("/new  - Start a fresh conversation")
    print("/exit - Exit the application")

    print("\nYou can ask me about restaurants and dining costs.")

    while True:

        user_input = input("\nYou: ").strip()

        # -----------------------------------------
        # EXIT COMMAND
        # -----------------------------------------

        if user_input.lower() == "/exit":

            print("\nThank you for using Restaurant AI Assistant!")
            break

        # -----------------------------------------
        # NEW CONVERSATION COMMAND
        # -----------------------------------------

        elif user_input.lower() == "/new":

            thread_id = str(uuid.uuid4())

            has_conversation = False

            print(
                "\n[MEMORY RESET] A new conversation has started."
            )

            print(
                "Previous conversation details will not be "
                "used in this conversation."
            )

            continue

        # -----------------------------------------
        # PROCESS NORMAL USER MESSAGE
        # -----------------------------------------

        process_user_message(user_input)


# =================================================
# 11. APPLICATION ENTRY POINT
# =================================================

if __name__ == "__main__":
    main()
