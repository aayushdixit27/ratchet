# cited.md — RATCHET's verified fix-pattern corpus

Every entry below was written by the agent after a fix was **verified** by QA.
Iteration N is cheaper than N-1 because of the rows on this page.

<!-- machine-readable: each pattern is one `## sig` block with a JSON payload -->

<!-- pattern:b7a3887a7811 -->
## `b7a3887a7811` — modal-state-not-reset (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T20:00:19.974+00:00 (3× re-verified)
Learned on **tasker** (acme) at iteration 3 · reused **3×**

**Fix strategy:**

Root cause: `editDraft` is stale after cancelling/closing the edit modal.

`openEdit()` currently does something like:

```js
editDraft = editDraft || { ... };
```

That means the draft is only created the first time, when `editDraft` is `null` or `undefined`.

But `closeModal()` only hides `#modal-edit`:

```js
modal.classList.add('hidden');
```

It does **not** clear `editDraft`. Therefore:

1. Open edit modal
2. Modify draft state
3. Close/cancel modal
4. Reopen edit modal
5. `editDraft` is still truthy
6. `openEdit()` reuses stale draft instead of creating a fresh one

`saveEdit()` clears `editDraft`, so the bug only appears when closing/cancelling without saving.

## Fix

Clear `editDraft` when closing the edit modal, and ideally also avoid `||` seeding in `openEdit()`.

### Minimal fix

```js
function closeModal(selector) {
  document.querySelector(selector).classList.add('hidden');

  if (selector === '#modal-edit') {
    editDraft = null;
  }
}
```

### Better fix

Always initialise a fresh draft when opening edit:

```js
function openEdit(item) {
  editDraft = {
    id: item.id,
    name: item.name,
    description: item.description,
    // etc...
  };

  document.querySelector('#modal-edit').classList.remove('hidden');
}
```

And still clear on close/cancel:

```js
function closeModal(selector) {
  document.querySelector(selector).classList.add('hidden');

  if (selector === '#modal-edit') {
    editDraft = null;
  }
}
```

This ensures `#modal-edit` never reopens with stale unsaved data.

**Code hint:** `openedit seeds editdraft with editdraft editdraft so it is only initialised when null closemodal only toggles the hidden class and never nulls editdraft only saveedit clears it`

<details><summary>machine-readable</summary>

```json
{
  "sig": "b7a3887a7811",
  "bug_class": "modal-state-not-reset",
  "strategy": "Root cause: `editDraft` is stale after cancelling/closing the edit modal.

`openEdit()` currently does something like:

```js
editDraft = editDraft || { ... };
```

That means the draft is only created the first time, when `editDraft` is `null` or `undefined`.

But `closeModal()` only hides `#modal-edit`:

```js
modal.classList.add('hidden');
```

It does **not** clear `editDraft`. Therefore:

1. Open edit modal
2. Modify draft state
3. Close/cancel modal
4. Reopen edit modal
5. `editDraft` is still truthy
6. `openEdit()` reuses stale draft instead of creating a fresh one

`saveEdit()` clears `editDraft`, so the bug only appears when closing/cancelling without saving.

## Fix

Clear `editDraft` when closing the edit modal, and ideally also avoid `||` seeding in `openEdit()`.

### Minimal fix

```js
function closeModal(selector) {
  document.querySelector(selector).classList.add('hidden');

  if (selector === '#modal-edit') {
    editDraft = null;
  }
}
```

### Better fix

Always initialise a fresh draft when opening edit:

```js
function openEdit(item) {
  editDraft = {
    id: item.id,
    name: item.name,
    description: item.description,
    // etc...
  };

  document.querySelector('#modal-edit').classList.remove('hidden');
}
```

And still clear on close/cancel:

```js
function closeModal(selector) {
  document.querySelector(selector).classList.add('hidden');

  if (selector === '#modal-edit') {
    editDraft = null;
  }
}
```

This ensures `#modal-edit` never reopens with stale unsaved data.",
  "code_hint": "openedit seeds editdraft with editdraft editdraft so it is only initialised when null closemodal only toggles the hidden class and never nulls editdraft only saveedit clears it",
  "verified": true,
  "uses": 3,
  "score": 0.9234,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T20:00:19.974+00:00",
  "verification_count": 3,
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

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T20:00:07.230+00:00 (3× re-verified)
Learned on **tasker** (acme) at iteration 2 · reused **3×**

