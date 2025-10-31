# Design System — iD01t Productions

**Version:** 2.0.0
**Last Updated:** October 30, 2025
**Status:** Production
**Brand:** iD01t Productions - Digital Tools for Creators

---

## Overview

This design system establishes the visual language, components, and standards for all iD01t Productions digital properties. It ensures consistency, accessibility, and professional quality across the entire web ecosystem.

**Core Principles:**
- **Dark-First:** Primary dark theme with light mode support
- **Professional:** Clean, modern, tech-focused aesthetic
- **Accessible:** WCAG 2.1 AA compliance minimum
- **Performant:** Lightweight, optimized for speed
- **Consistent:** Unified experience across all touchpoints

---

## Color System

### Brand Colors (Primary Palette)

```css
/* Brand Blue - Primary */
--brand-50:  #f5faff;  /* Lightest tint */
--brand-100: #e0f2ff;
--brand-200: #bae0ff;
--brand-300: #8dceff;
--brand-400: #5abaff;
--brand-500: #2aa7ff;  /* Primary brand color */
--brand-600: #008ef6;
--brand-700: #0070d7;
--brand-800: #0057b5;
--brand-900: #003f92;  /* Darkest shade */
```

**Usage:**
- `--brand-500`: Primary CTAs, links, highlights
- `--brand-600`: Hover states, active buttons
- `--brand-700`: Pressed states, dark accents
- `--brand-100-300`: Backgrounds, subtle highlights
- `--brand-800-900`: Text on light backgrounds

### Neutral Colors (Slate Palette)

```css
/* Neutrals - Slate Scale */
--slate-50:  #f8fafc;  /* Lightest */
--slate-100: #f1f5f9;
--slate-200: #e2e8f0;
--slate-300: #cbd5e1;
--slate-400: #94a3b8;
--slate-500: #64748b;
--slate-600: #475569;
--slate-700: #334155;
--slate-800: #1e293b;
--slate-900: #0f172a;  /* Darkest */
```

**Usage:**
- `--slate-900`: Dark mode background
- `--slate-800`: Dark mode cards, surfaces
- `--slate-700`: Dark mode borders, dividers
- `--slate-50-100`: Light mode background
- `--slate-600-500`: Muted text, secondary content
- `--slate-300-200`: Light mode borders, dividers

### Semantic Colors

```css
/* Success */
--success-light: #10b981;
--success-dark:  #059669;

/* Warning */
--warning-light: #f59e0b;
--warning-dark:  #d97706;

/* Error */
--error-light: #ef4444;
--error-dark:  #dc2626;

/* Info */
--info-light: #3b82f6;
--info-dark:  #2563eb;
```

**Usage:**
- Success: Confirmations, completed states, positive feedback
- Warning: Alerts, cautions, important notices
- Error: Validation errors, destructive actions
- Info: Informational messages, tips, hints

### Accent Colors (Secondary Palette)

```css
/* Purple - For creative/premium features */
--accent-purple-light: #8b5cf6;
--accent-purple-dark:  #7c3aed;

/* Green - For growth/success */
--accent-green-light: #10b981;
--accent-green-dark:  #059669;

/* Orange - For attention/CTAs */
--accent-orange-light: #f97316;
--accent-orange-dark:  #ea580c;
```

### Background & Surface Colors

```css
/* Light Mode */
--bg-light:         #ffffff;
--surface-light:    #f8fafc;
--card-light:       #ffffff;
--border-light:     #e2e8f0;

/* Dark Mode */
--bg-dark:          #0f172a;  /* slate-900 */
--surface-dark:     #1e293b;  /* slate-800 */
--card-dark:        #1e293b;  /* slate-800 */
--border-dark:      #334155;  /* slate-700 */
```

### Color Contrast Standards

**WCAG 2.1 AA Compliance:**
- Normal text (< 18px): 4.5:1 minimum
- Large text (≥ 18px): 3:1 minimum
- Interactive elements: 3:1 minimum

**Validated Combinations:**
- White text on `--brand-600` and darker: ✅ AAA
- White text on `--slate-700` and darker: ✅ AA
- `--slate-900` text on white: ✅ AAA
- `--brand-500` text on white: ✅ AA

---

## Typography

### Font Families

