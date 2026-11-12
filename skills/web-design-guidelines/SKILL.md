---
name: web-design-guidelines
description: >-
  Review UI code for Web Interface Guidelines compliance. Use when asked to
  review UI, check accessibility, audit design, review UX, or check a site
  against web best practices.
allowed-tools: Read, Grep, Glob, WebFetch, TodoWrite
---

# Web design guidelines

Review files for compliance with Vercel Web Interface Guidelines.

Source: [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) (`web-design-guidelines`).

## How it works

1. Fetch the latest guidelines from the source URL below
2. Read the specified files (or ask for files/pattern)
3. Check against all rules in the fetched guidelines
4. Output findings in the terse `file:line` format from the guidelines

## Guidelines source

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
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

- **docs-writer** — document UI standards after review
- **code-review** — fold blocking a11y/UX issues into PR review