**Fix strategy:**

Root cause: `editDraft` is stale after cancelling/closing the edit modal.

`openEdit()` currently does something like:

```js
editDraft = editDraft || { ... };
```

That means the draft is only created the first time, when `editDraft` is `null` or `undefined`.

But `closeModal()` only hides `#modal-edit`:

```js
modal.classList.add('hidden');
```

It does **not** clear `editDraft`. Therefore:

1. Open edit modal
2. Modify draft state
3. Close/cancel modal
4. Reopen edit modal
5. `editDraft` is still truthy
6. `openEdit()` reuses stale draft instead of creating a fresh one

`saveEdit()` clears `editDraft`, so the bug only appears when closing/cancelling without saving.

## Fix

Clear `editDraft` when closing the edit modal, and ideally also avoid `||` seeding in `openEdit()`.

### Minimal fix

```js
function closeModal(selector) {
  document.querySelector(selector).classList.add('hidden');

  if (selector === '#modal-edit') {
    editDraft = null;
  }
}
```

### Better fix

Always initialise a fresh draft when opening edit:

```js
function openEdit(item) {
  editDraft = {
    id: item.id,
    name: item.name,
    description: item.description,
    // etc...
  };

  document.querySelector('#modal-edit').classList.remove('hidden');
}
```

And still clear on close/cancel:

```js
function closeModal(selector) {
  document.querySelector(selector).classList.add('hidden');

  if (selector === '#modal-edit') {
    editDraft = null;
  }
}
```

This ensures `#modal-edit` never reopens with stale unsaved data.

**Code hint:** `openedit seeds editdraft with editdraft editdraft so it is only initialised when null closemodal only toggles the hidden class and never nulls editdraft only saveedit clears it`

<details><summary>machine-readable</summary>

```json
{
  "sig": "6c94eae3b140",
  "bug_class": "modal-state-not-reset",
  "strategy": "Root cause: `editDraft` is stale after cancelling/closing the edit modal.

`openEdit()` currently does something like:

```js
editDraft = editDraft || { ... };
```

That means the draft is only created the first time, when `editDraft` is `null` or `undefined`.

But `closeModal()` only hides `#modal-edit`:

```js
modal.classList.add('hidden');
```

It does **not** clear `editDraft`. Therefore:

1. Open edit modal
2. Modify draft state
3. Close/cancel modal
4. Reopen edit modal
5. `editDraft` is still truthy
6. `openEdit()` reuses stale draft instead of creating a fresh one

`saveEdit()` clears `editDraft`, so the bug only appears when closing/cancelling without saving.

## Fix

Clear `editDraft` when closing the edit modal, and ideally also avoid `||` seeding in `openEdit()`.

### Minimal fix

```js
function closeModal(selector) {
  document.querySelector(selector).classList.add('hidden');

  if (selector === '#modal-edit') {
    editDraft = null;
  }
}
```

### Better fix

Always initialise a fresh draft when opening edit:

```js
function openEdit(item) {
  editDraft = {
    id: item.id,
    name: item.name,
    description: item.description,
    // etc...
  };

  document.querySelector('#modal-edit').classList.remove('hidden');
}
```

And still clear on close/cancel:

```js
function closeModal(selector) {
  document.querySelector(selector).classList.add('hidden');

  if (selector === '#modal-edit') {
    editDraft = null;
  }
}
```

This ensures `#modal-edit` never reopens with stale unsaved data.",
  "code_hint": "openedit seeds editdraft with editdraft editdraft so it is only initialised when null closemodal only toggles the hidden class and never nulls editdraft only saveedit clears it",
  "verified": true,
  "uses": 3,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T20:00:07.230+00:00",
  "verification_count": 3,
  "born_at_iteration": 2,
  "saved_usd": 0.0,
  "origin_app": "tasker",
  "origin_org": "acme"
}
```
</details>
<!-- pattern:4f2912a15908 -->
## `4f2912a15908` — counter-off-by-one (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T20:02:01.647+00:00 (2× re-verified)
Learned on **tasker** (acme) at iteration 4 · reused **2×**

**Fix strategy:**

Root cause: `render()` still subtracts `1` from the active-task count:

```js
tasks.filter(t => !t.done).length - 1
```

That `-1` previously compensated for a pinned `"inbox"` row, but that row has since been removed from the markup. The stale compensation causes `#counter` to undercount by one.

