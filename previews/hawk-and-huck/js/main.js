document.addEventListener('DOMContentLoaded', function () {
  const hamburger = document.querySelector('.hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      mobileMenu.classList.toggle('open');
      document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
    });
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('open');
        mobileMenu.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }
});

// ── SEO banner toggle (Spork pattern) ──
function toggleSEO() {
  const p = document.getElementById('seo-panel');
  const b = document.getElementById('seo-btn');
  if (!p) return;
  p.classList.toggle('open');
  if (b) b.textContent = p.classList.contains('open') ? 'Close ▲' : 'Read this first ▼';
}

// ── Relaunch edit widget (preview mode — temp DOM-only edits via /.netlify/functions/edit) ──
let __relaunchEditLoading = false;

function toggleEditPanel() {
  const panel = document.getElementById('edit-panel');
  if (!panel) return;
  panel.classList.toggle('open');
  if (panel.classList.contains('open')) {
    setTimeout(() => {
      const i = document.getElementById('edit-input');
      if (i) i.focus();
    }, 100);
  }
}

function useChip(el) {
  const input = document.getElementById('edit-input');
  if (!input) return;
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
  if (!messages) return null;
  const msg = document.createElement('div');
  msg.className = `edit-msg ${type}`;
  msg.textContent = text;
  messages.appendChild(msg);
  messages.scrollTop = messages.scrollHeight;
  return msg;
}

async function sendEdit() {
  if (__relaunchEditLoading) return;
  const input = document.getElementById('edit-input');
  if (!input) return;
  const request = input.value.trim();
  if (!request) return;

  input.value = '';
  autoResize(input);
  const sug = document.getElementById('edit-suggestions');
  if (sug) sug.style.display = 'none';
  addMessage(request, 'user');

  __relaunchEditLoading = true;
  const sendBtn = document.getElementById('edit-send');
  if (sendBtn) sendBtn.disabled = true;
  const typing = document.getElementById('edit-typing');
  if (typing) typing.classList.add('show');

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

    if (typing) typing.classList.remove('show');

    if (!response.ok) {
      addMessage('Something went wrong. Try again.', 'error');
      __relaunchEditLoading = false;
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
    if (typing) typing.classList.remove('show');
    addMessage("Couldn't connect. Check your internet and try again.", 'error');
  }

  __relaunchEditLoading = false;
  if (sendBtn) sendBtn.disabled = false;
}
