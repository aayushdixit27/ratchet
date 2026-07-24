# Fixture bug ledger — ground truth

**This file is scoring ground truth. It is NOT shown during the demo.** The agent is
supposed to discover these from Replay QA output, not read them here.

`app/` is a prop. It is *supposed* to be broken (PRODUCT.md §5). Do not fix it.

**8 bugs seeded. Exactly 3 share one class: `modal-state-not-reset`.**

The three shared-class bugs are the load-bearing part of the demo: RATCHET pays full
cold-path price to reason about the first one, then recognises the other two by semantic
similarity of root cause and fixes them on the warm path for pennies. They are the same
bug wearing three different sets of clothes — different modals, different selectors,
different-looking symptoms, **one root cause and one fix strategy**.

---

## Class: `modal-state-not-reset` — 3 bugs

**Shared root cause.** Every modal keeps a lazily-seeded scratch object (`editDraft`,
`settingsDraft`, `pendingDelete`) so a half-finished interaction survives an accidental
dismissal. Each is seeded with the `x = x || seed()` idiom, so it is only initialised
when it is null. `closeModal()` (`app.js`) only adds the `.hidden` class — it never
nulls the scratch object. Only the *save* path clears it. So any close-without-saving
leaves the draft alive, and the next open of that modal resumes the previous target's
state instead of seeding from the new one.

**Shared fix strategy.** Clear the modal's scratch state on every close path, not only
on save — i.e. reset owned state in the dismiss handler, so open() always seeds fresh.

| id | selector | symptom (what a QA crawler sees) | precise root cause |
|---|---|---|---|
| **BUG-01** | `#modal-edit`, `#edit-title`, `[data-close="modal-edit"]` | Open Edit on "Review pull request #412", change the title, click Cancel. Open Edit on a *different* task — the title/notes/priority fields show the abandoned edit from the first task. Saving then overwrites the second task with the first task's text. | `openEdit()` does `editDraft = editDraft \|\| {...}`; `closeModal('modal-edit')` never sets `editDraft = null`. Only `saveEdit()` clears it. |
| **BUG-02** | `#modal-settings`, `#set-confirm`, `#set-compact`, `#set-name`, `[data-close="modal-settings"]` | Open Settings, untick "Ask before deleting", change the display name, click Cancel. Reopen Settings — the discarded values are shown as if they were saved. The UI now disagrees with persisted state. | `openSettings()` does `settingsDraft = settingsDraft \|\| {...}`; the close path never nulls `settingsDraft`, so the stale draft wins over `settings` on reopen. |
| **BUG-03** | `#modal-confirm`, `#confirm-text`, `#btn-confirm-delete`, `[data-close="modal-confirm"]` | Click Delete on "Draft the Q3 release notes", click Cancel. Now click Delete on "Renew the TLS certificate" — the dialog reads *Delete "Draft the Q3 release notes"?*. Confirming deletes the **wrong task** — the one from the cancelled interaction. | `requestDelete()` does `pendingDelete = pendingDelete \|\| {id, title}`; cancelling closes the dialog without nulling `pendingDelete`, so the stale target survives into the next confirmation. Data-loss severity. |

---

## Singletons — 5 bugs, 5 distinct root causes

| id | class | selector | symptom | precise root cause |
|---|---|---|---|---|
| **BUG-04** | `counter-off-by-one` | `#counter` | With 3 incomplete tasks the header reads "2 tasks remaining". With 1 it reads "0 tasks remaining"; with none it reads "-1 tasks remaining". | `render()` computes `tasks.filter(t => !t.done).length - 1`. The `- 1` compensated for a pinned "inbox" row that was removed from the markup and never un-compensated. |
| **BUG-05** | `filter-state-lost-on-mutation` | `.chip[data-filter]`, `#task-list` | Select the "Done" filter, then tick or add any task. The list snaps back to showing every task while the "Done" chip stays visually selected — filter UI and filter behaviour disagree. | `addTask()` and `toggleTask()` both assign `activeFilter = 'all'` before rendering, to guarantee the mutated task is visible. Neither updates the `.is-active` chip class, so the control desyncs from state. |
| **BUG-06** | `missing-preventdefault` | `#edit-form`, `#edit-title` | Open Edit, type into Title, press Enter. The whole page reloads and the edit is silently discarded. | `#edit-form` is a real `<form>` with exactly one implicit-submission-blocking field and no `submit` listener, so Enter triggers native GET submission to the same URL. No `preventDefault`, no submit handler. |
| **BUG-07** | `dead-control` | `#toast-close` | The notification toast in the top-right has an × button that does nothing. The toast never leaves the screen and covers the Settings button. | `init()` binds the listener to `$('#toast-dismiss')`, which does not exist; the markup's id is `toast-close`. The `if (toastX)` guard swallows the miss silently. |
| **BUG-08** | `missing-input-validation` | `#new-task`, `#btn-add` | Type a single space into the new-task box and press Add — a blank task row is created. Repeatable indefinitely. | `addTask()` guards on `title.length === 0` instead of `title.trim().length === 0`; whitespace-only input passes and is stored verbatim. |

---

## Scoring notes for `FixtureQA` (Lane B)

- Machine-readable form of this table: **`app/bugs.json`** — same ids, class, selectors,
  symptom, root cause, plus `fix_strategy` and `severity`.
- A fix counts as **verified** when the repro path in `symptom` no longer reproduces.
- Retention is measured on BUG-01 → BUG-02/BUG-03: the second and third members of
  `modal-state-not-reset` must resolve on the **warm** path if memory is working.
- Expected demo shape: iteration 0 pays cold price on BUG-01; by iteration 3 the class
  is a warm hit and cost-per-verified-fix has visibly dropped.
