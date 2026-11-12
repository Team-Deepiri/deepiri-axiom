---
name: grounded-commit-relay
description: >-
  Run grounded, push-back-capable ideation across one or more parallel agent
  sessions under a human's raw directive input — trigger-sourced accept/
  reject discipline, one committed pick (never a menu), and a human-brokered
  relay between parallel tracks that shares outcomes, not in-flight reasoning.
allowed-tools: Read, Write, Edit, Bash, WebSearch, WebFetch, Grep
---

# Grounded Commit Relay (GCR)

Extracted from a live, observed case (2026-09-10): a human ran a product-market-fit
brainstorm for a product line across two parallel Claude sessions, then had a
third session formalize the pattern by directly interviewing both working
sessions rather than inventing it from scratch. Reference implementation:
`<service>/app/agents/collaboration.py` (`TriggerGate`, `Commitment`,
`RelayBroker`). No Deepiri implementation ships this yet — the pattern below is
portable, the module is the part you would have to write.

## When to use

- A human is running one or more agent sessions on open-ended ideation,
  research-then-commit, or product-strategy work — not a scoped engineering
  task with a defined spec.
- The human's input is raw, high-energy, sometimes typo-heavy or
  self-interrupting, and pushes back hard on generic or hedge-y output.
- More than one session is working the same problem space in parallel and a
  human wants independent, uncorrelated takes to compare — not a chorus that
  converges to one answer.

## Core discipline

### 1. Push back with a citable bar, not vibes

Every claim needs a **sourced, dated trigger** — a law, outage, price hike,
non-renewal letter, regulatory change. "AI is growing" is not a trigger. Then
check for a well-funded **incumbent** already serving that exact trigger +
buyer. Two axes, three outcomes:

| Sourced trigger? | Incumbent gap? | Verdict |
|---|---|---|
| No | — | **Reject — generic.** No dated/sourced trigger to point at. |
| Yes | No (crowded) | **Reject — crowded.** Real trigger, but someone already owns it. Reframe the wedge or find an adjacent underserved population. |
| Yes | Yes | **Pursue.** |

This is the same two-axis pattern-match (coded as `TriggerGate` in the reference
implementation) generalized to any grounded-commitment task: gate every claim on a
sourced trigger plus an incumbent check before committing to it.

### 2. Commit to one pick, never a menu

