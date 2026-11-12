
import json


async def run_eligibility_agent(agent, request, policy_result):

    prompt = f"""
You are an E-commerce Return Eligibility Specialist.

Review the following customer return request.

CUSTOMER REQUEST:
{json.dumps(request, indent=2)}

DETERMINISTIC POLICY RESULTS:
{json.dumps(policy_result, indent=2)}

Your responsibilities:

1. Explain whether the request meets the return policy.
2. Explain every eligibility issue.
3. Explain why any exception requires human review.
4. Do not invent policy rules.
5. Do not approve or reject the request yourself.
6. Do not override the Python policy results.

Return a concise professional assessment.

Clearly distinguish:
- Eligible conditions
- Policy violations
- Exceptions requiring manager review
"""

    response = await agent.run(prompt)

    return response.text
