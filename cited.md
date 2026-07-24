# cited.md — RATCHET's verified fix-pattern corpus

Every entry below was written by the agent after a fix was **verified** by QA.
Iteration N is cheaper than N-1 because of the rows on this page.

<!-- machine-readable: each pattern is one `## sig` block with a JSON payload -->

<!-- pattern:b7a3887a7811 -->
## `b7a3887a7811` — modal-state-not-reset (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T21:37:31.673+00:00 (6× re-verified)
Learned on **tasker** (acme) at iteration 3 · reused **6×**

**Fix strategy:**

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

**Code hint:** `openedit seeds editdraft with editdraft editdraft so it is only initialised when null closemodal only toggles the hidden class and never nulls editdraft only saveedit clears it`

<details><summary>machine-readable</summary>

```json
{
  "sig": "b7a3887a7811",
  "bug_class": "modal-state-not-reset",
  "strategy": "STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.",
  "code_hint": "openedit seeds editdraft with editdraft editdraft so it is only initialised when null closemodal only toggles the hidden class and never nulls editdraft only saveedit clears it",
  "verified": true,
  "uses": 6,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T21:37:31.673+00:00",
  "verification_count": 6,
  "born_at_iteration": 3,
  "saved_usd": 0.0,
  "origin_app": "tasker",
  "origin_org": "acme"
}
```
</details>
<!-- pattern:4594936c757c -->
## `4594936c757c` — modal-state-not-reset

**Verified:** yes · **Reused:** 9x

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

```json
{
  "sig": "4594936c757c",
  "bug_class": "modal-state-not-reset",
  "strategy": "STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.",
  "code_hint": "openedit seeds editdraft with editdraft editdraft so it is only initialised when null closemodal only toggles the hidden class and never nulls editdraft only saveedit clears it",
  "verified": true,
  "uses": 9,
  "score": 0.9
}
```
<!-- pattern:6c94eae3b140 -->
## `6c94eae3b140` — modal-state-not-reset (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T21:37:31.658+00:00 (5× re-verified)
Learned on **tasker** (acme) at iteration 2 · reused **5×**

**Fix strategy:**

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

**Code hint:** `openedit seeds editdraft with editdraft editdraft so it is only initialised when null closemodal only toggles the hidden class and never nulls editdraft only saveedit clears it`

<details><summary>machine-readable</summary>

```json
{
  "sig": "6c94eae3b140",
  "bug_class": "modal-state-not-reset",
  "strategy": "STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.",
  "code_hint": "openedit seeds editdraft with editdraft editdraft so it is only initialised when null closemodal only toggles the hidden class and never nulls editdraft only saveedit clears it",
  "verified": true,
  "uses": 5,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T21:37:31.658+00:00",
  "verification_count": 5,
  "born_at_iteration": 2,
  "saved_usd": 0.0,
  "origin_app": "tasker",
  "origin_org": "acme"
}
```
</details>
<!-- pattern:4f2912a15908 -->
## `4f2912a15908` — counter-off-by-one (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T21:37:31.724+00:00 (2× re-verified)
Learned on **tasker** (acme) at iteration 4 · reused **2×**

**Fix strategy:**

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

**Code hint:** `render computes tasks filter t t done length 1 the 1 compensated for a pinned inbox row that was removed from the markup the compensation was left behind`

<details><summary>machine-readable</summary>

```json
{
  "sig": "4f2912a15908",
  "bug_class": "counter-off-by-one",
  "strategy": "STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.",
  "code_hint": "render computes tasks filter t t done length 1 the 1 compensated for a pinned inbox row that was removed from the markup the compensation was left behind",
  "verified": true,
  "uses": 2,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T21:37:31.724+00:00",
  "verification_count": 2,
  "born_at_iteration": 4,
  "saved_usd": 0.0,
  "origin_app": "tasker",
  "origin_org": "acme"
}
```
</details>
<!-- pattern:9fa805fa7e62 -->
## `9fa805fa7e62` — filter-state-lost-on-mutation (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T21:37:31.637+00:00 (2× re-verified)
Learned on **tasker** (acme) at iteration 2 · reused **2×**