The output shape is: **one recommendation**, the reasoning behind it, what
was considered and rejected (and why), and any caveats on the evidence. Not
a stated rule the human necessarily states on day one — in the observed case
it became a hard requirement through repeated correction ("what would you
personally build," rejecting hedge-y option lists). Assume it's the bar from
the start rather than waiting to be corrected into it.

Caveat rather than block on weak evidence: if research turns up nothing
better, commit anyway with the caveat named explicitly (e.g. "labor-shortage
figures came from an industry association with a stake in the number looking
large — lean on BLS/EIA in any real deck"). A genuine research dead end does
not halt the work; only two things do (see below).

### 3. Handle raw human input without flattening it

- Don't summarize or dedupe repeated phrasing before it reaches your
  reasoning — restatement is how a directive-style human signals *weight*,
  not noise. If they restate the same four criteria six times across one
  message, that's a strong prior, not redundant input to compress away.
- Expect mid-turn interruption and redirection. The right move is to absorb
  it and continue in the next turn, not restart the whole thought or
  re-litigate what was cut off.
- Ask only when genuinely blocked (see halt triggers below) — don't turn
  every ambiguity into a clarifying question. A directive-style human wants
  momentum, not a intake form.

### 4. Halt triggers — when to actually stop and surface to the human

Three real triggers, not a blanket "ask when unsure":

- **Genuine ambiguity or contradictory instructions** — e.g. two directives
  in the same message that can't both be followed. Ask; don't guess past it.
- **Consequential / hard-to-reverse actions** — messaging a peer session,
  editing an already-posted artifact, anything outward-facing. Confirm first.
- **Research dead end** — does *not* block. Commit anyway with an explicit
  caveat (see #2), rather than stalling on "I couldn't find good data."

### 5. Relay between parallel tracks: build the gate, not the pipe

If more than one session is working the same space in parallel, the human is
very likely running deliberately **uncorrelated tracks** to get independent
second opinions — not looking for two agents to converge on one answer. The
default routing is **human-brokered hub-and-spoke**: the human reads one
session's output and decides what (if anything) to relay into another's
prompt. No session reads another's output directly by default.

If a direct peer-to-peer bridge is warranted (e.g. real risk of duplicate
proposals), what crosses the bridge matters far more than whether a channel
exists at all:

| Share this | Not this |
|---|---|
| **Corpus** — a shared source doc both tracks should read | **In-flight reasoning** — this is the one that collapses independence. A peer's half-formed thinking, shared while still in flight, pulls both tracks toward the same answer and destroys the second opinion the human is paying for. |
| **Negative space** — "these concepts are already proposed," so a peer doesn't waste a cycle duplicating | |
| **Final artifacts** — a peer's *committed* Commitment, shared only after it's actually committed | |

Reasoning-sharing isn't hard-blocked (matches the org's general pattern:
watch-list a judgment call rather than gate it outright) — but it should be
a deliberate, visible exception, not the default mode a channel makes easy.
If you build tooling for this, make the artifact kind an explicit,
always-logged parameter (see `SharedArtifactKind` in the reference
implementation) so a reasoning-bridge is never silently indistinguishable
from a safe one.

**The kind label alone doesn't make a share safe** — a second review round
on this exact design (2026-09-10) found two more ways independence leaks
through a correctly-labeled share:

- **Negative space can smuggle reasoning.** "These concepts are already
  proposed" (bare names) is a fence; "concept X was rejected because the
  incumbent already owns that niche" carries the same `NEGATIVE_SPACE` label
  but is reasoning in substance — a single sentence like that can kill a
  parallel track before it starts, the same way sharing raw reasoning would.
  The tell is length/structure, not the declared kind: bare labels are
  short, rationales aren't. If you're building this, cap item length and
  flag anything that looks like it's carrying a "because."
- **A final artifact's safety depends on the RECEIVER's timing, not just
  the sender being done.** Receiving a peer's finished pick before you've
  published your own is anchoring with extra steps — it arrives labeled
  safe and does the damage of reasoning-sharing anyway. Gate the *receive*
  on the recipient having already committed, not just on the sender having
  finished.

Independence is a property of a share's **granularity and timing**, not
just its declared kind — don't read the four `SharedArtifactKind` values as
four safety levels; read them as four starting points that still need a
grain/timing check before they're actually safe.

### 6. Document as you go, async-reviewable

The collaboration artifact is the written record (PR comments, tracker tasks,
committed docs) — not a chat transcript. Every research pass and every
commitment should land somewhere the human can review on their own schedule,
structured enough that someone skimming later gets the trigger → gap →
device/idea → why-uncrowded → JTBD → validation shape without re-reading a
whole conversation.

## Reference implementation

Reference module shape (`<service>/app/agents/collaboration.py`):
- `TriggerGate.evaluate(claim, sourced_trigger=..., incumbent_check=...)` → `GateVerdict.PURSUE | REJECT_GENERIC | REJECT_CROWDED`
- `Commitment(pick, reasoning, rejected_alternatives=[...], caveats=[...])` — `.render()` for the async-reviewable write-up
- `RelayBroker.escalate_to_human(HaltTrigger.AMBIGUITY | CONSEQUENTIAL | RESEARCH_DEAD_END, detail, blocks_progress=...)`
- `RelayBroker.bridge_to_peer(peer_session, reason, kind=..., negative_space_items=[...], recipient_has_committed=...)` → `BridgeResult(kind, leak_suspected, premature_receive)`
  - `negative_space_items`: required for `NEGATIVE_SPACE` — a list of bare labels, not a paragraph; flags `leak_suspected=True` if any item is long enough to look like it's carrying a rationale
  - `recipient_has_committed`: required for `FINAL_ARTIFACT` — flags `premature_receive=True` if the recipient hasn't published their own pick yet

Every call emits a `trace_stage` event so a GCR-run
session leaves the same kind of inspectable per-stage trail the live advisor
path does.

## Handoff

- Product-market-fit-shaped ideation specifically → `pmf-master` (reframe the
  market, surface the underused asset, evidence plan)
- Stress-testing a committed pick → `locksmith-genius`
- Turning a committed pick into a weekend-scope build → `mvp`
