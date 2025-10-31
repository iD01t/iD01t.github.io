// Single-source header/footer loader — pulls from /index.html
(async function injectLayout(){
  try{
    const res  = await fetch('/index.html', {cache:'no-store'});
    const text = await res.text();
    const doc  = new DOMParser().parseFromString(text, 'text/html');

    // Copy shared stylesheets from index head (once)
    const head = document.querySelector('head');
    doc.querySelectorAll('link[rel="stylesheet"]').forEach(link => {
      const href = link.getAttribute('href');
      if (href && !document.querySelector(`link[rel="stylesheet"][href="${href}"]`)) {
        const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = href; head.appendChild(l);
      }
    });

    // Inject header/footer HTML
    const header = doc.querySelector('header');
    const footer = doc.querySelector('footer');
    if (header) document.getElementById('header-slot').innerHTML = header.outerHTML;
    if (footer) document.getElementById('footer-slot').innerHTML = footer.outerHTML;

    // Re-run any scripts inside injected regions (if your header/footer include JS)
    ['header-slot','footer-slot'].forEach(id => {
      const root = document.getElementById(id);
      if (!root) return;
      root.querySelectorAll('script').forEach(s => {
        const ns = document.createElement('script');
        [...s.attributes].forEach(a => ns.setAttribute(a.name, a.value));
        ns.textContent = s.textContent;
        s.replaceWith(ns);
      });
    });

    // Highlight active nav (from data-active or pathname)
    const active = (document.body.dataset.active || '').toLowerCase();
    document.querySelectorAll('header nav a,#site-header nav a').forEach(a => {
      a.removeAttribute('aria-current');
      const label = a.textContent.trim().toLowerCase();
      if ((active && label === active) || a.pathname === location.pathname) {
        a.setAttribute('aria-current','page');
      }
    });
  }catch(e){
    console.warn('Header/Footer injection failed', e);
  }
})();
