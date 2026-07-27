# papers-agent

A weekly literature-monitoring skill for AI/ML best practices in the life sciences:
DOME/reporting standards, research infrastructure, meta-research, templates and
guidelines, literature-focused meta-research, open science, big AI/ML
infrastructure, frontier models, and biological/scientific LLMs.

## What it does

Once a week it checks **Nature, Nature Methods, Nature Machine Intelligence,
Science, Bioinformatics, Nature Scientific Data, PLOS Computational Biology, and
PLOS Biology** for papers published since the last run, filters them against the
taxonomy in [`references/topics.md`](references/topics.md), and:

- Writes `logs/<date>.md` — a dated, git-tracked record of DOI links for provenance.
- Reports the same list back as clickable `https://doi.org/...` links.

State (`state/state.json`) tracks the last run date and recently-seen DOIs, so each
run only queries the days since the previous run and never re-reports the same paper.

## How it's wired up

- `SKILL.md` — thin orchestrator (state → date window → fetch → delegate → report).
- `agents/paper-scout.md` — dedicated subagent that filters candidates and writes
  the log; runs on a cheap model since the task is mechanical.
- `scripts/fetch_recent_papers.py` — single combined Europe PMC API query per run
  (stdlib only, no dependencies).
- `scripts/state.py` — reads/updates `state/state.json`.

Symlinked into `~/.claude/skills/papers-agent` and `~/.claude/agents/paper-scout.md`
so both are available as a Claude Code skill/subagent from any session.

## Running it manually

From within a Claude Code session: `/papers-agent`, or just ask "check for new
papers this week".

## Weekly automation

A scheduled cloud routine (set up via the `schedule` skill) triggers this weekly so
it runs without a live session. Since that routine runs in an isolated environment,
it works against this repo's GitHub remote rather than local state.

## Editing the scope

- Journals: edit the `JOURNALS` list in `scripts/fetch_recent_papers.py`.
- Topics/relevance criteria: edit `references/topics.md` — no code changes needed.
