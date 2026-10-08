---
name: quick-recap
description: >-
  Red/yellow/green final status block for agent responses. Use when adding or
  following a clear completion-state convention at the end of work.
allowed-tools: Read, Write
---

# Quick recap

Make completion state obvious at the end of every response that finishes a unit of work.

Source: [BuilderIO/skills](https://github.com/BuilderIO/skills) (`quick-recap`). MIT.

## Status block

End with exactly:

```md
🟢 Actual concise status sentence
```

Rules:

- Under 100 characters
- `🟢` — requested work finished
- `🟡` — non-routine follow-up remains; name the pending item
- `🔴` — blocked on user input
- Status line is the very last content (no `---` or text after)

## Examples

```md
🟢 Updated quick recap docs with output examples
```

```md
🟡 Code updated, set PROVIDER_WEBHOOK_SECRET before testing webhooks
```

```md
🔴 Need the production API key to continue
```

Choose status from the user's perspective: finished, pending a specific non-routine step, or blocked.

## Axiom note

Upstream installers optionally inject this into `AGENTS.md` / `CLAUDE.md`. Here it is a skill — apply when invoked or when the user asks for the convention.
