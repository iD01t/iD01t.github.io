# build_site_pack_v2.py
# Usage:
#   python build_site_pack_v2.py
#   python build_site_pack_v2.py --zip   # crée aussi un zip prêt à uploader
import os, sys, json, textwrap, zipfile, datetime
from pathlib import Path

BASE = Path("id01t_site_pack_v2")
DIRS = [
    "js","css","assets/data","assets/img/placeholders","assets/img/brand",
    "assets/harvested/apps","assets/harvested/ebooks","assets/harvested/games",
    "legal","tools"
]

INDEX_HTML = r"""<!DOCTYPE html>
<html lang="fr" class="scroll-smooth">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>iD01t Productions · Apps, eBooks, Games, Music · Official Site</title>
  <meta name="description" content="iD01t Productions: premium apps, eBooks, games, and music. Built for speed, automation, and ROI. Beta Nini’s Adventures: Kitties Mayhem on September 24, 2025." />
  <link rel="icon" href="/favicon.ico" />
  <link rel="canonical" href="https://id01t.github.io/" />
  <meta name="theme-color" content="#16185c" />
  <meta property="og:title" content="iD01t Productions" />
  <meta property="og:description" content="Apps, eBooks, games, music, and services. Growth-focused. Beta Nini’s Adventures on September 24, 2025." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://id01t.github.io/" />
  <meta property="og:image" content="https://id01t.github.io/assets/img/placeholders/hero-1600x900.webp" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="iD01t Productions" />
  <meta name="twitter:description" content="Apps, eBooks, games, music, services. Built for speed, clarity, and growth." />
  <meta name="twitter:image" content="https://id01t.github.io/assets/img/placeholders/hero-1600x900.webp" />
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"Organization","name":"iD01t Productions","url":"https://id01t.github.io/","logo":"https://id01t.github.io/logo.svg","founder":{"@type":"Person","name":"Guillaume Lessard"},"sameAs":["https://github.com/id01t","https://id01t.itch.io","https://play.google.com/store/books/author?id=Guillaume_Lessard","https://books.apple.com/us/author/guillaume-lessard/id1750250586"]}
  </script>
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"VideoGame","name":"Nini’s Adventures: Kitties Mayhem!","gamePlatform":"PC","applicationCategory":"Game","author":{"@type":"Organization","name":"iD01t Productions"},"datePublished":"2025-09-24","url":"https://id01t.github.io/#nini-beta","inLanguage":"en","description":"Explosive online multiplayer shooter. Public PC beta on September 24, 2025. No single-player. AWS-powered servers."}
  </script>
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"MusicGroup","name":"DJ iD01t","url":"https://id01t.github.io/#music","album":[
    {"@type":"MusicAlbum","name":"Last Transmission","datePublished":"2025-03-10"},
    {"@type":"MusicAlbum","name":"Signal Detected","datePublished":"2025-04-15"},
    {"@type":"MusicAlbum","name":"Sweat and Stardust","datePublished":"2025-05-10"},
    {"@type":"MusicAlbum","name":"Echo Protocol","datePublished":"2025-05-20"},
    {"@type":"MusicAlbum","name":"No Master Needed","datePublished":"2025-07-01"},
    {"@type":"MusicAlbum","name":"Anura Voidwalker DMT Chronicles","datePublished":"2025-08-10"}]}
  </script>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config={theme:{extend:{colors:{brand:{50:"#f5f6ff",100:"#e6e9ff",200:"#c9ccff",300:"#a2a8ff",400:"#7a82ff",500:"#545cff",600:"#3a3fe6",700:"#2c30b4",800:"#202383",900:"#16185c"}}}}};
  </script>
  <link rel="stylesheet" href="/css/custom.css">
  <script>(function(){const s=localStorage.getItem('theme');const d=matchMedia('(prefers-color-scheme: dark)').matches;if(s==='dark'||(!s&&d))document.documentElement.classList.add('dark');})();</script>
</head>
<body class="bg-white text-slate-800 dark:bg-slate-950 dark:text-slate-100">
<header class="sticky top-0 z-50 backdrop-blur supports-backdrop-blur:bg-white/70 bg-white/70 dark:bg-slate-950/60 border-b border-slate-200/60 dark:border-slate-800">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-16">
      <a href="#home" class="flex items-center gap-2" aria-label="Aller à l'accueil">
        <img src="/assets/img/brand/logo.png" alt="Logo iD01t Productions" class="h-8 w-8">
        <span class="font-semibold tracking-tight">iD01t Productions</span>
      </a>
      <nav class="hidden md:flex items-center gap-6" aria-label="Navigation principale">
        <a href="/store.html" class="link-underline">Store</a><a href="/ebooks.html" class="link-underline">eBooks</a>
        <a href="/apps.html" class="link-underline">Apps</a><a href="/games.html" class="link-underline">Games</a>
        <a href="/music.html" class="link-underline">Music</a><a href="/services.html" class="link-underline">Services</a>
        <a href="/portfolio.html" class="link-underline">Portfolio</a><a href="/about.html" class="link-underline">About</a>
        <a href="/contact.html" class="link-underline">Contact</a>
      </nav>
      <div class="flex items-center gap-3">
        <button id="themeToggle" class="rounded-full border border-slate-300 dark:border-slate-700 px-3 py-1 text-sm">Theme</button>
        <a href="#newsletter" class="inline-flex items-center rounded-full bg-brand-600 hover:bg-brand-700 text-white text-sm px-4 py-2">Newsletter</a>
        <button id="mobileMenuBtn" class="md:hidden inline-flex items-center justify-center p-2 rounded-lg border border-slate-300 dark:border-slate-700" aria-label="Ouvrir le menu">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
        </button>
      </div>
    </div>
  </div>
  <div id="mobileMenu" class="md:hidden hidden border-t border-slate-200 dark:border-slate-800" role="dialog" aria-modal="true">
    <div class="px-4 py-3 flex flex-col gap-2">
      <a href="/store.html" class="py-2">Store</a><a href="/ebooks.html" class="py-2">eBooks</a><a href="/apps.html" class="py-2">Apps</a>
      <a href="/games.html" class="py-2">Games</a><a href="/music.html" class="py-2">Music</a><a href="/services.html" class="py-2">Services</a>
      <a href="/portfolio.html" class="py-2">Portfolio</a><a href="/about.html" class="py-2">About</a><a href="/contact.html" class="py-2">Contact</a>
    </div>
  </div>
</header>

<section id="home" class="relative overflow-hidden">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-16 pb-24">
    <div class="grid md:grid-cols-2 items-center gap-10">
      <div>
        <h1 class="text-4xl sm:text-5xl font-bold tracking-tight">Premium apps, eBooks, games, music</h1>
        <p class="mt-4 text-lg text-slate-600 dark:text-slate-300">We build tools and stories for creators with clarity, speed, and measurable value. Designed for growth, automation, and a clean user journey.</p>
        <div class="mt-8 flex flex-wrap gap-3">
          <a href="/store.html" class="inline-flex items-center rounded-full bg-brand-600 hover:bg-brand-700 text-white px-6 py-3">Visit Store</a>
          <a href="#nini-beta" class="inline-flex items-center rounded-full border border-slate-300 dark:border-slate-700 px-6 py-3">Join Nini’s Beta</a>
          <a href="/portfolio.html" class="inline-flex items-center rounded-full border border-slate-300 dark:border-slate-700 px-6 py-3">See Work</a>
        </div>
      </div>
      <div class="relative">
        <img src="/assets/img/placeholders/hero-1600x900.webp" alt="iD01t Productions showcase image" class="aspect-[16/10] rounded-2xl object-cover ring-1 ring-slate-200 dark:ring-slate-800">
      </div>
    </div>
  </div>
</section>

<section id="nini-beta" class="py-16 border-t border-slate-200 dark:border-slate-800">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="grid md:grid-cols-2 gap-10 items-center">
      <div>
        <h2 class="text-3xl font-semibold">Nini’s Adventures: Kitties Mayhem! — Public PC Beta</h2>
        <p class="mt-3 text-slate-600 dark:text-slate-300">Explosive online multiplayer shooter. Public beta on <strong>September 24, 2025</strong>. No single-player. PC only for first beta. AWS-powered servers. Limited seats.</p>
        <ul class="mt-4 text-sm list-disc pl-5 space-y-1 text-slate-600 dark:text-slate-300">
          <li>High-energy deathmatches with unique feline abilities</li>
          <li>Colorful destructible arenas built for mayhem</li>
          <li>Scalable servers and anti-cheat pipeline</li>
        </ul>
      </div>
      <div>
        <img src="/assets/harvested/games/nini_hero.webp" alt="Nini’s Adventures: Kitties Mayhem artwork" class="rounded-2xl aspect-[16/10] object-cover ring-1 ring-slate-200 dark:ring-slate-800">
        <form class="mt-6 grid sm:grid-cols-2 gap-3" name="nini-beta" method="POST" data-netlify="true">
          <input type="hidden" name="form-name" value="nini-beta" />
          <input class="rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-3 sm:col-span-2" name="email" type="email" placeholder="Email for beta access" required>
          <button class="rounded-full bg-brand-600 hover:bg-brand-700 text-white px-6 py-3 w-max">Request Access</button>
          <p class="text-xs text-slate-500 sm:col-span-2">No payment. Email only. We will contact selected testers by email.</p>
        </form>
      </div>
    </div>
  </div>
</section>

<section id="store" class="py-16 border-t border-slate-200 dark:border-slate-800">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="flex items-end justify-between">
      <h2 class="text-2xl font-semibold">Store</h2>
      <a href="/store.html" class="text-sm link-underline">View all</a>
    </div>
    <div class="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <article class="group rounded-2xl border border-slate-200 dark:border-slate-800 p-5 hover:shadow-lg transition">
        <img src="/assets/harvested/apps/img_3.png" alt="Bedtime Story Maker for Windows" class="aspect-video rounded-xl object-cover bg-slate-100 dark:bg-slate-900">
        <h3 class="mt-4 font-semibold">Bedtime Story Maker · Windows</h3>
        <p class="text-sm text-slate-600 dark:text-slate-300 mt-1">Create full stories in seconds, bilingual, friendly UI, frequent updates.</p>
        <div class="mt-4 flex items-center justify-between"><span class="font-semibold">$9.99 CAD</span><a href="https://id01t.itch.io/" target="_blank" rel="noopener" class="text-sm link-underline">Buy</a></div>
      </article>
      <article class="group rounded-2xl border border-slate-200 dark:border-slate-800 p-5 hover:shadow-lg transition">
        <img src="/assets/harvested/ebooks/img_30.jpg" alt="Veo3 JSON Guide eBook" class="aspect-video rounded-xl object-cover bg-slate-100 dark:bg-slate-900">
        <h3 class="mt-4 font-semibold">Veo3 JSON Guide · eBook</h3>
        <p class="text-sm text-slate-600 dark:text-slate-300 mt-1">Learn smart JSON skills for cinematic results with real templates.</p>
        <div class="mt-4 flex items-center justify-between"><span class="font-semibold">$7.99 CAD</span><a href="https://books.google.com/books?id=MJFJEQAAQBAJ" target="_blank" rel="noopener" class="text-sm link-underline">Buy</a></div>
      </article>
      <article class="group rounded-2xl border border-slate-200 dark:border-slate-800 p-5 hover:shadow-lg transition">
        <img src="/assets/harvested/apps/img_4.png" alt="Sprite Forge Pro toolkit" class="aspect-video rounded-xl object-cover bg-slate-100 dark:bg-slate-900">
        <h3 class="mt-4 font-semibold">Sprite Forge Pro · Toolkit</h3>
        <p class="text-sm text-slate-600 dark:text-slate-300 mt-1">Modern sprite and texture creation, polished workflow, clear exports.</p>
        <div class="mt-4 flex items-center justify-between"><span class="font-semibold">$19.00 CAD</span><a href="#" class="text-sm link-underline">Buy</a></div>
      </article>
    </div>
  </div>
</section>

<section class="py-16" id="ebooks"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"><div class="flex items-end justify-between"><h2 class="text-2xl font-semibold">eBooks</h2><a href="/ebooks.html" class="text-sm link-underline">Explore catalog</a></div><p class="mt-4 text-slate-600 dark:text-slate-300 max-w-3xl">Guides for developers and creators with clean steps, examples, and real assets. Simple learning, fast results.</p></div></section>
<section class="py-16 border-t border-slate-200 dark:border-slate-800" id="apps"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"><h2 class="text-2xl font-semibold">Apps</h2><p class="mt-4 text-slate-600 dark:text-slate-300 max-w-3xl">Desktop and mobile tools with friendly design, simple setup, and useful features.</p></div></section>
<section class="py-16" id="games"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"><h2 class="text-2xl font-semibold">Games</h2><p class="mt-4 text-slate-600 dark:text-slate-300 max-w-3xl">Action and fun, fast pace and clear goals. Playtests open soon.</p></div></section>
<section class="py-16 border-t border-slate-200 dark:border-slate-800" id="music"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"><h2 class="text-2xl font-semibold">Music</h2><p class="mt-4 text-slate-600 dark:text-slate-300 max-w-3xl">Albums and sound design with energy and story. Find tracks on main platforms.</p></div></section>
<section class="py-16" id="services"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"><h2 class="text-2xl font-semibold">Services</h2><div class="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3"><div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-6"><h3 class="font-semibold">Web & Apps</h3><p class="mt-2 text-sm text-slate-600 dark:text-slate-300">Design, build, deploy, with clear docs and handover.</p></div><div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-6"><h3 class="font-semibold">Brand & Media</h3><p class="mt-2 text-sm text-slate-600 dark:text-slate-300">Logos, covers, banners, videos, with clean style and story.</p></div><div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-6"><h3 class="font-semibold">Automation</h3><p class="mt-2 text-sm text-slate-600 dark:text-slate-300">Pipelines and scripts for content, sales, and support.</p></div></div></div></section>
<section class="py-16 border-t border-slate-200 dark:border-slate-800" id="portfolio"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"><h2 class="text-2xl font-semibold">Portfolio</h2><p class="mt-4 text-slate-600 dark:text-slate-300 max-w-3xl">Selected work across tools and media, with short case studies and results.</p><div class="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3"><div class="aspect-video rounded-xl bg-slate-100 dark:bg-slate-900"></div><div class="aspect-video rounded-xl bg-slate-100 dark:bg-slate-900"></div><div class="aspect-video rounded-xl bg-slate-100 dark:bg-slate-900"></div></div></div></section>
<section class="py-16" id="about"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"><h2 class="text-2xl font-semibold">About</h2><p class="mt-4 text-slate-600 dark:text-slate-300 max-w-3xl">We are a Canadian creative and tech studio. We build with care, we ship with speed, and we focus on value and clean results for users.</p></div></section>
<section class="py-16 border-t border-slate-200 dark:border-slate-800" id="newsletter"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"><h2 class="text-2xl font-semibold">Newsletter</h2><p class="mt-2 text-slate-600 dark:text-slate-300 max-w-2xl">Get release notes, beta invites, and discounts. One concise email per month.</p><form class="mt-6 grid sm:grid-cols-2 gap-4 max-w-3xl" name="newsletter" method="POST" data-netlify="true"><input type="hidden" name="form-name" value="newsletter" /><input class="rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-3 sm:col-span-2" name="email" type="email" placeholder="Email" required><button class="rounded-full bg-brand-600 hover:bg-brand-700 text-white px-6 py-3 w-max">Subscribe</button><p class="mt-2 text-xs text-slate-500 sm:col-span-2">By subscribing you accept our privacy policy. Unsubscribe anytime.</p></form></div></section>
<section class="py-16 border-t border-slate-200 dark:border-slate-800" id="contact"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"><h2 class="text-2xl font-semibold">Contact</h2><form class="mt-6 grid sm:grid-cols-2 gap-4 max-w-3xl" name="contact" method="POST" data-netlify="true"><input type="hidden" name="form-name" value="contact" /><input class="rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-3" name="name" placeholder="Name" required><input class="rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-3" name="email" type="email" placeholder="Email" required><textarea class="rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-3 sm:col-span-2" name="message" rows="5" placeholder="Message" required></textarea><button class="rounded-full bg-brand-600 hover:bg-brand-700 text-white px-6 py-3 w-max">Send</button></form><p class="mt-4 text-sm text-slate-500">By sending a message you accept our privacy policy.</p></div></section>

<footer class="py-10 border-t border-slate-200 dark:border-slate-800"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"><div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-6"><div><p class="font-semibold">iD01t Productions</p><p class="text-sm text-slate-500">© <span id="year"></span> All rights reserved</p></div><nav class="flex flex-wrap gap-4 text-sm"><a href="/legal/terms.html" class="link-underline">Terms</a><a href="/legal/privacy.html" class="link-underline">Privacy</a><a href="/legal/refunds.html" class="link-underline">Refunds</a><a href="https://github.com/id01t" class="link-underline" target="_blank" rel="noopener">GitHub</a><a href="https://id01t.itch.io" class="link-underline" target="_blank" rel="noopener">itch.io</a></nav></div></div></footer>
<script>document.getElementById('year').textContent=new Date().getFullYear();const t=document.getElementById('themeToggle');if(t){t.addEventListener('click',()=>{const d=document.documentElement.classList.toggle('dark');localStorage.setItem('theme',d?'dark':'light');t.setAttribute('aria-pressed',String(d));});}const mb=document.getElementById('mobileMenuBtn'),mm=document.getElementById('mobileMenu');if(mb&&mm){mb.addEventListener('click',()=>{mm.classList.toggle('hidden');});}</script>
</body></html>
"""

