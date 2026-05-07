/* ============================================================
   Relaunch Live Editor Widget — Preview Demo
   Self-contained: injects own styles + DOM
   Drop into any page with: <script src="js/relaunch-editor.js"></script>
   ============================================================ */

(function() {
  'use strict';

  // --- Inject styles ---
  const style = document.createElement('style');
  style.textContent = `
    .rl-fab {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: linear-gradient(135deg, #0e7187 0%, #094a55 100%);
      color: #fff;
      border: none;
      cursor: pointer;
      box-shadow: 0 8px 24px rgba(14, 113, 135, 0.35), 0 2px 6px rgba(0,0,0,0.12);
      z-index: 9998;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.2s, box-shadow 0.2s;
      font-family: 'Inter', -apple-system, system-ui, sans-serif;
    }
    .rl-fab:hover {
      transform: translateY(-2px) scale(1.04);
      box-shadow: 0 12px 32px rgba(14, 113, 135, 0.5), 0 4px 8px rgba(0,0,0,0.15);
    }
    .rl-fab svg {
      width: 26px;
      height: 26px;
    }
    .rl-fab.hidden { display: none; }

    .rl-fab-pulse {
      position: absolute;
      inset: 0;
      border-radius: 50%;
      background: rgba(14, 113, 135, 0.4);
      animation: rlPulse 2.4s ease-out infinite;
    }
    @keyframes rlPulse {
      0% { transform: scale(1); opacity: 0.6; }
      100% { transform: scale(1.6); opacity: 0; }
    }

    .rl-tooltip {
      position: fixed;
      bottom: 38px;
      right: 96px;
      background: #0f1d2e;
      color: #fff;
      padding: 10px 16px;
      border-radius: 8px;
      font-family: 'Inter', system-ui, sans-serif;
      font-size: 13px;
      font-weight: 500;
      white-space: nowrap;
      box-shadow: 0 6px 20px rgba(0,0,0,0.18);
      z-index: 9997;
      opacity: 0;
      transform: translateY(4px);
      transition: opacity 0.25s, transform 0.25s;
      pointer-events: none;
    }
    .rl-tooltip.show { opacity: 1; transform: translateY(0); }
    .rl-tooltip::after {
      content: '';
      position: absolute;
      right: -6px;
      top: 50%;
      transform: translateY(-50%);
      border: 6px solid transparent;
      border-left-color: #0f1d2e;
    }

    .rl-panel {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 384px;
      max-width: calc(100vw - 32px);
      height: 560px;
      max-height: calc(100vh - 48px);
      background: #fff;
      border-radius: 16px;
      box-shadow: 0 20px 50px rgba(15, 29, 46, 0.25), 0 4px 12px rgba(0,0,0,0.08);
      z-index: 9999;
      display: none;
      flex-direction: column;
      overflow: hidden;
      font-family: 'Inter', -apple-system, system-ui, sans-serif;
      animation: rlSlideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .rl-panel.open { display: flex; }
    @keyframes rlSlideIn {
      from { opacity: 0; transform: translateY(12px) scale(0.98); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    .rl-header {
      background: linear-gradient(135deg, #0e7187 0%, #094a55 100%);
      color: #fff;
      padding: 18px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .rl-header-title {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 700;
      font-size: 15px;
      letter-spacing: -0.01em;
    }
    .rl-header-title svg { width: 20px; height: 20px; }
    .rl-header-sub {
      font-size: 11px;
      font-weight: 500;
      opacity: 0.75;
      margin-top: 2px;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }
    .rl-close {
      background: none;
      border: none;
      color: #fff;
      cursor: pointer;
      padding: 6px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.15s;
    }
    .rl-close:hover { background: rgba(255,255,255,0.15); }
    .rl-close svg { width: 18px; height: 18px; }

    .rl-body {
      flex: 1;
      overflow-y: auto;
      padding: 18px 20px;
      background: #f8fafc;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .rl-msg {
      display: flex;
      gap: 10px;
      max-width: 88%;
      animation: rlMsgIn 0.25s ease-out;
    }
    @keyframes rlMsgIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .rl-msg.bot { align-self: flex-start; }
    .rl-msg.user { align-self: flex-end; flex-direction: row-reverse; }

    .rl-avatar {
      width: 28px;
      height: 28px;
      border-radius: 50%;
      flex-shrink: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: -0.02em;
    }
    .rl-msg.bot .rl-avatar {
      background: linear-gradient(135deg, #0e7187 0%, #094a55 100%);
      color: #fff;
    }
    .rl-msg.user .rl-avatar {
      background: #0f1d2e;
      color: #fff;
    }

    .rl-bubble {
      padding: 10px 14px;
      border-radius: 14px;
      font-size: 14px;
      line-height: 1.5;
      color: #0f1d2e;
    }
    .rl-msg.bot .rl-bubble {
      background: #fff;
      border: 1px solid rgba(15,29,46,0.08);
      border-top-left-radius: 4px;
    }
    .rl-msg.user .rl-bubble {
      background: #0e7187;
      color: #fff;
      border-top-right-radius: 4px;
    }
    .rl-bubble strong { font-weight: 700; }
    .rl-bubble code {
      background: rgba(15,29,46,0.06);
      padding: 1px 6px;
      border-radius: 4px;
      font-size: 13px;
      font-family: ui-monospace, 'SF Mono', monospace;
    }
    .rl-msg.user .rl-bubble code { background: rgba(255,255,255,0.18); color: #fff; }

    .rl-typing { display: flex; gap: 4px; padding: 10px 14px; }
    .rl-typing span {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #0e7187;
      animation: rlBounce 1.2s infinite ease-in-out;
    }
    .rl-typing span:nth-child(2) { animation-delay: 0.15s; }
    .rl-typing span:nth-child(3) { animation-delay: 0.3s; }
    @keyframes rlBounce {
      0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
      30% { transform: translateY(-5px); opacity: 1; }
    }

    .rl-suggestions {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-top: 4px;
    }
    .rl-suggest {
      background: #fff;
      border: 1px solid rgba(14, 113, 135, 0.25);
      color: #0e7187;
      padding: 9px 12px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      text-align: left;
      transition: all 0.15s;
      font-family: inherit;
    }
    .rl-suggest:hover {
      background: #0e7187;
      color: #fff;
      border-color: #0e7187;
    }

    .rl-input-area {
      flex-shrink: 0;
      padding: 14px 16px 12px;
      background: #fff;
      border-top: 1px solid rgba(15,29,46,0.08);
    }
    .rl-input-row {
      display: flex;
      gap: 8px;
      align-items: flex-end;
    }
    .rl-input {
      flex: 1;
      border: 1px solid rgba(15,29,46,0.15);
      border-radius: 10px;
      padding: 10px 12px;
      font-family: inherit;
      font-size: 14px;
      color: #0f1d2e;
      resize: none;
      max-height: 100px;
      transition: border-color 0.15s;
      background: #f8fafc;
    }
    .rl-input:focus {
      outline: none;
      border-color: #0e7187;
      background: #fff;
    }
    .rl-send {
      background: #0e7187;
      color: #fff;
      border: none;
      border-radius: 10px;
      padding: 10px 14px;
      cursor: pointer;
      font-family: inherit;
      font-weight: 600;
      font-size: 14px;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: background 0.15s;
    }
    .rl-send:hover { background: #094a55; }
    .rl-send:disabled { opacity: 0.4; cursor: not-allowed; }
    .rl-send svg { width: 16px; height: 16px; }

    .rl-footer {
      text-align: center;
      padding: 6px 0 0;
      font-size: 11px;
      color: #5a6b7e;
    }
    .rl-footer a {
      color: #0e7187;
      font-weight: 600;
      text-decoration: none;
    }
    .rl-footer a:hover { text-decoration: underline; }

    @media (max-width: 480px) {
      .rl-panel {
        width: calc(100vw - 16px);
        height: calc(100vh - 90px);
        bottom: 80px;
        right: 8px;
      }
      .rl-fab { bottom: 16px; right: 16px; }
      .rl-tooltip { display: none; }
    }
  `;
  document.head.appendChild(style);

  // --- Build DOM ---
  const fab = document.createElement('button');
  fab.className = 'rl-fab';
  fab.setAttribute('aria-label', 'Open Relaunch live editor');
  fab.innerHTML = `
    <span class="rl-fab-pulse"></span>
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 3l1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5z"/>
      <path d="M19 14l.7 2.3L22 17l-2.3.7L19 20l-.7-2.3L16 17l2.3-.7z"/>
      <path d="M5 4l.5 1.5L7 6l-1.5.5L5 8l-.5-1.5L3 6l1.5-.5z"/>
    </svg>
  `;

  const tooltip = document.createElement('div');
  tooltip.className = 'rl-tooltip';
  tooltip.textContent = '✨ Edit your site by typing';

  const panel = document.createElement('div');
  panel.className = 'rl-panel';
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-label', 'Relaunch live editor');
  panel.innerHTML = `
    <div class="rl-header">
      <div>
        <div class="rl-header-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 3l1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5z"/>
            <path d="M19 14l.7 2.3L22 17l-2.3.7L19 20l-.7-2.3L16 17l2.3-.7z"/>
          </svg>
          Relaunch Live Editor
        </div>
        <div class="rl-header-sub">Powered by AI · No code needed</div>
      </div>
      <button class="rl-close" aria-label="Close editor">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6L6 18M6 6l12 12"/></svg>
      </button>
    </div>
    <div class="rl-body" id="rl-body"></div>
    <div class="rl-input-area">
      <div class="rl-input-row">
        <textarea class="rl-input" id="rl-input" placeholder="Type a change you'd like to see…" rows="1"></textarea>
        <button class="rl-send" id="rl-send" aria-label="Send">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/></svg>
        </button>
      </div>
      <div class="rl-footer">Powered by <a href="https://tryrelaunch.com" target="_blank" rel="noopener">Relaunch</a></div>
    </div>
  `;

  document.body.appendChild(fab);
  document.body.appendChild(tooltip);
  document.body.appendChild(panel);

  // --- State ---
  const body = panel.querySelector('#rl-body');
  const input = panel.querySelector('#rl-input');
  const sendBtn = panel.querySelector('#rl-send');
  const closeBtn = panel.querySelector('.rl-close');
  let opened = false;
  let initialized = false;

  // --- Helpers ---
  function addBotMessage(html, opts = {}) {
    const msg = document.createElement('div');
    msg.className = 'rl-msg bot';
    msg.innerHTML = `
      <div class="rl-avatar">R</div>
      <div class="rl-bubble">${html}</div>
    `;
    body.appendChild(msg);
    if (!opts.skipScroll) body.scrollTop = body.scrollHeight;
    return msg;
  }

  function addUserMessage(text) {
    const msg = document.createElement('div');
    msg.className = 'rl-msg user';
    msg.innerHTML = `
      <div class="rl-avatar">J</div>
      <div class="rl-bubble">${escapeHtml(text)}</div>
    `;
    body.appendChild(msg);
    body.scrollTop = body.scrollHeight;
  }

  function addTyping() {
    const msg = document.createElement('div');
    msg.className = 'rl-msg bot';
    msg.id = 'rl-typing-msg';
    msg.innerHTML = `
      <div class="rl-avatar">R</div>
      <div class="rl-bubble" style="padding: 4px 10px;">
        <div class="rl-typing"><span></span><span></span><span></span></div>
      </div>
    `;
    body.appendChild(msg);
    body.scrollTop = body.scrollHeight;
  }

  function removeTyping() {
    const t = document.getElementById('rl-typing-msg');
    if (t) t.remove();
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function addSuggestions(items) {
    const wrap = document.createElement('div');
    wrap.className = 'rl-suggestions';
    items.forEach(text => {
      const btn = document.createElement('button');
      btn.className = 'rl-suggest';
      btn.textContent = text;
      btn.addEventListener('click', () => {
        wrap.remove();
        handleUserInput(text);
      });
      wrap.appendChild(btn);
    });
    body.appendChild(wrap);
    body.scrollTop = body.scrollHeight;
  }

  // --- Mock responses ---
  // Picks a context-aware response based on what the user typed
  function getMockResponse(text) {
    const t = text.toLowerCase();

    if (/color|theme|palette|teal|blue|red|green|coral/.test(t)) {
      return `Got it — I'd update the site's color theme to match. <br><br>On your <strong>live</strong> site, this would deploy in ~30 seconds. In this preview I'll just confirm I understood the change.<br><br>Want to try another?`;
    }
    if (/photo|image|picture|hero/.test(t)) {
      return `Done — I'd swap the photo for one you upload. You can drag-and-drop images directly into a real Relaunch editor.<br><br>This preview doesn't push the change live, but on your real site it would happen instantly. What else?`;
    }
    if (/phone|number|contact|address/.test(t)) {
      return `Understood — I'd update the contact info everywhere it appears (header, footer, contact page, schema markup).<br><br>On a live Relaunch site, one edit propagates to every place that data shows up. No copy-paste, no missed spots.`;
    }
    if (/hour|open|close|schedule/.test(t)) {
      return `Got it — I'd update the business hours on the homepage, contact page, and the LocalBusiness schema (which is what Google reads for the "Open now" indicator in search results).<br><br>One change, everywhere it shows up.`;
    }
    if (/price|pricing|cost|rate|estimate/.test(t)) {
      return `Easy — I'd update pricing wherever it appears. Live edits show up everywhere within seconds.<br><br>Try me with another change?`;
    }
    if (/banner|holiday|promo|sale|discount/.test(t)) {
      return `Adding a holiday/promo banner is one of the most-used Relaunch features. I'd drop one across the top of every page with the message and dates you want.<br><br>You can schedule it to auto-disappear after a date too.`;
    }
    if (/text|copy|word|change/.test(t)) {
      return `Got it — I'd find that text and update it. The whole point of Relaunch is editing your site without learning HTML or waiting on a developer.<br><br>What else would you change?`;
    }
    if (/seo|google|search|rank/.test(t)) {
      return `SEO updates are baked in. I can update meta titles, descriptions, schema markup, and alt text — all the stuff that affects rankings — without you ever seeing the code.<br><br>This preview already has Local Business schema, FAQ schema, and Service schema on every page.`;
    }

    // Generic catch-all
    const responses = [
      `Got it — I'd make that change for you. On your <strong>live</strong> Relaunch site, edits like this deploy in ~30 seconds.<br><br>This preview just shows you what the editor experience feels like. Want to try another?`,
      `Understood. That's the kind of change Relaunch handles in seconds — no code, no waiting on a designer.<br><br>What else would you want to update?`,
      `Easy. On a real Relaunch site, that's a 10-second edit. Try me with another change.`
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  }

  function handleUserInput(text) {
    if (!text.trim()) return;
    addUserMessage(text);
    addTyping();
    setTimeout(() => {
      removeTyping();
      addBotMessage(getMockResponse(text));
    }, 700 + Math.random() * 500);
  }

  // --- Initialization (first open) ---
  function initConversation() {
    if (initialized) return;
    initialized = true;

    addBotMessage(`Hey 👋 I'm the <strong>Relaunch</strong> live editor.<br><br>On a real Relaunch site, you'd type any change you want and watch your site update in seconds — no code, no waiting on a designer.`);

    setTimeout(() => {
      addBotMessage(`Try one of these to see how it works:`, { skipScroll: true });
      addSuggestions([
        '"Change the hero photo to one I just uploaded"',
        '"Add a holiday discount banner"',
        '"Update the phone number across all pages"',
        '"Change the residential carpet pricing"'
      ]);
    }, 800);
  }

  // --- Event listeners ---
  fab.addEventListener('click', () => {
    opened = !opened;
    if (opened) {
      panel.classList.add('open');
      fab.classList.add('hidden');
      tooltip.classList.remove('show');
      initConversation();
      setTimeout(() => input.focus(), 350);
    } else {
      panel.classList.remove('open');
      fab.classList.remove('hidden');
    }
  });

  closeBtn.addEventListener('click', () => {
    opened = false;
    panel.classList.remove('open');
    fab.classList.remove('hidden');
  });

  sendBtn.addEventListener('click', () => {
    const txt = input.value.trim();
    if (!txt) return;
    input.value = '';
    handleUserInput(txt);
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendBtn.click();
    }
  });

  // Auto-resize textarea
  input.addEventListener('input', () => {
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 100) + 'px';
  });

  // Show tooltip after 3s on first visit (sessionStorage avoids re-pestering)
  if (!sessionStorage.getItem('rl-tooltip-shown')) {
    setTimeout(() => {
      if (!opened) {
        tooltip.classList.add('show');
        sessionStorage.setItem('rl-tooltip-shown', '1');
        setTimeout(() => tooltip.classList.remove('show'), 5000);
      }
    }, 3000);
  }

})();
