---
name: deepiri-sorge
description: Deepiri Sorge AI PR review bot — /sorge comments, workflows, sorge.toml. Use when reviewing PRs, triggering Sorge, wiring PR automation, or when the user mentions sorge, /sorge, or AI code review.
---

# Deepiri Sorge

Repo: `deepiri-sorge` — distributed AI PR review bot (GitHub Actions + optional Gemini/GitHub Models).

## When to use this skill
- Opening or updating a PR that needs a first-pass AI review
- Wiring Sorge into a Deepiri repo (workflow + config + secrets)
- Interpreting Sorge comments or skip messages
- User says `/sorge`, "sorge", or "AI PR review"

## Trigger a review (`/sorge`)
1. Ensure the PR exists and is pushed to GitHub.
2. Comment **`/sorge`** on the PR (issue comment body is exactly `/sorge`, optionally with a short note after).
3. Treat the bot reply as a **first pass that informs — not replaces — manual review**.
4. Fold Blocking / Important findings into the human review; do not merge on Sorge alone.

Also auto-runs on `pull_request` opened/synchronize/reopened (and configurable push) when the reusable workflow is installed.

## Agent checklist (ship a PR)
- [ ] Push branch; open PR against `main` or `dev` as repo policy requires
- [ ] Comment `/sorge` on the PR
- [ ] Wait for the review comment (or skip notice)
- [ ] Address real issues; re-comment `/sorge` after large follow-up pushes if needed
- [ ] Complete human/CI review gates before merge

## Install into a repo
1. Add `.github/workflows/pr_review.yml` calling the Sorge workflow (see `deepiri-sorge` README), or copy the workflow from that repo.
2. Optional root `sorge.toml` — defaults are fine for most repos.
3. Repo secret `GOOGLE_API_KEY` (Gemini) when using Gemini routing; `GITHUB_TOKEN` is provided by Actions.
4. Align with branch protection — Sorge comments are advisory unless the team explicitly requires a Sorge check.

### Minimal `sorge.toml`
```toml
[sorge]
enabled = true

[filters]
min_lines = 20
skip_docs = true
skip_deps = true

[review]
style = "concise"
include_security = true
include_performance = true
```

## Local dry-run (no PR comment)
```bash
cd deepiri-sorge   # or sibling clone from .axiom/ecosystem.json
poetry install     # or pip install -r requirements.txt
git -C <target-repo> diff origin/main...HEAD > /tmp/pr.diff
python -m bot.main --diff /tmp/pr.diff --dry-run --verbose
```

## Policy
- Never treat a Sorge skip as "LGTM".
- Do not commit secrets (`.env`, API keys) when adding Sorge config.
- Prefer concise review style; escalate large/complex diffs per `sorge.toml` routing thresholds.
- Pair with `axiom-review` / `deepiri-cross-repo` for human review structure and multi-repo PRs.
