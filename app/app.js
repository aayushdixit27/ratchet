/* Tasker — a small task tracker.
 *
 * NOTE FOR HUMANS READING THIS REPO: this app is a fixture. It is deliberately
 * broken in 8 specific ways (see BUGS.md). Do not "fix" it — it is the
 * subject under test for the RATCHET agent. The bugs are written to look like
 * ordinary drift, not like planted traps.
 */

(function () {
  'use strict';

  var STORE_KEY = 'tasker.tasks.v1';
  var SETTINGS_KEY = 'tasker.settings.v1';

  var tasks = [];
  var settings = { confirmDelete: true, compact: false, name: 'there' };
  var activeFilter = 'all';

  /* ------------------------------------------------------------------
   * Modal draft state.
   *
   * Each modal keeps a scratch object so a half-finished edit survives an
   * accidental click outside the dialog ("resume where you left off").
   * The drafts are seeded on open and cleared on save.
   * ------------------------------------------------------------------ */
  var editingId = null;
  var editDraft = null;
  var settingsDraft = null;
  var pendingDelete = null;

  var $ = function (sel) { return document.querySelector(sel); };

  /* ---------------------------- persistence ---------------------------- */

  function load() {
    try {
      var rawTasks = localStorage.getItem(STORE_KEY);
      tasks = rawTasks ? JSON.parse(rawTasks) : seed();
      var rawSettings = localStorage.getItem(SETTINGS_KEY);
      if (rawSettings) settings = JSON.parse(rawSettings);
    } catch (e) {
      tasks = seed();
    }
  }

  function save() {
    localStorage.setItem(STORE_KEY, JSON.stringify(tasks));
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
  }

  function seed() {
    return [
      { id: 1, title: 'Draft the Q3 release notes', notes: '', priority: 'normal', done: false },
      { id: 2, title: 'Review pull request #412', notes: 'Blocked on CI', priority: 'high', done: false },
      { id: 3, title: 'Renew the TLS certificate', notes: '', priority: 'high', done: false },
      { id: 4, title: 'Archive last quarter invoices', notes: '', priority: 'low', done: true }
    ];
  }

  function nextId() {
    var max = 0;
    for (var i = 0; i < tasks.length; i++) if (tasks[i].id > max) max = tasks[i].id;
    return max + 1;
  }

  function findTask(id) {
    for (var i = 0; i < tasks.length; i++) if (tasks[i].id === id) return tasks[i];
    return null;
  }

  /* ------------------------------ render ------------------------------ */

  function visibleTasks() {
    if (activeFilter === 'active') return tasks.filter(function (t) { return !t.done; });
    if (activeFilter === 'done') return tasks.filter(function (t) { return t.done; });
    return tasks.slice();
  }

  function render() {
    var list = $('#task-list');
    list.innerHTML = '';
    var rows = visibleTasks();

    rows.forEach(function (t) {
      var li = document.createElement('li');
      li.className = 'task' + (t.done ? ' is-done' : '') + (settings.compact ? ' compact' : '');
      li.setAttribute('data-id', String(t.id));

      var cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.checked = t.done;
      cb.className = 'task-check';
      cb.setAttribute('aria-label', 'Mark "' + t.title + '" complete');
      cb.addEventListener('change', function () { toggleTask(t.id); });

      var span = document.createElement('span');
      span.className = 'title';
      span.textContent = t.title;

      var pri = document.createElement('span');
      pri.className = 'pri ' + t.priority;
      pri.textContent = t.priority;

      var edit = document.createElement('button');
      edit.className = 'icon-btn btn-edit';
      edit.textContent = 'Edit';
      edit.setAttribute('aria-label', 'Edit "' + t.title + '"');
      edit.addEventListener('click', function () { openEdit(t.id); });

      var del = document.createElement('button');
      del.className = 'icon-btn btn-delete';
      del.textContent = 'Delete';
      del.setAttribute('aria-label', 'Delete "' + t.title + '"');
      del.addEventListener('click', function () { requestDelete(t.id); });

      li.appendChild(cb);
      li.appendChild(span);
      li.appendChild(pri);
      li.appendChild(edit);
      li.appendChild(del);
      list.appendChild(li);
    });

    $('#empty').classList.toggle('hidden', rows.length > 0);

    // The list used to render a pinned "inbox" row that was not a real task,
    // so the visible count was adjusted down by one. The pinned row is gone.
    var remaining = tasks.filter(function (t) { return !t.done; }).length - 1;
    $('#counter').textContent = remaining + (remaining === 1 ? ' task remaining' : ' tasks remaining');
  }

  /* ------------------------------ actions ------------------------------ */

  function addTask() {
    var input = $('#new-task');
    var title = input.value;
    if (title.length === 0) return;

    tasks.push({ id: nextId(), title: title, notes: '', priority: 'normal', done: false });
    input.value = '';

    // Make sure the task the user just created is actually on screen.
    activeFilter = 'all';

    save();
    render();
    showToast('Task added.');
  }

  function toggleTask(id) {
    var t = findTask(id);
    if (!t) return;
    t.done = !t.done;

    activeFilter = 'all';

    save();
    render();
  }

  /* ------------------------- edit-task modal -------------------------- */

  function openEdit(id) {
    var t = findTask(id);
    if (!t) return;
    editingId = id;

    // Resume an in-progress edit if one is still around, otherwise seed fresh.
    editDraft = editDraft || { title: t.title, notes: t.notes, priority: t.priority };

    $('#edit-title').value = editDraft.title;
    $('#edit-notes').value = editDraft.notes;
    $('#edit-priority').value = editDraft.priority;

    $('#modal-edit').classList.remove('hidden');
    $('#edit-title').focus();
  }

  function saveEdit() {
    var t = findTask(editingId);
    if (t) {
      t.title = $('#edit-title').value;
      t.notes = $('#edit-notes').value;
      t.priority = $('#edit-priority').value;
    }
    editDraft = null;
    editingId = null;
    save();
    render();
    closeModal('modal-edit');
    showToast('Task updated.');
  }

  /* -------------------------- settings modal -------------------------- */

  function openSettings() {
    settingsDraft = settingsDraft || {
      confirmDelete: settings.confirmDelete,
      compact: settings.compact,
      name: settings.name
    };

    $('#set-confirm').checked = settingsDraft.confirmDelete;
    $('#set-compact').checked = settingsDraft.compact;
    $('#set-name').value = settingsDraft.name;

    $('#modal-settings').classList.remove('hidden');
  }

  function stashSettingsDraft() {
    if (!settingsDraft) return;
    settingsDraft.confirmDelete = $('#set-confirm').checked;
    settingsDraft.compact = $('#set-compact').checked;
    settingsDraft.name = $('#set-name').value;
  }

  function saveSettings() {
    stashSettingsDraft();
    settings.confirmDelete = settingsDraft.confirmDelete;
    settings.compact = settingsDraft.compact;
    settings.name = settingsDraft.name;
    settingsDraft = null;
    save();
    render();
    closeModal('modal-settings');
    showToast('Settings saved.');
  }

  /* ------------------------ confirm-delete modal ----------------------- */

  function requestDelete(id) {
    var t = findTask(id);
    if (!t) return;

    if (!settings.confirmDelete) {
      removeTask(id);
      return;
    }

    // Hold onto what we are about to delete until the user answers.
    pendingDelete = pendingDelete || { id: t.id, title: t.title };

    $('#confirm-text').textContent = 'Delete "' + pendingDelete.title + '"? This cannot be undone.';
    $('#modal-confirm').classList.remove('hidden');
  }

  function confirmDelete() {
    if (pendingDelete) removeTask(pendingDelete.id);
    pendingDelete = null;
    closeModal('modal-confirm');
  }

  function removeTask(id) {
    tasks = tasks.filter(function (t) { return t.id !== id; });
    save();
    render();
    showToast('Task deleted.');
  }

  /* ------------------------------ modals ------------------------------ */

  function closeModal(id) {
    document.getElementById(id).classList.add('hidden');
  }

  /* ------------------------------ toast ------------------------------- */

  function showToast(msg) {
    $('#toast-msg').textContent = msg;
    $('#toast').classList.remove('hidden');
  }

  /* ------------------------------- wiring ------------------------------ */

  function init() {
    load();
    render();

    $('#btn-add').addEventListener('click', addTask);
    $('#new-task').addEventListener('keydown', function (e) {
      if (e.key === 'Enter') addTask();
    });

    var chips = document.querySelectorAll('.chip');
    for (var i = 0; i < chips.length; i++) {
      chips[i].addEventListener('click', function (e) {
        activeFilter = e.currentTarget.getAttribute('data-filter');
        for (var j = 0; j < chips.length; j++) chips[j].classList.remove('is-active');
        e.currentTarget.classList.add('is-active');
        render();
      });
    }

    $('#btn-settings').addEventListener('click', openSettings);
    $('#btn-save-settings').addEventListener('click', saveSettings);
    $('#set-confirm').addEventListener('change', stashSettingsDraft);
    $('#set-compact').addEventListener('change', stashSettingsDraft);
    $('#set-name').addEventListener('input', stashSettingsDraft);

    $('#btn-save-edit').addEventListener('click', saveEdit);
    $('#edit-title').addEventListener('input', function () { if (editDraft) editDraft.title = this.value; });
    $('#edit-notes').addEventListener('input', function () { if (editDraft) editDraft.notes = this.value; });
    $('#edit-priority').addEventListener('change', function () { if (editDraft) editDraft.priority = this.value; });

    $('#btn-confirm-delete').addEventListener('click', confirmDelete);

    var closers = document.querySelectorAll('[data-close]');
    for (var k = 0; k < closers.length; k++) {
      closers[k].addEventListener('click', function (e) {
        closeModal(e.currentTarget.getAttribute('data-close'));
      });
    }

    var toastX = $('#toast-dismiss');
    if (toastX) toastX.addEventListener('click', function () { $('#toast').classList.add('hidden'); });

    showToast('Welcome back, ' + settings.name + '.');
  }

  document.addEventListener('DOMContentLoaded', init);
})();
