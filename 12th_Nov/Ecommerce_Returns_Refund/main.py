
import asyncio
import json
from pathlib import Path

from config import create_foundry_client
from data_loader import load_return_requests

from agents.agent_factory import create_return_agents
from workflow.return_workflow import build_return_workflow


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "return_results.json"


def get_manager_decision(request_data):

    print("\n" + "=" * 60)
    print("             MANAGER APPROVAL REQUIRED")
    print("=" * 60)

    print("\nRequest ID:", request_data.request_id)

    details = request_data.details

    print("Order ID:", details["order_id"])
    print("Product:", details["product"])
    print("Amount: ₹", details["amount_inr"])
    return_type = details.get(
        "return_type",
        details.get("request_type", "Not specified")
    )

    print("Return Type:", return_type)
    print("Days Since Delivery:", details["days_since_delivery"])
    print("Item Condition:", details["item_condition"])

    print("\n--- ELIGIBILITY FINDINGS ---")

    for finding in request_data.eligibility["findings"]:
        print("[OK]", finding)

    for issue in request_data.eligibility["issues"]:
        print("[ISSUE]", issue)

    print("\n--- RISK ASSESSMENT ---")

    print("Risk Level:", request_data.risk["risk_level"])

    for risk in request_data.risk["high_risks"]:
        print("[HIGH RISK]", risk)

    for risk in request_data.risk["medium_risks"]:
        print("[MEDIUM RISK]", risk)

    print("\n" + "-" * 60)

    while True:

        decision = input(
            "Manager decision (approve/reject): "
        ).strip().lower()

        if decision in ("approve", "reject"):
            return decision

        print("Invalid input. Please enter approve or reject.")



async def run_single_request(workflow, request):

    # Start this return request
    stream = workflow.run(request, stream=True)

    outputs = []

    while True:

        responses = {}

        async for event in stream:

            if event.type == "request_info":

                request_data = event.data

                # Ask the manager for a valid decision.
                decision = get_manager_decision(request_data)

                # Associate the answer with the exact pending request.
                responses[event.request_id] = decision

            elif event.type == "output":

                outputs.append(event.data)

        # If there is no pending manager response, processing is over.
        if not responses:
            break

        # Resume the SAME workflow instance.
        stream = workflow.run(
            stream=True,
            responses=responses,
        )

    if not outputs:
        raise RuntimeError(
            f"No final output received for {request['request_id']}"
        )

    return outputs[-1]



async def main():

    print("\n========================================")
    print(" E-COMMERCE RETURNS & REFUND PROCESSING")
    print(" Microsoft Agent Framework")
    print("========================================")

    # Step 1: Load return data
    requests = load_return_requests()

    print(f"\nTotal requests loaded: {len(requests)}")

    # Step 2: Connect to Azure AI Foundry
    print("\nConnecting to Azure AI Foundry...")

    client = create_foundry_client()

    # Step 3: Initialize agents
    print("Initializing agents...")

    agents = create_return_agents(client)

    # Step 4: Build workflow
    print("Building workflow graph...")

    results = []

    # Step 5: Process all requests
    for index, request in enumerate(requests, start=1):

        print("\n\n")
        print("#" * 60)
        print(
            f" PROCESSING REQUEST {index}/{len(requests)}"
        )
        print("#" * 60)

        try:
            workflow = build_return_workflow(agents)
            result = await run_single_request(
                workflow,
                request,
            )

            results.append(result)

            print("\n--- FINAL DECISION ---")
            print("Request:", result["request_id"])
            print("Route:", result["approval_route"])
            print("Decision:", result["final_decision"])

            print("\n--- CUSTOMER MESSAGE DRAFT ---")
            print(result["customer_message"])

        except Exception as error:

            print(
                f"\nError processing {request['request_id']}: {error}"
            )

            results.append({
                "request_id": request["request_id"],
                "error": str(error),
            })

    # Step 6: Save output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print("\n\n========================================")
    print(" PROCESSING SUMMARY")
    print("========================================")

    for result in results:

        if "final_decision" in result:
            print(
                result["request_id"],
                "->",
                result["final_decision"],
            )
        else:
            print(
                result["request_id"],
                "-> PROCESSING ERROR",
            )

    print("\nResults saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    asyncio.run(main())
