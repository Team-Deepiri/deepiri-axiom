---
name: writing-guidelines
description: >-
  Review docs/prose for Writing Guidelines compliance. Use when asked to review
  docs, check writing style, audit prose, review voice and tone, or check a
  page against a writing handbook.
allowed-tools: Read, Grep, Glob, WebFetch, TodoWrite
---

# Writing guidelines

Review files for compliance with Vercel Writing Guidelines.

Source: [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) (`writing-guidelines`).

## How it works

1. Fetch the latest guidelines from the source URL below
2. Read the specified files (or ask for files/pattern)
3. Check against all rules in the fetched guidelines
4. Output findings in the terse `file:line` format from the guidelines

## Guidelines source

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/writing-guidelines/main/command.md
```

Use WebFetch to retrieve the latest rules. The fetched content has all rules and output format instructions.

## Usage

When the user provides a file or pattern:

1. Fetch guidelines from the URL above
2. Read the specified files
3. Apply all rules from the fetched guidelines
4. Output findings using the format specified in the guidelines

If no files specified, ask which files to review.

## Handoff

- **docs-writer** — apply fixes in Elomix docs paths
- **changelog-writer** / **pr-writer** — tone pass on release or PR copy
