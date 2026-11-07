# Study plan: current state and decisions

The handover file. A new agent reads this first, before it answers anything about the plan.
Update it at the end of every session (see the `study-plan-session` skill).

Last updated: Wed Nov 4, 2026, 6:35 PM (Week 3 Night 2, in progress). Tue Nov 3 was missed.
Tonight so far: the `except` fix is done (catches `UnicodeDecodeError`, friendly message; CSV 200,
PNG 400, `.txt` 400). `pytest` went into global Python by mistake, and he chose to skip the tests
tonight. Now: what-to-say page 1 (`notes/what_to_say/01_lld_parking_lot.md`).

---

## Who and the goal

- Tarun: junior .NET developer (2 years; C#, EF Core, SQL Server, Azure) at a lending platform.
  He is moving into LLM application engineering. His work already has two AI features (an AI
  assessment of bank statements, and an AI transaction categoriser). He knows the work, but not
  the terms or the way interviewers ask about them.
- Goal: interview-ready by **Jan 11, 2027**, then apply (hard limit: end of Feb).
- Priorities he chose: the AI project, system design, DSA in Python, and "say it out loud".
  The DSA he has met in interviews is easy level (loops, hash maps), not graphs or trees.

## Where the plan lives (sources of truth, in order)

1. **This file**: where we are now, what is open, and why the plan looks like it does.
2. **The tracker site**: `C:\Learn stuff\ai-engineer-roadmap\data.js` (live at
   https://tarun-gudapati.github.io/ai-engineer-roadmap/). It has every week, night and Saturday
   task, the evening timetable and the rules. **This is the real plan.**
3. **Tonight's note**: the newest `notes\<weekday>_<month><day>.md` (for example `monday_nov2.md`).
   It turns one night of `data.js` into steps and hints.
4. `roadmap\roadmap.html` and the PDF are the **old, original plan**. They are out of date
   (they still list the loan tracker, the URL shortener and the news feed). Don't plan from them.

The ticks are saved in Tarun's browser (localStorage), so an agent can't see them. Ask him,
or use the "Done" list below.

## The evening shape (study nights Mon to Thu, 5:00 to 10:00)

5:00 start ritual, 5:10 Block 1 DSA (30 min), 5:50 Block 2 system design (70 min, split 35 + 35),
8:00 Block 3 AI project (75 min, he types every line), 9:20 Block 4 say it out loud (30 min),
9:50 shut down (tick the site, write 3 lines and tomorrow's first step), 10:00 hard stop.
Fri off. Sat 10:00 to 12:00: SQL or a mock, the cab app build, then catch-up. Sun: 45 min review.
Night tasks slide; they are not tied to a date.

## Week 2 (Oct 26 to Nov 1): what is done

- DSA: Two Sum, Contains Duplicate, Valid Anagram.
- System design: the Uber map (7 steps, boxes only); the double-booking race; the conditional
  `UPDATE ... WHERE ride_status = 1` with `@@ROWCOUNT`; the two-window lock test in SSMS;
  two unique filtered indexes.
- AI project: ran `/analyze`; read `main.py`; pushed `AI-eng-proj` to GitHub.
- SQL ladder Levels 0 and 1 (SQLBolt).
- Notes written: `system_design_questions.md` (31-question bank, small to big),
  `ai_interview_qa.md` (25 AI interview questions), and a model pitch for the AI assessment
  feature (in the chat, not a file).

## Open now (tonight's note `monday_nov2.md` covers the first four)

1. Done Nov 2: Group Anagrams (sorted-string key; he gave the complexity and why a list can't be a key).
2. Done Nov 2: the CabDemo `CHECK`. **Moved to tomorrow's Block 2:** the dirty-read demo
   (`READ UNCOMMITTED`, two windows), then questions 13 and 14 in `system_design_questions.md`.
3. `statement_api` (Nov 2): the 400s work. A CSV gives 200 (9 and 1), and a PNG or `.txt` gives 400.
   The column check names the missing columns. **Still open, first in the next Block 3:**
   change `except Exception as e` / `detail=str(e)` to `except UnicodeDecodeError` with a
   user-friendly message (he types it); write `test_main.py` with two `pytest` tests; push.
4. Talk (Nov 2): he said the AI assessment pitch once in his own words. Feedback: about 2 times
   too long; say Claude, RAG and prompt caching clearly; the result numbers are unclear
   (check "reduced by" versus "reduced to"); the dynamic-question UI must be described as
   structured output plus typed inputs; add a "what I'd do better" point; prepare "how did you
   measure accuracy". The RAG versus prompt-caching decision (84% cache hit rate) is the strong
   part. **Next:** re-record using the 5-part, 2-minute shape.
5. Still open from Week 2: re-solve Two Sum from memory; the library console app in C#
   (lists inside the service). Week 3 Night 4 needs it (move the lists into a repository).
6. Week 3 Night 1 tasks pushed back by tonight's catch-up: Top K Frequent; Anthropic SDK and
   the first hello call (key in `.env`); the categoriser pitch.
7. At work: the real numbers for the pitch's [brackets] (applications per week, assessor time
   per application, budget rows resolved automatically).

## CabDemo (LocalDB) right now

`(localdb)\MSSQLLocalDB`, database `CabDemo`, tables `Rider`, `Driver`, `Ride`.
`Ride`: `id, rider_id (NOT NULL, FK), pickup_location, drop_location, requested_time,
ride_status (CHECK 1 to 6), driver_id (NULL, FK)`.
Status codes: 1 Requested, 2 Accepted, 3 Ongoing, 4 Completed, 5 Cancelled, 6 Expired.
Indexes: `UX_Ride_Driver_Active` (driver_id where status in 2, 3) and `UX_Ride_Rider_Active`
(rider_id where status in 1, 2, 3).
CHECK `ck_ride_driver_status` (added Nov 2): status 1 needs no driver, 2 to 4 need a driver,
5 and 6 allow either. Ride 4 was fixed to status 1 with no driver. He skipped the three tests.
Read it with `sqlcmd -S "(localdb)\MSSQLLocalDB" -d CabDemo -Q "..."`.

## Decisions, and why (read this before you suggest a new plan)

- **Oct 29: map first, then zoom in.** He asked whether to start with the whole Uber design.
  Decision: draw the full map with boxes only, then go deep on one box each week. Week 7 redoes
  the full cab HLD with real depth. Reason: boxes without depth fail the follow-up questions,
  which is what happened in the Oct 24 interview's cab-booking paper round.
- **Nov 1: the cab system is one continuous build.** It started small (3 tables, SQL first in
  CabDemo), and it grows on Saturdays, weeks 3 to 7, in C#:
  W3 console app + EF Core + `RideService.AcceptAsync` with `ExecuteUpdateAsync` (rows affected
  == 1); W4 two tasks accept at once (only one wins), filtered indexes in `OnModelCreating`,
  idempotency key; W5 Redis for driver locations (`GEOADD`, `GEOSEARCH`); W6 ASP.NET minimal
  API (`POST /rides`, `POST /rides/{id}/accept`, `GET /rides/{id}`); W7 outbox + background
  worker, and Mock 2 presents the design using the running app.
  Reason: he wanted to code (EF Core, models, services) and not only draw boxes. A running app
  makes the diagrams defensible.
- **Separate design cases for variety:** LLD library app (W2 to W3), parking lot (W4), rate
  limiter (W8), notification system (W8), loan application system (W9), RAG pipeline (W9),
  LLM gateway (W10), agent design (W11), then mocks.
- **Nov 2: "continuous build or small systems that get bigger?"** The plan already does both:
  the cab app is the continuous build, and the cases above give variety. The gap he raised:
  after the cab app, the HLD cases are diagram and talk only, with no typed code. Offered: add a
  45-minute typed build to those cases (2 tables, 2 endpoints, 1 test). **Not decided yet.**
- **Nov 4: two speeds (he chose it).** He felt we were "hovering over a small bubble" (3 nights on
  the 400 fix, 20 minutes on venv and pip) while an interview could come any day. Decision:
  1. **Breadth first:** a one-page "what to say" sheet for every interview topic, in
     `notes/what_to_say/`. He reads it, says it out loud, then the agent grills him. Schedule
     (first half of Block 2, also in `data.js`): 1 LLD method + parking lot (W3N2, written),
     2 library LLD (W3N3), 3 AI engineer core (W3N4), 4 concurrency and data (W4N1),
     5 HLD method + building blocks (W4N2), 6 cab booking HLD (W4N3), 7 rate limiter +
     notifications (W4N4), 8 project and work stories (W5N1). Target: all 8 by about Nov 16.
  2. **Builds stay, but short:** he types the logic (queries, services, tests); the agent does
     the plumbing (venv, installs, config) without asking him to. Stuck 10 minutes: "show me".
  3. Folded into page 4: idempotency, retries. Dropped as separate nights: delivery guarantees.
  Reason: keywords get first rounds, but the follow-ups need the builds (Oct 24 lesson), and
  higher offers go to people with production numbers (evals).
  Still open: install `pytest` into the venv (agent does it) and he types `test_main.py`.
- **Nov 4 review he asked for: "am I inconsistent?"** Honest answer given: the main problem is
  re-planning mid-week (5 plan debates in 8 days: Oct 28, 29, Nov 1, 2, 4). Each one costs a
  session. Agreed rule: **plan changes only at the Sunday review**; during the week, write the
  question in "For Sunday" below and keep going. He wants to be a "jack of all trades"
  (about 70 to 80% DSA and design); agreed, with one deep thing (his work AI features and the
  project). External roadmaps are used as content inside this plan, not as a replacement
  (the DSA order already follows NeetCode's roadmap).
  He is scared of recursion, trees and harder DSA topics. Be gentle there: small steps, draw
  the call stack (pythontutor.com), watch the NeetCode video first, then solve.
- An existing `C:\Learn stuff\mini projects for LLD\CabBookingService` (ASP.NET, made Oct 24
  for interview prep) and `LoanTracer` (Sep) exist. Ask before you reuse them. The Saturday build
  is meant to be typed by Tarun.

- **Nov 4: the teacher deal (Drona and Arjuna).** He asked the agent to be the strictest,
  best teacher it can be: criticize him directly, give orders not options, and he follows.
  His side: start at 5:00, do the task given, send doubts to the Sunday list. Full stance is in
  `.cursor/rules/study-plan-context.mdc`. Every session ends with a verdict in "Session log".

## Session log (newest first; a verdict for every session)

- **Fri Nov 6 (rest day, his choice), 7:46 to 8:27 PM, for fun: library LLD, first steps.**
  Requirements given (college library; book and copies; students 3 books for 14 days, teachers
  5 for 30; fine of Rs 10 a day; reserve and notify; librarian adds books). He listed the nouns
  and verbs well (missed search and pay). Learned: verbs that leave a record become classes
  (borrow creates `Loan`, like `Ticket` and `Ride`); name records after the event. His `Loan`:
  MemberId, dates, no title or author (normalization, his own idea). Fixed: `CopyId`, not
  `BookId`. He asked whether to store `DueDate`; answer: yes, as a snapshot, because rules
  change and overdue queries stay simple.
  Then Valid Palindrome: correct (regex clean, then two pointers), O(n) time and O(n) space.
  Open: the O(1)-space version (skip with `isalnum()` on the original). Clean-ups: no
  semicolons, the empty-string check isn't needed.
  **Open for page 2:** student versus teacher (enum and rules, or subclasses), the other
  classes and relationships, patterns (Observer for reservation notices, Strategy for fines),
  and the concurrency case (two members reserve the last copy).

- **Thu Nov 5 (W3N3), started 2:06 PM.** Parking lot grill finished, about 7.5/10 overall:
  Q2 classes 7 (retry, from 4), Q3 concurrency 8 (retry, from 5), Q4 patterns 6, Q5 EV
  extension 8 (after his follow-up). He learned: nouns to classes, details to fields, verbs to
  methods; enum when only data differs, interface when behaviour differs; Strategy, Factory,
  Observer; Singleton pattern versus DI lifetime (scoped is fine when state is in the DB);
  config for prices; additive migrations. Repeated gaps: tells a story instead of naming
  classes; reaches for Kafka where a conditional update is enough; forgets to say what doesn't
  change. He said "I don't know" honestly, which is good.
  Then Top K Frequent: correct (count dict, sort pairs by count, take k), O(n log n) after a
  correction (he first said O(n)). Review points: use `get` not `setdefault`, don't reuse `freq`
  for the sorted pairs, use a list comprehension. Bucket-sort O(n) version still open.
  Stopped at 4:42 PM for the gym and lunch (about 2.5 hours, a full night under the smaller plan).
  Verdict: good session; he stayed with hard questions and improved on every retry.
  Slip: `test_main.py` skipped again; it has been put off since Oct 29.
  **Next session starts with:** `test_main.py` + push (first, 15 minutes, no skipping), then the
  dirty-read demo. Fri Nov 6 is off; next is Sat Nov 7, 10:00 (SQL Level 2, cab app build).

- **Wed Nov 4 (W3N2), studied at the office after a full work day, stopped at 7:17 PM.**
  Done: the `except` fix; read page 1 (parking lot); grill Q1 (clarifying questions) 7/10, Q2
  (classes) 4/10 (missed `ParkingSpot`, scoped out the monthly pass the interviewer gave, no
  relationship words). Slip: the first hour went on three plan debates. Not a slip: the 5:19
  start (he was still at work). He apologized; no need. He loved learning from a page and then
  being grilled.
  **Next session starts with:** the Q2 retry (structure, what moves through, money), then grill
  Q3 to Q5 (concurrency, patterns, extensions), 10 minutes. Then Top K Frequent, `test_main.py`
  + push, the dirty-read demo, the pitch re-record, the first Claude call (pick 2 if short on time).

## For Sunday (Nov 8) review

- Resume v1 now (not Week 11), so he can start applying earlier.
- A gentle recursion ramp before trees: sum a list, reverse a string, factorial, then max depth.
- Check the two-speed plan after one week: is the pace right?
- **The plan is too big for his real evenings** (agreed Nov 4). He has never finished a planned
  night, and real evenings give about 2 to 2.5 hours. Proposal: 2 must-dos per night (one 60-minute
  main block rotating design and build, plus 30 minutes of DSA; talk practice is 10 minutes inside
  them). "Done" means the 2 must-dos. Measure real hours for a week; move the goal date 2 to 3
  weeks if needed.
- His preferred way to learn: a "what to say" page, then build it, then get grilled on it.

## Repos, paths and accounts

- `c:\Learn stuff\python` = `github.com/Tarun-Gudapati/AI-eng-proj` (public). It has `Exercises\`
  (Python Levels 1 to 5), `statement_project\` (`analyze.py`, `statement.csv`: 9 loaded, 1
  skipped), `statement_api\` (FastAPI: `main.py`, `analysis.py`), `notes\`, `ai_term_map.md`.
- `C:\Learn stuff\ai-engineer-roadmap` = `github.com/Tarun-Gudapati/ai-engineer-roadmap` (the site).
- Both repos use the **personal Tarun-Gudapati** account. Their local git config already sets the
  author. The work GitHub account is for the company repos only.
- Python: Command Prompt, `statement_api\.venv\Scripts\activate.bat`, then `uvicorn main:app --reload`.
- **Public repos: keep the company name, internal project names and colleagues out of every
  committed file.** Say "work" or "a lending platform".
