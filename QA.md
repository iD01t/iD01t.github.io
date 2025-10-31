# QA.md — Quality Assurance Test Plan
# iD01t Productions Website v2.0.0

**Date:** October 30, 2025
**Version:** 2.0.0
**QA Engineer:** Claude (iD01t Web Ecosystem Agent)
**Status:** Ready for Testing

---

## Executive Summary

This document outlines the comprehensive quality assurance testing plan for the iD01t Productions website upgrade to version 2.0.0. All tests must pass before deployment to production.

**Quality Standard:** 10/10 Production-Ready

**Testing Scope:**
- Functional Testing
- SEO Validation
- Performance Testing
- Accessibility Compliance
- Cross-Browser Compatibility
- Mobile Responsiveness
- Internationalization (EN/FR)
- Security & Privacy

---

## Pre-Deployment Checklist

### Critical Tests (Must Pass 100%)

- [ ] All HTML files validate with W3C HTML Validator
- [ ] sitemap.xml validates and includes all pages
- [ ] robots.txt syntax is correct
- [ ] All canonical links are present and correct
- [ ] No duplicate navigation elements
- [ ] No duplicate hero CTA blocks
- [ ] All meta tags are unique per page
- [ ] Lighthouse Performance ≥ 95
- [ ] Lighthouse Accessibility ≥ 95
- [ ] Lighthouse Best Practices ≥ 95
- [ ] Lighthouse SEO ≥ 95
- [ ] Zero critical accessibility violations (axe)
- [ ] All images have alt text
- [ ] All images have width/height attributes
- [ ] Color contrast meets WCAG 2.1 AA (4.5:1 minimum)
- [ ] Keyboard navigation works on all pages
- [ ] Language switcher functions correctly
- [ ] Theme toggle (dark/light) works
- [ ] Mobile menu works on all screen sizes
- [ ] No JavaScript errors in console
- [ ] No broken links (internal or external)
- [ ] Cookie consent banner displays and functions
- [ ] All forms validate properly

---

## Test Plan by Category

### 1. HTML Validation

**Objective:** Ensure all HTML is valid and follows standards

