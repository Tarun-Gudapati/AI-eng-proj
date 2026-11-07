---
name: study-plan-session
description: Runs Tarun's study-plan sessions in the "c:\Learn stuff\python" workspace. Covers starting a chat with the full plan context, answering "what's next" or "where did we stop", writing tomorrow's night note, updating the tracker site (ai-engineer-roadmap data.js), and the end-of-session handover into notes/STATE.md. Use when he says take in, what's next, where did we stop, gimme the note for tomorrow, update the site, what to tick, good night, or questions the plan, a block, or the order of topics.
---

# Study plan session

## Start of a chat, or "what's next"

1. Read `notes/STATE.md`.
2. Read the newest night note in `notes/` (`<weekday>_<month><day>.md`).
3. Read the current week in `C:\Learn stuff\ai-engineer-roadmap\data.js` (weeks start Monday;
   Week 3 starts 2026-11-02).
4. For "where did we stop", also search the newest past chat for the last few user messages.
5. Answer from these files. Say which file a fact came from when it matters.

## When he questions the plan

1. Find the matching decision in STATE.md ("Decisions, and why"). Check `data.js` too: the
   answer is often already planned in a later week or on a Saturday.
2. Tell him what is already planned, and where. Then give your honest view, including what
   the plan is missing.
3. If he agrees to a change, edit `data.js`, add the decision with its date and reason to
   STATE.md, and commit and push both.

## Writing tomorrow's note

- File: `notes/<weekday>_<month><day>.md`, for example `tuesday_nov3.md`.
- Use the same shape as `notes/monday_nov2.md`: a title with the week and night, one line on
  the night's goal, then Block 1 to Block 4 with the times from `data.js` `evening`,
  "At work tomorrow", and "9:50: shut down".
- Take the tasks from the next unfinished night in `data.js`. Open items from STATE.md come first
  ("finishing beats starting").
- Give hints and questions, not solutions. Each block ends with something to say out loud,
  run or test.
- Keep the company name, internal project names and colleagues out. The notes folder is public.

## Updating the tracker site

- Edit `data.js` only. Ticks are saved in the browser and keyed by week, night and track, and
  Saturday items by position. So don't reorder or delete Saturday items in a week he has
  already ticked. Add new items at the end.
- Commit and push from `C:\Learn stuff\ai-engineer-roadmap` with the personal Tarun-Gudapati
  account. The repo's local config already sets the author. Don't use the work GitHub
  account here.
- He can't tick for himself through you. Tell him exactly what to tick: the week, the night
  and the track.

## End of session (always, even when he only says "good night")

Give him a short verdict (what he did well, what he did wrong, tomorrow's first step), then
update `notes/STATE.md`:
- Add the verdict at the top of "Session log".
- "Last updated" date and time, and the week and night.
- Move finished items to "Done" and add new open items.
- Add any new decision, with its date and the reason.
- Change the CabDemo section if the schema or data changed (check with `sqlcmd`).

If he wants it pushed, commit STATE.md and the note to `AI-eng-proj`.