EBOOKS_HTML = r"""<!DOCTYPE html><html lang="fr" class="scroll-smooth"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>eBooks · iD01t Productions</title>
<meta name="description" content="Premium eBooks and guides for developers, creators, and teams."/>
<link rel="icon" href="/favicon.ico"/><link rel="canonical" href="https://id01t.github.io/ebooks.html"/>
<meta name="theme-color" content="#16185c"/>
<meta property="og:title" content="eBooks · iD01t Productions"/><meta property="og:description" content="Premium eBooks and guides."/>
<meta property="og:type" content="website"/><meta property="og:url" content="https://id01t.github.io/ebooks.html"/>
<meta property="og:image" content="https://id01t.github.io/assets/img/placeholders/card-portrait-384x576.webp"/>
<meta name="twitter:card" content="summary_large_image"/><meta name="twitter:title" content="eBooks · iD01t Productions"/>
<meta name="twitter:description" content="Premium eBooks and guides."/>
<meta name="twitter:image" content="https://id01t.github.io/assets/img/placeholders/card-portrait-384x576.webp"/>
<script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config={theme:{extend:{colors:{brand:{50:"#f5f6ff",100:"#e6e9ff",200:"#c9ccff",300:"#a2a8ff",400:"#7a82ff",500:"#545cff",600:"#3a3fe6",700:"#2c30b4",800:"#202383",900:"#16185c"}}}}};</script>
<link rel="stylesheet" href="/css/custom.css">
<script>(function(){const s=localStorage.getItem('theme');const d=matchMedia('(prefers-color-scheme: dark)').matches;if(s==='dark'||(!s&&d))document.documentElement.classList.add('dark');})();</script>
</head>
<body class="bg-white text-slate-800 dark:bg-slate-950 dark:text-slate-100">
<header class="sticky top-0 z-50 backdrop-blur supports-backdrop-blur:bg-white/70 bg-white/70 dark:bg-slate-950/60 border-b border-slate-200/60 dark:border-slate-800">
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="flex items-center justify-between h-16">
<a href="/" class="flex items-center gap-2" aria-label="Accueil"><img src="/assets/img/brand/logo.png" alt="iD01t Productions" class="h-8 w-8"><span class="font-semibold tracking-tight">iD01t Productions</span></a>
<nav class="hidden md:flex items-center gap-6"><a href="/store.html" class="link-underline">Store</a><a href="/ebooks.html" class="link-underline text-brand-600 dark:text-brand-400" aria-current="page">eBooks</a><a href="/apps.html" class="link-underline">Apps</a><a href="/games.html" class="link-underline">Games</a><a href="/music.html" class="link-underline">Music</a><a href="/services.html" class="link-underline">Services</a><a href="/portfolio.html" class="link-underline">Portfolio</a><a href="/about.html" class="link-underline">About</a><a href="/contact.html" class="link-underline">Contact</a></nav>
<div class="flex items-center gap-3"><button id="themeToggle" class="rounded-full border border-slate-300 dark:border-slate-700 px-3 py-1 text-sm">Theme</button><a href="/#newsletter" class="inline-flex items-center rounded-full bg-brand-600 hover:bg-brand-700 text-white text-sm px-4 py-2">Newsletter</a>
<button id="mobileMenuBtn" class="md:hidden inline-flex items-center justify-center p-2 rounded-lg border border-slate-300 dark:border-slate-700" aria-label="Open menu"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button></div></div></div>
<div id="mobileMenu" class="md:hidden hidden border-t border-slate-200 dark:border-slate-800" role="dialog" aria-modal="true"><div class="px-4 py-3 flex flex-col gap-2"><a href="/store.html" class="py-2">Store</a><a href="/ebooks.html" class="py-2 text-brand-600 dark:text-brand-400">eBooks</a><a href="/apps.html" class="py-2">Apps</a><a href="/games.html" class="py-2">Games</a><a href="/music.html" class="py-2">Music</a><a href="/services.html" class="py-2">Services</a><a href="/portfolio.html" class="py-2">Portfolio</a><a href="/about.html" class="py-2">About</a><a href="/contact.html" class="py-2">Contact</a></div></div>
</header>
<section class="relative overflow-hidden"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-12 pb-6"><div class="text-center"><h1 class="text-4xl sm:text-5xl font-bold tracking-tight">eBooks</h1><p class="mt-3 text-lg text-slate-600 dark:text-slate-300 max-w-3xl mx-auto">Guides for developers and creators. Clear steps, real examples, fast results.</p></div></div></section>
<section class="pb-4"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"><div class="grid gap-3 md:grid-cols-12 items-end">
<div class="md:col-span-6"><input id="search" type="search" placeholder="Search title, tags, or description" class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-3"></div>
<div class="md:col-span-2"><select id="length" class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-3"><option value="">All lengths</option><option value="short">Short &lt;60 pages</option><option value="medium">Medium 60–100</option><option value="long">Long &gt;100</option></select></div>
<div class="md:col-span-2"><select id="price" class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-3"><option value="">All prices</option><option value="lt10">&lt; $10</option><option value="10to15">$10–$15</option><option value="gt15">&gt; $15</option></select></div>
<div class="md:col-span-2"><select id="sort" class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-3"><option value="recent">Newest</option><option value="az">A → Z</option><option value="priceAsc">Price ↑</option><option value="priceDesc">Price ↓</option></select></div>
<div class="md:col-span-12 flex gap-2"><button id="resetFilters" class="text-sm px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-700">Reset</button></div>
</div></div></section>
<section class="py-8 border-t border-slate-200 dark:border-slate-800"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"><div id="ebookGrid" class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3"></div><div id="pagination" class="flex items-center justify-center gap-2 mt-10"></div></div></section>
<footer class="py-10 border-t border-slate-200 dark:border-slate-800"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"><div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-6"><div><p class="font-semibold">iD01t Productions</p><p class="text-sm text-slate-500">© <span id="year"></span> All rights reserved</p></div><nav class="flex flex-wrap gap-4 text-sm"><a href="/legal/terms.html" class="link-underline">Terms</a><a href="/legal/privacy.html" class="link-underline">Privacy</a><a href="/legal/refunds.html" class="link-underline">Refunds</a><a href="https://github.com/id01t" class="link-underline" target="_blank" rel="noopener">GitHub</a><a href="https://id01t.itch.io" class="link-underline" target="_blank" rel="noopener">itch.io</a></nav></div></div></footer>
<script>document.getElementById('year').textContent=new Date().getFullYear();const t=document.getElementById('themeToggle');if(t){t.addEventListener('click',()=>{const d=document.documentElement.classList.toggle('dark');localStorage.setItem('theme',d?'dark':'light');t.setAttribute('aria-pressed',String(d));});}const mb=document.getElementById('mobileMenuBtn'),mm=document.getElementById('mobileMenu');if(mb&&mm){mb.addEventListener('click',()=>mm.classList.toggle('hidden'));}</script>
<script src="/js/ebooks.js" defer></script></body></html>
"""