**Tools:**
- W3C HTML Validator (https://validator.w3.org/)
- Nu HTML Checker

**Test Cases:**

#### TC-001: Homepage Validation
**Steps:**
1. Navigate to https://validator.w3.org/
2. Enter URL: https://id01t.github.io/
3. Click "Check"

**Expected:** Zero errors, zero warnings
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-002: All Major Pages Validation
**Pages to Test:**
- /index.html
- /store.html
- /apps.html
- /games.html
- /ebooks.html
- /audiobooks.html
- /music.html
- /blog.html
- /about.html
- /contact.html

**Expected:** Each page validates with zero errors
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

---

### 2. SEO Validation

**Objective:** Ensure complete SEO implementation

**Tools:**
- Google Rich Results Test
- Schema.org Validator
- Screaming Frog SEO Spider (optional)

**Test Cases:**

#### TC-010: Canonical Links
**Steps:**
1. View source of each major page
2. Verify `<link rel="canonical">` is present
3. Verify canonical URL uses correct domain

**Expected:** All pages have canonical links
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-011: Unique Meta Tags
**Steps:**
1. Check each page's `<title>` tag
2. Check each page's `<meta name="description">` tag
3. Verify no two pages share identical values

**Expected:** All titles and descriptions are unique
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-012: Structured Data (JSON-LD)
**Steps:**
1. Navigate to https://search.google.com/test/rich-results
2. Enter homepage URL
3. Check for Organization and WebSite schema

**Expected:** Valid structured data detected
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-013: Open Graph Tags
**Steps:**
1. Check homepage for og:title, og:description, og:image, og:url, og:type
2. Verify values are appropriate

**Expected:** All OG tags present and accurate
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-014: Twitter Card Tags
**Steps:**
1. Check homepage for twitter:card, twitter:title, twitter:description, twitter:image
2. Verify values match OG tags

**Expected:** All Twitter Card tags present
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-015: Sitemap Validation
**Steps:**
1. Navigate to https://www.xml-sitemaps.com/validate-xml-sitemap.html
2. Enter sitemap URL: https://id01t.github.io/sitemap.xml
3. Verify validation passes

**Expected:** Sitemap is valid, 428 URLs present
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-016: Robots.txt Validation
**Steps:**
1. Navigate to https://id01t.github.io/robots.txt
2. Verify syntax is correct
3. Verify sitemap reference is present

**Expected:** Valid robots.txt with sitemap reference
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

---

### 3. Performance Testing

**Objective:** Achieve Lighthouse scores ≥ 95

**Tools:**
- Google Lighthouse (Chrome DevTools)
- PageSpeed Insights
- WebPageTest (optional)

**Test Cases:**

#### TC-020: Homepage Lighthouse (Desktop)
**Steps:**
1. Open Chrome DevTools
2. Navigate to Lighthouse tab
3. Select "Desktop" mode
4. Run audit

**Expected:**
- Performance: ≥ 95
- Accessibility: ≥ 95
- Best Practices: ≥ 95
- SEO: ≥ 95

**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-021: Homepage Lighthouse (Mobile)
**Steps:**
1. Open Chrome DevTools
2. Navigate to Lighthouse tab
3. Select "Mobile" mode
4. Run audit

**Expected:**
- Performance: ≥ 95
- Accessibility: ≥ 95
- Best Practices: ≥ 95
- SEO: ≥ 95

**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-022: Core Web Vitals
**Steps:**
1. Run Lighthouse on homepage
2. Check Core Web Vitals

**Expected:**
- LCP (Largest Contentful Paint): < 2.5s
- FID (First Input Delay): < 100ms
- CLS (Cumulative Layout Shift): < 0.1

**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-023: Image Optimization
**Steps:**
1. Check Network tab in DevTools
2. Verify all images use WebP format (where supported)
3. Verify all images have width/height attributes
4. Verify lazy loading on below-the-fold images

**Expected:** All optimizations implemented
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

---

### 4. Accessibility Testing

**Objective:** Achieve WCAG 2.1 AA compliance

**Tools:**
- axe DevTools (Chrome Extension)
- WAVE (Web Accessibility Evaluation Tool)
- Keyboard navigation (manual)
- Screen reader testing (optional - NVDA/JAWS)

**Test Cases:**

#### TC-030: axe DevTools Scan
**Steps:**
1. Install axe DevTools extension
2. Navigate to homepage
3. Run "Scan ALL of my page"
4. Review violations

**Expected:** 0 critical, 0 serious violations
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-031: WAVE Scan
**Steps:**
1. Navigate to https://wave.webaim.org/
2. Enter homepage URL
3. Review errors and alerts

**Expected:** 0 errors
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-032: Color Contrast
**Steps:**
1. Use axe or WAVE to check color contrast
2. Verify all text meets 4.5:1 ratio (normal text)
3. Verify all text meets 3:1 ratio (large text ≥18px)

**Expected:** All contrast ratios pass WCAG AA
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-033: Keyboard Navigation
**Steps:**
1. Navigate homepage using only keyboard (Tab, Shift+Tab, Enter, Space)
2. Verify all interactive elements are reachable
3. Verify focus indicators are visible
4. Verify skip-to-content link works

**Expected:** Full keyboard accessibility
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-034: ARIA Roles and Labels
**Steps:**
1. View source of homepage
2. Verify `role="navigation"`, `role="main"`, `role="contentinfo"` are present
3. Verify aria-label on navigation elements

**Expected:** All required ARIA attributes present
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-035: Alt Text on Images
**Steps:**
1. View source or use axe DevTools
2. Verify all images have alt attributes
3. Verify alt text is descriptive

**Expected:** All images have meaningful alt text
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

---

### 5. Functional Testing

**Objective:** Ensure all features work as expected

**Test Cases:**

#### TC-040: Navigation Links
**Steps:**
1. Click each navigation link in header
2. Verify correct page loads
3. Verify active page is highlighted

**Expected:** All navigation works, no 404 errors
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-041: Mobile Menu
**Steps:**
1. Resize browser to mobile width (< 768px)
2. Click hamburger menu icon
3. Verify menu opens
4. Click menu items
5. Close menu with X icon

**Expected:** Mobile menu functions properly
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-042: Theme Toggle
**Steps:**
1. Click theme toggle button
2. Verify dark mode activates
3. Click again
4. Verify light mode activates
5. Refresh page
6. Verify theme persists

**Expected:** Theme toggle works and persists
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-043: Language Switcher
**Steps:**
1. Click EN button
2. Verify language is English
3. Click FR button
4. Verify language changes to French
5. Refresh page
6. Verify language persists

**Expected:** Language switcher works and persists
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-044: Newsletter Form
**Steps:**
1. Scroll to newsletter section
2. Enter valid email
3. Click Subscribe
4. Verify success message

**Expected:** Form submits successfully
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-045: Cookie Consent Banner
**Steps:**
1. Clear localStorage
2. Refresh page
3. Verify consent banner appears
4. Click "Accept All"
5. Verify banner disappears
6. Verify consent saved to localStorage

**Expected:** Consent banner works properly
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-046: Consent Customization
**Steps:**
1. Reset consent
2. Click "Customize"
3. Toggle analytics/marketing checkboxes
4. Click "Save Preferences"
5. Verify preferences saved

**Expected:** Customization works
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

---

### 6. Cross-Browser Testing

**Objective:** Ensure compatibility across major browsers

**Browsers to Test:**
- Google Chrome (latest)
- Mozilla Firefox (latest)
- Microsoft Edge (latest)
- Safari (latest) - if available

**Test Cases:**

#### TC-050: Chrome Compatibility
**Steps:**
1. Open site in Chrome
2. Test all major features
3. Check for JavaScript errors

**Expected:** Site works perfectly in Chrome
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-051: Firefox Compatibility
**Steps:**
1. Open site in Firefox
2. Test all major features
3. Check for JavaScript errors

**Expected:** Site works perfectly in Firefox
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-052: Edge Compatibility
**Steps:**
1. Open site in Edge
2. Test all major features
3. Check for JavaScript errors

**Expected:** Site works perfectly in Edge
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-053: Safari Compatibility (Optional)
**Steps:**
1. Open site in Safari
2. Test all major features
3. Check for JavaScript errors

**Expected:** Site works perfectly in Safari
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

---

### 7. Mobile Responsiveness

**Objective:** Ensure perfect mobile experience

**Test Cases:**

#### TC-060: Mobile Layout (375px)
**Steps:**
1. Set viewport to 375px width (iPhone SE)
2. Scroll through entire page
3. Verify no horizontal scroll
4. Verify content is readable
5. Verify buttons are tappable (≥ 44x44px)

**Expected:** Perfect mobile layout
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-061: Tablet Layout (768px)
**Steps:**
1. Set viewport to 768px width (iPad)
2. Verify layout adapts properly
3. Test navigation

**Expected:** Tablet layout works properly
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-062: Desktop Layout (1280px+)
**Steps:**
1. Set viewport to 1280px+ width
2. Verify full desktop layout displays
3. Verify max-width container works

**Expected:** Desktop layout optimized
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-063: Touch Interactions
**Steps:**
1. Test on actual mobile device (if available)
2. Test touch gestures
3. Verify no hover-only interactions

**Expected:** All interactions work on touch
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

---

### 8. Internationalization (EN/FR)

**Objective:** Verify bilingual support works

**Test Cases:**

#### TC-070: English Content
**Steps:**
1. Set language to EN
2. Verify all UI strings are in English
3. Verify no broken translations

**Expected:** All English content displays correctly
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-071: French Content
**Steps:**
1. Set language to FR
2. Verify all UI strings are in French
3. Verify translations are accurate
4. Verify no English fallbacks

**Expected:** All French content displays correctly
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-072: Hreflang Tags
**Steps:**
1. View source of homepage
2. Verify hreflang tags for en and fr are present
3. Verify URLs are correct

**Expected:** Hreflang tags properly implemented
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

---

### 9. Security & Privacy

**Objective:** Ensure secure and privacy-compliant site

**Test Cases:**

#### TC-080: HTTPS
**Steps:**
1. Navigate to site
2. Verify URL starts with https://
3. Verify valid SSL certificate

**Expected:** Site uses HTTPS
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-081: No Mixed Content
**Steps:**
1. Open DevTools Console
2. Check for mixed content warnings
3. Verify all resources load over HTTPS

**Expected:** No mixed content warnings
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-082: Privacy Policy Link
**Steps:**
1. Verify privacy policy link in footer
2. Click link
3. Verify policy page loads

**Expected:** Privacy policy accessible
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-083: Cookie Consent Compliance
**Steps:**
1. Verify consent banner shows on first visit
2. Verify user can reject cookies
3. Verify consent choice is respected

**Expected:** GDPR/CCPA compliant consent
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

---

### 10. Link Validation

**Objective:** Ensure no broken links

**Tools:**
- W3C Link Checker
- Broken Link Checker (browser extension)

**Test Cases:**

#### TC-090: Internal Links
**Steps:**
1. Run link checker on homepage
2. Verify all internal links return 200
3. Fix any broken links

**Expected:** Zero broken internal links
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

#### TC-091: External Links
**Steps:**
1. Check all external links (GitHub, YouTube, Spotify, etc.)
2. Verify they open in new tab (target="_blank")
3. Verify rel="noopener noreferrer" is present

**Expected:** All external links work and are secure
**Actual:** (To be filled during testing)
**Status:** ⬜ PASS / ⬜ FAIL

---

## Regression Testing

**After any fixes, re-run the following:**
- HTML Validation
- Lighthouse Audit
- Accessibility Scan
- Key functionality tests

---

## Performance Benchmarks

**Target Metrics:**

| Metric | Target | Measured | Status |
|--------|--------|----------|--------|
| Lighthouse Performance (Mobile) | ≥ 95 | ___ | ⬜ |
| Lighthouse Performance (Desktop) | ≥ 95 | ___ | ⬜ |
| Lighthouse Accessibility | ≥ 95 | ___ | ⬜ |
| Lighthouse Best Practices | ≥ 95 | ___ | ⬜ |
| Lighthouse SEO | ≥ 95 | ___ | ⬜ |
| LCP (Largest Contentful Paint) | < 2.5s | ___ | ⬜ |
| FID (First Input Delay) | < 100ms | ___ | ⬜ |
| CLS (Cumulative Layout Shift) | < 0.1 | ___ | ⬜ |
| Total Page Size | < 1MB | ___ | ⬜ |
| Total Requests | < 30 | ___ | ⬜ |

---

## Issues Tracker

**Critical Issues:**
_(To be filled during testing)_

**Major Issues:**
_(To be filled during testing)_

**Minor Issues:**
_(To be filled during testing)_

**Fixed Issues:**
_(To be filled during testing)_

---

## Sign-Off

**QA Lead:** ___________________________ Date: __________

**Development Lead:** ___________________________ Date: __________

**Project Manager:** ___________________________ Date: __________

---

## Deployment Approval

- [ ] All critical tests passed
- [ ] All major tests passed
- [ ] Minor issues documented (if any)
- [ ] Performance targets met
- [ ] Accessibility compliance verified
- [ ] Cross-browser testing complete
- [ ] Mobile responsiveness verified
- [ ] SEO validation complete
- [ ] Security checklist complete
- [ ] Stakeholder approval obtained

**Approved for Production:** ⬜ YES / ⬜ NO

**Deployment Date:** _________________________

**Deployed By:** _________________________

---

**Notes:**
- This QA document should be filled out during actual testing
- All tests must pass before production deployment
- Any failures must be documented with screenshots/recordings
- Retest after all fixes are implemented
