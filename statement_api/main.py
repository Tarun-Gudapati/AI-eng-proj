import csv
import io

from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

from analysis import parse_amount, total_by_category


class Transaction(BaseModel):
    amount: float
    description: str
    date: str
    category: str


app = FastAPI()


@app.post("/transactions")
def create_transaction(transaction: Transaction):
    return {"received": transaction, "is_expense": transaction.amount < 0}


@app.get("/")
def hello():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello {name}"}


@app.post("/analyze")
async def analyze(file: UploadFile):
    # 1. Read the uploaded file's bytes and decode them to text.
    content = await file.read()
    text = content.decode("utf-8")

    # 2. Make a csv.DictReader over that text.
    reader = csv.DictReader(io.StringIO(text))

    # 3. For each row: parse the amount first. Skip rows we cannot read.
    txns = []
    skipped = 0
    for row in reader:
        amount = parse_amount(row["amount"])
        if amount is None:
            skipped += 1
            continue
        txns.append(
            {
                "date": row["date"].strip(),
                "description": row["description"].strip(),
                "amount": amount,
                "category": row["category"].strip(),
            }
        )

    # 4. Return the counts and the totals.
    return {
        "loaded": len(txns),
        "skipped": skipped,
        "totals": total_by_category(txns),
    }
