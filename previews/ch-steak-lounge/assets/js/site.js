// CH Steak Lounge — site JS (mobile nav + active-link highlight)
(function(){
  var burger = document.querySelector('.nav-burger');
  var links  = document.querySelector('.nav-links');
  if (burger && links) {
    burger.addEventListener('click', function(){
      links.classList.toggle('open');
      var open = links.classList.contains('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  // Highlight current page in nav
  var path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(function(a){
    var href = a.getAttribute('href');
    if (href === path) a.classList.add('active');
  });
})();
