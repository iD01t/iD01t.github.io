# iD01t Productions – Professional Website

A complete, SEO‑optimized static website built with HTML, CSS, and vanilla JavaScript. Features professional design, advanced SEO, performance monitoring, and traffic generation tools. **No build step required** — perfect for GitHub Pages deployment.

## ✨ New Features & Improvements

### 🚀 SEO & Performance
- **Advanced SEO**: Meta tags, Open Graph, Twitter Cards, structured data (JSON‑LD), `sitemap.xml`, `robots.txt`
- **Core Web Vitals**: Lightweight pages, Tailwind CDN, image sizing, lazy loading
- **Social Sharing**: Ready for X (Twitter), LinkedIn, Facebook
- **Search Functionality** *(optional)*: Built‑in hook for `/search.html`
- **Blog System**: HTML blog pages for content marketing and organic traffic

### 🎨 User Experience
- **Professional Design**: Modern, responsive layout with Tailwind utility classes
- **Dark/Light Theme**: User preference stored in `localStorage`
- **Newsletter Signup**: Netlify‑compatible forms
- **Custom 404 Page**: Cleaner error handling
- **Web App Manifest**: PWA‑ready

### 📊 Analytics & Tracking
- **Google Analytics 4**: Drop‑in snippet
- **Google Tag Manager**: Advanced event tracking
- **Performance Monitoring**: Lighthouse‑friendly defaults
- **Error Tracking**: Hook points for your provider of choice

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/id01t/id01t.github.io.git
   cd id01t.github.io
   ```

2. **Open in your browser**
   - Simply open `index.html` in any modern browser, or
   - Serve locally: `python -m http.server 8000` → http://localhost:8000

3. **Deploy to GitHub Pages**
   - Push to your `id01t.github.io` repository
   - Enable GitHub Pages in **Settings → Pages**
   - Source: `main` branch, root folder

## 🏗️ Project Structure

```
id01t.github.io/
├── index.html               # Homepage with hero, CTAs, cross-links, newsletter
├── store.html               # Product hub linking to all categories
├── ebooks.html              # Live Google Books catalog (books)
├── audiobooks.html          # Live Google Books catalog (audiobooks only)
├── apps.html                # App listings
├── games.html               # Game hub (Nini’s Adventures: Kitties Mayhem!)
├── music.html               # Music page (DJ iD01t)
├── blog.html                # Blog index (cards + JSON‑LD)
├── about.html               # Company bio
├── contact.html             # Contact form (Netlify‑ready)
├── 404.html                 # Custom 404 page
├── manifest.json            # Web app manifest (PWA)
├── legal/
│   ├── privacy.html
│   ├── terms.html
│   ├── refunds.html
│   └── cookies.html
├── css/
│   └── custom.css           # Optional overrides (Tailwind loaded via CDN)
├── assets/
│   ├── img/                 # Images and icons
│   └── data/                # JSON fallbacks (e.g., audiobooks.json)
├── sitemap.xml              # SEO sitemap
├── robots.txt               # Search engine rules
└── README.md                # This file
```

> **Note:** The site uses Tailwind via CDN in each page head. No Node or build pipeline is required.

## 🎨 Design System

- **Colors**: Brand palette with dark mode support
- **Typography**: System font stack with responsive sizing
- **Layout**: Mobile‑first, grid‑based sections and cards
- **Components**: Consistent buttons, cards, forms, and nav
- **Accessibility**: Semantic HTML, ARIA labels, focus states

## 🛠️ Customization

### Adding a New Page
1. Copy any page (e.g., `about.html`) as a starter.
2. Update `<title>`, meta description, and JSON‑LD if relevant.
3. Add links in the header nav (desktop and mobile).
4. Add the URL to `sitemap.xml`.

### Adding a New Product or Card
1. Edit the relevant page (`store.html`, `apps.html`, etc.).
2. Use the existing card markup for visual consistency.
3. Include structured data where applicable (e.g., `SoftwareApplication`, `VideoGame`, `MusicGroup`).

### Modifying Styles
- Use Tailwind utility classes directly in HTML.
- Put custom tweaks in `css/custom.css`.
- Brand colors are configured inline in each page’s Tailwind config block.

## 📱 Features

### Core Functionality
- ✅ Responsive navigation with mobile menu
- ✅ Dark/light theme toggle with `localStorage`
- ✅ Netlify‑compatible forms (newsletter, contact)
- ✅ Blog cards with schema
- ✅ Optional site search hook
- ✅ Web app manifest (PWA‑ready)
- ✅ Active nav highlighting
- ✅ Clean breadcrumbs (optional)

### SEO & Marketing
- ✅ Complete meta tag setup
- ✅ Open Graph + Twitter Cards
- ✅ JSON‑LD structured data
- ✅ XML sitemap
- ✅ Robots.txt
- ✅ Canonical URLs
- ✅ Blog for organic growth
- ✅ Newsletter for retention

### Performance
- ✅ Optimized hero and card imagery
- ✅ Lazy loading below the fold
- ✅ Minimal JS footprint
- ✅ Tailwind via CDN
- ✅ Resource preconnects where helpful

### Analytics & Tracking
- ✅ GA4 drop‑in
- ✅ GTM integration
- ✅ Hooks for error monitoring

### Accessibility
- ✅ Semantic headings and landmarks
- ✅ ARIA labels and roles
- ✅ Keyboard navigation support
- ✅ Focus management
- ✅ High contrast in dark mode

## 🔧 Configuration

### Analytics Setup

**Google Analytics 4**
```html
<!-- Replace G-XXXXXXX with your GA4 ID -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);} gtag('js', new Date());
  gtag('config', 'G-XXXXXXX');
</script>
```

**Google Tag Manager**
```html
<!-- Replace GTM-XXXXXXX with your GTM ID -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>
```

### Netlify Forms (example)
- Add `data-netlify="true"` and a hidden `form-name` input.
- Optional honeypot: add a hidden field (e.g., `bot-field`).

## 🚀 Deployment

### GitHub Pages
1. Create repo `id01t.github.io`
2. Push code to `main`
3. Enable **Pages** in Settings
4. Set source to `main` branch, root
5. Done — GitHub will publish automatically

### Custom Domain
1. Add `CNAME` file with your domain (e.g., `id01t.store`)
2. Point DNS to GitHub Pages
3. Configure the custom domain in repository Settings

### Other Hosting
- **Netlify**: Drag‑and‑drop the folder
- **Vercel**: Import from GitHub
- **Traditional hosting**: Upload all files to web root

## 📊 Performance Targets
- Lighthouse Performance: **90+**
- Accessibility: **95+**
- SEO: **95+**
- Best Practices: **95+**
- CLS < **0.1**, FCP < **1.5s**

## 🧪 Testing
- Test on multiple browsers and breakpoints
- Verify dark/light theme behavior
- Check forms (newsletter, contact)
- Validate links and images

**Validation Tools**
- [W3C HTML Validator](https://validator.w3.org/)
- [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)

## 🔄 Maintenance
- Update content and links regularly
- Review analytics for growth opportunities
- Keep `sitemap.xml` and `robots.txt` current
- Add new blog posts to build topical authority

## 📚 Resources
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [GitHub Pages Docs](https://pages.github.com/)
- [Web Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Schema.org](https://schema.org/)

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make changes and test
4. Open a pull request

## 📄 License
© 2025 iD01t Productions. All rights reserved.

## 🆘 Support
- **Issues**: Open a GitHub issue
- **Questions**: Use the contact form
- **Business**: hello@id01t.com

---

Built with ❤️ by iD01t Productions
