## QA engineer workflow (Deepiri)

Use when the task is **reviewing/approving a PR as QA**, setting up a QA test environment, or
onboarding a new QA engineer. This is the Deepiri QA team's canonical workflow — do not invent
steps or skip the review-submission requirements below.

### 1. Task identification

- **Plaky board:** check for assigned PR tasks.
- **GitHub review inbox:** check `https://github.com/pulls/inbox` for PRs where you've been
  requested as a reviewer — this is often how an assignment actually surfaces, in addition to
  Discord/Plaky.
- **Scope definition:** read the PR description and diff to determine which repo(s) or
  submodule(s) are affected before touching a local environment. If a PR is connected to other
  open PRs (shared branch, dependent submodule bump), identify those first — testing one in
  isolation when it depends on another will produce false failures.
- **Status:** once assigned, update your status in the availability channel to "Busy," and keep
  it current in general — it's how leads know who's free to pick up new work.

### 2. Local environment setup

- **Repository access:** locate the relevant repo(s)/submodule(s) on GitHub.
- **Branch checkout:** in the local directory of each affected submodule, checkout the branch the
  PR is built from — not `main`, and not a stale local branch with the same name.
- **Environment initialization:** use the Docker scripts in
  `/deepiri-platform/team_dev_environments/qa-team/`:
  - `start.sh` — bring the environment up.
  - `build.sh` — rebuild containers when the PR changes dependencies (lockfiles, Dockerfiles,
    base images) — a plain `start.sh` will silently run against stale images otherwise.
  - `stop.sh` — tear the environment down once testing is complete. Don't leave stacks running
    between PRs; the next reviewer (or your next task) may need the ports/resources clean.

### 3. Verification and testing

- **Health check:** after `start.sh`, confirm every container reports healthy before testing
  functionality on top of it. A "healthy enough" container that's actually still initializing
  produces test results that look like the PR's fault when they're the environment's.
- **Sorge bot pass:** comment `/sorge` on the PR to get an automated code review flagging things
  worth looking into. Treat this as a first pass that informs your manual review — it does not
  replace the code review or testing steps below; run both.
- **Code review:** read the source for logic and consistency, not just "does it run."
- **Frontend PRs:** verify UI/UX against the design spec, not just "the page loads."
- **Backend PRs:** verify functional requirements and data integrity — check what the change
  actually persists or returns, not only that the endpoint responds.

### 4. Documentation requirements

Current guidance overrides earlier onboarding docs on this point: **do not hold up a PR over
missing README or changelog updates** — don't treat those as a review blocker. If earlier
material you've read says to check README/changelog updates before approving, this supersedes it.

### 5. Submitting the review

On the PR's **Files changed** tab, use **Submit review**:

- Write a summary of what you actually tested (environment, health check result, what you
  exercised manually, what Sorge flagged and how you handled it).
- Select **Approve** if the PR is good to go, or **Request Changes** if it isn't — and if
  requesting changes, the summary must say specifically what needs to be looked into, not just
  "needs work."
- **Never leave a review as plain "Comment."** Always resolve to Approve or Request Changes —
  QA reviews are expected to show up as real contributions on the reviewer's GitHub profile, and
  a Comment-only review doesn't count as one.

### Escalation and cadence

- Questions about PR specifics, environment setup, or "is this actually QA's problem or dev's":
  ask in the QA/git Discord channels, or a QA lead directly, before guessing.
- Weekly QA check-in happens in the support-team Discord room — use it for status, blockers, and
  onboarding questions, not just as a standup formality.
- Once comfortable with the workflow, take initiative: ask a QA lead for the next PR rather than
  waiting to be assigned one.
