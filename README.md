# iD01t Productions - eBooks & Audiobooks Catalog

Complete production-ready catalog system for [id01t.github.io](https://id01t.github.io) with ebooks and audiobooks from Google Play.

## 🚀 Features

### Core Functionality
- **📚 Dual Catalogs**: Separate pages for eBooks and Audiobooks
- **🔍 Instant Search**: Real-time filtering across titles, authors, publishers
- **🎨 Advanced Filters**:
  - Language selection
  - Brand/Author filtering (Guillaume Lessard, iD01t Productions, El'Nox Rah, DJ iD01t)
  - Price range (min/max)
  - Multiple sort options (relevance, date, title, price)
- **📱 Responsive Design**: Mobile-first, tablet, desktop optimized
- **🌓 Dark Mode**: Automatic theme detection with manual toggle
- **⚡ Performance**: Session storage caching, lazy image loading, optimized assets

### SEO & Discoverability
- **Schema.org Structured Data**:
  - WebSite with SearchAction
  - ItemList for catalog pages
  - Book/Audiobook entities with full metadata
  - Offer pricing data
- **Complete Sitemap**: Auto-generated for all pages and detail views
- **Robots.txt**: Proper search engine directives
- **Canonical URLs**: SEO-friendly URL structure
- **Open Graph & Twitter Cards**: Social media sharing optimized
- **Semantic HTML**: Proper heading hierarchy, ARIA labels

### PWA Support
- **Offline Ready**: Service Worker with intelligent caching
- **Installable**: Web app manifest for add-to-homescreen
- **Fast Loading**: Core assets pre-cached

### Developer Experience
- **Automated Build**: GitHub Actions CI/CD
- **Python Build Tools**: CSV → JSON conversion, sitemap generation
- **Zero Dependencies**: Pure vanilla JS, Tailwind CDN
- **Clean Code**: Well-documented, modular architecture

## 📁 File Structure

```
/
├── index.html                    # Your existing homepage (unchanged)
├── ebooks.html                   # eBooks catalog page
├── audiobooks.html               # Audiobooks catalog page
├── book.html                     # Individual book/audiobook detail page
├── robots.txt                    # SEO robots directives
├── sitemap.xml                   # Auto-generated sitemap
├── manifest.webmanifest          # PWA manifest
├── service-worker.js             # PWA service worker
├── assets/
│   ├── css/
│   │   └── site.css              # Extended Tailwind styles
│   └── js/
│       └── app.js                # Catalog application logic
├── data/
│   ├── catalog.csv               # Source CSV from Google Play export
│   └── catalog.json              # Generated catalog data
├── tools/
│   ├── build_catalog.py          # CSV → JSON converter
│   └── build_sitemap.py          # Sitemap generator
└── .github/
    └── workflows/
        └── build.yml              # GitHub Actions automation
```

## 🛠️ Setup Instructions

### 1. Add Files to Repository

Copy all files to your repository maintaining the directory structure shown above.

### 2. Add Your Catalog Data

Place your Google Play Books export CSV at `data/catalog.csv`.

**Required CSV columns** (flexible names supported):
- `Identifier` or `ID` - Google Play book ID (e.g., GGKEY:...)
- `Title` - Book title
- `Format` - "eBook" or "Audiobook"
- `Primary Creator(s) / Contributors` or `Author` - Author/narrator
- `Publisher / Label` - Publisher name
- `Language` - Language code (e.g., "en", "fr")
- `Release / Publish Date` - Publication date
- `HD Cover Image URL` - High-resolution cover URL
- `Google Play Buy Link` - Store URL
- `Price (if present)` - Price in USD (optional)

### 3. Build Catalog

Run locally or let GitHub Actions handle it:

```bash
# Generate catalog.json
python tools/build_catalog.py

# Generate sitemap.xml
python tools/build_sitemap.py
```

### 4. Configure GitHub Pages

1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` / `root`
4. Save

### 5. Enable GitHub Actions

The workflow will automatically run when you:
- Push changes to `data/catalog.csv`
- Push changes to build scripts
- Manually trigger from Actions tab

## 📊 Catalog Data Format

### Example JSON Structure

```json
[
  {
    "id": "GGKEY:9FBS6JZA71F",
    "title": "Advanced Chess Tactics",
    "subtitle": "Psychological Play and Tournament Strategies",
    "format": "eBook",
    "contributors": "Guillaume Lessard",
    "publisher": "iD01t Productions",
    "language": "en",
    "date": "2024-08-12",
    "cover_hd": "https://books.google.com/books/content?id=GGKEY%3A9FBS6JZA71F&printsec=frontcover&img=1&zoom=3",
    "buy": "https://play.google.com/store/books/details?id=GGKEY:9FBS6JZA71F",
    "price": "9.99"
  }
]
```

## 🎨 Customization

### Brand Colors

Modify Tailwind config in HTML files:

```javascript
tailwind.config = {
  theme: {
    extend: {
      colors: {
        brand: {
          500: '#2aa7ff',  // Primary brand color
          600: '#008ef6',  // Hover state
          // ... other shades
        }
      }
    }
  }
}
```

### Search Behavior

Edit `assets/js/app.js`:
- `makeIndex()` - Control which fields are searchable
- `apply()` - Modify filter logic
- `renderCards()` - Customize card layout

### Filters

Add new filters by:
1. Adding HTML form control in catalog pages
2. Extracting values in `apply()` function
3. Adding filter logic to the `rows` filtering chain

## 🔧 Build Tools

### build_catalog.py

Converts CSV to optimized JSON format.

**Features**:
- Flexible column name mapping
- Data validation and cleaning
- Format filtering (eBook/Audiobook)
- UTF-8 encoding support
- Statistics reporting

### build_sitemap.py

Generates complete sitemap.xml.

**Includes**:
- Homepage (priority 1.0)
- Catalog pages (priority 0.9)
- All book detail pages (priority 0.8)
- Automatic lastmod dates
- URL encoding

## 📈 SEO Best Practices Implemented

✅ **Clean URLs**: `/book.html?id=GGKEY:...` format  
✅ **Structured Data**: Schema.org Book/Audiobook entities  
✅ **Meta Tags**: Complete Open Graph and Twitter Cards  
✅ **Canonical URLs**: Prevent duplicate content  
✅ **Alt Text**: All images have descriptive alt attributes  
✅ **Semantic HTML**: Proper heading hierarchy  
✅ **Mobile-First**: Responsive design, fast loading  
✅ **Sitemap**: Complete site structure  
✅ **Robots.txt**: Proper crawl directives  
✅ **Performance**: Lazy loading, preconnect, caching  

## 🚨 Important Notes

### Copyright & Content

- **Never quote song lyrics** - The system respects copyright
- **Affiliate Links**: Buy buttons use `rel="noopener nofollow sponsored"`
- **Image Rights**: Uses official Google Books cover URLs
- **Terms Compliance**: Follows Google Play Partner program guidelines

### Rate Limits

- Service Worker caches assets to reduce bandwidth
- External images (Google Books) load on-demand
- Session storage reduces API calls

### Browser Support

- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Progressive Enhancement**: Works without JavaScript (limited)
- **Dark Mode**: Respects system preference + manual toggle

## 🐛 Troubleshooting

### Catalog not loading

1. Check `data/catalog.json` exists
2. Verify JSON is valid (use jsonlint.com)
3. Check browser console for errors
4. Clear browser cache and sessionStorage

### Build script fails

```bash
# Check Python version (3.7+ required)
python --version

# Verify CSV path
ls -la data/catalog.csv

# Test manually
python tools/build_catalog.py
```

### GitHub Actions fails

1. Check Actions tab for error logs
2. Verify CSV is committed to repository
3. Ensure workflow has write permissions
4. Check branch protection rules

### Images not loading

- Verify cover URLs in `catalog.json`
- Check browser console for CORS errors
- Ensure URLs use HTTPS
- Google Books sometimes rate-limits requests

## 📝 License

This catalog system is provided as-is for use with iD01t Productions content.

## 🤝 Support

For issues specific to this catalog system:
1. Check this README
2. Review code comments in source files
3. Check GitHub Actions logs
4. Inspect browser console for errors

---

**Built with ❤️ for iD01t Productions**  
Professional digital tools for creators worldwide.