EBOOKS_JS = r"""// /js/ebooks.js
const CATALOG_URL="/assets/data/ebooks.json";const PAGE_SIZE=18;
const grid=document.getElementById("ebookGrid"),pagination=document.getElementById("pagination"),searchInput=document.getElementById("search"),lengthSelect=document.getElementById("length"),priceSelect=document.getElementById("price"),sortSelect=document.getElementById("sort"),resetBtn=document.getElementById("resetFilters");let items=[],filtered=[],page=1;
function lengthBucket(p){if(!p)return"";if(p<60)return"short";if(p<=100)return"medium";return"long";}
function formatPrice(v){if(typeof v!=="number")return"";return`$${v.toFixed(2)} CAD`;}
function cardTemplate(b){const img=b.image||"/assets/img/placeholders/card-portrait-384x576.webp";const pages=b.pages?`${b.pages} pages`:"";const desc=b.description||"";return `
<article class="group rounded-2xl border border-slate-200 dark:border-slate-800 p-6 hover:shadow-lg transition">
  <img src="${img}" alt="${b.title}" class="aspect-[3/4] w-full rounded-xl object-cover ring-1 ring-slate-200 dark:ring-slate-800 mb-4" loading="lazy" decoding="async">
  <h3 class="font-semibold text-lg mb-2">${b.title}</h3>
  <p class="text-slate-600 dark:text-slate-300 text-sm mb-4">${desc}</p>
  <div class="flex items-center justify-between mb-4"><span class="font-semibold text-lg">${formatPrice(b.price_cad)}</span><span class="text-xs text-slate-500">${pages}</span></div>
  <div class="flex gap-2">
    ${b.preview_url?`<a href="${b.preview_url}" target="_blank" rel="noopener" class="flex-1 text-center py-2 px-4 border border-slate-300 dark:border-slate-700 rounded-lg text-sm hover:bg-slate-50 dark:hover:bg-slate-900 transition">Preview</a>`:""}
    <a href="${b.url}" target="_blank" rel="noopener" class="flex-1 text-center py-2 px-4 bg-brand-600 hover:bg-brand-700 text-white rounded-lg text-sm transition">Buy Now</a>
  </div>
</article>`;}
function render(){const start=(page-1)*PAGE_SIZE;const slice=filtered.slice(start,start+PAGE_SIZE);grid.innerHTML=slice.map(cardTemplate).join("");renderPagination();}
function renderPagination(){const totalPages=Math.ceil(filtered.length/PAGE_SIZE)||1;pagination.innerHTML="";const btn=(p,label=p,disabled=false,active=false)=>{const b=document.createElement("button");b.textContent=label;b.className=`px-3 py-2 rounded-lg border ${active?"bg-brand-600 text-white border-brand-600":"border-slate-300 dark:border-slate-700"} ${disabled?"opacity-50 cursor-not-allowed":"hover:bg-slate-50 dark:hover:bg-slate-900"}`;b.disabled=disabled;b.addEventListener("click",()=>{page=p;render();window.scrollTo({top:0,behavior:"smooth"});});pagination.appendChild(b);};btn(Math.max(1,page-1),"Prev",page===1);for(let p=1;p<=totalPages;p++){if(p===1||p===totalPages||Math.abs(p-page)<=2){btn(p,String(p),false,p===page);}else if(Math.abs(p-page)===3){const span=document.createElement("span");span.textContent="…";span.className="px-2 text-slate-500";pagination.appendChild(span);}}btn(Math.min(totalPages,page+1),"Next",page===totalPages);}
function applyFilters(){const q=(searchInput.value||"").toLowerCase().trim(),len=lengthSelect.value,price=priceSelect.value,sort=sortSelect.value;filtered=items.filter(b=>{const hay=`${b.title} ${b.description||""} ${(b.tags||[]).join(" ")}`.toLowerCase();const matchQ=!q||hay.includes(q),matchLen=!len||lengthBucket(b.pages)===len,matchPrice=!price||(price==="lt10"&&Number(b.price_cad)<10)||(price==="10to15"&&Number(b.price_cad)>=10&&Number(b.price_cad)<=15)||(price==="gt15"&&Number(b.price_cad)>15);return matchQ&&matchLen&&matchPrice;});filtered.sort((a,b)=>{if(sort==="az")return a.title.localeCompare(b.title);if(sort==="priceAsc")return Number(a.price_cad)-Number(b.price_cad);if(sort==="priceDesc")return Number(b.price_cad)-Number(a.price_cad);const da=new Date(a.date||"1970-01-01").getTime(),db=new Date(b.date||"1970-01-01").getTime();return db-da;});page=1;render();}
async function init(){try{const res=await fetch(CATALOG_URL,{cache:"no-store"});if(!res.ok)throw new Error("Catalog fetch failed");items=await res.json();}catch(e){console.error(e);items=[];}applyFilters();}
searchInput.addEventListener("input",()=>applyFilters());lengthSelect.addEventListener("change",()=>applyFilters());priceSelect.addEventListener("change",()=>applyFilters());sortSelect.addEventListener("change",()=>applyFilters());resetBtn.addEventListener("click",()=>{searchInput.value="";lengthSelect.value="";priceSelect.value="";sortSelect.value="recent";applyFilters();});init();
"""