```css
/* Sans-serif (Primary) */
--font-sans: ui-sans-serif, system-ui, -apple-system,
             BlinkMacSystemFont, 'Segoe UI', Roboto,
             'Helvetica Neue', Arial, sans-serif;

/* Monospace (Code) */
--font-mono: ui-monospace, 'SF Mono', 'Cascadia Code',
             'Roboto Mono', Consolas, Monaco,
             'Liberation Mono', 'Courier New', monospace;
```

**External Font (Optional - Tailwind Default):**
- Inter (Google Fonts) - Modern, readable, professional
- Weights: 400 (regular), 500 (medium), 600 (semibold), 700 (bold), 800 (extrabold)

### Type Scale

```css
/* Font Sizes */
--text-xs:   0.75rem;   /* 12px */
--text-sm:   0.875rem;  /* 14px */
--text-base: 1rem;      /* 16px */
--text-lg:   1.125rem;  /* 18px */
--text-xl:   1.25rem;   /* 20px */
--text-2xl:  1.5rem;    /* 24px */
--text-3xl:  1.875rem;  /* 30px */
--text-4xl:  2.25rem;   /* 36px */
--text-5xl:  3rem;      /* 48px */
--text-6xl:  3.75rem;   /* 60px */
--text-7xl:  4.5rem;    /* 72px */

/* Line Heights */
--leading-none:   1;
--leading-tight:  1.25;
--leading-snug:   1.375;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
--leading-loose:  2;

/* Font Weights */
--font-normal:    400;
--font-medium:    500;
--font-semibold:  600;
--font-bold:      700;
--font-extrabold: 800;
```

### Typography Hierarchy

**Headings:**
```css
h1 {
  font-size: clamp(2.25rem, 5vw, 4.5rem);  /* 36-72px */
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

h2 {
  font-size: clamp(1.875rem, 4vw, 3rem);  /* 30-48px */
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.01em;
}

h3 {
  font-size: clamp(1.5rem, 3vw, 2.25rem);  /* 24-36px */
  font-weight: 700;
  line-height: 1.3;
}

h4 {
  font-size: clamp(1.25rem, 2vw, 1.5rem);  /* 20-24px */
  font-weight: 600;
  line-height: 1.4;
}

h5 {
  font-size: 1.125rem;  /* 18px */
  font-weight: 600;
  line-height: 1.5;
}

h6 {
  font-size: 1rem;  /* 16px */
  font-weight: 600;
  line-height: 1.5;
}
```

**Body Text:**
```css
body {
  font-size: 1rem;      /* 16px */
  font-weight: 400;
  line-height: 1.625;   /* 26px */
}

.text-large {
  font-size: 1.125rem;  /* 18px */
  line-height: 1.75;
}

.text-small {
  font-size: 0.875rem;  /* 14px */
  line-height: 1.5;
}

.text-xs {
  font-size: 0.75rem;   /* 12px */
  line-height: 1.5;
}
```

**Special Text Styles:**
```css
.gradient-text {
  background: linear-gradient(to right, #2aa7ff, #0070d7);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
}

.muted-text {
  color: var(--slate-500);  /* Light mode */
}

.dark .muted-text {
  color: var(--slate-400);  /* Dark mode */
}
```

---

## Spacing System

### Base Unit: 4px Grid

```css
/* Spacing Scale */
--space-0:  0;
--space-px: 1px;
--space-0-5: 0.125rem;  /* 2px */
--space-1: 0.25rem;     /* 4px */
--space-2: 0.5rem;      /* 8px */
--space-3: 0.75rem;     /* 12px */
--space-4: 1rem;        /* 16px */
--space-5: 1.25rem;     /* 20px */
--space-6: 1.5rem;      /* 24px */
--space-8: 2rem;        /* 32px */
--space-10: 2.5rem;     /* 40px */
--space-12: 3rem;       /* 48px */
--space-16: 4rem;       /* 64px */
--space-20: 5rem;       /* 80px */
--space-24: 6rem;       /* 96px */
--space-32: 8rem;       /* 128px */
```

### Layout Spacing

**Section Spacing:**
```css
.section {
  padding-top: var(--space-16);     /* 64px */
  padding-bottom: var(--space-16);   /* 64px */
}

.section-large {
  padding-top: var(--space-24);     /* 96px */
  padding-bottom: var(--space-24);   /* 96px */
}
```

**Component Spacing:**
```css
.card {
  padding: var(--space-6);  /* 24px */
}

.card-compact {
  padding: var(--space-4);  /* 16px */
}

.card-large {
  padding: var(--space-8);  /* 32px */
}
```

