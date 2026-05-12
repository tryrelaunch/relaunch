/* ──────────────────────────────────────────────────────────
   ANGRY PETE'S — Relaunch demo widget logic
   - SEO banner expand/collapse
   - Sticky "Make this my real site" bar (shows after scroll)
   - AI edit widget — sends prompt + editable content to
     /.netlify/functions/edit, replaces text in place
   - Mobile hamburger toggle
   ────────────────────────────────────────────────────────── */

// ── SEO BANNER ──────────────────────────────────────────
function toggleSEO() {
  const panel = document.getElementById('seo-panel');
  const btn = document.getElementById('seo-btn');
  if (!panel) return;
  panel.classList.toggle('open');
  if (btn) {
    btn.textContent = panel.classList.contains('open') ? 'Hide ▲' : 'Read this first ▼';
  }
}

// ── STICKY BAR ──────────────────────────────────────────
let barDismissed = false;
function showBar() {
  if (barDismissed) return;
  const bar = document.getElementById('sticky-bar');
  if (bar) bar.classList.add('show');
}
function closeBar() {
  barDismissed = true;
  const bar = document.getElementById('sticky-bar');
  if (bar) bar.classList.remove('show');
}
window.addEventListener('scroll', () => {
  if (window.scrollY > 600) showBar();
}, { passive: true });

// ── HAMBURGER ───────────────────────────────────────────
function toggleNav() {
  const links = document.getElementById('nav-links');
  if (links) links.classList.toggle('open');
}

// ── EDIT WIDGET ─────────────────────────────────────────
let isLoading = false;

function toggleEditPanel() {
  const p = document.getElementById('edit-panel');
  const f = document.getElementById('edit-fab');
  if (!p) return;
  const open = p.classList.toggle('open');
  if (f) f.style.display = open ? 'none' : 'flex';
  if (open) setTimeout(() => document.getElementById('edit-input')?.focus(), 100);
}

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

function addMessage(text, type) {
  const messages = document.getElementById('edit-messages');
  if (!messages) return;
  const msg = document.createElement('div');
  msg.className = `edit-msg ${type}`;
  msg.textContent = text;
  messages.appendChild(msg);
  messages.scrollTop = messages.scrollHeight;
  return msg;
}

function fillSuggestion(text) {
  const input = document.getElementById('edit-input');
  if (!input) return;
  input.value = text;
  autoResize(input);
  input.focus();
}

async function sendEdit() {
  if (isLoading) return;
  const input = document.getElementById('edit-input');
  const request = input?.value.trim();
  if (!request) return;

  input.value = '';
  autoResize(input);
  const sugg = document.getElementById('edit-suggestions');
  if (sugg) sugg.style.display = 'none';
  addMessage(request, 'user');

  isLoading = true;
  const sendBtn = document.getElementById('edit-send');
  if (sendBtn) sendBtn.disabled = true;
  document.getElementById('edit-typing')?.classList.add('show');

  // Build content map — every editable element by ID
  const content = {};
  document.querySelectorAll('[id^="edit-"]').forEach(el => {
    content[el.id] = el.textContent.trim();
  });

  try {
    const response = await fetch('/.netlify/functions/edit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ request, content })
    });

    document.getElementById('edit-typing')?.classList.remove('show');

    if (!response.ok) {
      addMessage('Something went wrong. Try again.', 'error');
      isLoading = false;
      if (sendBtn) sendBtn.disabled = false;
      return;
    }

    const data = await response.json();

    if (data.changes && data.changes.length > 0) {
      data.changes.forEach(change => {
        const el = document.getElementById(change.id);
        if (el) el.textContent = change.text;
      });
      addMessage(data.confirmation || 'Done! Change applied.', 'system');
    } else {
      addMessage("I couldn't find what to change. Try being more specific.", 'claude');
    }
  } catch (err) {
    document.getElementById('edit-typing')?.classList.remove('show');
    addMessage("Couldn't connect. Check your internet and try again.", 'error');
  }

  isLoading = false;
  if (sendBtn) sendBtn.disabled = false;
}

// keyboard shortcut: Cmd/Ctrl+Enter sends
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('edit-input');
  if (input) {
    input.addEventListener('input', () => autoResize(input));
    input.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        e.preventDefault();
        sendEdit();
      }
    });
  }
});
