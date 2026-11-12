
import json


async def run_risk_agent(agent, request, risk_result):

    prompt = f"""
You are an E-commerce Returns Risk Analyst.

Analyze this customer return request.

REQUEST:
{json.dumps(request, indent=2)}

PYTHON RISK ANALYSIS:
{json.dumps(risk_result, indent=2)}

Your responsibilities:

1. Explain the identified risks.
2. Consider return frequency.
3. Consider missing evidence.
4. Consider high-value requests.
5. Provide a concise risk assessment.

IMPORTANT:
- Use the Python risk classification as authoritative.
- Do not downgrade HIGH risk.
- Do not invent customer history.
- Do not approve or reject requests.

Provide:
Risk Level: {risk_result["risk_level"]}
Risk Assessment: A short explanation.
"""

    response = await agent.run(prompt)

    return {
        **risk_result,
        "assessment": response.text
    }