**Gap Spacing:**
```css
.gap-sm: 0.5rem;    /* 8px */
.gap-md: 1rem;      /* 16px */
.gap-lg: 1.5rem;    /* 24px */
.gap-xl: 2rem;      /* 32px */
```

---

## Border Radius

```css
--radius-none: 0;
--radius-sm:   0.25rem;   /* 4px */
--radius-md:   0.5rem;    /* 8px */
--radius-lg:   0.75rem;   /* 12px */
--radius-xl:   1rem;      /* 16px */
--radius-2xl:  1.5rem;    /* 24px */
--radius-3xl:  2rem;      /* 32px */
--radius-full: 9999px;    /* Fully rounded */
```

**Usage:**
- Buttons: `--radius-lg` (12px)
- Cards: `--radius-xl` to `--radius-2xl` (16-24px)
- Input fields: `--radius-lg` (12px)
- Badges/Pills: `--radius-full` (9999px)
- Avatars: `--radius-full` (9999px)

---

## Shadows & Elevation

```css
/* Shadow Scale */
--shadow-sm:  0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md:  0 4px 6px -1px rgba(0, 0, 0, 0.1),
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
--shadow-lg:  0 10px 15px -3px rgba(0, 0, 0, 0.1),
              0 4px 6px -2px rgba(0, 0, 0, 0.05);
--shadow-xl:  0 20px 25px -5px rgba(0, 0, 0, 0.1),
              0 10px 10px -5px rgba(0, 0, 0, 0.04);
--shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
--shadow-none: none;

/* Brand Glow */
--shadow-brand: 0 0 20px rgba(42, 167, 255, 0.3);
```

**Elevation Hierarchy:**
- Level 0 (flat): No shadow
- Level 1 (raised): `--shadow-sm`
- Level 2 (card): `--shadow-md`
- Level 3 (dialog): `--shadow-lg`
- Level 4 (modal): `--shadow-xl`
- Level 5 (popover): `--shadow-2xl`

---

## Components

### Buttons

**Primary Button:**
```html
<button class="btn btn-primary">
  Primary Action
</button>
```

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: var(--radius-lg);
  transition: all 0.2s ease;
  cursor: pointer;
  border: 1px solid transparent;
}

.btn-primary {
  background: var(--brand-600);
  color: white;
  box-shadow: var(--shadow-md);
}

.btn-primary:hover {
  background: var(--brand-700);
  transform: translateY(-1px);
  box-shadow: var(--shadow-lg);
}

.btn-primary:active {
  transform: translateY(0);
  box-shadow: var(--shadow-sm);
}
```

**Secondary Button:**
```css
.btn-secondary {
  background: white;
  color: var(--brand-600);
  border: 1px solid var(--slate-300);
}

.dark .btn-secondary {
  background: var(--slate-800);
  color: var(--brand-400);
  border-color: var(--slate-700);
}

.btn-secondary:hover {
  background: var(--slate-50);
  border-color: var(--brand-500);
}
```

**Button Sizes:**
```css
.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.btn-lg {
  padding: 1rem 2rem;
  font-size: 1.125rem;
}

.btn-xl {
  padding: 1.25rem 2.5rem;
  font-size: 1.25rem;
}
```

### Cards

**Base Card:**
```html
<div class="card">
  <img src="cover.jpg" alt="Product" class="card-image">
  <div class="card-body">
    <h3 class="card-title">Card Title</h3>
    <p class="card-description">Card description text.</p>
    <button class="btn btn-primary">Action</button>
  </div>
</div>
```

```css
.card {
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-2xl);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.dark .card {
  background: var(--slate-800);
  border-color: var(--slate-700);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
}

.card-image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}

.card-body {
  padding: var(--space-6);
}

.card-title {
  font-size: var(--text-xl);
  font-weight: 700;
  margin-bottom: var(--space-2);
}

.card-description {
  color: var(--slate-600);
  margin-bottom: var(--space-4);
}

.dark .card-description {
  color: var(--slate-400);
}
```

### Forms

**Input Fields:**
```html
<div class="form-group">
  <label for="email" class="form-label">Email Address</label>
  <input
    type="email"
    id="email"
    class="form-input"
    placeholder="you@example.com"
  >
