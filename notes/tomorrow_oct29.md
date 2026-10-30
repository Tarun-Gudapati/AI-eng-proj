# Thursday Oct 29: tonight's plan

First step at 5:00: start uvicorn (commands are in Block 3 below), then come back to Block 2.

---

## Block 2 (5:50 to 7:05): the Uber map, then race conditions

### Part 1 (35 min): the Uber map, boxes only

Draw it on paper. One or two lines per step. Don't go deep yet.

1. **Requirements:** 4 or 5 rider and driver features, plus 2 rules that must never break (one about drivers, one about riders).
2. **Scale:** one rough guess, for example ride requests per second in one city.
3. **APIs:** about 4 endpoints (request a ride, send a driver's location, accept a ride, get a ride's status).
4. **Data model:** 3 or 4 tables. Which columns decide "who has this ride"?
5. **Boxes:** apps, then a load balancer, then services (rides, locations, notifications), then the database.
6. **Scariest moment:** where can two people collide on the same data?
7. **Deep dive:** that's Part 2.

Stand up for 5 minutes.

### Part 2 (35 min): zoom into "accept ride"

### What a race condition is

A race condition happens when two operations touch the same data at the same time,
and the result depends on **who goes first**. Run it twice and you can get two different results.

The most common shape is **check, then act**:

1. Read the data ("is the ride free?")
2. Decide ("yes, it's free")
3. Write ("I take it")

Between step 1 and step 3 there is a **gap**. Another user can slip into that gap.

C# comparison: it's the same reason `count++` from two threads can lose an increment.
`count++` is really read, add, write.

### The Uber example

Ride 42 has `Status = 'Requested'`. Driver A and Driver B tap **Accept** at the same moment.

Naive code (pseudocode):

```
ride = SELECT * FROM Rides WHERE Id = 42
if ride.Status == 'Requested':
    UPDATE Rides SET Status = 'Accepted', DriverId = @me WHERE Id = 42
    return "You got the ride"
```

Timeline (time goes down):

| Time | Driver A | Driver B |
|---|---|---|
| t1 | reads ride 42: Requested | |
| t2 | | reads ride 42: Requested |
| t3 | "it's free" | "it's free" |
| t4 | writes DriverId = A | |
| t5 | | writes DriverId = B |
| t6 | app shows "You got the ride" | app shows "You got the ride" |

Result: **both** drivers are told they got it. The database says B. A drives to the rider for nothing.
A's write was overwritten. That's called a **lost update**.

The rider side has the same bug: the rider taps "Book" twice and gets **two cabs**.

### How to handle it (smallest fix first)

1. **Make check and act one step: a conditional UPDATE.**
   Put the check inside the `WHERE`. The database runs it as one atomic step.
   Then look at **rows affected**: 1 means you won, 0 means someone else got it first.
   This is the main answer. It needs no locks in your code and works with any number of servers.
2. **Optimistic concurrency (a version number).**
   Add a `rowversion` column. Update `WHERE Id = 42 AND RowVersion = @versionIRead`.
   If someone changed the row since you read it, 0 rows change. In EF Core, mark the column as a
   concurrency token, and EF throws `DbUpdateConcurrencyException`.
   Good when conflicts are rare.
3. **Pessimistic locking.**
   `SELECT ... WITH (UPDLOCK, ROWLOCK)` inside a transaction. The second driver **waits** until the
   first one commits. It's safe, but there's waiting, and deadlocks are possible. Good when conflicts are common.
4. **A database constraint as the last line of defence.**
   A unique filtered index, for example "one driver can have only one accepted ride":
   unique on `DriverId` where `Status = 'Accepted'`. Even if the code has a bug, the database refuses the second row.
5. **Idempotency key for the rider's double tap.**
   The app sends the same request ID twice, and the server creates the ride only once. (This is Week 4.)

**Why a lock in your code is not enough:** C# `lock` or Python `threading.Lock` only works inside
**one process**. With 3 servers behind a load balancer, each server has its own lock, and the race comes back.
That's why the fix lives in the **database** (or in a distributed lock, such as Redis, for non-database cases).

