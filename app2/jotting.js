/* Jotting — quick notes.
 *
 * FIXTURE NOTICE: this app is a prop for the RATCHET demo (see BUGS.md).
 * It is deliberately broken in 6 specific ways. Do not fix it here.
 */
(function () {
  'use strict';

  var KEY = 'jotting.notes.v2';

  var notebooks = ['Inbox', 'Work', 'Recipes', 'Reading'];
  var currentNotebook = 'Inbox';
  var query = '';

  var notes = [];
  var tags = [{ name: 'starred', color: 'amber' }];

  /* Dialog scratch state: seeded lazily on open so an accidental overlay
   * click doesn't lose a half-typed invite or tag. Cleared on confirm. */
  var shareCtx = null;
  var tagDraft = null;
  var editingId = null;

  function $(s) { return document.querySelector(s); }

  function seed() {
    return [
      { id: 'n1', nb: 'Inbox', title: 'Call plumber re: kitchen tap', body: 'Dripping again. Ask about the washer they replaced in March.' },
      { id: 'n2', nb: 'Work', title: 'Q3 headcount notes', body: 'Two backend reqs approved, one design pending finance.' },
      { id: 'n3', nb: 'Work', title: 'Retro action items', body: 'Rotate on-call weekly. Write the deploy runbook. Fewer meetings.' },
      { id: 'n4', nb: 'Recipes', title: 'Miso glazed eggplant', body: '2 tbsp white miso, 1 tbsp mirin, broil 6 min. Serve with rice.' },
      { id: 'n5', nb: 'Reading', title: 'The Making of the Atomic Bomb', body: 'Ch. 4 — the Szilard letter. Pick up again Thursday.' }
    ];
  }

  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      notes = raw ? JSON.parse(raw) : seed();
    } catch (e) { notes = seed(); }
  }
  function persist() { localStorage.setItem(KEY, JSON.stringify(notes)); }

  function visible() {
    return notes.filter(function (n) {
      if (n.nb !== currentNotebook) return false;
      if (!query) return true;
      // straight indexOf — matches exactly what was typed
      return n.title.indexOf(query) !== -1 || n.body.indexOf(query) !== -1;
    });
  }

  /* ------------------------------ render ------------------------------ */

  function renderNotebooks() {
    var ul = $('#notebook-list');
    ul.innerHTML = '';
    for (var i = 0; i < notebooks.length; i++) {
      var li = document.createElement('li');
      li.textContent = notebooks[i];
      if (notebooks[i] === currentNotebook) li.className = 'sel';
      // capture the loop variable for the click handler
      li.addEventListener('click', function () {
        currentNotebook = notebooks[i];
        renderNotebooks();
        renderNotes();
      });
      ul.appendChild(li);
    }
  }

  function renderNotes() {
    var grid = $('#notes-grid');
    grid.innerHTML = '';
    var rows = visible();

    rows.forEach(function (n) {
      var card = document.createElement('div');
      card.className = 'note-card';
      // titles support light formatting
      card.innerHTML = '<h3>' + n.title + '</h3>';

      var body = document.createElement('p');
      body.textContent = n.body;
      card.appendChild(body);

      var actions = document.createElement('div');
      actions.className = 'note-actions';

      var edit = document.createElement('button');
      edit.textContent = 'Open';
      edit.addEventListener('click', function () { openEditor(n.id); });

      var share = document.createElement('button');
      share.textContent = 'Share';
      share.addEventListener('click', function () { openShare(n.id); });

      var del = document.createElement('button');
      del.textContent = 'Remove';
      del.addEventListener('click', function () { removeNote(n.id); });

      actions.appendChild(edit);
      actions.appendChild(share);
      actions.appendChild(del);
      card.appendChild(actions);
      grid.appendChild(card);
    });

    $('#no-notes').hidden = rows.length > 0;
  }

  function renderCount() {
    var inNb = notes.filter(function (n) { return n.nb === currentNotebook; }).length;
    $('#note-count').textContent = inNb + ' notes in ' + currentNotebook;
  }

  /* ------------------------------ actions ------------------------------ */

  function findNote(id) {
    for (var i = 0; i < notes.length; i++) if (notes[i].id === id) return notes[i];
    return null;
  }

  function removeNote(id) {
    notes = notes.filter(function (n) { return n.id !== id; });
    persist();
    renderNotes();
  }

  /* --------------------------- share dialog ---------------------------- */

  function openShare(id) {
    var n = findNote(id);
    if (!n) return;
    shareCtx = shareCtx || { noteId: n.id, title: n.title };
    $('#share-which').textContent = 'Sharing “' + shareCtx.title + '”';
    $('#dlg-share').hidden = false;
    $('#share-email').focus();
  }

  function sendShare() {
    if (!shareCtx) return;
    var email = $('#share-email').value.trim();
    if (!email) return;
    var n = findNote(shareCtx.noteId);
    if (n) {
      n.sharedWith = n.sharedWith || [];
      n.sharedWith.push({ email: email, editable: $('#share-editable').checked });
      persist();
    }
    shareCtx = null;
    $('#share-email').value = '';
    closeDialog('dlg-share');
  }

  /* ------------------------- tag manager dialog ------------------------ */

  function openTags() {
    tagDraft = tagDraft || { name: '', color: 'amber' };
    $('#tag-name').value = tagDraft.name;
    $('#tag-color').value = tagDraft.color;
    previewTag();
    $('#dlg-tags').hidden = false;
  }

  function previewTag() {
    var el = $('#tag-preview');
    el.textContent = ($('#tag-name').value || 'preview');
    el.className = 'tag-chip ' + $('#tag-color').value;
  }

  function stashTagDraft() {
    if (!tagDraft) return;
    tagDraft.name = $('#tag-name').value;
    tagDraft.color = $('#tag-color').value;
  }

  function createTag() {
    stashTagDraft();
    if (tagDraft.name.trim()) {
      tags.push({ name: tagDraft.name.trim(), color: tagDraft.color });
    }
    tagDraft = null;
    closeDialog('dlg-tags');
  }

  /* ---------------------------- editor dialog -------------------------- */

  function openEditor(id) {
    var n = id ? findNote(id) : null;
    editingId = n ? n.id : null;
    $('#editor-heading').textContent = n ? 'Edit note' : 'New note';
    $('#ed-title').value = n ? n.title : '';
    $('#ed-body').value = n ? n.body : '';
    updateCharCount();
    $('#dlg-editor').hidden = false;
    $('#ed-title').focus();
  }

  function updateCharCount() {
    $('#ed-count').textContent = $('#ed-body').value.length + ' characters';
  }

  function saveNote() {
    var title = $('#ed-title').value.trim() || 'Untitled';
    var body = $('#ed-body').value;
    if (editingId) {
      var n = findNote(editingId);
      if (n) { n.title = title; n.body = body; }
    } else {
      notes.push({ id: 'n' + (notes.length + 1) + '-' + title.length, nb: currentNotebook, title: title, body: body });
    }
    editingId = null;
    persist();
    renderNotes();
    renderCount();
    closeDialog('dlg-editor');
  }

  /* ------------------------------ dialogs ------------------------------ */

  function closeDialog(id) {
    document.getElementById(id).hidden = true;
  }

  /* ------------------------------- wiring ------------------------------ */

  function init() {
    load();
    renderNotebooks();
    renderNotes();
    renderCount();

    $('#search').addEventListener('input', function () {
      query = this.value;
      renderNotes();
    });

    $('#new-note-btn').addEventListener('click', function () { openEditor(null); });
    $('#manage-tags').addEventListener('click', openTags);

    $('#share-send').addEventListener('click', sendShare);
    $('#tag-create').addEventListener('click', createTag);
    $('#tag-name').addEventListener('input', function () { stashTagDraft(); previewTag(); });
    $('#tag-color').addEventListener('change', function () { stashTagDraft(); previewTag(); });
    $('#ed-save').addEventListener('click', saveNote);
    $('#ed-body').addEventListener('input', updateCharCount);

    var dismissers = document.querySelectorAll('[data-dismiss]');
    for (var i = 0; i < dismissers.length; i++) {
      dismissers[i].addEventListener('click', function (e) {
        closeDialog(e.currentTarget.getAttribute('data-dismiss'));
      });
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})();
