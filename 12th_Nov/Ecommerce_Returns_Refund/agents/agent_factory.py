
def create_return_agents(client):

    eligibility_agent = client.as_agent(
        name="EligibilityAgent",
        instructions=(
            "You are an e-commerce return eligibility specialist. "
            "Explain policy eligibility findings and exceptions. "
            "Never override deterministic Python policy decisions."
        )
    )

    risk_agent = client.as_agent(
        name="RiskAgent",
        instructions=(
            "You are an e-commerce returns risk analyst. "
            "Analyze return frequency, evidence and transaction risks. "
            "Never downgrade a HIGH risk classification supplied by Python."
        )
    )

    customer_response_agent = client.as_agent(
        name="CustomerResponseAgent",
        instructions=(
            "You are a professional customer support specialist. "
            "Generate accurate customer-facing return decision messages. "
            "Never claim that payments or replacements are completed."
        )
    )

    return {
        "eligibility": eligibility_agent,
        "risk": risk_agent,
        "customer_response": customer_response_agent
    }
