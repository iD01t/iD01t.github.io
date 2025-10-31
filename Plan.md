# Plan.md — iD01t Productions Website Upgrade v2.0.0

**Project:** Full Website Upgrade for id01t.github.io
**Version:** 2.0.0
**Date:** October 30, 2025
**Status:** In Progress
**Quality Standard:** 10/10 Production-Ready

---

## Executive Summary

This plan outlines a comprehensive upgrade to address critical issues identified in findings.md, implementing professional-grade fixes for SEO, performance, accessibility, internationalization, and design consistency. The upgrade transforms the site from a functional catalog to a production-ready, enterprise-quality digital presence.

**Primary Goals:**
- Eliminate all duplicate content and navigation
- Achieve Lighthouse score ≥ 95 on all metrics
- Implement full EN/FR bilingual support
- Establish consistent design system
- Meet WCAG 2.1 AA accessibility standards
- Deploy professional SEO and structured data

---

## Scope

### In Scope

**Critical (Priority 1) - Must Fix:**
1. Navigation deduplication (single shared header/footer)
2. Cross-domain canonical links and routing clarity
3. Complete SEO meta tags and structured data
4. Sitemap.xml and robots.txt generation
5. Remove duplicate hero CTA blocks

**Major (Priority 2) - High Value:**
6. Internationalization (EN/FR) with language switcher
7. Design system documentation and implementation
8. Performance optimization (images, lazy loading)
9. Accessibility compliance (WCAG 2.1 AA)
10. Analytics and consent management

**Deliverables:**
- Plan.md (this document)
- DesignSystem.md
- Shared components (header.html, footer.html, hero.html)
- Updated HTML files (all pages)
- sitemap.xml
- robots.txt
- i18n structure (/locales/en/, /locales/fr/)
- Updated CSS with design tokens
- QA.md
- Release.md (v2.0.0 EN/FR)

### Out of Scope
- Backend ecommerce implementation (planned for v2.1.0)
- Blog content creation
- Social media integration beyond meta tags
- Email marketing automation
- Payment processing

---

## Timeline

**Total Duration:** 2-3 days (Intensive Sprint)

### Phase 1: Foundation (Day 1 Morning)
- ✅ Create Plan.md
- Create DesignSystem.md
- Create shared header/footer components
- Establish CSS design system

### Phase 2: Content & SEO (Day 1 Afternoon)
- Remove duplicate navigation/content
- Add canonical links to all pages
- Implement unique meta tags
- Add structured data (JSON-LD)
- Generate sitemap.xml and robots.txt

### Phase 3: Internationalization (Day 2 Morning)
- Create i18n JSON structure
- Add language switcher UI
- Implement hreflang tags
- Ensure EN/FR content parity

### Phase 4: Accessibility & Performance (Day 2 Afternoon)
- Add skip-to-content links
- Implement ARIA roles and labels
- Add keyboard focus indicators
- Optimize images (WebP conversion instructions)
- Add lazy loading

### Phase 5: Polish & Testing (Day 3)
- Analytics and consent banner setup
- Cross-browser testing
- Accessibility validation
- SEO validation
- Create QA.md
- Create Release.md
- Final review

---

## Objectives & Success Criteria

### 1. Navigation Deduplication
**Objective:** Single source of truth for header/footer across all pages

**Implementation:**
- Create `/includes/header.html` with complete navigation
- Create `/includes/footer.html` with footer content
- Create `/includes/hero-cta.html` for reusable CTAs
- Update all HTML files to reference shared components (or use consistent structure)

**Acceptance Criteria:**
- [ ] No page contains duplicate navigation sections
- [ ] No page contains duplicate hero CTA blocks
- [ ] All pages use identical navigation structure
- [ ] Footer is consistent across all pages

### 2. Cross-Domain Consistency
**Objective:** Clear canonical URLs and routing strategy

