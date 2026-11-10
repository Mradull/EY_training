import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PRODUCTS_FILE = BASE_DIR / "products.json"

def load_products():
    """
    Load products from products.json.
    """

    if not PRODUCTS_FILE.exists():
        raise FileNotFoundError(
            f"Product dataset not found: {PRODUCTS_FILE}"
        )

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
        products = json.load(file)

    return products

# TOOL 1: Search Products

def search_products(query: str) -> dict:
    """
    Search products by product name or category.

    Args:
        query: Product name or category.

    Returns:
        Dictionary containing matching products.
    """

    if not isinstance(query, str) or not query.strip():
        return {
            "success": False,
            "message": "Please provide a valid product name or category.",
            "products": []
        }

    products = load_products()

    search_term = query.strip().lower()

    matching_products = []

    for product in products:

        product_name = product["name"].lower()
        product_category = product["category"].lower()

        if (
            search_term in product_name
            or search_term in product_category
        ):

            matching_products.append({
                "id": product["id"],
                "name": product["name"],
                "category": product["category"],
                "price_inr": product["price_inr"],
                "stock": product["stock"],
                "rating": product["rating"]
            })

    if not matching_products:
        return {
            "success": False,
            "message": f"No products found matching '{query}'.",
            "products": []
        }

    return {
        "success": True,
        "message": f"Found {len(matching_products)} matching products.",
        "products": matching_products
    }

# TOOL 2: Calculate Order Total
def calculate_order_total(product_id: str, quantity: int) -> dict:
    """
    Calculate total order cost and verify stock.

    Args:
        product_id: Unique product ID.
        quantity: Requested quantity.

    Returns:
        Dictionary containing price and order validation.
    """

    if not isinstance(product_id, str) or not product_id.strip():
        return {
            "success": False,
            "message": "Invalid product ID."
        }

    if isinstance(quantity, bool) or not isinstance(quantity, int):
        return {
            "success": False,
            "message": "Quantity must be a whole number."
        }

    if quantity <= 0:
        return {
            "success": False,
            "message": "Quantity must be greater than zero."
        }

    products = load_products()

    selected_product = None
    for product in products:
        if product["id"].lower() == product_id.strip().lower():
            selected_product = product
            break

    # Check whether product exists
    if selected_product is None:
        return {
            "success": False,
            "message": f"Product ID '{product_id}' does not exist."
        }
    available_stock = selected_product["stock"]
    if quantity > available_stock:
        return {
            "success": False,
            "message": (
                f"Insufficient stock for {selected_product['name']}. "
                f"Requested: {quantity}, Available: {available_stock}."
            ),
            "product_id": selected_product["id"],
            "requested_quantity": quantity,
            "available_stock": available_stock
        }
    unit_price = selected_product["price_inr"]
    total_cost = unit_price * quantity

    return {
        "success": True,
        "message": "Order calculation successful.",
        "product_id": selected_product["id"],
        "product_name": selected_product["name"],
        "unit_price": unit_price,
        "quantity": quantity,
        "total_cost": total_cost,
        "available_stock": available_stock,
        "rating": selected_product["rating"]
    }

# INDEPENDENT TOOL TESTING

if __name__ == "__main__":

    print("\n========== TOOL 1: SEARCH PRODUCTS ==========\n")

    result = search_products("Laptop")

    print(json.dumps(result, indent=4))

    print("\n========== TOOL 2: CALCULATE ORDER TOTAL ==========\n")

    result = calculate_order_total("P101", 2)

    print(json.dumps(result, indent=4))