Fix: remove the `-1`.

```js
function render() {
  const activeCount = tasks.filter(t => !t.done).length;
  document.querySelector('#counter').textContent = activeCount;
}
```

If the counter text includes a label:

```js
document.querySelector('#counter').textContent =
  `${activeCount} task${activeCount === 1 ? '' : 's'} remaining`;
```

Expected result: `#counter` now displays the actual number of unfinished tasks.

**Code hint:** `render computes tasks filter t t done length 1 the 1 compensated for a pinned inbox row that was removed from the markup the compensation was left behind`

<details><summary>machine-readable</summary>

```json
{
  "sig": "4f2912a15908",
  "bug_class": "counter-off-by-one",
  "strategy": "Root cause: `render()` still subtracts `1` from the active-task count:

```js
tasks.filter(t => !t.done).length - 1
```

That `-1` previously compensated for a pinned `\"inbox\"` row, but that row has since been removed from the markup. The stale compensation causes `#counter` to undercount by one.

Fix: remove the `-1`.

```js
function render() {
  const activeCount = tasks.filter(t => !t.done).length;
  document.querySelector('#counter').textContent = activeCount;
}
```

If the counter text includes a label:

```js
document.querySelector('#counter').textContent =
  `${activeCount} task${activeCount === 1 ? '' : 's'} remaining`;
```

Expected result: `#counter` now displays the actual number of unfinished tasks.",
  "code_hint": "render computes tasks filter t t done length 1 the 1 compensated for a pinned inbox row that was removed from the markup the compensation was left behind",
  "verified": true,
  "uses": 2,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T20:02:01.647+00:00",
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

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T19:57:07.073+00:00 (2× re-verified)
Learned on **tasker** (acme) at iteration 2 · reused **2×**

**Fix strategy:**

Root cause: `activeFilter` is changed programmatically in `addTask()` and `toggleTask()`, but the filter chip UI is only updated when a chip is clicked. So state becomes `"all"`, while the old `.chip.is-active` remains highlighted.

Fix: centralize filter changes and always sync chips using:

```js
const FILTER_CHIP_SELECTOR = '.chip[data-filter]';

function syncFilterChips() {
  document.querySelectorAll(FILTER_CHIP_SELECTOR).forEach(chip => {
    const isActive = chip.dataset.filter === activeFilter;
    chip.classList.toggle('is-active', isActive);
    chip.setAttribute('aria-pressed', String(isActive));
  });
}

function setActiveFilter(filter) {
  activeFilter = filter;
  render();
  syncFilterChips();
}
```

Then replace direct assignments:

```js
function addTask() {
  // create task...
  setActiveFilter('all');
}

function toggleTask(id) {
  // mutate task...
  setActiveFilter('all');
}
```

And update chip click handling:

```js
document.querySelectorAll('.chip[data-filter]').forEach(chip => {
  chip.addEventListener('click', () => {
    setActiveFilter(chip.dataset.filter);
  });
});
```

If `render()` recreates the chips, call `syncFilterChips()` at the end of `render()` instead:

```js
function render() {
  // existing render logic...

  syncFilterChips();
}
```

Key point: never do only this anymore:

```js
activeFilter = 'all';
render();
```

Use the shared path so state and `.chip[data-filter].is-active` stay in sync.

**Code hint:** `addtask and toggletask both assign activefilter all before render so the mutated task is guaranteed visible but neither updates the is active chip class control and state desync`

<details><summary>machine-readable</summary>

```json
{
  "sig": "9fa805fa7e62",
  "bug_class": "filter-state-lost-on-mutation",
  "strategy": "Root cause: `activeFilter` is changed programmatically in `addTask()` and `toggleTask()`, but the filter chip UI is only updated when a chip is clicked. So state becomes `\"all\"`, while the old `.chip.is-active` remains highlighted.

Fix: centralize filter changes and always sync chips using:

```js
const FILTER_CHIP_SELECTOR = '.chip[data-filter]';

function syncFilterChips() {
  document.querySelectorAll(FILTER_CHIP_SELECTOR).forEach(chip => {
    const isActive = chip.dataset.filter === activeFilter;
    chip.classList.toggle('is-active', isActive);
    chip.setAttribute('aria-pressed', String(isActive));
  });
}

function setActiveFilter(filter) {
  activeFilter = filter;
  render();
  syncFilterChips();
}
```