**Implementation:**
- Add `<link rel="canonical">` to every page
- Define clear routing: catalog on .github.io, purchases on .store
- Add cross-domain navigation links where appropriate

**Acceptance Criteria:**
- [ ] Every HTML file has canonical link
- [ ] Canonical URLs use correct domain (github.io vs store)
- [ ] No mixed domain references in internal links

### 3. SEO & Structured Data
**Objective:** Complete meta tags and rich snippets for all pages

**Implementation:**
- Add unique `<title>` and `<meta name="description">` to each page
- Implement Schema.org JSON-LD:
  - Organization (homepage)
  - WebSite (homepage)
  - Product (store items)
  - SoftwareApplication (apps)
  - Book (ebooks)
  - MusicAlbum (music)
- Complete Open Graph tags (og:title, og:description, og:image, og:url, og:type)
- Complete Twitter Card tags (twitter:card, twitter:title, twitter:description, twitter:image)

**Acceptance Criteria:**
- [ ] Every page has unique title (max 60 chars)
- [ ] Every page has unique meta description (max 155 chars)
- [ ] All pages pass Google Rich Results Test
- [ ] All OG tags present and accurate
- [ ] All Twitter Card tags present and accurate

### 4. Sitemap & Robots
**Objective:** Proper search engine indexing infrastructure

**Implementation:**
- Generate sitemap.xml with all indexable pages
- Create robots.txt with sitemap reference
- Ensure proper lastmod dates
- Set correct priorities (homepage=1.0, category pages=0.8, product pages=0.6)

**Acceptance Criteria:**
- [ ] sitemap.xml validates at https://www.xml-sitemaps.com/validate-xml-sitemap.html
- [ ] robots.txt follows proper syntax
- [ ] All important pages included in sitemap
- [ ] sitemap.xml referenced in robots.txt

### 5. Internationalization (EN/FR)
**Objective:** Full bilingual support with language switcher

**Implementation:**
- Create `/locales/en/common.json` with English translations
- Create `/locales/fr/common.json` with French translations
- Add language switcher to header (flag icons or text)
- Implement `<link rel="alternate" hreflang="en">` and `hreflang="fr"` tags
- Ensure EN/FR content parity on key pages (home, about, contact)

**Acceptance Criteria:**
- [ ] Language switcher visible on all pages
- [ ] All UI strings available in EN/FR
- [ ] hreflang tags present on all pages
- [ ] No broken translations or missing strings

### 6. Design System
**Objective:** Documented, consistent design tokens across all pages

**Implementation:**
- Create DesignSystem.md with:
  - Color palette (primary, secondary, accent, neutrals)
  - Typography scale (headings, body, small)
  - Spacing system (margins, padding, gaps)
  - Component patterns (buttons, cards, forms)
- Create CSS with CSS custom properties
- Ensure all pages use design tokens

**Acceptance Criteria:**
- [ ] DesignSystem.md is comprehensive and actionable
- [ ] CSS uses consistent variables
- [ ] No hardcoded colors/sizes in HTML
- [ ] Visual consistency across all pages

### 7. Performance Optimization
**Objective:** Lighthouse Performance score ≥ 95

**Implementation:**
- Convert hero images to WebP format (provide conversion instructions)
- Add `<picture>` elements for responsive images
- Add `width` and `height` attributes to all images
- Implement `loading="lazy"` for below-the-fold images
- Defer non-critical JavaScript
- Minimize CSS and inline critical styles

**Acceptance Criteria:**
- [ ] Lighthouse Performance ≥ 95 (mobile & desktop)
- [ ] LCP (Largest Contentful Paint) < 2.5s
- [ ] CLS (Cumulative Layout Shift) < 0.1
- [ ] FID (First Input Delay) < 100ms
- [ ] All images have width/height
- [ ] All images use modern formats (WebP)

### 8. Accessibility (WCAG 2.1 AA)
**Objective:** Fully accessible site for all users