CUSTOM_CSS = """/* /css/custom.css */
.link-underline{ text-decoration:none; border-bottom:1px solid rgba(100,116,139,.35); padding-bottom:2px;}
.link-underline:hover{ border-color:rgba(84,92,255,.9);}
"""

SAMPLE_JSON = [
  {"title":"Veo3 JSON Guide","price_cad":7.99,"pages":45,"image":"/assets/harvested/ebooks/img_30.jpg","url":"https://books.google.com/books?id=MJFJEQAAQBAJ","preview_url":"","tags":["json","veo3","video"],"date":"2025-08-10","description":"Learn smart JSON skills for cinematic results with real templates."},
  {"title":"DIY Digital Skills","price_cad":16.99,"pages":140,"image":"/assets/harvested/ebooks/img_45.jpg","url":"https://books.google.com/books?id=f8o9EQAAQBAJ","preview_url":"","tags":["career","skills"],"date":"2025-07-01","description":"Build a career in tech from scratch with a practical roadmap."},
  {"title":"Chess Mastery","price_cad":18.99,"pages":180,"image":"/assets/harvested/ebooks/img_48.jpg","url":"https://books.google.com/books?id=m5M4EQAAQBAJ","preview_url":"","tags":["chess","strategy"],"date":"2025-05-01","description":"Advanced chess strategies and expert analysis for serious players."}
]

