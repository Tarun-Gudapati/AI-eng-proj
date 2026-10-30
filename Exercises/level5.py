class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount<=0:
           raise ValueError("Deposit should be higher than 0")
        self.balance += amount


    def withdraw(self, amount):
        """Raise ValueError if amount <= 0 or more than the balance."""
        if amount<=0:
           raise ValueError("withdraw should be higher than 0")
        if self.balance<amount :
            raise ValueError("insufficient balance")
        self.balance -= amount
        return f"withdrawn amount :{amount}\nremaining balance : {self.balance}"

    def __repr__(self):
        return f"BankAccount(owner={self.owner!r}, balance={self.balance})"
        


# def parse_amount(text):
#     """Parse amounts the way they show up on bank statements:
#     '$1,234.50' -> 1234.5, '(200.00)' -> -200.0 (brackets mean negative),
#     '-75' -> -75.0, anything unparseable -> None. Use try/except ValueError."""
#     pass


acc = BankAccount("Tarun", 100)
acc.deposit(50)
assert acc.balance == 150
try:
    acc.withdraw(500)
    assert False, "withdraw should have raised"
except ValueError:
    pass
assert acc.balance == 150
assert repr(acc) == "BankAccount(owner='Tarun', balance=150)"

# assert parse_amount("$1,234.50") == 1234.5
# assert parse_amount("(200.00)") == -200.0
# assert parse_amount("-75") == -75.0
# assert parse_amount("abc") is None
print("Level 5 passed")
