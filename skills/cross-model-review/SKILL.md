---
name: cross-model-review
description: >-
  Get an independent second opinion on risky code, architecture, or a plan from a different
  model/provider than the one that produced it, so a shared blind spot in one model's training
  doesn't sail through review unchallenged. Use before merging security-sensitive changes,
  irreversible migrations, or any diff the author is not fully confident in.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, TodoWrite
---

# Cross-model review

The single blind spot every reviewer shares with the author is the strongest kind: if the same model
wrote the code and reviewed it, systematic gaps in that model's training or reasoning style show up in
neither pass. A second, differently-trained model reviewing the same diff is far more likely to catch
what a same-model review misses — not because any one model is smarter, but because their failure modes
don't overlap. This is the same principle as adversarial verification with independent voters in the
`plan-arbiter` and `agent-watchdog` skills, applied at the model-provider level instead of the
prompt-instance level.

## When to reach for this

- Security-sensitive diffs: auth, secrets handling, input validation, anything touching a trust boundary.
- Irreversible or hard-to-reverse changes: schema migrations, force-pushes, destructive scripts,
  infrastructure changes.
- Anything the author flags as uncertain, or anywhere a plausible-but-wrong answer would be expensive to
  discover later.
- Before merging a PR authored substantially by an agent with no independent human review yet.

Skip it for routine, easily-reversible, low-blast-radius changes — the overhead isn't worth it, and
constant cross-model review for everything trains people to skim it.

## How to run it

1. **Isolate the artifact.** Diff, plan, or design doc — as self-contained as possible so the second
   model doesn't need the first model's full conversation context to evaluate it fairly.
2. **Route to a genuinely different model/provider**, not just a different conversation with the same
   model. Options depend on what's available in this environment: a different Claude model tier (e.g.
   Opus reviewing Sonnet's output, or vice versa) still shares training lineage — prefer a different
   provider entirely (GPT, Gemini) when the stakes justify it. `browser-relay` / `mailnotmilk-bridge` can
   drive a browser-based chat with another provider when no API key is configured locally.
3. **Ask the reviewer to refute, not confirm.** Prompt it to find the strongest reason the change is wrong
   or unsafe, not to summarize what it does. A reviewer asked "is this good?" tends to agree; a reviewer
   asked "what would make this fail in production?" finds real issues.
4. **Treat disagreement as signal, not a tiebreak to average away.** If the second model flags something
   the first missed, investigate before dismissing it — the whole point of the exercise is that it might
   be seeing something structurally invisible to the first model, not just being pedantic.
5. **Record what each model missed.** Feed this back into how much cross-model review is worth doing
   routinely for this class of change — if one direction consistently misses the same category of issue,
   that's useful information about where routine same-model review is weakest.

## What this is not

Not a substitute for tests, for `security-review`, or for domain-expert human review on anything with
real consequences. It catches a different class of error — blind spots correlated with model training —
not correctness bugs a careful single-model review would also catch. Use alongside the existing
`code-review` / `security-review` skills, not instead of them.
