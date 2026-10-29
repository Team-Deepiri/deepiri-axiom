---
name: read-the-damn-docs
description: >-
  Force a docs-first pass before guessing: third-party APIs, libraries,
  frameworks, CLIs, cloud/provider SDKs, upgrades, auth/security/billing,
  migrations, deploys, or anything "latest/current/official". Web-search and
  read primary docs before coding from memory.
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch, Bash, TodoWrite
---

# Read the damn docs

Do not guess when authoritative docs can answer. Search, open, and read current official docs before coding.

Source: [BuilderIO/skills](https://github.com/BuilderIO/skills) (`read-the-damn-docs`). MIT.

## Docs-first triggers

- User asks for latest / current / official / recommended / look it up
- Needed docs are not already in the repo or supplied
- Adding, upgrading, configuring, or importing a package/SDK/CLI/provider
- Fast-moving surfaces (AI SDKs, React/Next, Stripe, GitHub, auth, cloud)
- Auth, secrets, webhooks, billing, PII, migrations, rate limits, compliance
- Errors mentioning deprecation, unknown options, version mismatch
- Local ADRs, OpenAPI, schemas, or package READMEs define the contract
- Expensive-to-reverse choices (schema, wire formats, public IDs, events)
- About to write "usually", "probably", or "from memory" for an external API

## What counts as docs

1. Local repo docs, specs, ADRs, schemas, tests
2. Official product docs, API refs, migration guides, changelogs, SDK types
3. Registry version checks (`npm view <pkg> version` or equivalent)
4. Source/types when official docs are incomplete (evidence, not folklore)

Avoid Stack Overflow / blogs / memory as the primary source when official docs exist.

## Workflow

1. Name the surface (package, version, endpoint, CLI, config, feature)
2. Web-search official docs unless already local / URL-supplied
3. Read the closest docs; verify package major before install/import
4. Extract only needed facts (options, imports, limits, breaking changes)
5. Implement/answer from those facts; call out doc↔code drift
6. Verify with the smallest useful check
7. Cite docs or local files that shaped the answer

## When local is enough

Brief local reads are fine for existing helpers, nearby tests, typed interfaces. Proceed normally for trivial syntax/typos with no external contract.

## If docs unavailable

Say so plainly before relying on memory. Narrow uncertainty; do not present results as confirmed-current.

## Handoff

- **docs-writer** — capture lasting Elomix contracts after the pass
- **deepiri-doc-grounding** — prefer live repo docs over memory
