import json
import os
from agent_framework import Agent, tool
from agent_framework.openai import OpenAIChatCompletionClient
from tools import search_products, calculate_order_total

@tool(approval_mode="never_require")
def inventory_search_tool(query: str) -> str:
    """
    Search the product dataset by product name or category.

    Returns matching product details, prices, stock and ratings.
    """

    result = search_products(query)
    return json.dumps(result, indent=2)


@tool(approval_mode="never_require")
def pricing_calculation_tool(product_id: str, quantity: int) -> str:
    """
    Calculate the order total and verify product stock.

    Args:
        product_id: Unique product ID.
        quantity: Number of units requested.
    """

    result = calculate_order_total(product_id, quantity)
    return json.dumps(result, indent=2)

def create_agents():

    # Shared OpenAI model client
    client = OpenAIChatCompletionClient(
        model="openai/gpt-oss-120b",
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )

    # AGENT 1: INVENTORY AGENT

    inventory_agent = Agent(
        client=client,
        name="InventoryAgent",

        instructions="""
        You are an Inventory Agent for an e-commerce company.

        Your responsibility is to search the available product dataset.

        Follow these rules:

        1. Understand the customer's product category or product name.
        2. Identify the requested quantity and total budget.
        3. ALWAYS use inventory_search_tool to retrieve products.
        4. Never invent product names, prices, stock or ratings.
        5. Display matching products with:
           - Product ID
           - Product name
           - Category
           - Price in INR
           - Available stock
           - Customer rating
        6. Clearly identify products with zero stock.
        7. Do not recommend products yourself.
        8. Pass the customer's original quantity and budget,
           along with the complete matching product information,
           to the Pricing Agent through your response.

        If no products match, clearly report that no matching
        products were found.
        """,

        tools=[inventory_search_tool]
    )

    # AGENT 2: PRICING AGENT

    pricing_agent = Agent(
        client=client,
        name="PricingAgent",

        instructions="""
        You are a Pricing Agent for an e-commerce company.

        You receive the customer's request and the Inventory
        Agent's results.

        Follow these rules:

        1. Identify the requested quantity and total budget.
        2. Read the product IDs and stock information from the
           Inventory Agent's response.
        3. Use pricing_calculation_tool for EACH matching product
           that has sufficient stock for the requested quantity.
        4. Do not calculate prices using invented or assumed data.
        5. Do not calculate an order for unavailable products.
        6. Compare each successful calculated total with the
           customer's TOTAL budget.
        7. Mark each product as:
           - Affordable
           - Over budget
           - Insufficient stock
        8. Display:
           - Product ID
           - Product name
           - Requested quantity
           - Unit price
           - Calculated total
           - Stock validation
           - Budget validation
           - Customer rating
        9. Pass only valid, in-stock and affordable products
           to the Recommendation Agent.

        If no products satisfy the requirements, clearly report
        that no affordable and available options were found.
        """,

        tools=[pricing_calculation_tool]
    )

    # AGENT 3: RECOMMENDATION AGENT

    recommendation_agent = Agent(
        client=client,
        name="RecommendationAgent",

        instructions="""
        You are a Product Recommendation Agent.

        Your responsibility is to select the most suitable
        product using the Inventory Agent and Pricing Agent results.

        Follow these rules:

        1. Only consider products confirmed as affordable
           and in stock by the Pricing Agent.
        2. Never recommend unavailable products.
        3. Never exceed the customer's total budget.
        4. Select the product with the highest customer rating.
        5. If ratings are equal, prefer the lower total cost.
        6. Display:
           - Recommended product name
           - Product ID
           - Unit price
           - Requested quantity
           - Total order cost
           - Customer rating
           - Available stock
           - Remaining budget
           - Short explanation for the recommendation
        7. If no products satisfy the requirements, explain
           why no recommendation can be made.

        Do not invent product information or change the
        requested quantity.
        """
    )

    return (
        client,
        inventory_agent,
        pricing_agent,
        recommendation_agent
    )