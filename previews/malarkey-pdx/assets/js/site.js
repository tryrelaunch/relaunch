/* THE MALARKEY — interactions */
(function () {
  document.documentElement.classList.add('js');
  var nav = document.querySelector('.nav');
  var burger = document.querySelector('.nav__burger');
  var drawer = document.querySelector('.drawer');

  /* mobile drawer */
  if (burger && drawer) {
    burger.addEventListener('click', function () {
      drawer.classList.toggle('open');
      document.body.style.overflow = drawer.classList.contains('open') ? 'hidden' : '';
    });
    drawer.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        drawer.classList.remove('open'); document.body.style.overflow = '';
      });
    });
  }

  /* nav solid + theme recolor based on the section under the header */
  var themed = Array.prototype.slice.call(document.querySelectorAll('[data-theme]'));
  var brandImg = nav.querySelector('.nav__brand img');
  var LOGO_LIGHTBG = 'assets/img/wordmark-red.png';   // red logo on light sections
  var LOGO_DARKBG  = 'assets/img/wordmark-cream.png';  // cream logo on dark sections
  var curLogo = '';
  function lum(rgbStr) {
    var m = (rgbStr || '').match(/(\d+(\.\d+)?)/g);
    if (!m) return 0;
    var r = +m[0], g = +m[1], b = +m[2];
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  }
  function setLogo(src) { if (src !== curLogo) { brandImg.src = src; curLogo = src; } }
  function paintNav() {
    var solid = window.scrollY > 24;
    nav.classList.toggle('solid', solid);
    if (!solid) { // over hero
      nav.style.background = '';
      nav.style.color = '';
      setLogo(LOGO_DARKBG);
      return;
    }
    var current = null;
    for (var i = 0; i < themed.length; i++) {
      var r = themed[i].getBoundingClientRect();
      if (r.top <= 72 && r.bottom > 72) { current = themed[i]; break; }
    }
    if (!current) return;
    var bg = getComputedStyle(current).backgroundColor;
    var light = lum(bg) > 0.62;
    nav.style.background = bg.replace('rgb(', 'rgba(').replace(')', ',0.93)');
    nav.style.color = light ? 'var(--ink)' : 'var(--cream)';
    setLogo(light ? LOGO_LIGHTBG : LOGO_DARKBG);
  }
  window.addEventListener('scroll', paintNav, { passive: true });
  window.addEventListener('resize', paintNav);
  paintNav();

  /* scroll reveal (with graceful fallbacks) */
  var reveals = document.querySelectorAll('.reveal');
  function revealAll() { reveals.forEach(function (el) { el.classList.add('in'); }); }
  if (!('IntersectionObserver' in window) || /[?&]qa\b/.test(location.search)) {
    revealAll();
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
    /* safety net: never leave content hidden */
    setTimeout(revealAll, 2600);
  }

  /* waitlist (no backend — captures and confirms) */
  document.querySelectorAll('.waitlist .form').forEach(function (f) {
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      f.closest('.waitlist').classList.add('done');
    });
  });
})();
