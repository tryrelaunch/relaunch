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

// Photo gallery slider — native scroll-snap + button/dot controls
document.querySelectorAll('.gallery-slider').forEach(slider => {
  const track = slider.querySelector('.gallery-track');
  const slides = Array.from(slider.querySelectorAll('.gallery-slide'));
  const dots = Array.from(slider.querySelectorAll('.gallery-dot'));
  const prev = slider.querySelector('.gallery-prev');
  const next = slider.querySelector('.gallery-next');
  if (!track || !slides.length) return;

  function step(direction) {
    const slideWidth = slides[0].getBoundingClientRect().width;
    const gap = parseFloat(getComputedStyle(track).gap) || 0;
    track.scrollBy({ left: direction * (slideWidth + gap), behavior: 'smooth' });
  }
  prev && prev.addEventListener('click', () => step(-1));
  next && next.addEventListener('click', () => step(1));

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      const target = slides[i];
      if (!target) return;
      const left = target.offsetLeft - (track.clientWidth - target.offsetWidth) / 2;
      track.scrollTo({ left, behavior: 'smooth' });
    });
  });

  // Update active dot based on which slide is centered in viewport
  let rafId = null;
  function updateActive() {
    const trackRect = track.getBoundingClientRect();
    const trackCenter = trackRect.left + trackRect.width / 2;
    let activeIdx = 0;
    let minDist = Infinity;
    slides.forEach((slide, i) => {
      const r = slide.getBoundingClientRect();
      const dist = Math.abs((r.left + r.width / 2) - trackCenter);
      if (dist < minDist) { minDist = dist; activeIdx = i; }
    });
    dots.forEach((d, i) => d.classList.toggle('active', i === activeIdx));
  }
  track.addEventListener('scroll', () => {
    if (rafId) return;
    rafId = requestAnimationFrame(() => { updateActive(); rafId = null; });
  }, { passive: true });
  window.addEventListener('resize', updateActive);
  updateActive();
});


/* ── BACK TO TOP BUTTON ── */
(function() {
  var btn = document.getElementById('back-to-top');
  if (!btn) return;
  function toggle() {
    if (window.scrollY > 600) btn.classList.add('visible');
    else btn.classList.remove('visible');
  }
  window.addEventListener('scroll', toggle, { passive: true });
  btn.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  toggle();
})();
