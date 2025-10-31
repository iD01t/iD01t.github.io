Awesome — here’s your **full Website Audit (Findings.md)** for `id01t.github.io` and `id01t.store`, with **prioritized fixes, acceptance criteria, and next steps**. I browsed the live pages to ground everything below.

---

# Findings.md — iD01t Productions Web Audit

**Scope date:** Oct 30, 2025 (America/Toronto)
**Sites:** `id01t.github.io` (catalog/landing) ([iD01t Productions][1]) • `id01t.github.io/games.html` (links into id01t.store) ([iD01t Productions][2])
**Related surfaces:** Social + itch.io posts confirming product footprint and content needs (music, tools, games, books) ([youtube.com][3])

---

## Executive Summary

* **Overall**: Solid brand direction (dark aesthetic, product pillars) and content breadth. However, there are **duplications, placeholders, and structural gaps** (SEO, performance, a11y, i18n, automation).
* **Priority**: Unify information architecture across both domains, enforce a design system, add automation for catalogs, and harden SEO/perf.
* **Goal**: Hit **Lighthouse ≥ 95 (mobile/desktop)**, **WCAG 2.1 AA**, **EN/FR parity**, **automated catalog generation**.

---

## Critical (Fix immediately – impacts UX/SEO/Trust)

1. **Navigation duplication / layout anomalies**

* Observed repeated nav sections and duplicated headings/CTAs on the catalog & games pages (e.g., “Store eBooks Audiobooks …” printed twice in the games page; repeated “DJ iD01t New Album Available Now!” block on the home). This confuses users and bloats DOM. ([iD01t Productions][1])
  **Fix**: Refactor header/footer into a single shared include; dedupe sections; enforce component IDs.
  **AC**: No page contains duplicate nav bars or duplicated hero CTA blocks.

2. **Cross-domain inconsistency (`id01t.github.io` → `id01t.store`)**

* The **Games** page on GitHub Pages points to a **store-domain games page**, creating mixed contexts and brand drift. Decide canonical source-of-truth per content type and link accordingly. ([iD01t Productions][2])
  **Fix**: Route catalog discovery on `id01t.github.io`; checkout & purchases on `id01t.store`. Add canonical links.
  **AC**: Each page declares a canonical URL; sitewide nav consistently routes to the correct domain per intent.

3. **Missing structured data & SEO meta hygiene**

* Product/Book/Game pages lack **Schema.org** (`Product`, `SoftwareApplication`, `Book`, `MusicAlbum`) and often rely on generic copy. This limits search visibility/snippets. (Home & games show no structured data blocks; OG/Twitter tags not comprehensive.) ([iD01t Productions][1])
  **Fix**: Add JSON-LD templates, per content type; ensure unique `<title>`, `<meta name="description">`, OG/Twitter cards.
  **AC**: Rich results are detected in Google’s Rich Results Test; all pages have unique titles/descriptions.

4. **Sitemaps/robots/canonical gaps**

* No explicit **sitemap.xml** / **robots.txt** surfaced from the pages scanned; canonical tags appear absent/inconsistent. ([iD01t Productions][1])
  **Fix**: Generate sitemap(s) per domain, add robots.txt, declare canonical on every indexable page.
  **AC**: `/<sitemap.xml>` returns a valid sitemap; `/<robots.txt>` lists at least the sitemap location.

---

## Major (High value within 2–4 weeks)

5. **Internationalization (EN/FR) not fully implemented**

* Your footprint clearly spans EN/FR (books, music, itch posts mention bilingual features), but the sites aren’t consistently bilingual. ([play.google.com][4])
  **Fix**: Introduce a language switcher + content JSON bundles.
  **AC**: Each page renders EN/FR parity; `hreflang` tags present.

6. **Design System & consistency**

* Dark theme exists, but typography/spacing/button styles vary between pages; some sections feel templated. ([iD01t Productions][1])
  **Fix**: Create a **DesignSystem.md** + tokens (colors, font scale, spacing, radii), component library (Header, Footer, Hero, ProductCard, CTA, Grid, FooterLegal).
  **AC**: All pages import the same CSS vars/tokens; visual diffs show consistent paddings and type ramps.

7. **Performance (images & layout shifts)**

* Hero imagery and product artwork appear un-optimized; no `<picture>` responsive sets; likely LCP/CLS hits on mobile. ([iD01t Productions][1])
  **Fix**: WebP/AVIF responsive assets, lazy-load below-the-fold, set explicit width/height and `aspect-ratio`.
  **AC**: Lighthouse LCP ≤ 2.5s on 4G throttling; CLS < 0.1; total page weight reduced ≥ 40%.

8. **Accessibility**

* Potential color-contrast issues for muted text, duplicated nav harming semantics, and missing landmark roles. ([iD01t Productions][1])
  **Fix**: Run axe-core checks; add roles/labels, ensure 4.5:1 contrast; keyboard focus rings; skip-to-content link.
  **AC**: axe violations = 0 critical/serious; WCAG 2.1 AA pass on core flows.

9. **Analytics, consent, and event tracking**

* No clear GA4/alternative analytics and consent banner observed; no purchase/download conversion funnel instrumentation described on-page. ([iD01t Productions][1])
  **Fix**: Add privacy-preserving analytics, consent UI, and custom events (CTA clicks, outbound store clicks, purchase completes).
  **AC**: Dashboard shows conversions by channel; consent state respected.

