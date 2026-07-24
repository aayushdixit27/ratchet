# cited.md — RATCHET's verified fix-pattern corpus

Every entry below was written by the agent after a fix was **verified** by QA.
Iteration N is cheaper than N-1 because of the rows on this page.

<!-- machine-readable: each pattern is one `## sig` block with a JSON payload -->

<!-- pattern:b7a3887a7811 -->
## `b7a3887a7811` — modal-state-not-reset

**Verified:** yes · **Reused:** 6x

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

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
  "score": 0.9024
}
```
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
## `6c94eae3b140` — modal-state-not-reset

**Verified:** yes · **Reused:** 5x

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

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
  "score": 0.9
}
```
<!-- pattern:4f2912a15908 -->
## `4f2912a15908` — counter-off-by-one

**Verified:** yes · **Reused:** 2x

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

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
  "score": 0.9
}
```
<!-- pattern:9fa805fa7e62 -->
## `9fa805fa7e62` — filter-state-lost-on-mutation

**Verified:** yes · **Reused:** 2x

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

```json
{
  "sig": "9fa805fa7e62",
  "bug_class": "filter-state-lost-on-mutation",
  "strategy": "STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.",
  "code_hint": "init binds the click listener to toast dismiss an id that does not exist in the markup the button is toast close the if toastx guard swallows the miss silently",
  "verified": true,
  "uses": 2,
  "score": 0.9
}
```
<!-- pattern:7e406ab2999c -->
## `7e406ab2999c` — missing-preventdefault

**Verified:** yes · **Reused:** 4x

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

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
  "score": 0.9
}
```
<!-- pattern:0dddda0faee2 -->
## `0dddda0faee2` — dead-control

**Verified:** yes · **Reused:** 3x

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

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
  "score": 0.9
}
```
<!-- pattern:a1735b95f51d -->
## `a1735b95f51d` — missing-input-validation

**Verified:** yes · **Reused:** 3x

STRATEGY: Reset the component's local state on every open rather than initialising it once. Derive the form values from the record passed in, key the component on the record id so a different record forces a fresh mount, and clear any module-level draft object in the close handler.
CODE_HINT: key={record.id} on the dialog; useEffect(() => setForm(initial), [record.id]); onClose(() => draft.clear())
VERIFY: reopen with a second record and assert the fields are empty.

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
  "score": 0.9
}
```