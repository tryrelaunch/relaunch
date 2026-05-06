/* widget.js — Relaunch production edit widget.
 * Lives at https://tryrelaunch.com/widget.js
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
 */
(function () {
  'use strict';

  if (window.__relaunchWidgetMounted) return;

  const cfg = window.__relaunchWidgetConfig;
  if (!cfg || !cfg.slug || !cfg.token || !cfg.endpoint) {
    console.warn('[Relaunch] Widget config missing — not mounting.');
    return;
  }
  window.__relaunchWidgetMounted = true;

  const SLUG = cfg.slug;
  const TOKEN = cfg.token;
  const ENDPOINT = cfg.endpoint;
  const EDIT_PAGE = cfg.editPageUrl || '/edit/';
  const SUPPORT_EMAIL = cfg.supportEmail || 'support@tryrelaunch.com';

  // ── Styles (scoped with rl- prefix to avoid collisions) ──
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
      display: flex; justify-content: space-between; align-items: center; }
    .rl-panel-title { font-weight: 800; letter-spacing: 0.02em;
      display: flex; align-items: center; gap: 8px; font-size: 14px; }
    .rl-panel-title-dot { width: 7px; height: 7px; background: #4baf0f; border-radius: 50%; }
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

    .rl-typing { padding: 8px 16px; display: none; gap: 4px; }
    .rl-typing.rl-show { display: flex; }
    .rl-typing span { width: 6px; height: 6px; background: #6ec934; border-radius: 50%;
      animation: rl-bounce 1.4s ease-in-out infinite; }
    .rl-typing span:nth-child(2) { animation-delay: 0.15s; }
    .rl-typing span:nth-child(3) { animation-delay: 0.3s; }
    @keyframes rl-bounce { 0%,80%,100%{opacity:0.3;transform:translateY(0)} 40%{opacity:1;transform:translateY(-4px)} }

    .rl-actions { padding: 0 14px 10px;
      display: flex; gap: 6px; flex-wrap: wrap; }
    .rl-action-btn { background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.1); color: rgba(255,255,255,0.75);
      border-radius: 16px; padding: 6px 12px; font-size: 12px; cursor: pointer;
      font-family: inherit; transition: all 0.2s; }
    .rl-action-btn:hover { background: rgba(75,175,15,0.18); color: #6ec934;
      border-color: #4baf0f; }

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

    @media (max-width: 480px) {
      .rl-panel { right: 12px; left: 12px; width: auto; }
      .rl-fab { bottom: 16px; right: 16px; }
    }
  `;

  // ── DOM build ──
  function injectStyles() {
    const style = document.createElement('style');
    style.id = 'rl-widget-styles';
    style.textContent = css;
    document.head.appendChild(style);
  }

  let panelEl, messagesEl, typingEl, inputEl, sendBtn, fabEl;
  let isLoading = false;

  function buildDom() {
    fabEl = document.createElement('button');
    fabEl.className = 'rl-fab';
    fabEl.type = 'button';
    fabEl.innerHTML = '<span class="rl-fab-dot"></span> Edit your site';
    fabEl.addEventListener('click', togglePanel);
    document.body.appendChild(fabEl);

    panelEl = document.createElement('div');
    panelEl.className = 'rl-panel';
    panelEl.innerHTML = `
      <div class="rl-panel-header">
        <div class="rl-panel-title">
          <span class="rl-panel-title-dot"></span>
          Edit your site
        </div>
        <button class="rl-panel-close" type="button" aria-label="Close">×</button>
      </div>
      <div class="rl-messages"></div>
      <div class="rl-typing"><span></span><span></span><span></span></div>
      <div class="rl-actions">
        <button class="rl-action-btn rl-help-btn" type="button">Request human help</button>
      </div>
      <div class="rl-input-row">
        <textarea class="rl-input" rows="1" placeholder="What would you like to change?"></textarea>
        <button class="rl-send" type="button" aria-label="Send">→</button>
      </div>
    `;
    document.body.appendChild(panelEl);

    messagesEl = panelEl.querySelector('.rl-messages');
    typingEl = panelEl.querySelector('.rl-typing');
    inputEl = panelEl.querySelector('.rl-input');
    sendBtn = panelEl.querySelector('.rl-send');

    panelEl.querySelector('.rl-panel-close').addEventListener('click', togglePanel);
    panelEl.querySelector('.rl-help-btn').addEventListener('click', requestHumanHelp);
    sendBtn.addEventListener('click', sendEdit);
    inputEl.addEventListener('input', autoResize);
    inputEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendEdit(); }
    });

    addMessage("Hi! Tell me what you'd like to change — hours, prices, descriptions, contact info, anything text on the page.", 'assistant');
  }

  // ── Behavior ──
  function togglePanel() {
    panelEl.classList.toggle('rl-open');
    if (panelEl.classList.contains('rl-open')) {
      setTimeout(() => inputEl.focus(), 100);
    }
  }

  function autoResize() {
    inputEl.style.height = 'auto';
    inputEl.style.height = Math.min(inputEl.scrollHeight, 100) + 'px';
  }

  function addMessage(text, kind) {
    const div = document.createElement('div');
    div.className = `rl-msg rl-msg-${kind}`;
    div.textContent = text;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function setLoading(loading) {
    isLoading = loading;
    sendBtn.disabled = loading;
    typingEl.classList.toggle('rl-show', loading);
    if (loading) messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function applyOptimistic(changes) {
    for (const change of changes) {
      const el = document.getElementById(change.id);
      if (el && el.children.length === 0) {
        el.textContent = change.text;
      }
    }
  }

  function requestHumanHelp() {
    const lastReq = inputEl.value || '(describe what you need here)';
    const subject = encodeURIComponent(`[${SLUG}] Edit help needed`);
    const body = encodeURIComponent(
      `Site: ${SLUG}\nPage: ${window.location.href}\n\nWhat I need:\n${lastReq}\n\n--\nSent from the edit widget.`
    );
    window.location.href = `mailto:${SUPPORT_EMAIL}?subject=${subject}&body=${body}`;
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
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${TOKEN}`
        },
        body: JSON.stringify({ slug: SLUG, request })
      });

      if (res.status === 401) {
        addMessage('Your edit session expired. Redirecting to log in...', 'error');
        setLoading(false);
        try { localStorage.removeItem('relaunch_jwt'); } catch (e) {}
        setTimeout(() => { window.location.href = EDIT_PAGE; }, 1500);
        return;
      }

      if (res.status === 429) {
        addMessage("You've hit the edit limit for this hour. Take a breather and try again in a bit.", 'error');
        setLoading(false);
        return;
      }

      if (!res.ok) {
        addMessage("Something went wrong on our end. Try again in a moment, or use 'Request human help' if it keeps failing.", 'error');
        setLoading(false);
        return;
      }

      const data = await res.json();
      setLoading(false);

      if (Array.isArray(data.changes) && data.changes.length > 0) {
        applyOptimistic(data.changes);
        addMessage(data.confirmation || `Saved ${data.changes.length} change${data.changes.length === 1 ? '' : 's'}. Your live site updates within a minute or two.`, 'system');
      } else {
        addMessage(data.confirmation || "I couldn't make that change automatically. Try rephrasing, or use 'Request human help'.", 'assistant');
      }
    } catch (err) {
      setLoading(false);
      addMessage("Couldn't reach the edit service. Check your connection and try again.", 'error');
    }
  }

  // ── Boot ──
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