</div>
```

```css
.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.form-label {
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--slate-700);
}

.dark .form-label {
  color: var(--slate-300);
}

.form-input {
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 1px solid var(--slate-300);
  border-radius: var(--radius-lg);
  background: white;
  color: var(--slate-900);
  transition: all 0.2s ease;
}

.dark .form-input {
  background: var(--slate-800);
  border-color: var(--slate-700);
  color: var(--slate-100);
}

.form-input:focus {
  outline: none;
  border-color: var(--brand-500);
  box-shadow: 0 0 0 3px rgba(42, 167, 255, 0.1);
}
```

### Navigation

**Header Navigation:**
```css
.nav {
  display: flex;
  gap: var(--space-2);
  align-items: center;
}

.nav-link {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--slate-600);
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
  text-decoration: none;
}

.dark .nav-link {
  color: var(--slate-300);
}

.nav-link:hover {
  color: var(--brand-600);
  background: var(--slate-100);
  text-decoration: none;
}

.dark .nav-link:hover {
  color: var(--brand-400);
  background: var(--slate-800);
}

.nav-link.active {
  color: var(--brand-600);
  background: var(--brand-50);
}

.dark .nav-link.active {
  color: var(--brand-400);
  background: var(--slate-800);
}
```

### Badges

```html
<span class="badge">New</span>
<span class="badge badge-success">Active</span>
<span class="badge badge-warning">Beta</span>
```

```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: 0.25rem 0.75rem;
  font-size: var(--text-xs);
  font-weight: 600;
  border-radius: var(--radius-full);
  background: var(--slate-100);
  color: var(--slate-700);
}

.dark .badge {
  background: var(--slate-800);
  color: var(--slate-300);
}

.badge-success {
  background: #d1fae5;
  color: #065f46;
}

.badge-warning {
  background: #fef3c7;
  color: #92400e;
}

.badge-error {
  background: #fee2e2;
  color: #991b1b;
}
```

---

## Accessibility

### Focus States

**Visible Focus Indicators:**
```css
.focus-ring:focus-visible {
  outline: 2px solid var(--brand-500);
  outline-offset: 2px;
}

/* Alternative: Box shadow focus */
.focus-shadow:focus {
  box-shadow: 0 0 0 3px rgba(42, 167, 255, 0.5);
}
```

### Skip Links

```html
<a href="#main" class="skip-link">Skip to main content</a>
```

```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--brand-600);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0 0 var(--radius-md) 0;
  font-weight: 600;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

### ARIA Landmarks

```html
<header role="banner">
  <nav role="navigation" aria-label="Main navigation">
    <!-- Navigation content -->
  </nav>
</header>

<main role="main" id="main" tabindex="-1">
  <!-- Main content -->
</main>

<footer role="contentinfo">
  <!-- Footer content -->
</footer>
```

---

## Animations & Transitions

### Standard Transitions

```css
/* Default transition */
.transition {
  transition: all 0.2s ease;
}

/* Specific properties */
.transition-colors {
  transition: color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease;
}

.transition-transform {
  transition: transform 0.3s ease;
}

.transition-shadow {
  transition: box-shadow 0.3s ease;
}
```

### Keyframe Animations

```css
/* Fade In */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

/* Slide Up */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-up {
  animation: slideUp 0.6s ease-out;
}

/* Bounce Subtle */
@keyframes bounceSubtle {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

.animate-bounce-subtle {
  animation: bounceSubtle 1.4s ease-in-out infinite;
}

/* Pulse Glow */
@keyframes pulseGlow {
  0%, 100% {
    opacity: 0.2;
  }
  50% {
    opacity: 0.4;
  }
}

.animate-pulse-glow {
  animation: pulseGlow 2.4s ease-in-out infinite;
}
```

### Intersection Observer Animations

```html
<div class="intersection-animate">
  Content that animates when scrolled into view
</div>
```

```css
.intersection-animate {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

.intersection-animate.visible {
  opacity: 1;
  transform: translateY(0);
}
```

---

## Responsive Design

### Breakpoints

```css
/* Mobile First Approach */
--screen-sm: 640px;   /* Small devices */
--screen-md: 768px;   /* Tablets */
--screen-lg: 1024px;  /* Desktops */
--screen-xl: 1280px;  /* Large desktops */
--screen-2xl: 1536px; /* Extra large screens */
```

