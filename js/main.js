// Minimal JS for nav toggle and small enhancements
(function(){
  // Nav toggle for mobile
  const navToggle = document.getElementById('nav-toggle');
  const primaryNav = document.getElementById('primary-nav');
  if(navToggle && primaryNav){
    navToggle.addEventListener('click', () => {
      const expanded = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', String(!expanded));
      primaryNav.setAttribute('aria-hidden', String(expanded));
    });
  }

  // Set current year in index footer
  const yearEl = document.getElementById('year');
  if(yearEl) yearEl.textContent = new Date().getFullYear();

  // Smooth scroll for internal links (progressive enhancement)
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if(!a) return;
    e.preventDefault();
    const id = a.getAttribute('href').slice(1);
    const target = document.getElementById(id);
    if(target) target.scrollIntoView({behavior:'smooth', block:'start'});
  });

  // Form submit enhancement: disable button after submit
  const form = document.getElementById('contact-form');
  if(form){
    form.addEventListener('submit', (e) => {
      const btn = form.querySelector('button[type="submit"]');
      if(btn){
        btn.disabled = true;
        btn.textContent = "Sending…";
      }
    });
  }
})();