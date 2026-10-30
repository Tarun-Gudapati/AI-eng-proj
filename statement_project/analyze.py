import csv



def parse_amount(text):
    amount=text.replace("$","").replace(",","").strip()
    if text.startswith("("):
        amount=amount.replace("(","-").replace(")","")
    try:
        return float(amount)
    except ValueError:
        return None
    



def load_transactions(path):
    """Read the CSV with csv.DictReader. For each row, build a dict with the same
    keys as Level 4 (date, desc, amount, category).
    Use parse_amount for the amount. Skip rows where it returns None."""
    with open(path,mode="r",encoding="utf-8")as file:
        reader=csv.DictReader(file)
        statement=[]
        for row in reader:
            amount=parse_amount(row["amount"])
            if amount is None:continue
            
            each_stmnt={"date":row["date"].strip(),"description":row["description"].strip(),"amount":amount,"category":row["category"]}
            statement.append(each_stmnt)
        return statement

    

def total_by_category(txns):
    total_by_cat={}
    for txn in txns:
        category=txn["category"]
        amount=txn["amount"]
        total_by_cat[category]=total_by_cat.get(category,0)+amount
    return total_by_cat



def main():
    txns = load_transactions("statement.csv")
    print(f"Loaded {len(txns)} transactions")
    print(total_by_category(txns))


if __name__ == "__main__":
    main()
