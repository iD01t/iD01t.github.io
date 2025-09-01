(async function(){
  const $$ = (s, r=document)=>r.querySelector(s);
  const $$$ = (s, r=document)=>r.querySelectorAll(s);

  // Header injection (keeps current style but guarantees links exist)
  function header(active){
    const links = [
      ["Store","/store.html"],
      ["eBooks","/ebooks.html"],
      ["Audiobooks","/audiobooks.html"],
      ["Series","/series.html"],
      ["Apps","/apps.html"],
      ["Games","/games.html"],
      ["Music","/music.html"],
      ["Services","/services.html"],
      ["Portfolio","/portfolio.html"],
      ["About","/about.html"],
      ["Contact","/contact.html"]
    ];
    return `
    <div class="header">
      <nav class="nav">
        <a href="/" aria-label="Home"><strong>iD01t Productions</strong></a>
        ${links.map(([t,href])=>`<a href="${href}" ${active===t?'style="text-decoration:underline"':''}>${t}</a>`).join('')}
      </nav>
    </div>`;
  }

  // Render header if not present
  if(!document.querySelector('.header')){
    document.body.insertAdjacentHTML('afterbegin', header(document.body.dataset.active || ""));
  }

  // Card renderer
  async function renderGrid(kind){
    const grid = $$('.grid');
    if(!grid) return;
    try{
      const res = await fetch('/assets/catalog.json', {cache:'no-store'});
      const data = await res.json();
      const items = data[kind] || [];
      grid.innerHTML = items.map(it => `
        <article class="card">
          <img loading="lazy" alt="${it.title}" src="${it.image}">
          <div class="badge">${kind.slice(0,1).toUpperCase()+kind.slice(1,kind.endsWith('s')? -1:undefined)}</div>
          <h3 class="title"><a href="${it.link}">${it.title}</a></h3>
          <div class="meta">${it.author || 'Unknown'} • ${it.lang || 'EN'}</div>
          <a class="btn" href="${it.link}">Open</a>
        </article>`).join('');
    }catch(e){
      console.warn('Could not load catalog:', e);
      grid.innerHTML = '<p>Loading catalog...</p>';
    }
  }

  // If the page asks for a catalog, render it
  const kind = document.body.dataset.catalog;
  if(kind) renderGrid(kind);

  // Simple internal-link check: warn in console if any nav link 404s
  window.addEventListener('load', ()=>{
    [...$$$('.nav a')].forEach(async a=>{
      if(a.getAttribute('href').startsWith('/')){
        try{
          const r = await fetch(a.href, {method:'HEAD'});
          if(!r.ok) console.warn('Broken link:', a.href, r.status);
        }catch(e){ console.warn('Broken link:', a.href, e); }
      }
    });
  });
})();