**Fix strategy:**

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

**Code hint:** `addtask and toggletask both assign activefilter all before render so the mutated task is guaranteed visible but neither updates the is active chip class control and state desync`

<details><summary>machine-readable</summary>

```json
{
  "sig": "9fa805fa7e62",
  "bug_class": "filter-state-lost-on-mutation",
  "strategy": "STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.",
  "code_hint": "addtask and toggletask both assign activefilter all before render so the mutated task is guaranteed visible but neither updates the is active chip class control and state desync",
  "verified": true,
  "uses": 2,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T21:37:31.637+00:00",
  "verification_count": 2,
  "born_at_iteration": 2,
  "saved_usd": 0.0,
  "origin_app": "tasker",
  "origin_org": "acme"
}
```
</details>
<!-- pattern:7e406ab2999c -->
## `7e406ab2999c` — missing-preventdefault (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T21:37:31.718+00:00 (4× re-verified)
Learned on **tasker** (acme) at iteration 4 · reused **4×**

**Fix strategy:**

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

**Code hint:** `edit form is a real form containing exactly one implicit submission blocking field and no submit listener so enter triggers native get submission to the same url no preventdefault anywhere`

<details><summary>machine-readable</summary>

```json
{
  "sig": "7e406ab2999c",
  "bug_class": "missing-preventdefault",
  "strategy": "STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.",
  "code_hint": "edit form is a real form containing exactly one implicit submission blocking field and no submit listener so enter triggers native get submission to the same url no preventdefault anywhere",
  "verified": true,
  "uses": 4,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T21:37:31.718+00:00",
  "verification_count": 4,
  "born_at_iteration": 4,
  "saved_usd": 0.0,
  "origin_app": "tasker",
  "origin_org": "acme"
}
```
</details>
<!-- pattern:0dddda0faee2 -->
## `0dddda0faee2` — dead-control (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T21:37:31.713+00:00 (3× re-verified)
Learned on **tasker** (acme) at iteration 4 · reused **3×**

**Fix strategy:**

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

**Code hint:** `init binds the click listener to toast dismiss an id that does not exist in the markup the button is toast close the if toastx guard swallows the miss silently`

<details><summary>machine-readable</summary>

```json
{
  "sig": "0dddda0faee2",
  "bug_class": "dead-control",
  "strategy": "STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.",
  "code_hint": "init binds the click listener to toast dismiss an id that does not exist in the markup the button is toast close the if toastx guard swallows the miss silently",
  "verified": true,
  "uses": 3,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T21:37:31.713+00:00",
  "verification_count": 3,
  "born_at_iteration": 4,
  "saved_usd": 0.0,
  "origin_app": "tasker",
  "origin_org": "acme"
}
```
</details>
<!-- pattern:a1735b95f51d -->
## `a1735b95f51d` — missing-input-validation (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T21:37:31.683+00:00 (3× re-verified)
Learned on **tasker** (acme) at iteration 3 · reused **3×**

**Fix strategy:**

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

**Code hint:** `addtask guards on title length 0 rather than title trim length 0 so whitespace only input passes validation and is stored verbatim`

<details><summary>machine-readable</summary>

```json
{
  "sig": "a1735b95f51d",
  "bug_class": "missing-input-validation",
  "strategy": "STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.",
  "code_hint": "addtask guards on title length 0 rather than title trim length 0 so whitespace only input passes validation and is stored verbatim",
  "verified": true,
  "uses": 3,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T21:37:31.683+00:00",
  "verification_count": 3,
  "born_at_iteration": 3,
  "saved_usd": 0.0,
  "origin_app": "tasker",
  "origin_org": "acme"
}
```
</details>
<!-- pattern:sig-live-smoke -->
## `sig-live-smoke` — modal-state-not-reset (✅ verified)

Discovered by **replay-qa** · root cause from **replay-qa** · fix verified by **replay-qa** at 2026-07-24T12:20:00Z
Learned on **tasker** (acme) at iteration 0 · reused **1×**

