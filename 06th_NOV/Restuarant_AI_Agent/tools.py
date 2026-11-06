import json
from pathlib import Path
from langchain.tools import tool
from guardrails import validate_guest_count

BASE_DIR = Path(__file__).resolve().parent
RESTAURANT_FILE = BASE_DIR / "restaurants.json"

def load_restaurants():
    with open(RESTAURANT_FILE, "r", encoding="utf-8") as file:
        restaurants = json.load(file)

    return restaurants

@tool
def search_restaurants(keyword: str) -> str:
    """
    Find restaurants by their name or cuisine.
    """
    restaurants = load_restaurants()
    keyword = keyword.strip().lower()

    if not keyword:
        return "Please enter a restaurant name or cuisine."

    matching_restaurants = []

    for restaurant in restaurants:
        name = restaurant["name"].lower()
        cuisine = restaurant["cuisine"].lower()

        if keyword in name or keyword in cuisine:
            matching_restaurants.append(restaurant)

    if len(matching_restaurants) == 0:
        return f"No restaurants found for '{keyword}'."

    result = "Here are the matching restaurants:\n"

    for restaurant in matching_restaurants:
        result += (
            f"\nID: {restaurant['id']}"
            f"\nName: {restaurant['name']}"
            f"\nCuisine: {restaurant['cuisine']}"
            f"\nLocation: {restaurant['location']}"
            f"\nPrice per person: Rs. {restaurant['price_per_person']}"
            f"\nAvailable seats: {restaurant['available_seats']}"
            "\n-------------------------\n"
        )

    return result

@tool
def calculate_dining_cost(restaurant_id: str, guests: int) -> str:
    """
    Calculate the estimated dining cost for a restaurant.
    """
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
        return f"Restaurant ID '{restaurant_id}' was not found."

    price = selected_restaurant["price_per_person"]
    total_cost = price * guests

    result = (
        f"Dining Cost Estimate\n"
        f"Restaurant: {selected_restaurant['name']}\n"
        f"Number of guests: {guests}\n"
        f"Price per person: Rs. {price}\n"
        f"Total estimated cost: Rs. {total_cost}"
    )

    if guests > selected_restaurant["available_seats"]:
        result += (
            f"\nNote: Only {selected_restaurant['available_seats']} "
            "seats are listed as available."
        )

    return result
