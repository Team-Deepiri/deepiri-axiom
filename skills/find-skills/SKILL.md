---
name: find-skills
description: >-
  Discover and install agent skills when the user asks "how do I do X",
  "find a skill for X", "is there a skill that can…", or wants to extend
  capabilities beyond the Axiom catalog.
allowed-tools: Bash, WebSearch, WebFetch, Read
---

# Find skills

Discover skills from the open agent skills ecosystem (`npx skills` / [skills.sh](https://skills.sh/)).

Source: [vercel-labs/skills](https://github.com/vercel-labs/skills) (`find-skills`).

## When to use

- "How do I do X" where X might have an existing skill
- "Find a skill for X" / "is there a skill for…"
- Interest in extending agent capabilities (design, testing, deploy, etc.)

## Before searching externally

1. Check the **Axiom catalog** — `skills/README.md` and installed skills
2. Prefer an existing Axiom skill when it already covers the job

## Skills CLI

```bash
npx skills find [query] [--owner <owner>]
npx skills add <package>
npx skills update
```

Browse: https://skills.sh/

## Workflow

1. **Need** — domain + specific task
2. **Leaderboard** — check [skills.sh](https://skills.sh/) for popular options first
3. **Search** — `npx skills find [query]` if needed
4. **Verify** — prefer 1K+ installs; trusted sources (`vercel-labs`, `anthropics`, …); treat low-star repos cautiously
5. **Present** — name, what it does, install count/source, install command, skills.sh link
6. **Install** (if asked) — `npx skills add <owner/repo@skill> -g -y`

Example:

```
npx skills add vercel-labs/agent-skills@react-best-practices
# https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

## Search tips

| Category | Example queries |
|----------|-----------------|
| Web | react, nextjs, typescript, css |
| Testing | jest, playwright, e2e |
| DevOps | deploy, docker, kubernetes, ci-cd |
| Docs | readme, changelog, api-docs |
| Quality | review, lint, refactor |
| Design | ui, accessibility, design-system |

If nothing fits: help directly, or suggest `npx skills init my-skill`.

## Axiom note

Skills added via `npx skills` land in agent skill dirs. Axiom catalog skills live in `skills/<name>/SKILL.md` and install via `./install.sh install`.
