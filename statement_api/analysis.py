def parse_amount(text):
    """'$1,234.50' -> 1234.5, '(200.00)' -> -200.0, '-75' -> -75.0,
    anything unparseable -> None."""
    amount = text.replace("$", "").replace(",", "").strip()
    if text.strip().startswith("("):
        amount = amount.replace("(", "-").replace(")", "")
    try:
        return float(amount)
    except ValueError:
        return None


def total_by_category(txns):
    total_by_cat = {}
    for txn in txns:
        category = txn["category"]
        amount = txn["amount"]
        total_by_cat[category] = total_by_cat.get(category, 0) + amount
    return total_by_cat