CSV_TO_JSON = r'''#!/usr/bin/env python3
"""
CSV -> JSON converter for iD01t eBooks catalog.
Headers: title, price_cad, pages, image, url, preview_url, tags, date, description
Usage: python tools/csv_to_json.py input.csv assets/data/ebooks.json
"""
import csv, json, sys, os
def norm_header(s): return s.strip().lower().replace(" ", "_")
def to_number(v):
    try: return float(v)
    except Exception: return None
def main():
    if len(sys.argv)<3:
        print("Usage: csv_to_json.py input.csv output.json"); sys.exit(1)
    inp,outp=sys.argv[1],sys.argv[2]; rows=[]
    with open(inp, newline='', encoding='utf-8') as f:
        rdr=csv.DictReader(f)
        for row in rdr:
            r={norm_header(k):(v.strip() if isinstance(v,str) else v) for k,v in row.items()}
            item={"title":r.get("title",""),
                  "price_cad":to_number(r.get("price_cad","") or r.get("price","")),
                  "pages":int(float(r.get("pages","0") or 0)) if (r.get("pages") or "").strip() else None,
                  "image":r.get("image",""),"url":r.get("url",""),"preview_url":r.get("preview_url",""),
                  "tags":[t.strip() for t in (r.get("tags","").split(",") if r.get("tags") else []) if t.strip()],
                  "date":r.get("date",""),"description":r.get("description","")}
            rows.append(item)
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    with open(outp,"w",encoding="utf-8") as f: json.dump(rows,f,ensure_ascii=False,indent=2)
    print(f"Wrote {len(rows)} items to {outp}")
if __name__=="__main__": main()
'''

