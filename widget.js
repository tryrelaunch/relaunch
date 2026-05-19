/* widget.js — Relaunch / Boatr production edit widget.
 * Lives at https://tryrelaunch.com/widget.js (also reachable at tryrelaunch.netlify.app/widget.js).
 * Loaded cross-origin by customer sites when their bootstrap script detects a valid JWT.
 *
 * Expects window.__relaunchWidgetConfig to be set BEFORE this script loads:
 *   {
 *     slug: "spork",
 *     token: "<jwt>",
 *     endpoint: "https://tryrelaunch.com/.netlify/functions/edit-persistent",
 *     editPageUrl: "/edit/",
 *     supportEmail: "support@tryrelaunch.com"
 *   }
 *
 * Modes:
 *   - Chat mode: type natural-language requests. Server routes through Claude.
 *   - Click-to-edit: click any [id^="edit-"] element to edit inline. Direct ops, no AI.
 *
 * Reliability features:
 *   - One-step undo on every successful change.
 *   - Specific "30-60s rebuild" messaging + 60s auto-refresh countdown.
 *   - Server-confirmed DOM updates (no optimistic divergence).
 */
(function () {
  'use strict';

  if (window.__relaunchWidgetMounted) return;

  const cfg = window.__relaunchWidgetConfig;
  if (!cfg || !cfg.slug || !cfg.token || !cfg.endpoint) {
    console.warn('[Relaunch] Widget config missing - not mounting.');
    return;
  }
  window.__relaunchWidgetMounted = true;

  const SLUG = cfg.slug;
  const TOKEN = cfg.token;
  const ENDPOINT = cfg.endpoint;
  const EDIT_PAGE = cfg.editPageUrl || '/edit/';
  const SUPPORT_EMAIL = cfg.supportEmail || 'support@tryrelaunch.com';

  const css = `
    .rl-fab { position: fixed; bottom: 24px; right: 24px; z-index: 999998;
      background: #1a3320; color: #fff; padding: 12px 18px; border-radius: 999px;
      display: inline-flex; align-items: center; gap: 10px; border: none;
      font: 600 13px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      letter-spacing: 0.04em; cursor: pointer;
      box-shadow: 0 10px 30px rgba(0,0,0,0.25);
      transition: transform 0.2s, background 0.2s; }
    .rl-fab:hover { background: #0e1f15; transform: translateY(-2px); }
    .rl-fab-dot { width: 8px; height: 8px; background: #4baf0f; border-radius: 50%;
      animation: rl-pulse 2s ease-in-out infinite; }
    @keyframes rl-pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(1.2)} }

    .rl-panel { position: fixed; bottom: 86px; right: 24px; z-index: 999999;
      width: min(380px, calc(100vw - 48px)); max-height: 70vh;
      background: #1a3320; color: #fff; border-radius: 12px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.4); display: none;
      flex-direction: column; overflow: hidden;
      border: 1px solid rgba(255,255,255,0.08);
      font: 14px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .rl-panel.rl-open { display: flex; }
    .rl-panel-header { padding: 14px 18px;
      border-bottom: 1px solid rgba(255,255,255,0.08);
      display: flex; justify-content: space-between; align-items: center; gap: 8px; }
    .rl-panel-title { font-weight: 800; letter-spacing: 0.02em;
      display: flex; align-items: center; gap: 8px; font-size: 14px; }
    .rl-panel-title-dot { width: 7px; height: 7px; background: #4baf0f; border-radius: 50%; }
    .rl-header-actions { display: flex; gap: 6px; align-items: center; }
    .rl-mode-toggle { background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.85);
      border: 1px solid rgba(255,255,255,0.12); border-radius: 999px;
      padding: 5px 11px; font: 700 11px inherit; cursor: pointer; letter-spacing: 0.04em;
      transition: all 0.15s; }
    .rl-mode-toggle:hover { background: rgba(75,175,15,0.18); color: #6ec934; border-color: #4baf0f; }
    .rl-mode-toggle.rl-active { background: #4baf0f; color: #1a3320; border-color: #4baf0f; }
    .rl-panel-close { background: none; border: none; color: rgba(255,255,255,0.6);
      font-size: 22px; cursor: pointer; line-height: 1; }
    .rl-panel-close:hover { color: #fff; }

    .rl-messages { flex: 1; overflow-y: auto; padding: 14px;
      display: flex; flex-direction: column; gap: 10px; min-height: 200px; }
    .rl-msg { padding: 10px 14px; border-radius: 12px; font-size: 14px;
      line-height: 1.45; max-width: 86%; word-wrap: break-word; }
    .rl-msg-user { background: #4baf0f; color: #1a3320; align-self: flex-end;
      border-bottom-right-radius: 3px; font-weight: 600; }
    .rl-msg-assistant { background: rgba(255,255,255,0.06); color: rgba(255,255,255,0.92);
      align-self: flex-start; border-bottom-left-radius: 3px; }
    .rl-msg-system { background: rgba(75,175,15,0.18); color: #6ec934;
      align-self: flex-start; border-bottom-left-radius: 3px; font-size: 13px; }
    .rl-msg-error { background: rgba(239,68,68,0.18); color: #f97171;
      align-self: flex-start; border-bottom-left-radius: 3px; font-size: 13px; }
    .rl-msg-actions { margin-top: 8px; display: flex; gap: 6px; flex-wrap: wrap; }
    .rl-undo-btn { background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.9);
      border: 1px solid rgba(255,255,255,0.18); border-radius: 6px;
      padding: 4px 10px; font: 700 11px inherit; cursor: pointer; transition: all 0.15s; }
    .rl-undo-btn:hover { background: rgba(239,68,68,0.18); color: #f97171; border-color: #f97171; }
    .rl-undo-btn:disabled { opacity: 0.5; cursor: not-allowed; }
    .rl-countdown { color: rgba(110,201,52,0.85); font-weight: 700; font-variant-numeric: tabular-nums; }

    .rl-typing { padding: 8px 16px; display: none; gap: 4px; }
    .rl-typing.rl-show { display: flex; }
    .rl-typing span { width: 6px; height: 6px; background: #6ec934; border-radius: 50%;
      animation: rl-bounce 1.4s ease-in-out infinite; }
    .rl-typing span:nth-child(2) { animation-delay: 0.15s; }
    .rl-typing span:nth-child(3) { animation-delay: 0.3s; }
    @keyframes rl-bounce { 0%,80%,100%{opacity:0.3;transform:translateY(0)} 40%{opacity:1;transform:translateY(-4px)} }

    .rl-actions { padding: 0 14px 10px; display: flex; gap: 6px; flex-wrap: wrap; }
    .rl-action-btn { background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.1); color: rgba(255,255,255,0.75);
      border-radius: 16px; padding: 6px 12px; font-size: 12px; cursor: pointer;
      font-family: inherit; transition: all 0.2s; }
    .rl-action-btn:hover { background: rgba(75,175,15,0.18); color: #6ec934; border-color: #4baf0f; }

    .rl-input-row { padding: 12px 14px 14px;
      border-top: 1px solid rgba(255,255,255,0.06);
      display: flex; gap: 8px; align-items: flex-end; }
    .rl-input { flex: 1; background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.1); border-radius: 8px;
      padding: 10px 12px; font: inherit; font-size: 14px; color: #fff;
      outline: none; resize: none; min-height: 40px; max-height: 100px;
      line-height: 1.4; box-sizing: border-box; }
    .rl-input::placeholder { color: rgba(255,255,255,0.3); }
    .rl-input:focus { border-color: #4baf0f; }
    .rl-send { background: #4baf0f; color: #1a3320; border: none;
      border-radius: 8px; width: 40px; height: 40px; cursor: pointer;
      font-size: 18px; flex-shrink: 0; font-weight: 900;
      transition: background 0.2s; }
    .rl-send:hover { background: #6ec934; }
    .rl-send:disabled { background: rgba(255,255,255,0.1); cursor: not-allowed; }

    body.rl-click-mode [id^="edit-"]:not(.rl-editing) {
      outline: 1px dashed rgba(75,175,15,0.55); outline-offset: 3px;
      cursor: text; transition: outline 0.12s, background 0.12s; }
    body.rl-click-mode [id^="edit-"]:hover:not(.rl-editing) {
      outline: 2px solid #4baf0f; outline-offset: 3px;
      background: rgba(75,175,15,0.07); }
    body.rl-click-mode .rl-panel [id^="edit-"],
    body.rl-click-mode .rl-panel [id^="edit-"]:hover {
      outline: none; background: transparent; cursor: auto; }
    .rl-editing { outline: 2px solid #6ec934 !important; outline-offset: 3px;
      background: rgba(75,175,15,0.08); }

    .rl-click-banner { position: fixed; top: 80px; left: 50%; transform: translateX(-50%);
      z-index: 999997; background: #4baf0f; color: #1a3320;
      padding: 10px 16px; border-radius: 999px;
      font: 700 13px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      box-shadow: 0 8px 24px rgba(75,175,15,0.36);
      display: none; align-items: center; gap: 12px; }
    .rl-click-banner.rl-show { display: flex; }
    .rl-click-banner button { background: rgba(26,51,32,0.18); color: #1a3320;
      border: none; padding: 5px 10px; border-radius: 5px;
      font: 700 11px inherit; cursor: pointer; }
    .rl-click-banner button:hover { background: rgba(26,51,32,0.32); }

    .rl-click-toolbar { position: absolute; z-index: 999999;
      background: #1a3320; color: #fff; padding: 7px;
      border-radius: 8px; display: flex; gap: 6px; align-items: center;
      box-shadow: 0 10px 28px rgba(0,0,0,0.4);
      font: 700 12px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .rl-click-toolbar button { background: rgba(255,255,255,0.12); color: #fff;
      border: none; padding: 7px 11px; border-radius: 5px;
      font: 700 12px inherit; cursor: pointer; transition: all 0.12s; }
    .rl-click-toolbar button:hover { background: rgba(255,255,255,0.22); }
    .rl-click-toolbar .rl-tb-save { background: #4baf0f; color: #1a3320; }
    .rl-click-toolbar .rl-tb-save:hover { background: #6ec934; }

    .rl-flash { background: linear-gradient(90deg, transparent 0%, rgba(75,175,15,0.28) 50%, transparent 100%) !important;
      background-size: 200% 100% !important; animation: rl-flash 1.6s ease !important; }
    @keyframes rl-flash { from { background-position: 200% 0; } to { background-position: -200% 0; } }

    @media (max-width: 480px) {
      .rl-panel { right: 12px; left: 12px; width: auto; }
      .rl-fab { bottom: 16px; right: 16px; }
      .rl-click-banner { top: 12px; font-size: 11px; padding: 8px 12px; }
    }
  `;

  function injectStyles() {
    const style = document.createElement('style');
    style.id = 'rl-widget-styles';
    style.textContent = css;
    document.head.appendChild(style);
  }

  let panelEl, messagesEl, typingEl, inputEl, sendBtn, fabEl, modeToggleEl, bannerEl;
  let isLoading = false;
  let clickMode = false;
  let currentEditing = null;

  function buildDom() {
    fabEl = document.createElement('button');
    fabEl.className = 'rl-fab';
    fabEl.type = 'button';
    fabEl.innerHTML = '<span class="rl-fab-dot"></span> Edit your site';
    fabEl.addEventListener('click', togglePanel);
    document.body.appendChild(fabEl);

    panelEl = document.createElement('div');
    panelEl.className = 'rl-panel';
    panelEl.innerHTML =
      '<div class="rl-panel-header">' +
      '  <div class="rl-panel-title">' +
      '    <span class="rl-panel-title-dot"></span>Edit your site' +
      '  </div>' +
      '  <div class="rl-header-actions">' +
      '    <button class="rl-mode-toggle" type="button" title="Click any text on the page to edit it">Click to edit</button>' +
      '    <button class="rl-panel-close" type="button" aria-label="Close">&times;</button>' +
      '  </div>' +
      '</div>' +
      '<div class="rl-messages"></div>' +
      '<div class="rl-typing"><span></span><span></span><span></span></div>' +
      '<div class="rl-actions">' +
      '  <button class="rl-action-btn rl-help-btn" type="button">Request human help</button>' +
      '</div>' +
      '<div class="rl-input-row">' +
      '  <textarea class="rl-input" rows="1" placeholder="What would you like to change?"></textarea>' +
      '  <button class="rl-send" type="button" aria-label="Send">&rarr;</button>' +
      '</div>';
    document.body.appendChild(panelEl);

    bannerEl = document.createElement('div');
    bannerEl.className = 'rl-click-banner';
    bannerEl.innerHTML = '<span>Click any text on the page to edit it</span><button type="button">Exit</button>';
    document.body.appendChild(bannerEl);
    bannerEl.querySelector('button').addEventListener('click', exitClickMode);

    messagesEl = panelEl.querySelector('.rl-messages');
    typingEl = panelEl.querySelector('.rl-typing');
    inputEl = panelEl.querySelector('.rl-input');
    sendBtn = panelEl.querySelector('.rl-send');
    modeToggleEl = panelEl.querySelector('.rl-mode-toggle');

    panelEl.querySelector('.rl-panel-close').addEventListener('click', togglePanel);
    panelEl.querySelector('.rl-help-btn').addEventListener('click', requestHumanHelp);
    modeToggleEl.addEventListener('click', toggleClickMode);
    sendBtn.addEventListener('click', sendEdit);
    inputEl.addEventListener('input', autoResize);
    inputEl.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendEdit(); }
    });

    addMessage("Hi! Type a change in the box, or click 'Click to edit' to edit any text right on the page.", 'assistant');
  }

  function togglePanel() {
    panelEl.classList.toggle('rl-open');
    if (panelEl.classList.contains('rl-open')) {
      setTimeout(function () { inputEl.focus(); }, 100);
    }
  }

  function autoResize() {
    inputEl.style.height = 'auto';
    inputEl.style.height = Math.min(inputEl.scrollHeight, 100) + 'px';
  }

  function addMessage(text, kind) {
    const div = document.createElement('div');
    div.className = 'rl-msg rl-msg-' + kind;
    div.textContent = text;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return div;
  }

  function addSuccessMessage(text, previousById) {
    const div = document.createElement('div');
    div.className = 'rl-msg rl-msg-system';
    const textSpan = document.createElement('span');
    textSpan.textContent = text + ' ';
    div.appendChild(textSpan);

    const countdown = document.createElement('span');
    countdown.className = 'rl-countdown';
    countdown.textContent = '60s';
    div.appendChild(countdown);

    if (previousById && Object.keys(previousById).length > 0) {
      const actions = document.createElement('div');
      actions.className = 'rl-msg-actions';
      const undoBtn = document.createElement('button');
      undoBtn.className = 'rl-undo-btn';
      undoBtn.type = 'button';
      undoBtn.textContent = 'Undo';
      undoBtn.addEventListener('click', function () {
        undoBtn.disabled = true;
        undoBtn.textContent = 'Undoing...';
        undoChange(previousById).then(function (ok) {
          if (ok) { undoBtn.textContent = 'Undone'; }
          else { undoBtn.disabled = false; undoBtn.textContent = 'Undo'; }
        });
      });
      actions.appendChild(undoBtn);
      div.appendChild(actions);
    }

    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;

    let seconds = 60;
    const tick = setInterval(function () {
      seconds--;
      if (seconds <= 0) {
        clearInterval(tick);
        countdown.textContent = 'reloading...';
        setTimeout(function () { location.reload(); }, 500);
      } else {
        countdown.textContent = seconds + 's';
      }
    }, 1000);
  }

  function setLoading(loading) {
    isLoading = loading;
    sendBtn.disabled = loading;
    typingEl.classList.toggle('rl-show', loading);
    if (loading) messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function applyChanges(changes) {
    for (const change of changes) {
      const el = document.getElementById(change.id);
      if (el && el.children.length === 0) {
        el.textContent = change.text;
      }
    }
  }

  function captureCurrent(ids) {
    const out = {};
    for (const id of ids) {
      const el = document.getElementById(id);
      if (el && el.children.length === 0) {
        out[id] = el.textContent;
      }
    }
    return out;
  }

  function getCurrentPage() {
    try {
      const path = String(window.location.pathname || '')
        .replace(/^\/+|\/+$/g, '')
        .replace(/\/?index\.html?$/i, '');
      return path;
    } catch (e) {
      return '';
    }
  }

  function requestHumanHelp() {
    const lastReq = inputEl.value || '(describe what you need here)';
    const subject = encodeURIComponent('[' + SLUG + '] Edit help needed');
    const body = encodeURIComponent(
      'Site: ' + SLUG + '\nPage: ' + window.location.href + '\n\nWhat I need:\n' + lastReq + '\n\n--\nSent from the edit widget.'
    );
    window.location.href = 'mailto:' + SUPPORT_EMAIL + '?subject=' + subject + '&body=' + body;
  }

  async function sendEdit() {
    if (isLoading) return;
    const request = inputEl.value.trim();
    if (!request) return;

    inputEl.value = '';
    autoResize();
    addMessage(request, 'user');
    setLoading(true);

    try {
      const res = await fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + TOKEN },
        body: JSON.stringify({ slug: SLUG, request: request, page: getCurrentPage() })
      });

      if (res.status === 401) {
        addMessage('Your edit session expired. Redirecting to log in...', 'error');
        setLoading(false);
        try { localStorage.removeItem('relaunch_jwt'); } catch (e) {}
        setTimeout(function () { window.location.href = EDIT_PAGE; }, 1500);
        return;
      }
      if (res.status === 429) {
        addMessage("You've hit the edit limit for this hour. Take a breather and try again in a bit.", 'error');
        setLoading(false);
        return;
      }
      if (!res.ok) {
        addMessage("Something went wrong on our end. Try again in a moment, or use 'Request human help'.", 'error');
        setLoading(false);
        return;
      }

      const data = await res.json();
      setLoading(false);

      if (Array.isArray(data.changes) && data.changes.length > 0) {
        const ids = data.changes.map(function (c) { return c.id; });
        const previousById = captureCurrent(ids);
        applyChanges(data.changes);
        const n = data.changes.length;
        addSuccessMessage(
          'Saved ' + n + ' change' + (n === 1 ? '' : 's') + '. Your live site updates in ~30-60 seconds. Page refreshes in',
          previousById
        );
      } else {
        addMessage(data.confirmation || "I couldn't make that change automatically. Try rephrasing, or use 'Request human help'.", 'assistant');
      }
    } catch (err) {
      setLoading(false);
      addMessage("Couldn't reach the edit service. Check your connection and try again.", 'error');
    }
  }

  async function saveOps(ops, previousById, label) {
    setLoading(true);
    try {
      const res = await fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + TOKEN },
        body: JSON.stringify({ slug: SLUG, ops: ops, page: getCurrentPage() })
      });

      if (res.status === 401) {
        addMessage('Your edit session expired. Redirecting to log in...', 'error');
        setLoading(false);
        try { localStorage.removeItem('relaunch_jwt'); } catch (e) {}
        setTimeout(function () { window.location.href = EDIT_PAGE; }, 1500);
        return false;
      }
      if (res.status === 429) {
        addMessage("You've hit the edit limit for this hour. Take a breather and try again in a bit.", 'error');
        setLoading(false);
        return false;
      }
      if (!res.ok) {
        addMessage("Something went wrong saving that change. Try again or use 'Request human help'.", 'error');
        setLoading(false);
        return false;
      }

      const data = await res.json();
      setLoading(false);

      if (Array.isArray(data.changes) && data.changes.length > 0) {
        applyChanges(data.changes);
        for (const change of data.changes) {
          const el = document.getElementById(change.id);
          if (el) {
            el.classList.add('rl-flash');
            setTimeout(function () { el.classList.remove('rl-flash'); }, 1600);
          }
        }
        addSuccessMessage(
          (label || ('Saved ' + data.changes.length + ' change' + (data.changes.length === 1 ? '' : 's') + '.'))
            + ' Live site updates in ~30-60 seconds. Page refreshes in',
          previousById || null
        );
        return true;
      } else {
        addMessage("Server didn't apply the change. The element may not be editable.", 'error');
        return false;
      }
    } catch (err) {
      setLoading(false);
      addMessage("Couldn't reach the edit service. Check your connection and try again.", 'error');
      return false;
    }
  }

  async function undoChange(previousById) {
    const ids = Object.keys(previousById);
    const ops = ids.map(function (id) {
      return { op: 'replace_text', id: id, text: previousById[id] };
    });
    if (ops.length === 0) return false;
    return await saveOps(ops, null, 'Reverted to previous version.');
  }

  function toggleClickMode() {
    if (clickMode) exitClickMode(); else enterClickMode();
  }

  function enterClickMode() {
    clickMode = true;
    document.body.classList.add('rl-click-mode');
    bannerEl.classList.add('rl-show');
    modeToggleEl.classList.add('rl-active');
    modeToggleEl.textContent = 'Exit click mode';
    panelEl.classList.remove('rl-open');
    document.addEventListener('click', clickHandler, true);
  }

  function exitClickMode() {
    clickMode = false;
    document.body.classList.remove('rl-click-mode');
    bannerEl.classList.remove('rl-show');
    modeToggleEl.classList.remove('rl-active');
    modeToggleEl.textContent = 'Click to edit';
    document.removeEventListener('click', clickHandler, true);
    if (currentEditing) finishEditing(currentEditing, true);
  }

  function clickHandler(e) {
    if (e.target.closest('.rl-panel, .rl-fab, .rl-click-toolbar, .rl-click-banner')) return;
    const target = e.target.closest('[id^="edit-"]');
    if (!target) {
      e.preventDefault();
      e.stopPropagation();
      return;
    }
    if (target.classList.contains('rl-editing')) return;
    e.preventDefault();
    e.stopPropagation();
    if (target.children.length > 0) {
      panelEl.classList.add('rl-open');
      addMessage(
        "That section has multiple editable parts inside it (like a headline plus a subtitle). Click the specific piece you want to change.",
        'assistant'
      );
      return;
    }
    if (currentEditing && currentEditing !== target) {
      finishEditing(currentEditing, false);
    }
    selectForEditing(target);
  }

  function selectForEditing(el) {
    currentEditing = el;
    el.dataset.rlOrigText = el.textContent;
    el.classList.add('rl-editing');
    el.contentEditable = 'true';
    el.spellcheck = true;
    el.focus();

    const range = document.createRange();
    range.selectNodeContents(el);
    range.collapse(false);
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);

    el.addEventListener('keydown', editableKeydown);
    showToolbar(el);
  }

  function editableKeydown(e) {
    if (e.key === 'Escape') {
      e.preventDefault();
      finishEditing(currentEditing, true);
    } else if (e.key === 'Enter' && !e.shiftKey) {
      const tag = (currentEditing && currentEditing.tagName || '').toLowerCase();
      if (['h1','h2','h3','h4','h5','h6','span','button','a','li','strong','em'].indexOf(tag) >= 0) {
        e.preventDefault();
        finishEditing(currentEditing, false);
      }
    }
  }

  function showToolbar(el) {
    const existing = document.querySelector('.rl-click-toolbar');
    if (existing) existing.remove();
    const tb = document.createElement('div');
    tb.className = 'rl-click-toolbar';
    tb.innerHTML =
      '<button class="rl-tb-cancel" type="button" title="Cancel (Esc)">Cancel</button>' +
      '<button class="rl-tb-save" type="button" title="Save (Enter)">Save</button>';
    document.body.appendChild(tb);

    const rect = el.getBoundingClientRect();
    const tbRect = tb.getBoundingClientRect();
    let top = rect.top + window.scrollY - tbRect.height - 10;
    if (top < window.scrollY + 70) top = rect.bottom + window.scrollY + 10;
    let left = rect.left + window.scrollX;
    const maxLeft = window.scrollX + window.innerWidth - tbRect.width - 12;
    if (left > maxLeft) left = maxLeft;
    if (left < window.scrollX + 12) left = window.scrollX + 12;
    tb.style.top = top + 'px';
    tb.style.left = left + 'px';

    tb.querySelector('.rl-tb-cancel').addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      finishEditing(el, true);
    });
    tb.querySelector('.rl-tb-save').addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      finishEditing(el, false);
    });
  }

  function finishEditing(el, cancelled) {
    if (!el) return;
    el.contentEditable = 'false';
    el.classList.remove('rl-editing');
    el.removeEventListener('keydown', editableKeydown);
    const tb = document.querySelector('.rl-click-toolbar');
    if (tb) tb.remove();

    const origText = el.dataset.rlOrigText || '';
    const newText = el.textContent.trim();
    delete el.dataset.rlOrigText;
    const targetId = el.id;
    currentEditing = null;

    if (cancelled || newText === origText.trim() || !targetId) {
      if (cancelled) el.textContent = origText;
      return;
    }

    el.textContent = origText;
    panelEl.classList.add('rl-open');

    const ops = [{ op: 'replace_text', id: targetId, text: newText }];
    const previousById = {};
    previousById[targetId] = origText;
    const summary = 'Edited: "' + origText.trim().slice(0, 30) + '..." to "' + newText.slice(0, 30) + '..."';
    addMessage(summary, 'user');
    saveOps(ops, previousById, 'Inline edit saved.');
  }

  function boot() {
    injectStyles();
    buildDom();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