### Say it like this in an interview (30 seconds)

"Accepting a ride is a check-then-act race: two drivers can both read 'Requested' before either writes.
I'd make it atomic with a conditional update, `WHERE Id = @id AND Status = 'Requested'`, and use the rows
affected to tell the driver whether they won. I'd back it with a unique filtered index so the database
rejects a second active ride even if the code has a bug. An in-memory lock wouldn't work, because we run more than one server."

### The small app (you type it): `system_design\race_demo.py`

The goal is to **see** the race happen, then fix it. No database yet.

**Step 1: make the bug.**
- A dict `rides = {42: {"status": "Requested", "driver": None}}`
- A function `accept(driver)` that:
  - reads the status
  - waits `time.sleep(0.1)`, which makes the gap big enough to see
  - if the status was `"Requested"`, sets the status and driver, then prints `f"{driver}: you got the ride"`
- Start two threads, for `"A"` and `"B"`, then print the final ride.
- Hints: `threading.Thread(target=accept, args=("A",))`, then `.start()` on both, then `.join()` on both.
  C#: `Thread` / `Task.Run` plus `Wait`.
- **Before you run it, predict the output.** Then run it. Did both drivers get "you got the ride"?

**Step 2: fix it with a lock.**
- `lock = threading.Lock()`, and wrap the check **and** the write in `with lock:`.
  C#: `lock (obj) { ... }`
- Predict, then run. Only one driver should win now.

**Step 3: answer out loud (no code).**
- Why does this fix break if the app runs on two servers?
- Which line of SQL gives you the same "only one wins" result without any lock?

Done when you can explain the timeline table above in 1 minute without notes.

---

## Block 3 (8:00 to 9:15): finish the statement upload

Start the server (Command Prompt):

```
cd "c:\Learn stuff\python\statement_api"
.venv\Scripts\activate.bat
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs`. Keep that window open.

### Checklist

1. **Run it.** `POST /analyze`, then Try it out, choose `c:\Learn stuff\python\statement_project\statement.csv`, then Execute.
   Expect `loaded: 9`, `skipped: 1`.
2. **Walkthrough.** Read `main.py` and answer the 5 questions. Send me the answers, and I'll grade them.
   - Why `async def` and `await file.read()`?
   - What type are `content` and `text`? What's the C# equivalent of the conversion?
   - What does `io.StringIO(text)` do?
   - What happens if there's no `amount` column?
   - Why doesn't `/analyze` use the `Transaction` model?
3. **Break it, then name the errors.** Upload a PNG, then a `.txt` file with random lines.
   Read the traceback in the uvicorn window. Write down the **exception name** for each one.
4. **Fix it: return a clear 400, not a 500.**
   - Hint: `from fastapi import HTTPException`, then `raise HTTPException(status_code=400, detail="...")`
   - Hint: wrap the decode in `try` / `except <the exception you found>`.
   - Hint: after making the reader, `reader.fieldnames` tells you the column names. Check that
     `date`, `description`, `amount` and `category` are all there.
   - C#: like returning `BadRequest("...")` from a controller instead of letting it throw.
5. **First pytest test:** `statement_api\test_main.py`
   - `pip install pytest` (httpx is already installed)
   - Hint: `from fastapi.testclient import TestClient`, then `client = TestClient(app)`
   - Hint: build the CSV path from the test file, so the test works from any folder:
     `Path(__file__).parent.parent / "statement_project" / "statement.csv"`
   - Hint: `client.post("/analyze", files={"file": ("statement.csv", f, "text/csv")})`
   - Assert status `200`, `loaded == 9`, `skipped == 1`.
   - Second test: upload bytes that aren't a CSV, then assert status `400`.
   - Run it with `pytest` from inside `statement_api`.

**Done** means both tests pass, and `/docs` shows a 400 with your message when you upload a PNG.
That finishes the upload feature. Friday's step is to push it to GitHub.

---

## 9:50: shut-down

Write 3 lines and tomorrow's first step on the roadmap site.
