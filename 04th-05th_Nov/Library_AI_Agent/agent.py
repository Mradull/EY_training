import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import search_books, reserve_book


load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Please check your .env file."
    )

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-20b"

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_books",
            "description": (
                "Search the library for books using "
                "a title, author, keyword, or category."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": (
                            "Book title, author, or search keyword."
                        )
                    }
                },
                "required": ["keyword"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "reserve_book",
            "description": (
                "Reserve a book for a customer. "
                "Use this when the user explicitly requests "
                "a book reservation. Always provide the book ID "
                "and customer name."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": "The ID of the book."
                    },
                    "customer_name": {
                        "type": "string",
                        "description": "The customer's name."
                    }
                },
                "required": [
                    "book_id",
                    "customer_name"
                ]
            }
        }
    }

]


def execute_tool(tool_name, arguments, ui_mode=False):

    print(f"\n[AI AGENT] Selected Tool: {tool_name}")

    if tool_name == "search_books":
        return search_books(arguments["keyword"])

    elif tool_name == "reserve_book":
        return reserve_book(
            arguments["book_id"],
            arguments["customer_name"],
            confirmed=False if ui_mode else None
        )

    return {
        "success": False,
        "message": "Unknown tool requested."
    }



def run_agent(user_input, ui_mode=False):

    messages = [

        {
            "role": "system",
            "content": (
                "You are an AI Library Assistant. "
                "Help users search for books and reserve books. "
                "Use search_books for book searches. "
                "Use reserve_book for explicit reservation requests. "
                "If the user does not provide enough information "
                "to reserve a book, ask a clarification question. "
                "Never claim a reservation succeeded unless the "
                "reserve_book tool returns success=true. "
                "Never invent book IDs or availability."
            )
        },

        {
            "role": "user",
            "content": user_input
        }

    ]
    pending_reservation = None

    for _ in range(5):

        response = client.chat.completions.create(

            model=MODEL,

            messages=messages,

            tools=tools,

            tool_choice="auto"

        )

        assistant_message = response.choices[0].message

        if not assistant_message.tool_calls:

            print("\nAI Library Assistant:")
            print(assistant_message.content)

            if ui_mode:
                return {
                    "response": assistant_message.content,
                    "pending_reservation": pending_reservation
                }

            return assistant_message.content

        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            result = execute_tool(tool_name, arguments, ui_mode)

            if result.get("requires_confirmation"):
                pending_reservation = result["reservation_request"]

            messages.append({

                "role": "tool",

                "tool_call_id": tool_call.id,

                "content": json.dumps(result)

            })

    print("Maximum tool interaction limit reached.")


if __name__ == "__main__":

    print("\n===================================")
    print("       AI LIBRARY ASSISTANT")
    print("===================================")

    print("Ask me to search or reserve books.")
    print("Type 'exit' to stop.")

    while True:

        user_input = input(
            "\nYou: "
        ).strip()

        if user_input.lower() in ["exit", "quit"]:

            print("\nThank you for using AI Library Assistant!")

            break

        if not user_input:
            continue

        try:

            run_agent(user_input)

        except Exception as error:

            print("\nAn error occurred:")
            print(error)
