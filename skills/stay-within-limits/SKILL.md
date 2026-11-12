---
name: stay-within-limits
description: >-
  Long-running or parallel agent work that must respect usage budgets: check
  usage between waves, pause near the cap (~95%), resume only when the window
  is clear enough to continue.
allowed-tools: Bash, Read, TodoWrite
---

# Stay within limits

Keep long-running work inside the host's usage windows (e.g. 5-hour and weekly). Check before substantial work and between parallel waves. At ≥95% of an active window, pause new launches until safe to continue.

Source: [BuilderIO/skills](https://github.com/BuilderIO/skills) (`stay-within-limits`). MIT.

## Core loop

1. Bounded wave — default ≤3 parallel subagents unless told otherwise
2. Wait for the wave to finish (don't kill in-flight work just to save budget)
3. Check current usage with the host's budget/usage tool
4. If ≥95% on any active window — stop new work; schedule a self-contained resume
5. On resume, re-check the real window (do not trust wall-clock alone)

## Usage signals

Prefer a first-party host usage tool when available.

Claude Code example:

```bash
npx -y ccusage@latest blocks --active --json
```

Use active block start, cost/percentage, and time remaining. A new block-start timestamp beats "enough time passed."

If only cost is reported, map through the known account limit. User-configured earlier caution thresholds are fine; default stop remains **95%**.

Cursor / other hosts: use whatever usage/billing UI or CLI the environment provides; same pause/resume rules apply.

## Pausing and resuming

When a wake/resume tool exists, schedule:

```txt
min(3600, secondsUntilWindowClears)
```

Chain wakeups for longer waits. Each wakeup: re-check usage → reschedule if still hot → continue only when safely below threshold.

Wake prompts must be self-contained: remaining plan, 95% rule, wave throttle, usage command, previous window id, next verification, next handoff packets.

## Choosing wait mechanism

- Wake/resume tool — instructions attached to future resume
- Background sleep/watcher — fixed timers / observable process events
- Cron — only for recurring fresh-session work

Avoid short-interval polling for events the host already notifies. Prompt-cache miss after a long sleep is acceptable; preserving the limit matters more.

## Reporting

On pause: which window, observed usage, next check time, remaining work. Enough state that the next turn resumes without conversation momentum.

## Handoff

- **efficient-frontier** — throttle parallel waves under budget
- **quick-recap** — 🟡 when paused on budget