LEGAL_TERMS = "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'><title>Terms</title><meta name='viewport' content='width=device-width, initial-scale=1'></head><body style='font-family:system-ui;max-width:800px;margin:40px auto;line-height:1.6'><h1>Terms</h1><p>Simple licensing: personal use unless otherwise stated. No unauthorized redistribution. Contact us for commercial terms.</p></body></html>"
LEGAL_PRIVACY = "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'><title>Privacy</title><meta name='viewport' content='width=device-width, initial-scale=1'></head><body style='font-family:system-ui;max-width:800px;margin:40px auto;line-height:1.6'><h1>Privacy</h1><p>We collect minimal data via forms (name, email, message). We do not sell data. You can request deletion at any time.</p></body></html>"
LEGAL_REFUNDS = "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'><title>Refunds</title><meta name='viewport' content='width=device-width, initial-scale=1'></head><body style='font-family:system-ui;max-width:800px;margin:40px auto;line-height:1.6'><h1>Refunds</h1><p>Digital goods are generally non-refundable once delivered. If there's a technical issue, contact us within 7 days.</p></body></html>"

ROBOTS = "User-agent: *\nAllow: /\nSitemap: https://id01t.github.io/sitemap.xml\n"

def ensure_dirs():
    for d in DIRS: (BASE / d).mkdir(parents=True, exist_ok=True)

def write(p: Path, content: str, binary=False):
    p.parent.mkdir(parents=True, exist_ok=True)
    mode = "wb" if binary else "w"
    with open(p, mode, encoding=None if binary else "utf-8") as f:
        f.write(content)

def make_simple_svg(w,h,label):
    # Fallback images if Pillow not installed
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}'>
<defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0%' stop-color='#16185c'/><stop offset='100%' stop-color='#7a82ff'/></linearGradient></defs>
<rect width='100%' height='100%' fill='url(#g)'/>
<text x='50%' y='50%' font-family='Segoe UI,Arial' font-size='{int(min(w,h)/12)}' fill='white' text-anchor='middle' dominant-baseline='middle'>{label}</text>
</svg>"""

def make_images():
    try:
        from PIL import Image, ImageDraw, ImageFont
        def mk(w,h,text,color=(24,26,92)):
            img = Image.new("RGB",(w,h),color)
            d = ImageDraw.Draw(img)
            try: font = ImageFont.truetype("DejaVuSans.ttf", size=max(20,w//24))
            except: font = ImageFont.load_default()
            tw,th = d.textbbox((0,0), text, font=font)[2:]
            d.text(((w-tw)//2,(h-th)//2), text, fill=(240,240,255), font=font)
            return img
        mk(1600,900,"iD01t Productions — Hero").save(BASE/"assets/img/placeholders/hero-1600x900.webp","WEBP")
        mk(384,576,"Cover Placeholder").save(BASE/"assets/img/placeholders/card-portrait-384x576.webp","WEBP")
        mk(256,256,"iD01t").save(BASE/"assets/img/brand/logo.png","PNG")
        mk(480,270,"App Image").save(BASE/"assets/harvested/apps/img_3.png","PNG")
        mk(480,270,"Toolkit Image").save(BASE/"assets/harvested/apps/img_4.png","PNG")
        mk(384,576,"Veo3 JSON Guide").save(BASE/"assets/harvested/ebooks/img_30.jpg","JPEG")
        mk(480,270,"Nini Hero").save(BASE/"assets/harvested/games/nini_hero.webp","WEBP")
        mk(512,512,"About").save(BASE/"assets/img/placeholders/about.webp","WEBP")
    except Exception:
        write(BASE/"assets/img/placeholders/hero-1600x900.webp", make_simple_svg(1600,900,"iD01t Hero"))
        write(BASE/"assets/img/placeholders/card-portrait-384x576.webp", make_simple_svg(384,576,"Cover"))
        write(BASE/"assets/img/brand/logo.png", make_simple_svg(256,256,"iD01t"))
        write(BASE/"assets/harvested/apps/img_3.png", make_simple_svg(480,270,"App"))
        write(BASE/"assets/harvested/apps/img_4.png", make_simple_svg(480,270,"Toolkit"))
        write(BASE/"assets/harvested/ebooks/img_30.jpg", make_simple_svg(384,576,"Veo3"))
        write(BASE/"assets/harvested/games/nini_hero.webp", make_simple_svg(480,270,"Nini"))
        write(BASE/"assets/img/placeholders/about.webp", make_simple_svg(512,512,"About"))

def write_secondary_pages():
    def page(title, heading, body, active=""):
        def nav_active(x): return " text-brand-600 dark:text-brand-400" if x==active else ""
        return f"""<!DOCTYPE html><html lang="fr" class="scroll-smooth"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/><title>{title} · iD01t Productions</title>
