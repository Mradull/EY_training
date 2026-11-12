
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "returns.json"


def load_return_requests():

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Returns file not found: {DATA_FILE}"
        )

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        requests = json.load(file)

    if not isinstance(requests, list):
        raise ValueError("Expected a JSON list.")

    required_fields = [
        "request_id",
        "order_id",
        "product",
        "amount_inr",
        "days_since_delivery",
        "item_condition",
        "invoice_available",
        "photo_evidence_available",
        "previous_returns_90_days",
    ]

    for request in requests:
        missing = [
            field for field in required_fields
            if field not in request
        ]

        if missing:
            raise ValueError(
                f"{request.get('request_id', 'Unknown')}: "
                f"Missing fields: {missing}"
            )

    print(f"Successfully loaded {len(requests)} requests.")

    return requests


if __name__ == "__main__":
    records = load_return_requests()

    for record in records:
        print(
            record["request_id"],
            record["product"],
            record["amount_inr"]
        )
