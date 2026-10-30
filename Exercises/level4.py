
TRANSACTIONS = [
    {"date": "2026-08-01", "desc": "Salary", "amount": 5200.00, "category": "income"},
    {"date": "2026-08-02", "desc": "Rent", "amount": -1800.00, "category": "housing"},
    {"date": "2026-08-05", "desc": "Woolworths", "amount": -142.50, "category": "groceries"},
    {"date": "2026-08-09", "desc": "Uber", "amount": -23.40, "category": "transport"},
    {"date": "2026-08-15", "desc": "Coles", "amount": -98.10, "category": "groceries"},
    {"date": "2026-09-01", "desc": "Salary", "amount": 5200.00, "category": "income"},
    {"date": "2026-09-02", "desc": "Rent", "amount": -1800.00, "category": "housing"},
    {"date": "2026-09-12", "desc": "Sportsbet", "amount": -400.00, "category": "gambling"},
    {"date": "2026-09-20", "desc": "Woolworths", "amount": -160.00, "category": "groceries"},
]

def total_by_category(txns):
    total_by_cat={}
    for txn in txns:
        category=txn["category"]
        amount=txn["amount"]
        total_by_cat[category]=total_by_cat.get(category,0)+amount
    return total_by_cat


def largest_expense(txns):
    trans=[txn["desc"] for txn in txns if txn["amount"]<0]
    for txn in txns: 
        if txn["amount"]<0:
            trans.append(txn["desc"])
    return min(trans,key=lambda x: txn["amount"])


def running_balance(txns, opening):
    balance=[]
    #balance.append(opening)
    for txn in txns:
        opening+=txn["amount"]
        balance.append(round(opening,2))
    return balance


def monthly_net(txns):
    monthly_trans={}
    for txn in txns:
        date=txn["date"][0:7]
        monthly_trans[date]=monthly_trans.get(date,0)+txn["amount"]
    return monthly_trans


def gambling_descs(txns):
    gambling_desc=[]
    for txn in txns:
        if txn["category"]=="gambling":
            gambling_desc.append(txn["desc"])
    return gambling_desc


def expense_ratio(txns):
    expense=0
    income=0
    for txn in txns:            
        if txn["category"]=="income":
            income+=txn["amount"]
        else:
            expense+=txn["amount"]
    return round(abs(expense)/income,2)


t = TRANSACTIONS
assert total_by_category(t)["groceries"] == -400.6
assert total_by_category(t)["income"] == 10400.0
assert largest_expense(t) == "Rent"
assert running_balance(t, 1000)[:3] == [6200.0, 4400.0, 4257.5]
assert running_balance(t, 1000)[-1] == 6976.0
assert monthly_net(t) == {"2026-08": 3136.0, "2026-09": 2840.0}
assert gambling_descs(t) == ["Sportsbet"]
assert expense_ratio(t) == 0.43
print("Level 4 passed")