---

## Minor (Quality polish / ongoing)

10. **Content repetition & placeholder text**

* Repeated “DJ iD01t New Album Available Now!” and generic “Discover More” sections look boilerplate; weak for SEO. ([iD01t Productions][1])
  **Fix**: Replace with targeted, keyword-rich copy and deep links (YouTube/Spotify/itch posts).
  **AC**: No placeholder sections remain; all CTAs are unique and specific.

11. **Footer legal & policies**

* Footer lists policies, but ensure links point to **actual** policy pages with up-to-date content and correct domains. ([iD01t Productions][1])
  **AC**: All legal links resolve; last-updated dates included; domain-appropriate.

12. **Social proof & cross-surface cohesion**

* You have active social & itch presence; mirror highlights to site (releases, betas, testers callouts) via a “News” block. ([youtube.com][3])
  **AC**: Home includes a Recent Updates module (3–5 items) auto-fed from a JSON feed.

---

## Quick Wins (1–3 days)

* Deduplicate header/footer & hero; centralize as includes. ([iD01t Productions][1])
* Add `<link rel="canonical">` to all pages.
* Ship `sitemap.xml` + `robots.txt`.
* Convert hero images to **WebP** + `loading="lazy"` for non-hero images.
* Add OG/Twitter tags with real titles/descriptions per page.
* Insert Accessibility basics: `role="navigation"`, `aria-label`, skip link, visible focus.

---

## 2-Week Sprint Plan (Implementation AC included)

**Sprint Goal:** Information Architecture + SEO/Perf/A11y Baseline

1. **Unified Layout & Components**

   * Shared `header.html`, `footer.html`, `hero.html`, `product-card.html`.
   * **AC**: No duplicate nav; one source of truth; build uses includes.

2. **SEO & Metadata**

   * Per-page unique `<title>`, `<meta>`; OG/Twitter; canonical; sitemap/robots.
   * **AC**: Rich Results Test passes for product pages; coverage in GSC sitemaps.

3. **Performance**

   * WebP/AVIF pipeline; responsive `<picture>`; width/height on `<img>`; defer non-critical JS.
   * **AC**: Lighthouse ≥ 95 mobile/desktop on home + top product pages.

4. **Accessibility**

   * Axe-core CI; roles/labels; contrast fixes; keyboard traversal.
   * **AC**: 0 critical/serious violations; WCAG AA checks pass.

5. **Cross-Domain Routing**

   * Clear “browse vs. buy” flow; canonical ownership per page.
   * **AC**: Games catalog browsed on `.github.io`; purchase flows on `.store`.

---

## Roadmap (60–90 days)

* **Phase 2:** EN/FR i18n infra + content parity; launch language switcher; `hreflang`.
* **Phase 3:** Catalog automation — `upgrade_all_landing_pages.py` v2 to read a JSON manifest and generate per-item pages with schema & images.
* **Phase 4:** Store hardening — event tracking, email receipts, license delivery; SEO landing pages per app/book/music.
* **Phase 5:** Blog/News feed with social ingestion (YouTube/itch/Instagram). ([youtube.com][3])

---

## Implementation Notes (starter snippets)

**Canonical + OG/Twitter (template head):**

```html
<link rel="canonical" href="https://id01t.github.io/path/to/page" />
<meta property="og:title" content="Last Broadcast – Indie Horror Game" />
<meta property="og:description" content="Psychological horror at WKRX radio." />
<meta property="og:image" content="https://id01t.github.io/assets/cover.jpg" />
<meta name="twitter:card" content="summary_large_image" />
```

**Responsive images:**

```html
<picture>
  <source srcset="/assets/cover@2x.avif 2x, /assets/cover.avif 1x" type="image/avif">
  <source srcset="/assets/cover@2x.webp 2x, /assets/cover.webp 1x" type="image/webp">
  <img src="/assets/cover.jpg" width="1280" height="720" alt="Last Broadcast cover">
</picture>
```

**Skip link & landmarks:**

```html
<a class="skip-link" href="#main">Skip to content</a>
<nav aria-label="Primary"></nav>
<main id="main" tabindex="-1"></main>
```

---

Do Now

1. **Sprint Plan.md** for the tonight full upgrade baseline sprint above.
2. **Create shared layout includes** (header/footer/hero), wire into both sites.
3. **Add sitemap/robots, canonical, OG/Twitter**, and a **WebP pipeline**.
4. **Run Lighthouse + axe** and deliver a **before/after QA.md**.

Tell me which you prefer, and I’ll execute it end-to-end.

[1]: https://id01t.github.io/?utm_source=chatgpt.com "iD01t Productions — Apps, eBooks, Games & Music"
[2]: https://id01t.github.io/games.html?utm_source=chatgpt.com "Online Games - iD01t Productions"
[3]: https://www.youtube.com/%40djid01t?utm_source=chatgpt.com "DJ iD01T"
[4]: https://play.google.com/store/books/details/Guillaume_Lessard_iD01t_Academy_Python_Exercises_B?id=BqR_EQAAQBAJ&utm_source=chatgpt.com "iD01t Academy: Python Exercises Book 3: Building Real ..."
