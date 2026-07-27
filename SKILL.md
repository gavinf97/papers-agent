---
name: papers-agent
description: >
  Weekly literature-monitoring skill for AI/ML best practices in the life sciences
  (DOME/reporting standards, research infrastructure, meta-research, templates and
  guidelines, literature-focused meta-research, open science, big AI/ML infrastructure,
  frontier models, biological/scientific LLMs). Checks Nature, Nature Methods, Nature
  Machine Intelligence, Science, Bioinformatics, Nature Scientific Data, PLOS
  Computational Biology, and PLOS Biology for new relevant papers since the last run,
  logs DOI links to a dated file for provenance, and reports a clickable DOI list back
  to the user. Trigger on "run the papers agent", "check for new papers", "weekly
  literature check", "any new papers this week", "/papers-agent", or when a scheduled
  weekly routine fires this skill. Not for one-off searches on a specific topic or
  paper — use general web search for that instead.
---

# papers-agent

Thin orchestrator. Deterministic work (API calls, date math) happens in
`scripts/`; semantic filtering and writing the log happens in the dedicated
`paper-scout` subagent — do not do the filtering yourself, delegate it, to keep this
session's context and token cost small.

## Steps

1. **Read state.** Run:
   ```bash
   python3 scripts/state.py read
   ```
   This gives `last_run_date` and the current `seen_dois` list.

2. **Compute the date window.**
   - `until` = today (YYYY-MM-DD).
   - `since` = `last_run_date` if set, otherwise `until` minus 7 days (first run).
   - If `since == until` (already ran today), still proceed — the window will just be
     small/empty, which is cheap.

3. **Fetch candidates.** Run, from the repo root:
   ```bash
   python3 scripts/fetch_recent_papers.py --since <since> --until <until> \
     --out state/.last_fetch.json --exclude-dois "<comma-joined seen_dois>"
   ```
   This writes trimmed JSON (title/doi/journal/date/abstract, ≤500-char abstracts) to
   `state/.last_fetch.json` and prints just a count — the full payload never enters
   your own context.

4. **Delegate filtering + logging.** Invoke the `paper-scout` subagent (Agent tool,
   `subagent_type: paper-scout`) with a prompt giving it:
   - The path to `state/.last_fetch.json`.
   - The `since` / `until` dates.
   - The repo root path (so it can find `references/topics.md`, `logs/`, and
     `scripts/state.py`).

   Run it in the foreground (`run_in_background: false`) — you need its result before
   you can report back to the user in this same turn.

5. **Report to the user.** Take the subagent's compact `LOG:` / `KEPT:` / bullet-list
   output and present it directly: the date range checked, how many were kept, and the
   DOI links as clickable markdown (`https://doi.org/<doi>`). Mention the log file
   path for provenance. Keep this short — the subagent already did the work, you're
   just relaying it.

6. **Clean up.** Delete `state/.last_fetch.json` (it's a scratch file, not meant to be
   committed) once the subagent has read it.

## Notes

- Never call the Europe PMC API yourself for ad-hoc topic searches — this skill is
  specifically the weekly monitoring job. For a one-off "find me papers about X" ask,
  use ordinary web search instead.
- If `fetch_recent_papers.py` fails (network error, API down), report that plainly to
  the user and do not update state — the next run should retry the same window.
