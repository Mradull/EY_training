import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
BOOKS_FILE = BASE_DIR / "books.json"
RESERVATIONS_FILE = BASE_DIR / "reservations.json"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# TOOL 1: SEARCH BOOKS

def search_books(keyword):
    """
    Search books using title, author, or category.
    Ignores unnecessary words in user queries.
    """

    books = load_json(BOOKS_FILE)

    # Words that do not help identify a book
    stop_words = {
        "search", "find", "show", "me", "books", "book",
        "for", "the", "a", "an", "is", "are", "any",
        "related", "to", "available", "please", "get"
    }

    # Clean the search query
    keyword = keyword.lower().strip()

    keywords = [
        word for word in keyword.split()
        if word not in stop_words
    ]

    matching_books = []

    for book in books:

        searchable_text = (
            book["title"] + " " +
            book["author"] + " " +
            book["category"]
        ).lower()

        # Match all meaningful keywords
        if keywords and all(
            word in searchable_text for word in keywords
        ):

            matching_books.append({
                "id": book["id"],
                "title": book["title"],
                "author": book["author"],
                "category": book["category"],
                "available_copies": book["available_copies"],
                "availability": (
                    "Available"
                    if book["available_copies"] > 0
                    else "Out of stock"
                )
            })

    if not matching_books:
        return {
            "success": False,
            "message": "No matching books found."
        }

    return {
        "success": True,
        "total_results": len(matching_books),
        "books": matching_books
    }

# TOOL 2: RESERVE BOOK

def reserve_book(book_id, customer_name, confirmed=None):
    """
    Reserve a book.
    confirmed=None: ask in terminal (CLI mode).
    confirmed=False: request confirmation from the UI.
    confirmed=True: complete the reservation.
    """

    books = load_json(BOOKS_FILE)
    reservations = load_json(RESERVATIONS_FILE)

    selected_book = next(
        (book for book in books if book["id"] == book_id),
        None
    )

    if selected_book is None:
        return {
            "success": False,
            "message": "Book ID not found."
        }

    if selected_book["available_copies"] <= 0:
        return {
            "success": False,
            "message": f"{selected_book['title']} is currently unavailable."
        }
    reservation_request = {
        "book_id": selected_book["id"],
        "book_title": selected_book["title"],
        "customer_name": customer_name,
        "available_copies": selected_book["available_copies"]
    }

    if confirmed is None:
        print("\n========== RESERVATION DETAILS ==========")
        print("Book:", selected_book["title"])
        print("Customer:", customer_name)
        confirmation = input(
            "\nConfirm reservation? (yes/no): "
        ).strip().lower()

        confirmed = confirmation in ["yes", "y"]
    if confirmed is False:
        return {
            "success": False,
            "requires_confirmation": True,
            "message": "Please confirm this reservation.",
            "reservation_request": reservation_request
        }
    if confirmed is not True:
        return {
            "success": False,
            "message": "Reservation cancelled."
        }
    reservation = {
        "reservation_id": len(reservations) + 1,
        "book_id": selected_book["id"],
        "book_title": selected_book["title"],
        "customer_name": customer_name,
        "reservation_date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "status": "Confirmed"
    }

    reservations.append(reservation)
    selected_book["available_copies"] -= 1

    save_json(BOOKS_FILE, books)
    save_json(RESERVATIONS_FILE, reservations)

    return {
        "success": True,
        "message": "Book reserved successfully!",
        "reservation": reservation,
        "remaining_copies": selected_book["available_copies"]
    }