Then replace direct assignments:

```js
function addTask() {
  // create task...
  setActiveFilter('all');
}

function toggleTask(id) {
  // mutate task...
  setActiveFilter('all');
}
```

And update chip click handling:

```js
document.querySelectorAll('.chip[data-filter]').forEach(chip => {
  chip.addEventListener('click', () => {
    setActiveFilter(chip.dataset.filter);
  });
});
```

If `render()` recreates the chips, call `syncFilterChips()` at the end of `render()` instead:

```js
function render() {
  // existing render logic...

  syncFilterChips();
}
```

Key point: never do only this anymore:

```js
activeFilter = 'all';
render();
```

Use the shared path so state and `.chip[data-filter].is-active` stay in sync.",
  "code_hint": "addtask and toggletask both assign activefilter all before render so the mutated task is guaranteed visible but neither updates the is active chip class control and state desync",
  "verified": true,
  "uses": 2,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T19:57:07.073+00:00",
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

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T20:01:22.932+00:00 (5× re-verified)
Learned on **tasker** (acme) at iteration 4 · reused **5×**

**Fix strategy:**

Root cause: `addTask()` validates the raw input with:

```js
title.length === 0
```

That only rejects an actually empty string. A whitespace-only value like `"   "` has a length greater than `0`, so it passes validation and gets saved verbatim.

Fix: trim the input before validating, and preferably store the trimmed value too.

```js
function addTask() {
  const input = document.querySelector('#new-task');
  const title = input.value.trim();

  if (title.length === 0) {
    return;
  }

  // store the cleaned title
  tasks.push({
    title,
    completed: false
  });

  input.value = '';
  renderTasks();
}
```

If your existing code looks like this:

```js
const title = document.querySelector('#new-task').value;

if (title.length === 0) {
  return;
}
```

change it to:

```js
const title = document.querySelector('#new-task').value.trim();

if (title.length === 0) {
  return;
}
```

This prevents whitespace-only tasks and avoids storing titles with accidental leading/trailing spaces.

**Code hint:** `addtask guards on title length 0 rather than title trim length 0 so whitespace only input passes validation and is stored verbatim`

<details><summary>machine-readable</summary>

```json
{
  "sig": "7e406ab2999c",
  "bug_class": "missing-preventdefault",
  "strategy": "Root cause: `addTask()` validates the raw input with:

```js
title.length === 0
```

That only rejects an actually empty string. A whitespace-only value like `\"   \"` has a length greater than `0`, so it passes validation and gets saved verbatim.

Fix: trim the input before validating, and preferably store the trimmed value too.

```js
function addTask() {
  const input = document.querySelector('#new-task');
  const title = input.value.trim();

  if (title.length === 0) {
    return;
  }

  // store the cleaned title
  tasks.push({
    title,
    completed: false
  });

  input.value = '';
  renderTasks();
}
```

If your existing code looks like this:

```js
const title = document.querySelector('#new-task').value;

if (title.length === 0) {
  return;
}
```

change it to:

```js
const title = document.querySelector('#new-task').value.trim();

if (title.length === 0) {
  return;
}
```

This prevents whitespace-only tasks and avoids storing titles with accidental leading/trailing spaces.",
  "code_hint": "addtask guards on title length 0 rather than title trim length 0 so whitespace only input passes validation and is stored verbatim",
  "verified": true,
  "uses": 5,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T20:01:22.932+00:00",
  "verification_count": 5,
  "born_at_iteration": 4,
  "saved_usd": 0.0,
  "origin_app": "tasker",
  "origin_org": "acme"
}
```
</details>
<!-- pattern:0dddda0faee2 -->
## `0dddda0faee2` — dead-control (✅ verified)

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T20:01:15.901+00:00 (3× re-verified)
Learned on **tasker** (acme) at iteration 4 · reused **3×**

**Fix strategy:**

Confirmed.

**Root cause:** `init()` is binding the click handler to `#toast-dismiss`, but the actual close button in the markup is `#toast-close`. Because the missing selector is guarded/silent, the click handler is never attached and the toast close button does nothing.

**Fix:** update the selector used in `init()` to:

```js
selector = '#toast-close';
```

Example patch:

```diff
- const toastX = $('#toast-dismiss');
+ const toastX = $('#toast-close');

- if (toastX) {
+ if (toastX.length) {
    toastX.on('click', dismissToast);
  }
```

