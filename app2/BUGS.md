# Jotting fixture bug ledger — ground truth (App #2, org: globex)

**Scoring ground truth. NOT shown during the demo.** Machine-readable twin: `app2/bugs.json`
(same schema Lane B already consumes for Tasker).

Jotting is the **cross-org transfer** fixture (AMENDMENT-03): a notes app from a "different
team" — different domain, DOM, copy and author voice than Tasker. It exists to prove that a
pattern verified on Tasker (org **acme**) fixes its first-ever bug on Jotting (org **globex**)
for warm-path pennies. **6 bugs. Exactly 2 share `modal-state-not-reset` with Tasker.**

## The shared class — same latent root cause, unrecognisable symptoms

Same defect as Tasker's BUG-01/02/03: dialog scratch state lazily seeded with
`x = x || seed()`, and the dismiss path (`closeDialog()`) only hides the overlay — it never
nulls the scratch object. Only the confirm path clears it.

But the clothes are completely different:

| id | dialog | symptom |
|---|---|---|
| **J-01** | share (`#dlg-share`) | Cancel a share, share a different note → **invite goes to the first note**. Privacy breach, wrong-object action. |
| **J-02** | tag manager (`#dlg-tags`) | Cancel a tag → it **resurrects pre-filled** on reopen; Create makes the ghost tag. |

Neither says "stale form text" like Tasker did. The semantic root cause — and the fix
strategy `reset-modal-owned-state-on-close` — is identical. That's the transfer.

## Singletons — 4, all classes novel to the corpus

| id | class | symptom |
|---|---|---|
| **J-03** | `case-sensitive-filter` | Search misses notes unless the case matches exactly. |
| **J-04** | `stale-derived-state` | Note-count pill doesn't update on Remove (only on Save/switch). |
| **J-05** | `closure-loop-capture` | Clicking any notebook empties the grid (`for var i` handler reads `notebooks[i]` after loop end → `undefined`). |
| **J-06** | `unescaped-html-injection` | Note titles concatenated into `innerHTML` — stored XSS via title. |

Full selectors, repro steps, root causes and fix strategies: `app2/bugs.json`.

## Scoring notes
- Transfer is measured on J-01/J-02: run with `--target app2 --corpus-from tasker` — first
  encounter of either should resolve **warm** off a Tasker-born pattern. Never pre-seed app2's
  own patterns into its first run (AMENDMENT-03, Lane A section).
- J-03..J-06 must go **cold** on first encounter — they are novel classes by construction, so
  the run isn't trivially all-warm.