**Fix strategy:**

Reset modal scratch state in the dismiss handler so open() always seeds fresh.

**Code hint:** `closeModal(): editDraft = null`

<details><summary>machine-readable</summary>

```json
{
  "sig": "sig-live-smoke",
  "bug_class": "modal-state-not-reset",
  "strategy": "Reset modal scratch state in the dismiss handler so open() always seeds fresh.",
  "code_hint": "closeModal(): editDraft = null",
  "verified": true,
  "uses": 1,
  "score": 0.88,
  "discovered_by": "replay-qa",
  "root_cause_source": "replay-qa",
  "verified_by": "replay-qa",
  "verified_at": "2026-07-24T12:20:00Z",
  "verification_count": 0,
  "born_at_iteration": 0,
  "saved_usd": 0.0,
  "origin_app": "tasker",
  "origin_org": "acme"
}
```
</details>

<!-- pattern:sig-toast-occlusion -->
## `sig-toast-occlusion` — glitches (✅ verified)

Discovered by **replay-qa** · root cause from **replay-qa** · fix verified by **replay-qa** at 2026-07-24T12:26:00Z
Learned on **tasker** (acme) at iteration 0 · reused **0×**

**Fix strategy:**

Lower the toast z-index below interactive chrome, or auto-dismiss after timeout; never let passive notifications intercept clicks.

<details><summary>machine-readable</summary>

```json
{
  "sig": "sig-toast-occlusion",
  "bug_class": "glitches",
  "strategy": "Lower the toast z-index below interactive chrome, or auto-dismiss after timeout; never let passive notifications intercept clicks.",
  "code_hint": null,
  "verified": true,
  "uses": 0,
  "score": 0.9,
  "discovered_by": "replay-qa",
  "root_cause_source": "replay-qa",
  "verified_by": "replay-qa",
  "verified_at": "2026-07-24T12:26:00Z",
  "verification_count": 0,
  "born_at_iteration": 0,
  "saved_usd": 0.0,
  "origin_app": "tasker",
  "origin_org": "acme"
}
```
</details>

<!-- pattern:b03162e3f930 -->
## `b03162e3f930` — unescaped-html-injection (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T20:43:06.068+00:00
Learned on **notes-globex** (globex) at iteration 3 · reused **1×**

**Fix strategy:**

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

**Code hint:** `rendernotes builds each card with card innerhtml h3 n title h3 user controlled title concatenated into html unescaped body uses textcontent and is safe the title path is not`

<details><summary>machine-readable</summary>

```json
{
  "sig": "b03162e3f930",
  "bug_class": "unescaped-html-injection",
  "strategy": "STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.",
  "code_hint": "rendernotes builds each card with card innerhtml h3 n title h3 user controlled title concatenated into html unescaped body uses textcontent and is safe the title path is not",
  "verified": true,
  "uses": 1,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T20:43:06.068+00:00",
  "verification_count": 1,
  "born_at_iteration": 3,
  "saved_usd": 0.0,
  "origin_app": "notes-globex",
  "origin_org": "globex"
}
```
</details>
<!-- pattern:d2cee719eb67 -->
## `d2cee719eb67` — modal-state-not-reset (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T20:43:06.042+00:00 (9× re-verified)
Learned on **notes-globex** (globex) at iteration 1 · reused **9×**

**Fix strategy:**

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

**Code hint:** `openedit seeds editdraft with editdraft editdraft so it is only initialised when null closemodal only toggles the hidden class and never nulls editdraft only saveedit clears it`

<details><summary>machine-readable</summary>

```json
{
  "sig": "d2cee719eb67",
  "bug_class": "modal-state-not-reset",
  "strategy": "STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.",
  "code_hint": "openedit seeds editdraft with editdraft editdraft so it is only initialised when null closemodal only toggles the hidden class and never nulls editdraft only saveedit clears it",
  "verified": true,
  "uses": 9,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T20:43:06.042+00:00",
  "verification_count": 9,
  "born_at_iteration": 1,
  "saved_usd": 0.0,
  "origin_app": "notes-globex",
  "origin_org": "globex"
}
```
</details>
<!-- pattern:90fd0c6c9238 -->
## `90fd0c6c9238` — stale-derived-state (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T20:43:06.034+00:00 (4× re-verified)
Learned on **notes-globex** (globex) at iteration 1 · reused **4×**

