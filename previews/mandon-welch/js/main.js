// MW Physical Therapy preview — UI behavior
// SEO banner toggle + mobile menu

(function () {
  'use strict';

  // SEO banner toggle (top of page)
  const seoBtn = document.getElementById('seo-btn');
  const seoPanel = document.getElementById('seo-panel');
  const seoTop = document.querySelector('.seo-top');
  function toggleSEO() {
    if (!seoPanel) return;
    const open = seoPanel.classList.toggle('open');
    if (seoBtn) seoBtn.textContent = open ? 'Hide ▲' : 'Read this first ▼';
  }
  window.toggleSEO = toggleSEO;
  if (seoBtn) seoBtn.addEventListener('click', (e) => { e.stopPropagation(); toggleSEO(); });
  if (seoTop) seoTop.addEventListener('click', toggleSEO);

  // Mobile menu
  const hamburger = document.querySelector('.hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      mobileMenu.classList.toggle('open');
    });
    // Close on link click
    mobileMenu.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => mobileMenu.classList.remove('open'));
    });
  }
})();
