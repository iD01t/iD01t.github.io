# iD01t Productions - Official Website

A complete static website built with HTML, Tailwind CSS, and vanilla JavaScript. No build step required - perfect for GitHub Pages deployment.

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/id01t/id01t.github.io.git
   cd id01t.github.io
   ```

2. **Open in your browser**
   - Simply open `index.html` in any modern web browser
   - Or use a local server: `python -m http.server 8000`

3. **Deploy to GitHub Pages**
   - Push to your `id01t.github.io` repository
   - Enable GitHub Pages in Settings → Pages
   - Set source to `main` branch, root folder

## 🏗️ Project Structure

```
id01t.github.io/
├── index.html              # Homepage
├── store.html              # Product store
├── ebooks.html             # eBook catalog
├── apps.html               # App listings
├── games.html              # Game hub
├── music.html              # Music albums
├── services.html           # Service offerings
├── portfolio.html          # Case studies
├── about.html              # Company info
├── contact.html            # Contact form
├── legal/                  # Legal pages
│   ├── privacy.html
│   ├── terms.html
│   ├── refunds.html
│   └── cookies.html
├── assets/                 # Images and media
├── css/
│   └── custom.css         # Custom styles
├── js/
│   └── utilities.js       # Shared JavaScript
├── sitemap.xml            # SEO sitemap
├── robots.txt             # Search engine rules
└── README.md              # This file
```

## 🎨 Design System

- **Colors**: Custom brand palette with dark mode support
- **Typography**: System fonts with responsive sizing
- **Layout**: Mobile-first responsive design
- **Components**: Consistent card designs, buttons, and forms
- **Accessibility**: ARIA labels, keyboard navigation, focus management

## 🛠️ Customization

### Adding a New Page

1. **Copy an existing page** (e.g., `about.html`)
2. **Update the content** and meta tags
3. **Add navigation links** in the header
4. **Update sitemap.xml** with the new URL

### Adding a New Product

1. **Edit the relevant page** (e.g., `store.html`)
2. **Add product card** with consistent styling
3. **Include structured data** for SEO
4. **Update product links** and pricing

### Modifying Styles

- **Tailwind classes**: Use utility classes directly in HTML
- **Custom CSS**: Edit `css/custom.css` for overrides
- **Brand colors**: Update the Tailwind config in each page

## 📱 Features

### Core Functionality
- ✅ Responsive navigation with mobile menu
- ✅ Dark/light theme toggle with localStorage
- ✅ Contact form with Netlify integration
- ✅ Modal system for previews and details
- ✅ Accordion components for FAQs
- ✅ Active navigation highlighting
- ✅ Breadcrumb navigation
- ✅ SEO-optimized with structured data

### Performance
- ✅ Lazy loading for images
- ✅ Minimal JavaScript footprint (< 8KB)
- ✅ Optimized CSS with Tailwind CDN
- ✅ Fast page loads with no build step

### Accessibility
- ✅ Semantic HTML structure
- ✅ ARIA labels and roles
- ✅ Keyboard navigation support
- ✅ Focus management
- ✅ Screen reader friendly
- ✅ High contrast ratios

## 🔧 Configuration

### Analytics Setup

1. **Google Analytics 4**
   ```html
   <!-- Replace G-XXXXXXX with your GA4 ID -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);} gtag('js', new Date());
     gtag('config', 'G-XXXXXXX');
   </script>
   ```

2. **Google Tag Manager**
   ```html
   <!-- Replace GTM-XXXXXXX with your GTM ID -->
   <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
   new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
   j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
   'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
   })(window,document,'script','dataLayer','GTM-XXXXXXX');</script>
   ```

### Contact Form

The contact form is configured for Netlify:
- Form name: `contact`
- Hidden field: `form-name`
- Honeypot protection: `bot-field`
- Success handling: Shows thank you message

For other hosting providers, update the form action and method as needed.

## 🚀 Deployment

### GitHub Pages (Recommended)

1. **Create repository** named `id01t.github.io`
2. **Push code** to main branch
3. **Enable Pages** in repository settings
4. **Set source** to main branch, root folder
5. **Wait for build** (usually 1-2 minutes)

### Custom Domain

1. **Add CNAME file** to root directory
2. **Update DNS** with your domain provider
3. **Configure GitHub Pages** custom domain setting

### Other Hosting

- **Netlify**: Drag and drop the folder
- **Vercel**: Import from GitHub
- **Traditional hosting**: Upload all files to web root

## 📊 Performance Targets

- **Lighthouse Performance**: 90+
- **Lighthouse Accessibility**: 95+
- **Lighthouse SEO**: 95+
- **Lighthouse Best Practices**: 95+
- **Cumulative Layout Shift**: < 0.1
- **First Contentful Paint**: < 1.5s

## 🧪 Testing

### Local Testing
- Open pages in multiple browsers
- Test responsive design at various breakpoints
- Verify dark/light theme switching
- Check form functionality
- Test keyboard navigation

### Validation
- [W3C HTML Validator](https://validator.w3.org/)
- [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)

## 🔄 Maintenance

### Regular Updates
- **Content**: Update product information, pricing, descriptions
- **Links**: Check external links are working
- **Analytics**: Review performance metrics
- **Security**: Keep dependencies updated

### Adding Features
- **New pages**: Follow the existing template structure
- **New components**: Add to `utilities.js` and `custom.css`
- **New products**: Update relevant pages and sitemap

## 📚 Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [GitHub Pages Documentation](https://pages.github.com/)
- [Web Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Schema.org Markup](https://schema.org/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

© 2025 iD01t Productions. All rights reserved.

## 🆘 Support

- **Issues**: Create a GitHub issue
- **Questions**: Contact via the website form
- **Business**: hello@id01t.com

---

Built with ❤️ by iD01t Productions