Or, with plain DOM:

```js
const toastX = document.querySelector('#toast-close');

if (toastX) {
  toastX.addEventListener('click', dismissToast);
}
```

Recommended improvement: log or fail loudly when the expected element is missing so selector mismatches are not silently swallowed.

**Code hint:** `init binds the click listener to toast dismiss an id that does not exist in the markup the button is toast close the if toastx guard swallows the miss silently`

<details><summary>machine-readable</summary>

```json
{
  "sig": "0dddda0faee2",
  "bug_class": "dead-control",
  "strategy": "Confirmed.

**Root cause:** `init()` is binding the click handler to `#toast-dismiss`, but the actual close button in the markup is `#toast-close`. Because the missing selector is guarded/silent, the click handler is never attached and the toast close button does nothing.

**Fix:** update the selector used in `init()` to:

```js
selector = '#toast-close';
```

Example patch:

```diff
- const toastX = $('#toast-dismiss');
+ const toastX = $('#toast-close');

- if (toastX) {
+ if (toastX.length) {
    toastX.on('click', dismissToast);
  }
```

Or, with plain DOM:

```js
const toastX = document.querySelector('#toast-close');

if (toastX) {
  toastX.addEventListener('click', dismissToast);
}
```

Recommended improvement: log or fail loudly when the expected element is missing so selector mismatches are not silently swallowed.",
  "code_hint": "init binds the click listener to toast dismiss an id that does not exist in the markup the button is toast close the if toastx guard swallows the miss silently",
  "verified": true,
  "uses": 3,
  "score": 0.9306,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T20:01:15.901+00:00",
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

Discovered by **ratchet** · root cause from **fixture** · fix verified by **fixture** at 2026-07-24T20:00:28.169+00:00 (3× re-verified)
Learned on **tasker** (acme) at iteration 3 · reused **3×**

**Fix strategy:**

Root cause: `addTask()` validates the raw input with:

```js
title.length === 0
```

That only rejects an actually empty string. A whitespace-only value like `"   "` has a length greater than `0`, so it passes validation and gets saved verbatim.

Fix: trim the input before validating, and preferably store the trimmed value too.

```js
function addTask() {
  const input = document.querySelector('#new-task');
  const title = input.value.trim();

  if (title.length === 0) {
    return;
  }

  // store the cleaned title
  tasks.push({
    title,
    completed: false
  });

  input.value = '';
  renderTasks();
}
```

If your existing code looks like this:

```js
const title = document.querySelector('#new-task').value;

if (title.length === 0) {
  return;
}
```

change it to:

```js
const title = document.querySelector('#new-task').value.trim();

if (title.length === 0) {
  return;
}
```

This prevents whitespace-only tasks and avoids storing titles with accidental leading/trailing spaces.

**Code hint:** `addtask guards on title length 0 rather than title trim length 0 so whitespace only input passes validation and is stored verbatim`

<details><summary>machine-readable</summary>

```json
{
  "sig": "a1735b95f51d",
  "bug_class": "missing-input-validation",
  "strategy": "Root cause: `addTask()` validates the raw input with:

```js
title.length === 0
```

That only rejects an actually empty string. A whitespace-only value like `\"   \"` has a length greater than `0`, so it passes validation and gets saved verbatim.

Fix: trim the input before validating, and preferably store the trimmed value too.

```js
function addTask() {
  const input = document.querySelector('#new-task');
  const title = input.value.trim();

  if (title.length === 0) {
    return;
  }

  // store the cleaned title
  tasks.push({
    title,
    completed: false
  });

  input.value = '';
  renderTasks();
}
```

If your existing code looks like this:

```js
const title = document.querySelector('#new-task').value;

if (title.length === 0) {
  return;
}
```

change it to:

```js
const title = document.querySelector('#new-task').value.trim();

if (title.length === 0) {
  return;
}
```

This prevents whitespace-only tasks and avoids storing titles with accidental leading/trailing spaces.",
  "code_hint": "addtask guards on title length 0 rather than title trim length 0 so whitespace only input passes validation and is stored verbatim",
  "verified": true,
  "uses": 3,
  "score": 0.9,
  "discovered_by": "ratchet",
  "root_cause_source": "fixture",
  "verified_by": "fixture",
  "verified_at": "2026-07-24T20:00:28.169+00:00",
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
