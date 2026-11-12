
import json


async def run_customer_response_agent(
    agent,
    request,
    final_decision,
    eligibility_result,
    risk_result
):

    prompt = f"""
You are a professional E-commerce Customer Support Agent.

Generate a customer-facing message for this return request.

CUSTOMER REQUEST:
{json.dumps(request, indent=2)}

FINAL WORKFLOW DECISION:
{final_decision}

ELIGIBILITY FINDINGS:
{json.dumps(eligibility_result, indent=2)}

RISK ASSESSMENT:
{json.dumps(risk_result, indent=2)}

Instructions:

1. If AUTO_APPROVED:
   Communicate that the return request has been approved
   automatically.

2. If MANAGER_APPROVED:
   Communicate that the manager approved the request.

3. If MANAGER_REJECTED:
   Politely communicate that the request was rejected.

4. Explain the decision in customer-friendly language.
5. Remain professional and empathetic.
6. Do not expose internal risk scores.
7. Never claim that money has been refunded.
8. Never claim that a replacement has been shipped.
9. Never claim that a refund or replacement is completed.

This is a simulation only.

Return only the customer communication draft.
"""

    response = await agent.run(prompt)

    return response.text