<meta name="description" content="{heading} — iD01t Productions"/><link rel="icon" href="/favicon.ico"/>
<meta name="theme-color" content="#16185c"/><script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config={{theme:{{extend:{{colors:{{brand:{{50:'#f5f6ff',100:'#e6e9ff',200:'#c9ccff',300:'#a2a8ff',400:'#7a82ff',500:'#545cff',600:'#3a3fe6',700:'#2c30b4',800:'#202383',900:'#16185c'}}}}}}}}}};</script>
<link rel="stylesheet" href="/css/custom.css"><script>(function(){{const s=localStorage.getItem('theme');const d=matchMedia('(prefers-color-scheme: dark)').matches;if(s==='dark'||(!s&&d))document.documentElement.classList.add('dark');}})();</script>
</head><body class="bg-white text-slate-800 dark:bg-slate-950 dark:text-slate-100">
<header class="sticky top-0 z-50 backdrop-blur supports-backdrop-blur:bg-white/70 bg-white/70 dark:bg-slate-950/60 border-b border-slate-200/60 dark:border-slate-800">
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="flex items-center justify-between h-16">
<a href="/" class="flex items-center gap-2" aria-label="Accueil"><img src="/assets/img/brand/logo.png" class="h-8 w-8" alt="iD01t Productions"><span class="font-semibold tracking-tight">iD01t Productions</span></a>
<nav class="hidden md:flex items-center gap-6" aria-label="Navigation principale">
<a href="/store.html" class="link-underline{nav_active('store')}">Store</a>
<a href="/ebooks.html" class="link-underline{nav_active('ebooks')}">eBooks</a>
<a href="/apps.html" class="link-underline{nav_active('apps')}">Apps</a>
<a href="/games.html" class="link-underline{nav_active('games')}">Games</a>
<a href="/music.html" class="link-underline{nav_active('music')}">Music</a>
<a href="/services.html" class="link-underline{nav_active('services')}">Services</a>
<a href="/portfolio.html" class="link-underline{nav_active('portfolio')}">Portfolio</a>
<a href="/about.html" class="link-underline{nav_active('about')}">About</a>
<a href="/contact.html" class="link-underline{nav_active('contact')}">Contact</a>
</nav>
<div class="flex items-center gap-3"><button id="themeToggle" class="rounded-full border border-slate-300 dark:border-slate-700 px-3 py-1 text-sm">Theme</button>
<a href="/#newsletter" class="inline-flex items-center rounded-full bg-brand-600 hover:bg-brand-700 text-white text-sm px-4 py-2">Newsletter</a>
<button id="mobileMenuBtn" class="md:hidden inline-flex items-center justify-center p-2 rounded-lg border border-slate-300 dark:border-slate-700" aria-label="Ouvrir le menu"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button></div></div></div>
<div id="mobileMenu" class="md:hidden hidden border-t border-slate-200 dark:border-slate-800" role="dialog" aria-modal="true"><div class="px-4 py-3 flex flex-col gap-2">
<a href="/store.html" class="py-2">Store</a><a href="/ebooks.html" class="py-2">eBooks</a><a href="/apps.html" class="py-2">Apps</a><a href="/games.html" class="py-2">Games</a><a href="/music.html" class="py-2">Music</a><a href="/services.html" class="py-2">Services</a><a href="/portfolio.html" class="py-2">Portfolio</a><a href="/about.html" class="py-2">About</a><a href="/contact.html" class="py-2">Contact</a>
</div></div></header>
<section class="relative overflow-hidden"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-12 pb-6"><div class="text-center"><h1 class="text-4xl sm:text-5xl font-bold tracking-tight">{heading}</h1></div></div></section>
<main class="py-8 border-t border-slate-200 dark:border-slate-800"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">{body}</div></main>
<footer class="py-10 border-t border-slate-200 dark:border-slate-800"><div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"><div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-6"><div><p class="font-semibold">iD01t Productions</p><p class="text-sm text-slate-500">© <span id="year"></span> All rights reserved</p></div><nav class="flex flex-wrap gap-4 text-sm"><a href="/legal/terms.html" class="link-underline">Terms</a><a href="/legal/privacy.html" class="link-underline">Privacy</a><a href="/legal/refunds.html" class="link-underline">Refunds</a><a href="https://github.com/id01t" class="link-underline" target="_blank" rel="noopener">GitHub</a><a href="https://id01t.itch.io" class="link-underline" target="_blank" rel="noopener">itch.io</a></nav></div></div></footer>
<script>document.getElementById('year').textContent=new Date().getFullYear();const t=document.getElementById('themeToggle');if(t){t.addEventListener('click',()=>{const d=document.documentElement.classList.toggle('dark');localStorage.setItem('theme',d?'dark':'light');t.setAttribute('aria-pressed',String(d));});}const mb=document.getElementById('mobileMenuBtn'),mm=document.getElementById('mobileMenu');if(mb&&mm){mb.addEventListener('click',()=>mm.classList.toggle('hidden'));}</script>
</body></html>"""
    return page

def write_pages():
    # Core pages already: index + ebooks
    # Simple store/apps/games/music/services/portfolio/about/contact
    page = write_secondary_pages()
    store = """
<p class="text-slate-600 dark:text-slate-300 mb-6">All-in-one storefront. Explore eBooks, apps, games, and music.</p>
<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
  <article class="rounded-2xl border border-slate-200 dark:border-slate-800 p-5">
    <img src="/assets/harvested/apps/img_3.png" class="aspect-video rounded-xl object-cover mb-4" alt="Bedtime Story Maker">
    <h3 class="font-semibold">Bedtime Story Maker · Windows</h3>
    <p class="text-sm text-slate-600 dark:text-slate-300 mt-1">Create full stories in seconds. Friendly UI.</p>
  </article>
  <article class="rounded-2xl border border-slate-200 dark:border-slate-800 p-5">
    <img src="/assets/harvested/ebooks/img_30.jpg" class="aspect-[3/4] rounded-xl object-cover mb-4" alt="Veo3 JSON Guide">
    <h3 class="font-semibold">Veo3 JSON Guide · eBook</h3>
    <p class="text-sm text-slate-600 dark:text-slate-300 mt-1">Smart JSON for cinematic results.</p>
  </article>
  <article class="rounded-2xl border border-slate-200 dark:border-slate-800 p-5">
    <img src="/assets/harvested/games/nini_hero.webp" class="aspect-video rounded-xl object-cover mb-4" alt="Nini’s Adventures">
    <h3 class="font-semibold">Nini’s Adventures: Kitties Mayhem! · PC Beta</h3>
    <p class="text-sm text-slate-600 dark:text-slate-300 mt-1">Public beta Sep 24, 2025. PC-only.</p>
  </article>
</div>
"""
    apps = """
<p class="text-slate-600 dark:text-slate-300 mb-6">Desktop and mobile apps designed for clarity and speed.</p>
<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
  <article class="rounded-2xl border border-slate-200 dark:border-slate-800 p-5"><img src="/assets/harvested/apps/img_3.png" class="aspect-video rounded-xl object-cover mb-4" alt="Bedtime Story Maker"><h3 class="font-semibold">Bedtime Story Maker · Windows</h3><p class="text-sm text-slate-600 dark:text-slate-300">Bilingual stories in seconds.</p></article>
  <article class="rounded-2xl border border-slate-200 dark:border-slate-800 p-5"><img src="/assets/harvested/apps/img_4.png" class="aspect-video rounded-xl object-cover mb-4" alt="Sprite Forge Pro"><h3 class="font-semibold">Sprite Forge Pro · Toolkit</h3><p class="text-sm text-slate-600 dark:text-slate-300">Modern sprite and texture creation.</p></article>
</div>
"""
    games = """
<p class="text-slate-600 dark:text-slate-300 mb-6">Fast-paced action built for online play.</p>
<div class="grid md:grid-cols-2 gap-8 items-start">
  <div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-5">
    <img src="/assets/harvested/games/nini_hero.webp" class="rounded-xl aspect-video object-cover mb-4" alt="Nini’s Adventures artwork">
    <h3 class="font-semibold text-xl">Nini’s Adventures: Kitties Mayhem!</h3>
    <p class="text-sm text-slate-600 dark:text-slate-300 mt-2">Explosive online multiplayer shooter. PC public beta on <strong>September 24, 2025</strong>. No single-player. AWS powered servers.</p>
  </div>
  <div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-5">
    <h4 class="font-semibold mb-3">Request Beta Access</h4>
    <form name="nini-beta" method="POST" data-netlify="true" class="grid gap-3">
      <input type="hidden" name="form-name" value="nini-beta" />
      <input name="email" type="email" placeholder="Email" required class="rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-3">
      <button class="rounded-full bg-brand-600 hover:bg-brand-700 text-white px-6 py-3 w-max">Request Access</button>
      <p class="text-xs text-slate-500">No payment. Email only.</p>
    </form>
  </div>
