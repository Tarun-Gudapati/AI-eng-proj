from pathlib import Path

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

CSV_PATH = Path(__file__).parent.parent / "statement_project" / "statement.csv"


def test_analyze_csv():
    with open(CSV_PATH, "rb") as f:
        response = client.post("/analyze", files={"file": ("statement.csv", f.read())})

    assert response.status_code == 200
    body = response.json()
    assert body["loaded"] == 9
    assert body["skipped"] == 1


def test_analyze_bad_file():
    response = client.post("/analyze", files={"file": ("bad.csv", b"invalid data")})

    assert response.status_code == 400