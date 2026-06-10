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


// ── OpenTable reservation lightbox ──
(function () {
  var otLoaded = false;
  function buildReserveModal() {
    if (document.getElementById('reserve-modal')) return;
    var m = document.createElement('div');
    m.id = 'reserve-modal';
    m.className = 'reserve-modal';
    m.innerHTML =
      '<div class="reserve-modal-panel">' +
        '<button class="reserve-modal-close" type="button" aria-label="Close">&times;</button>' +
        '<div class="reserve-modal-title">Reserve a Table</div>' +
        '<div id="reserve-modal-body"></div>' +
      '</div>';
    document.body.appendChild(m);
    m.addEventListener('click', function (e) {
      if (e.target === m || e.target.classList.contains('reserve-modal-close')) window.closeReserve();
    });
  }
  window.openReserve = function (e) {
    if (e && e.preventDefault) e.preventDefault();
    buildReserveModal();
    document.getElementById('reserve-modal').classList.add('open');
    document.body.style.overflow = 'hidden';
    if (!otLoaded) {
      otLoaded = true;
      var s = document.createElement('script');
      s.type = 'text/javascript';
      s.src = '//www.opentable.com/widget/reservation/loader?rid=1340929&type=standard&theme=standard&color=1&dark=false&iframe=true&domain=com&lang=en-US&newtab=false&ot_source=Restaurant%20website&cfe=true';
      document.getElementById('reserve-modal-body').appendChild(s);
    }
  };
  window.closeReserve = function () {
    var m = document.getElementById('reserve-modal');
    if (m) m.classList.remove('open');
    document.body.style.overflow = '';
  };
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') window.closeReserve(); });
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('a[href*="opentable.com/r/"], a[href="#reserve"]').forEach(function (a) {
      a.addEventListener('click', window.openReserve);
    });
  });
})();
