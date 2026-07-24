---
description: Dump this lane's working memory to disk before clearing context. Usage: /rebrief B
argument-hint: [lane letter]
---
You are about to be cleared. **Everything not written down now is lost.** Your job is to make a fresh session as effective as you are, without it re-reading your history.

1. Commit any uncommitted work first. Never `/rebrief` with a dirty tree.
2. Run `/handoff $ARGUMENTS` if you have unlogged progress.
3. Write `.cowork/state/$ARGUMENTS.md`, **overwriting it**, with exactly these sections and nothing else:

```
# LANE $ARGUMENTS — working state as of <HH:MM>

## 1. Identity
What I own (paths). What I must never touch. Current model.

## 2. Ground truth right now
5–10 one-line facts a fresh session would otherwise get wrong.
What is live, what is fixture, what numbers are current, what file is canonical.

## 3. Commands that work
Copy-pasteable, verified. Exact env vars. Include the ones with non-obvious flags.

## 4. REJECTED — do not retry
The highest-value section. Every approach tried and abandoned, with ONE line of why.
A fresh session will otherwise burn 20 minutes rediscovering each of these.

## 5. In flight
What is half-done, where it stopped, what the next concrete action is.

## 6. Gotchas
Environment quirks, API oddities, things that fail confusingly.

## 7. Pointers, not content
Which docs to read and in what order. Do NOT paste their contents here.
```

4. Keep it under ~150 lines. This is a briefing, not a transcript. Prefer a rejected-approach line over a paragraph of narrative.
5. `git add .cowork/state/$ARGUMENTS.md && git commit -m "chore: rebrief lane $ARGUMENTS"`
6. Print: `Rebriefed. Start a new session and run: /resume $ARGUMENTS`
