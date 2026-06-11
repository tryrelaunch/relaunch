// ── Mobile hamburger nav ──
function toggleNav() {
  var links = document.getElementById('nav-links');
  var btn = document.getElementById('nav-toggle');
  if (!links) return;
  links.classList.toggle('open');
  if (btn) btn.classList.toggle('open');
}
// Close the mobile menu after tapping a link
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('#nav-links a');
  if (a) {
    var links = document.getElementById('nav-links');
    var btn = document.getElementById('nav-toggle');
    if (links) links.classList.remove('open');
    if (btn) btn.classList.remove('open');
  }
});

// ── SEO panel ──
function toggleSEO() {
  const p = document.getElementById('seo-panel');
  if (p.classList.contains('open')) closeSEO();
  else openSEO();
}
function openSEO() {
  const p = document.getElementById('seo-panel');
  const b = document.getElementById('seo-btn');
  p.classList.add('open');
  b.textContent = 'Close ▲';
  setTimeout(() => {
    const banner = document.querySelector('.seo-banner');
    if (banner) banner.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 50);
}
function closeSEO() {
  const p = document.getElementById('seo-panel');
  const b = document.getElementById('seo-btn');
  p.classList.remove('open');
  b.textContent = 'What changed ▼';
  setTimeout(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, 50);
}

// ── Sticky claim bar ──
const bar = document.getElementById('sticky-bar');
let barClosed = false;
window.addEventListener('scroll', () => {
  if (barClosed || !bar) return;
  bar.classList.toggle('show', window.scrollY > 600);
});
function closeBar() { barClosed = true; if (bar) bar.classList.remove('show'); }

// ── Booking modal (FareHarbor iframe) ──
const FH_FERRY  = 'https://fareharbor.com/embeds/book/monheganboat/items/?selected-items=60827,60831&sheet=89753&full-items=yes';
const FH_PUFFIN = 'https://fareharbor.com/embeds/book/monheganboat/items/?selected-items=60827,60831&sheet=89759&full-items=yes';
const FH_GIFT   = 'https://fareharbor.com/embeds/book/monheganboat/items/';
let bookModalLoadTimer = null;
function openBookModal(which) {
  const url = which === 'puffin' ? FH_PUFFIN : which === 'gift' ? FH_GIFT : FH_FERRY;
  const modal = document.getElementById('book-modal');
  const iframe = document.getElementById('book-modal-iframe');
  const fallback = document.getElementById('book-modal-fallback');
  if (fallback) { fallback.querySelector('a').href = url; fallback.style.display = 'none'; }
  iframe.style.display = 'block';
  iframe.src = url;
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
  clearTimeout(bookModalLoadTimer);
}
function closeBookModal() {
  const modal = document.getElementById('book-modal');
  const iframe = document.getElementById('book-modal-iframe');
  modal.classList.remove('open');
  iframe.src = 'about:blank';
  document.body.style.overflow = '';
  clearTimeout(bookModalLoadTimer);
}
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const m = document.getElementById('book-modal');
    if (m && m.classList.contains('open')) closeBookModal();
  }
});
document.addEventListener('click', (e) => {
  if (e.target && e.target.id === 'book-modal') closeBookModal();
});

// ── Edit widget ──
let isLoading = false;
function toggleEditPanel() {
  const panel = document.getElementById('edit-panel');
  panel.classList.toggle('open');
  if (panel.classList.contains('open')) {
    setTimeout(() => document.getElementById('edit-input').focus(), 100);
  }
}
function useChip(el) {
  const input = document.getElementById('edit-input');
  input.value = el.textContent;
  input.focus();
  autoResize(input);
}
function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 100) + 'px';
}
function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendEdit();
  }
}
function addMessage(text, type) {
  const messages = document.getElementById('edit-messages');
  const msg = document.createElement('div');
  msg.className = `edit-msg ${type}`;
  msg.textContent = text;
  messages.appendChild(msg);
  messages.scrollTop = messages.scrollHeight;
  return msg;
}
async function sendEdit() {
  if (isLoading) return;
  const input = document.getElementById('edit-input');
  const request = input.value.trim();
  if (!request) return;

  input.value = '';
  autoResize(input);
  document.getElementById('edit-suggestions').style.display = 'none';
  addMessage(request, 'user');

  isLoading = true;
  document.getElementById('edit-send').disabled = true;
  document.getElementById('edit-typing').classList.add('show');

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

    document.getElementById('edit-typing').classList.remove('show');

    if (!response.ok) {
      addMessage('Something went wrong. Try again.', 'error');
      isLoading = false;
      document.getElementById('edit-send').disabled = false;
      return;
    }

    const data = await response.json();
    const ops = Array.isArray(data.ops) ? data.ops
              : Array.isArray(data.changes) ? data.changes.map(c => ({ op: 'replace_text', id: c.id, text: c.text }))
              : [];

    if (ops.length > 0) {
      ops.forEach(op => {
        const el = document.getElementById(op.id);
        if (!el) return;
        if (op.op === 'replace_text' && typeof op.text === 'string') {
          el.textContent = op.text;
        } else if (op.op === 'set_style' && typeof op.style === 'string') {
          el.style.cssText = (el.style.cssText ? el.style.cssText + ';' : '') + op.style;
        } else if (op.op === 'set_attr' && op.attr && typeof op.value === 'string') {
          if (['src','href','alt','title','aria-label','placeholder'].includes(op.attr)) {
            el.setAttribute(op.attr, op.value);
          }
        }
      });
      addMessage(data.confirmation || 'Done! Change applied.', 'system');
    } else {
      addMessage("I couldn't figure out what to change. Try being more specific.", 'claude');
    }
  } catch (err) {
    document.getElementById('edit-typing').classList.remove('show');
    addMessage("Couldn't connect. Check your internet and try again.", 'error');
  }

  isLoading = false;
  document.getElementById('edit-send').disabled = false;
}
