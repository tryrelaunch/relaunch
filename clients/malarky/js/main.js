/* Malarky Charters — main.js */

// Mobile nav toggle
const hamburger = document.querySelector('.nav-hamburger');
const mobileMenu = document.querySelector('.mobile-menu');
if (hamburger && mobileMenu) {
  hamburger.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
    const expanded = mobileMenu.classList.contains('open');
    hamburger.setAttribute('aria-expanded', expanded);
  });
}

// Mobile Charter Types accordion
document.querySelectorAll('.mobile-accordion-trigger').forEach(btn => {
  btn.addEventListener('click', () => {
    const acc = btn.closest('.mobile-accordion');
    const isOpen = acc.getAttribute('data-open') === 'true';
    acc.setAttribute('data-open', String(!isOpen));
    btn.setAttribute('aria-expanded', String(!isOpen));
  });
});

// Desktop Charter Types dropdown — click toggle (hover handled by CSS)
document.querySelectorAll('.nav-dropdown-trigger').forEach(btn => {
  btn.addEventListener('click', e => {
    e.stopPropagation();
    const dd = btn.closest('.nav-dropdown');
    const isOpen = dd.getAttribute('data-open') === 'true';
    document.querySelectorAll('.nav-dropdown[data-open="true"]').forEach(d => {
      d.setAttribute('data-open', 'false');
      const t = d.querySelector('.nav-dropdown-trigger');
      if (t) t.setAttribute('aria-expanded', 'false');
    });
    if (!isOpen) {
      dd.setAttribute('data-open', 'true');
      btn.setAttribute('aria-expanded', 'true');
    }
  });
});
document.addEventListener('click', () => {
  document.querySelectorAll('.nav-dropdown[data-open="true"]').forEach(d => {
    d.setAttribute('data-open', 'false');
    const t = d.querySelector('.nav-dropdown-trigger');
    if (t) t.setAttribute('aria-expanded', 'false');
  });
});

// FAQ accordion
document.querySelectorAll('.faq-q').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  });
});