**Implementation:**
- Add skip-to-content link at top of every page
- Add `role="navigation"`, `role="main"`, `role="contentinfo"`
- Add `aria-label` to all navigation elements
- Ensure color contrast ratio ≥ 4.5:1
- Add visible keyboard focus indicators
- Use semantic HTML5 elements
- Add alt text to all images

**Acceptance Criteria:**
- [ ] axe-core violations = 0 critical/serious
- [ ] WAVE tool shows no errors
- [ ] Keyboard navigation works on all pages
- [ ] Screen reader compatible
- [ ] Color contrast meets WCAG AA

### 9. Analytics & Consent
**Objective:** Privacy-friendly analytics with user consent

**Implementation:**
- Add Google Analytics 4 or Plausible Analytics setup
- Create consent banner (cookie notice)
- Add event tracking for key actions:
  - CTA clicks
  - Outbound store links
  - Newsletter sign-ups
  - Download initiations

**Acceptance Criteria:**
- [ ] Analytics tracking code present
- [ ] Consent banner displays on first visit
- [ ] User choice is respected (localStorage)
- [ ] Key events are tracked
- [ ] Privacy policy updated with analytics info

---

## Risk Mitigation

### Risk 1: Breaking Existing Functionality
**Mitigation:**
- Test all changes in local environment first
- Create backups before major changes
- Implement changes incrementally
- Validate HTML structure after each change

### Risk 2: Inconsistent Updates Across Files
**Mitigation:**
- Use shared components where possible
- Create checklist for each file type
- Use search/replace for bulk updates
- Final validation pass on all pages

### Risk 3: Performance Degradation
**Mitigation:**
- Test Lighthouse scores before and after
- Monitor page load times
- Optimize images before deployment
- Use lazy loading strategically

### Risk 4: SEO Impact During Transition
**Mitigation:**
- Keep all existing URLs intact
- Add canonical links immediately
- Submit updated sitemap to Google Search Console
- Monitor search rankings post-deployment

### Risk 5: Translation Quality
**Mitigation:**
- Use professional-quality French translations
- Review all translations for accuracy
- Test language switcher thoroughly
- Ensure no broken language references

---

## Dependencies

**Required Before Start:**
- Access to repository: C:\Users\Admin\Desktop\iD01t.github.io-main
- Findings.md and iD01tWebAgent.md reviewed
- Understanding of current site structure

**Required During Implementation:**
- Text editor (VS Code or similar)
- Browser for testing (Chrome/Firefox)
- Lighthouse tool
- axe DevTools browser extension
- HTML/CSS validation tools

**Optional But Recommended:**
- Image optimization tool (for WebP conversion)
- JSON-LD validator
- Schema.org validator
- Google Rich Results Test

---

## Implementation Strategy

### Approach
**Modular & Incremental:** Make changes in logical groups, test frequently, and validate continuously.

**Quality Over Speed:** Every change must meet the 10/10 production standard before moving to the next task.

**Documentation First:** Create documentation (Plan.md, DesignSystem.md) before implementation to ensure clarity.

### File Organization
```
iD01t.github.io-main/
├── index.html (homepage)
├── apps.html
├── games.html
├── ebooks.html
├── audiobooks.html
├── music.html
├── blog.html
├── about.html
├── contact.html
├── store.html
├── includes/ (NEW)
│   ├── header.html
│   ├── footer.html
│   └── hero-cta.html
├── locales/ (NEW)
│   ├── en/
│   │   └── common.json
│   └── fr/
│       └── common.json
├── css/
│   ├── site.css (updated with design tokens)
│   └── design-system.css (NEW)
├── legal/
│   ├── privacy.html
│   ├── terms.html
│   ├── refunds.html
│   └── cookies.html
├── sitemap.xml (NEW)
├── robots.txt (NEW)
├── Plan.md (this file)
├── DesignSystem.md (NEW)
├── QA.md (NEW)
└── Release.md (NEW)
```

