# Monday Nov 2 (Week 3, Night 1): finish Week 2 first

Tonight closes the open Week 2 items before new Week 3 work. Finishing beats starting.
First step at 5:00: read this file, then start Block 1 at 5:10 sharp.

---

## Block 1 (5:10 to 5:40): DSA, Group Anagrams

Input: `["eat", "tea", "tan", "ate", "nat", "bat"]`
Output: `[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]`, in any order.

The idea: every word in a group must produce **the same dict key**.
- Question 1: what do "eat", "tea" and "ate" have in common that "tan" doesn't? Turn that into a key.
- Question 2: a list can't be a dict key in Python. Why not, and what can you use instead?
  Hint: `tuple(...)`, or join the letters back into a string.
- Store `key -> list of words`, then return the dict's values.
- Helpful: `from collections import defaultdict`, then `groups = defaultdict(list)`.

Before coding, say the time complexity out loud. If each word has length k and there are n words, what does sorting each word cost?

---

## Block 2 (5:50 to 7:05): CabDemo CHECK constraint, then isolation levels

### Part 1 (35 min): the CHECK constraint

**What a CHECK constraint is:** a yes-or-no question the database asks about **every row**,
on every insert and update. If the answer is no, it refuses the change.
You already have one: `ride_status BETWEEN 1 AND 6`. That asks: "is the status a number from 1 to 6?"

**Tonight's rule:** the status and the driver must agree.

| Status | `driver_id` must be |
|---|---|
| 1 Requested | NULL (nobody has accepted yet) |
| 2 Accepted, 3 Ongoing, 4 Completed | NOT NULL (somebody has it) |
| 5 Cancelled, 6 Expired | either (it could be cancelled before or after an accept) |

The CHECK is one question made of **three "or" parts**, one for each row of that table.
A ride passes if **any** part is true:

```
(status is 1            AND driver_id IS NULL)
OR (status is 2, 3 or 4 AND driver_id IS NOT NULL)
OR (status is 5 or 6)
```

Turn that into SQL yourself. The shape:
`ALTER TABLE Ride ADD CONSTRAINT CK_Ride_Driver_Status CHECK ( (...) OR (...) OR (...) );`

Steps:
1. First fix the bad row: ride 4 is Requested but has driver 1. Set its `driver_id` to NULL.
   (Otherwise the `ALTER` fails, because a row already breaks the rule.)
2. Add the constraint.
3. Test it. Each of these should **fail**:
   - insert a Requested ride (status 1) **with** a driver
   - update a ride to Accepted (status 2) **without** setting a driver
4. And this should **work**: insert a Requested ride with no driver, for a rider with no active ride.

Say it out loud: "Each rule guards one thing. The unique index guards *only one active ride*. The CHECK guards *the status and the driver agree*."

### Part 2 (35 min): isolation levels, seen with your own eyes

Yesterday you saw window 2 **wait** for window 1's lock. Tonight you see what happens when it **doesn't** wait.

1. **Window 1:**
   `BEGIN TRAN;` then `UPDATE Ride SET pickup_location = 'FAKE' WHERE id = 2;`. Don't commit.
2. **Window 2:**
   `SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;` then `SELECT * FROM Ride WHERE id = 2;`
   Predict first: does it wait, like yesterday? What does it show?
3. **Window 1:** `ROLLBACK;`
4. **Window 2:** run the `SELECT` again. What changed?

What you just saw is called a **dirty read**: window 2 read data that was never real.
`READ COMMITTED` is the default level, and it's why yesterday's window 2 waited instead of reading half-done work.

Then read questions 13 and 14 in `notes\system_design_questions.md` (ACID and isolation levels).

---

## Block 3 (8:00 to 9:15): finish the upload feature

Start the server:

```
cd "c:\Learn stuff\python\statement_api"
.venv\Scripts\activate.bat
uvicorn main:app --reload
```

Fix the **two failures** you found:
- a **PNG** crashes with a 500
- a `.txt` file with **one line** returns a silent 200 with `loaded: 0`; with **several lines**, it crashes with a 500

Steps:
1. `from fastapi import HTTPException`, then `raise HTTPException(status_code=400, detail="...")` for bad input.
2. Wrap the `decode` line in `try` / `except` (use the exception name from the PNG traceback).
3. After making the reader, check `reader.fieldnames` contains `date`, `description`, `amount` and `category`.
   If any are missing, return a 400 that **names the missing columns**.
4. Test all three files in `/docs`: the real CSV (200), the PNG (400) and the `.txt` (400).

Then write `statement_api\test_main.py`:
- `pip install pytest`
- `from fastapi.testclient import TestClient`, then `client = TestClient(app)`
- CSV path: `Path(__file__).parent.parent / "statement_project" / "statement.csv"`
- Test 1: upload the CSV and assert status 200, `loaded == 9` and `skipped == 1`
- Test 2: upload `b"not,a,statement"` and assert status 400
- Run `pytest` from inside `statement_api`

When both pass, commit and push (your personal GitHub account should still be active).

---

## Block 4 (9:20 to 9:50): say it out loud

1. Say the AI assessment pitch **in your own words**, without reading. Record it on your phone.
2. Listen once. Did it have all 5 parts: problem, what you built, one hard decision, result, what you'd do better?
3. Re-record once.

---

## At work tomorrow (office hours, not study time)

Find the real numbers for the pitch's [brackets]:
- how many applications the feature runs on, per week
- roughly how long an assessor used to spend writing client questions, per application
- how many flagged budget rows get resolved automatically from client answers

---

## 9:50: shut down

Tick the site. Write 3 lines and tomorrow's first step. Stop at 10.