**Fix strategy:**

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

**Code hint:** `addtask and toggletask both assign activefilter all before render so the mutated task is guaranteed visible but neither updates the is active chip class control and state desync`

<details><summary>machine-readable</summary>

```json
{
  "sig": "90fd0c6c9238",
  "bug_class": "stale-derived-state",
  "strategy": "STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.",
  "code_hint": "addtask and toggletask both assign activefilter all before render so the mutated task is guaranteed visible but neither updates the is active chip class control and state desync",
  "verified": true,
  "uses": 4,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T20:43:06.034+00:00",
  "verification_count": 4,
  "born_at_iteration": 1,
  "saved_usd": 0.0,
  "origin_app": "notes-globex",
  "origin_org": "globex"
}
```
</details>
<!-- pattern:b07add504c7d -->
## `b07add504c7d` — closure-loop-capture (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T20:43:06.050+00:00 (2× re-verified)
Learned on **notes-globex** (globex) at iteration 2 · reused **2×**

**Fix strategy:**

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

**Code hint:** `rendernotebooks binds click handlers inside a for var i loop and the handler reads notebooks i at click time by then i notebooks length so currentnotebook becomes undefined and nothing matches it`

<details><summary>machine-readable</summary>

```json
{
  "sig": "b07add504c7d",
  "bug_class": "closure-loop-capture",
  "strategy": "STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.",
  "code_hint": "rendernotebooks binds click handlers inside a for var i loop and the handler reads notebooks i at click time by then i notebooks length so currentnotebook becomes undefined and nothing matches it",
  "verified": true,
  "uses": 2,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T20:43:06.050+00:00",
  "verification_count": 2,
  "born_at_iteration": 2,
  "saved_usd": 0.0,
  "origin_app": "notes-globex",
  "origin_org": "globex"
}
```
</details>
<!-- pattern:e1fe78dbbba3 -->
## `e1fe78dbbba3` — modal-state-not-reset (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T20:43:06.065+00:00 (12× re-verified)
Learned on **notes-globex** (globex) at iteration 3 · reused **12×**

**Fix strategy:**

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

**Code hint:** `openedit seeds editdraft with editdraft editdraft so it is only initialised when null closemodal only toggles the hidden class and never nulls editdraft only saveedit clears it`

<details><summary>machine-readable</summary>

```json
{
  "sig": "e1fe78dbbba3",
  "bug_class": "modal-state-not-reset",
  "strategy": "STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.",
  "code_hint": "openedit seeds editdraft with editdraft editdraft so it is only initialised when null closemodal only toggles the hidden class and never nulls editdraft only saveedit clears it",
  "verified": true,
  "uses": 12,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T20:43:06.065+00:00",
  "verification_count": 12,
  "born_at_iteration": 3,
  "saved_usd": 0.0,
  "origin_app": "notes-globex",
  "origin_org": "globex"
}
```
</details>
<!-- pattern:1980c79669cd -->
## `1980c79669cd` — case-sensitive-filter (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T20:43:06.059+00:00
Learned on **notes-globex** (globex) at iteration 3 · reused **1×**

**Fix strategy:**

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

**Code hint:** `visible filters with raw string indexof on title and body no case normalisation on either side`

<details><summary>machine-readable</summary>

```json
{
  "sig": "1980c79669cd",
  "bug_class": "case-sensitive-filter",
  "strategy": "STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.",
  "code_hint": "visible filters with raw string indexof on title and body no case normalisation on either side",
  "verified": true,
  "uses": 1,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T20:43:06.059+00:00",
  "verification_count": 1,
  "born_at_iteration": 3,
  "saved_usd": 0.0,
  "origin_app": "notes-globex",
  "origin_org": "globex"
}
```
</details>