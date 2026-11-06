import json
from pathlib import Path
from langchain.tools import tool
from guardrails import validate_guest_count

BASE_DIR = Path(__file__).resolve().parent
RESTAURANT_FILE = BASE_DIR / "restaurants.json"

def load_restaurants():
    with open(RESTAURANT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# -------------------------------------------------
# TOOL 1: Search Restaurants
# -------------------------------------------------

@tool
def search_restaurants(keyword: str) -> str:
    """
    Search restaurants using cuisine type or restaurant name.
    Returns matching restaurants with prices and available seats.
    """

    restaurants = load_restaurants()

    keyword = keyword.strip().lower()

    if not keyword:
        return "Please provide a restaurant name or cuisine type."

    matching_restaurants = []

    for restaurant in restaurants:
        if (
            keyword in restaurant["name"].lower()
            or keyword in restaurant["cuisine"].lower()
        ):
            matching_restaurants.append(restaurant)

    if not matching_restaurants:
        return f"No restaurants found matching '{keyword}'."

    result = f"Found {len(matching_restaurants)} restaurant(s):\n"

    for restaurant in matching_restaurants:
        result += (
            f"\nRestaurant ID: {restaurant['id']}"
            f"\nName: {restaurant['name']}"
            f"\nCuisine: {restaurant['cuisine']}"
            f"\nLocation: {restaurant['location']}"
            f"\nPrice per person: Rs. {restaurant['price_per_person']}"
            f"\nAvailable seats: {restaurant['available_seats']}"
            "\n----------------------------"
        )

    return result


# -------------------------------------------------
# TOOL 2: Calculate Dining Cost
# -------------------------------------------------

@tool
def calculate_dining_cost(
    restaurant_id: str,
    guests: int
) -> str:
    """
    Calculate estimated dining cost for a restaurant.
    Requires restaurant ID and number of guests.
    Maximum allowed guests: 20.
    """

    # Validate guest count
    is_valid, error_message = validate_guest_count(guests)

    if not is_valid:
        return error_message

    restaurants = load_restaurants()

    selected_restaurant = None

    for restaurant in restaurants:
        if restaurant["id"].lower() == restaurant_id.strip().lower():
            selected_restaurant = restaurant
            break

    if selected_restaurant is None:
        return f"Restaurant with ID '{restaurant_id}' does not exist."

    price = selected_restaurant["price_per_person"]

    total_cost = price * guests

    return (
        f"Dining Cost Estimate\n"
        f"Restaurant: {selected_restaurant['name']}\n"
        f"Guests: {guests}\n"
        f"Price per person: Rs. {price}\n"
        f"Estimated total cost: Rs. {total_cost}"
    )