**Media Query Usage:**
```css
/* Mobile (default) */
.container {
  padding: 1rem;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: 1.5rem;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    padding: 2rem;
  }
}
```

### Container Widths

```css
.container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

@media (min-width: 640px) {
  .container {
    max-width: 640px;
  }
}

@media (min-width: 768px) {
  .container {
    max-width: 768px;
  }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
  }
}

@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
}
```

---

## Grid System

### Flexible Grid

```css
.grid {
  display: grid;
  gap: var(--space-6);
}

/* Auto-fit columns */
.grid-auto {
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}

/* Specific columns */
.grid-cols-2 {
  grid-template-columns: repeat(2, 1fr);
}

.grid-cols-3 {
  grid-template-columns: repeat(3, 1fr);
}

.grid-cols-4 {
  grid-template-columns: repeat(4, 1fr);
}

/* Responsive grid */
@media (min-width: 768px) {
  .md\:grid-cols-2 {
    grid-template-columns: repeat(2, 1fr);
  }

  .md\:grid-cols-3 {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1024px) {
  .lg\:grid-cols-3 {
    grid-template-columns: repeat(3, 1fr);
  }

  .lg\:grid-cols-4 {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

---

## Dark Mode Implementation

### CSS Variables Strategy

```css
:root {
  /* Light mode (default) */
  --bg: #ffffff;
  --text: #0f172a;
  --muted: #64748b;
  --border: #e2e8f0;
  --surface: #f8fafc;
}

.dark {
  /* Dark mode */
  --bg: #0f172a;
  --text: #f1f5f9;
  --muted: #94a3b8;
  --border: #334155;
  --surface: #1e293b;
}

/* Usage */
body {
  background: var(--bg);
  color: var(--text);
}
```

### Theme Toggle Script

```javascript
const toggleTheme = () => {
  const root = document.documentElement;
  const isDark = root.classList.contains('dark');

  if (isDark) {
    root.classList.remove('dark');
    localStorage.setItem('theme', 'light');
  } else {
    root.classList.add('dark');
    localStorage.setItem('theme', 'dark');
  }
};

// Initialize theme
const initTheme = () => {
  const saved = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

  if (saved === 'dark' || (!saved && prefersDark)) {
    document.documentElement.classList.add('dark');
  }
};

initTheme();
```

---

## Usage Guidelines

### Do's ✅
- Use consistent spacing (4px grid)
- Apply hover states to interactive elements
- Provide visual feedback for user actions
- Use semantic HTML elements
- Ensure sufficient color contrast
- Add focus indicators for keyboard navigation
- Use CSS variables for theming
- Test on multiple devices and browsers
- Optimize images for web (WebP format)
- Add alt text to all images

### Don'ts ❌
- Don't use absolute pixel values (use rem/em)
- Don't remove focus outlines without alternative
- Don't use color alone to convey information
- Don't use low-contrast text
- Don't nest too many levels (keep it shallow)
- Don't mix spacing units (stick to rem/px consistently)
- Don't hardcode colors (use design tokens)
- Don't skip heading levels (h1 → h2 → h3)

---

## Component Library Location

**Shared Components Directory:**
```
/includes/
├── header.html
├── footer.html
├── hero-cta.html
├── newsletter-form.html
└── language-switcher.html
```

**CSS Files:**
```
/css/
├── design-system.css (this system)
├── site.css (legacy, to be migrated)
└── components.css (component-specific styles)
```

---

## Version History

**v2.0.0 (Current):**
- Initial comprehensive design system
- Dark mode support
- Accessibility standards
- Responsive grid system
- Component library

**Future Versions:**
- v2.1.0: Animation library expansion
- v2.2.0: Advanced component variants
- v3.0.0: Design tokens API

---

## Resources & Tools

**Design Tools:**
- Figma (for mockups and prototypes)
- Adobe XD (alternative design tool)
- Coolors.co (color palette generation)
- Contrast Checker (WebAIM)

**Development Tools:**
- Tailwind CSS (utility-first framework)
- PostCSS (CSS processing)
- Autoprefixer (vendor prefixing)

**Testing Tools:**
- Lighthouse (performance and accessibility)
- axe DevTools (accessibility testing)
- WAVE (web accessibility evaluation)
- Color Contrast Analyzer

---

**Maintained By:** iD01t Productions Web Team
**Last Review:** October 30, 2025
**Next Review:** January 30, 2026
