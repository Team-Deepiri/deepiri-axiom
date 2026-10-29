---
name: business-analyst
description: >-
  Business analysis: requirements elicitation, process models, user stories,
  gap analysis, BRD sections, acceptance criteria, stakeholder maps. Deepiri product context.
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, TodoWrite
---

# Business analyst skill (Deepiri)

## When to use

- Turn fuzzy asks into **testable requirements**
- Document **as-is / to-be** process flows
- Produce **user stories** and **acceptance criteria** for engineering
- **Gap analysis** between product vision and current platform capabilities
- Prep **stakeholder workshops** and decision memos

## Core outputs

| Artifact | Contents |
|----------|----------|
| Problem statement | Who, pain, frequency, cost of status quo |
| Scope | In / out of scope; assumptions |
| User stories | As a … I want … so that … + Gherkin-style AC |
| Process flow | Steps, actors, systems (gateway, core-api, Cyrex, etc.) |
| Data needs | Entities, sources, retention (which service owns the schema?) |
| Risks | Technical, compliance, adoption |
| Success metrics | Leading / lagging; SMART |

## Deepiri-aware questions

1. Which **repo** owns the change? (check the `deepiri-ecosystem` manifest)
2. Does this cross a **service boundary**? (no shared DB reads — **deepiri-service-boundaries**)
3. Does it touch the **AI runtime** (Cyrex) or **model versions** (Helox)?
4. Auth and gateway ordering affected?
5. Blast radius across sibling repos — coordinated release needed? (**deepiri-cross-repo**)

## Techniques

- **5 Whys** — root cause before requirements
- **MoSCoW** — Must / Should / Could / Won't
- **RACI** — Responsible, Accountable, Consulted, Informed
- **SWOT** — positioning for new wedges
- **Interface table** — API, event, queue between services

## Handoff

- To **mvp** skill when scope should shrink to a weekend wedge
- To **ship** skill when ready to cut and deliver
- To **git-committer** when docs/BRD land in repo as separate commits

## Quality bar

- No solution jargon without a user outcome
- Every requirement traceable to a metric or pain
- Call out **doc↔code drift** if `docs/` disagrees with implementation
