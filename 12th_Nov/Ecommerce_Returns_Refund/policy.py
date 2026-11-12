
def evaluate_eligibility(request):

    issues = []
    findings = []

    # Rule 1: Amount must be below ₹25,000
    if request["amount_inr"] >= 25000:
        issues.append(
            "Product amount must be below ₹25,000."
        )
    else:
        findings.append("Product amount is within the limit.")

    # Rule 2: Return must be within 30 days
    days = request["days_since_delivery"]

    if days < 0 or days > 30:
        issues.append(
            "Return request is outside the 30-day return window."
        )
    else:
        findings.append("Return request is within 30 days.")

    # Rule 3: Invoice must be available
    if not request["invoice_available"]:
        issues.append("Customer invoice is missing.")
    else:
        findings.append("Customer invoice is available.")

    # Rule 4: Condition must qualify
    condition = request["item_condition"]

    condition_valid = (
        condition == "UNOPENED"
        or (
            condition == "DAMAGED"
            and request["photo_evidence_available"]
        )
    )

    if not condition_valid:
        issues.append(
            "Item condition does not meet the policy "
            "or supporting photographs are missing."
        )
    else:
        findings.append("Item condition meets the policy.")

    # Rule 5: Fewer than 3 previous returns
    if request["previous_returns_90_days"] >= 3:
        issues.append(
            "Customer has 3 or more previous returns "
            "within 90 days."
        )
    else:
        findings.append(
            "Customer return frequency is within the limit."
        )

    return {
        "eligible": len(issues) == 0,
        "issues": issues,
        "findings": findings
    }


def evaluate_automatic_approval(eligibility, risk):

    return (
        eligibility["eligible"]
        and risk["risk_level"] != "HIGH"
    )



def evaluate_risk(request):

    high_risks = []
    medium_risks = []

    if request["amount_inr"] >= 25000:
        high_risks.append("High-value return request.")

    if request["previous_returns_90_days"] >= 3:
        high_risks.append(
            "Unusually frequent customer returns."
        )

    if not request["invoice_available"]:
        high_risks.append("Invoice evidence is missing.")

    if (
        request["item_condition"] == "DAMAGED"
        and not request["photo_evidence_available"]
    ):
        medium_risks.append(
            "Damaged item has no supporting photographs."
        )

    if request["item_condition"] == "USED":
        medium_risks.append(
            "Used item requires additional inspection."
        )

    if request["days_since_delivery"] > 30:
        medium_risks.append(
            "Return request exceeds the standard return window."
        )

    if high_risks:
        risk_level = "HIGH"
    elif medium_risks:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "risk_level": risk_level,
        "high_risks": high_risks,
        "medium_risks": medium_risks
    }
