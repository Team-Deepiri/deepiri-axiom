---
name: token-efficiency
description: >-
  Deliberate context and token budgeting for long or expensive agent sessions — what to read
  versus grep, when to delegate to a subagent or fork instead of inlining output, how to keep
  a session productive as it approaches context limits. Use on long-running work, large-repo
  exploration, or whenever a session is burning tokens faster than the work justifies.
allowed-tools: Read, Grep, Glob, Bash, TodoWrite
---

# Token efficiency

The scarce resource in a long agent session is rarely compute — it's the context window, and by
extension the model's ability to keep the actually load-bearing facts in view. Every unnecessary token
read into context is a token that isn't a real requirement, a real file, or a real decision competing for
attention later in the same session. Optimize for signal density, not for doing less work.

## Read narrowly before reading broadly

- **Grep before Read.** If you know roughly what you're looking for — a function name, an error string, an
  import — search for it first and read only the matching region, not the whole file. A 2,000-line file
  read in full to find one 20-line function wastes the other 1,980 lines of context for the rest of the
  session.
- **Use line-range reads on files you already know are large.** Most read tools accept an offset/limit;
  use it once `wc -l` or a directory listing tells you a file is big.
- **Don't re-read what you just wrote.** An edit tool that succeeded already confirms the change landed —
  reading the file back to verify is usually pure waste unless something downstream depends on the exact
  resulting bytes.
- **Prefer targeted tool output over dumping raw command output.** `git diff --stat` before `git diff`;
  `git log --oneline -20` before an unbounded log; a filtered grep before `cat`-ing a whole directory.

## Delegate what you don't need to keep

- **Fork or subagent for research whose conclusion matters more than its trail.** If you need an answer —
  "what does this module do," "where is X defined," "is there a skill for Y" — but not the search process
  that produced it, hand it to a subagent (or a fork, when one is available) and consume only its final
  summary. This is the single biggest lever: a subagent's tool noise never enters the parent's context at
  all.
- **Batch independent lookups into one round of parallel calls** rather than serial back-and-forth, so the
  model isn't re-stating context between each one.
- **Push large intermediate artifacts to disk, not to the transcript.** Write scratch analysis, generated
  data, or long intermediate output to a file and reference the file path, rather than pasting the full
  content into the conversation for a later step to re-read anyway.

## Manage the arc of a long session

- **Summarize state at natural checkpoints**, not just when forced to by an automatic context-compression
  event. A short "here's what's done, what's left, what decisions were made" note written deliberately
  survives compression far better than letting the system guess what mattered.
- **Keep a running task list (`TodoWrite`/`TaskCreate`) instead of re-deriving status from scrollback.**
  Re-reading the last 50 messages to remember what's left to do is a common and avoidable token sink.
- **Recognize when a session should restart clean rather than continue.** If a session has accumulated a
  lot of dead-end exploration, a fresh session briefed with a tight, deliberately-written summary of
  conclusions (not process) often outperforms continuing to carry the exploration's full weight.
- **Match verbosity to audience.** Terse, information-dense responses in an agent-to-agent or
  agent-to-tool exchange; fuller explanation only where a human is actually reading it.

## Recognizing waste in real time

Watch for these patterns as a signal to change approach mid-task, not just in retrospect:

- Reading the same file more than twice in one session without it having changed.
- A subagent's full raw output being pasted back and re-summarized by the parent instead of the subagent
  being asked to return the summary directly.
- Re-explaining background the model already established earlier in the same session, because state was
  never checkpointed.
- Serial exploration of independent leads that could have been parallelized.

## What this is not

Not a mandate to under-read and guess — misreading a file to save tokens and then debugging a wrong
assumption costs far more than reading it correctly once. The goal is precision, not minimalism for its
own sake: read exactly what's needed, at the resolution needed, and no more.