### Code Quality Standards
- Clean, readable code
- Proper indentation (2 spaces)
- Comments for complex sections
- No broken links
- No duplicate content
- Consistent formatting
- Semantic HTML5
- Accessible markup
- Valid HTML/CSS

---

## Testing Requirements

### Pre-Deployment Validation

**HTML Validation:**
- [ ] All pages pass https://validator.w3.org/

**SEO Validation:**
- [ ] All pages pass Google Rich Results Test
- [ ] sitemap.xml validates
- [ ] robots.txt syntax correct

**Accessibility Testing:**
- [ ] axe DevTools: 0 critical/serious violations
- [ ] WAVE: 0 errors
- [ ] Keyboard navigation works
- [ ] Screen reader compatible

**Performance Testing:**
- [ ] Lighthouse Performance ≥ 95
- [ ] Lighthouse Accessibility ≥ 95
- [ ] Lighthouse Best Practices ≥ 95
- [ ] Lighthouse SEO ≥ 95

**Cross-Browser Testing:**
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Edge (latest)
- [ ] Safari (if available)

**Mobile Testing:**
- [ ] Responsive on mobile (375px width)
- [ ] Touch targets ≥ 44x44px
- [ ] No horizontal scroll
- [ ] Mobile-friendly test passes

**Internationalization Testing:**
- [ ] Language switcher works
- [ ] EN/FR content displays correctly
- [ ] No broken translations
- [ ] hreflang tags correct

---

## Success Metrics

**Technical Metrics:**
- Lighthouse Performance: ≥ 95
- Lighthouse Accessibility: ≥ 95
- Lighthouse SEO: ≥ 95
- HTML Validation: 0 errors
- Accessibility Violations: 0 critical/serious

**SEO Metrics:**
- All pages have unique titles/descriptions
- All pages have canonical links
- Structured data present on appropriate pages
- sitemap.xml and robots.txt live

**Consistency Metrics:**
- 0 duplicate navigation sections
- 0 duplicate hero CTA blocks
- 100% design system compliance
- EN/FR parity on core pages

**User Experience Metrics:**
- Page load time < 2s (on 4G)
- CLS < 0.1
- All interactive elements accessible via keyboard
- Color contrast ≥ 4.5:1

---

## Post-Deployment

### Immediate Actions
1. Submit sitemap.xml to Google Search Console
2. Monitor analytics for traffic patterns
3. Check for broken links using external tool
4. Verify all pages render correctly
5. Test language switcher on live site

### Week 1 Monitoring
- Monitor Lighthouse scores
- Check for JavaScript errors
- Review analytics data
- Gather user feedback
- Monitor search rankings

### Month 1 Review
- Analyze traffic trends
- Review conversion metrics
- Identify optimization opportunities
- Plan v2.1.0 features

---

## Next Steps After v2.0.0

**v2.1.0 (Planned):**
- Blog content creation
- Enhanced analytics events
- A/B testing framework
- Email marketing integration

**v2.2.0 (Planned):**
- Backend ecommerce integration
- User accounts and authentication
- Shopping cart implementation
- Payment processing

**v3.0.0 (Vision):**
- Progressive Web App (PWA)
- Offline support
- Advanced personalization
- AI-powered recommendations

---

## Approval & Sign-Off

**Prepared By:** Claude (iD01t Web Ecosystem Agent)
**Date:** October 30, 2025
**Status:** Ready for Implementation

**Acceptance Criteria for Plan Approval:**
- [ ] All sections complete and detailed
- [ ] Timeline realistic and achievable
- [ ] Success criteria measurable
- [ ] Risks identified and mitigated
- [ ] Dependencies documented
- [ ] Testing strategy comprehensive

---

**Note:** This plan is a living document and may be updated as implementation progresses. All changes will be tracked and documented in Release.md.