</div>
"""
    music = """
<p class="text-slate-600 dark:text-slate-300 mb-6">Albums and sound design with energy and story.</p>
<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
  <div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-4"><p class="font-semibold">Last Transmission</p><p class="text-sm text-slate-500">Mar 2025</p></div>
  <div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-4"><p class="font-semibold">Signal Detected</p><p class="text-sm text-slate-500">Apr 2025</p></div>
  <div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-4"><p class="font-semibold">Sweat and Stardust</p><p class="text-sm text-slate-500">May 2025</p></div>
  <div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-4"><p class="font-semibold">Echo Protocol</p><p class="text-sm text-slate-500">May 2025</p></div>
  <div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-4"><p class="font-semibold">No Master Needed</p><p class="text-sm text-slate-500">Jul 2025</p></div>
  <div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-4"><p class="font-semibold">Anura Voidwalker DMT Chronicles</p><p class="text-sm text-slate-500">Aug 2025</p></div>
</div>
"""
    services = """
<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
  <div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-6"><h3 class="font-semibold">Web & Apps</h3><p class="mt-2 text-sm text-slate-600 dark:text-slate-300">Design, build, deploy, with clear docs and handover.</p></div>
  <div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-6"><h3 class="font-semibold">Brand & Media</h3><p class="mt-2 text-sm text-slate-600 dark:text-slate-300">Logos, covers, banners, videos, clean style and story.</p></div>
  <div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-6"><h3 class="font-semibold">Automation</h3><p class="mt-2 text-sm text-slate-600 dark:text-slate-300">Pipelines and scripts for content, sales, and support.</p></div>
</div>
"""
    portfolio = """
<p class="text-slate-600 dark:text-slate-300 mb-6">Selected work with short case studies and results.</p>
<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
  <div class="aspect-video rounded-xl bg-slate-100 dark:bg-slate-900"></div>
  <div class="aspect-video rounded-xl bg-slate-100 dark:bg-slate-900"></div>
  <div class="aspect-video rounded-xl bg-slate-100 dark:bg-slate-900"></div>
</div>
"""
    about = """
<div class="grid md:grid-cols-2 gap-10 items-center">
  <div><img src="/assets/img/placeholders/about.webp" alt="About iD01t Productions" class="rounded-2xl aspect-square object-cover ring-1 ring-slate-200 dark:ring-slate-800"></div>
  <div><p class="text-slate-600 dark:text-slate-300">We are a Canadian creative and tech studio. We build with care, ship with speed, and focus on value and clean results for users.</p>
  <ul class="list-disc pl-5 mt-4 space-y-1 text-sm text-slate-600 dark:text-slate-300"><li>Apps, eBooks, games, music</li><li>Automation-first, ROI-driven</li><li>Clean UX, strong publishing pipelines</li></ul></div>
</div>
"""
    contact = """
<p class="text-slate-600 dark:text-slate-300 mb-6">Send us a message. We reply to selected requests.</p>
<form class="grid sm:grid-cols-2 gap-4 max-w-3xl" name="contact" method="POST" data-netlify="true">
  <input type="hidden" name="form-name" value="contact" />
  <input class="rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-3" name="name" placeholder="Name" required>
  <input class="rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-3" name="email" type="email" placeholder="Email" required>
  <textarea class="rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-3 sm:col-span-2" name="message" rows="5" placeholder="Message" required></textarea>
  <button class="rounded-full bg-brand-600 hover:bg-brand-700 text-white px-6 py-3 w-max">Send</button>
</form>
"""
    PAGES = {
        "store.html": ("Store","Store",store,"store"),
        "apps.html": ("Apps","Apps",apps,"apps"),
        "games.html": ("Games","Games",games,"games"),
        "music.html": ("Music","Music",music,"music"),
        "services.html": ("Services","Services",services,"services"),
        "portfolio.html": ("Portfolio","Portfolio",portfolio,"portfolio"),
        "about.html": ("About","About",about,"about"),
        "contact.html": ("Contact","Contact",contact,"contact"),
    }
    for fname,(title,heading,body,active) in PAGES.items():
        html = write_secondary_pages()(title, heading, body, active)
        write(BASE/fname, html)

def write_sitemap_and_legal():
    write(BASE/"legal/terms.html", LEGAL_TERMS)
    write(BASE/"legal/privacy.html", LEGAL_PRIVACY)
    write(BASE/"legal/refunds.html", LEGAL_REFUNDS)
    write(BASE/"robots.txt", ROBOTS)
    # Basic sitemap
    urls = ["","index.html","store.html","ebooks.html","apps.html","games.html","music.html","services.html","portfolio.html","about.html","contact.html","legal/terms.html","legal/privacy.html","legal/refunds.html"]
    base = "https://id01t.github.io"
    entries = "\n".join([f"  <url><loc>{base}/{' ' if u=='' else u}</loc></url>".replace(" /","/") for u in urls])
    sm = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n'
    write(BASE/"sitemap.xml", sm)

def build():
    ensure_dirs()
    write(BASE/"index.html", INDEX_HTML)
    write(BASE/"ebooks.html", EBOOKS_HTML)
    write(BASE/"js/ebooks.js", EBOOKS_JS)
    write(BASE/"css/custom.css", CUSTOM_CSS)
    write(BASE/"assets/data/ebooks.json", json.dumps(SAMPLE_JSON, ensure_ascii=False, indent=2))
    write(BASE/"assets/data/ebooks.sample.json", json.dumps(SAMPLE_JSON, ensure_ascii=False, indent=2))
    write(BASE/"tools/csv_to_json.py", CSV_TO_JSON)
    make_images()
    write_pages()
    write_sitemap_and_legal()
    print(f"✅ Built at {BASE.resolve()}")
    if "--zip" in sys.argv:
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        zpath = Path(f"id01t_site_pack_v2-{ts}.zip")
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            for root,_,files in os.walk(BASE):
                for f in files:
                    p = Path(root)/f
                    z.write(p, p.relative_to(BASE.parent))
        print(f"📦 Zipped: {zpath.resolve()}")

if __name__=="__main__":
    build()
