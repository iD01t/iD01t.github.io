# 🚀 Quick Start Guide

Get your catalog live in **5 minutes**!

## Step 1: Copy Files to Your Repository

Copy the entire `id01t-catalog-complete` folder contents to your `id01t.github.io` repository:

```bash
# From your repository root
cp -r id01t-catalog-complete/* .
```

Your repository should now have:
```
id01t.github.io/
├── ebooks.html              ← NEW
├── audiobooks.html          ← NEW
├── book.html                ← NEW
├── robots.txt               ← NEW
├── manifest.webmanifest     ← NEW
├── service-worker.js        ← NEW
├── assets/
│   ├── css/
│   │   └── site.css         ← NEW
│   └── js/
│       └── app.js           ← NEW
├── data/
│   └── catalog.csv          ← REPLACE WITH YOUR DATA
├── tools/
│   ├── build_catalog.py     ← NEW
│   └── build_sitemap.py     ← NEW
└── .github/
    └── workflows/
        └── build.yml        ← NEW
```

## Step 2: Add Your Catalog Data

**Option A: Replace the sample CSV**

1. Delete `data/catalog.csv` (sample file)
2. Copy your Google Play Books export CSV to `data/catalog.csv`

**Option B: Use your existing CSV**

If your CSV has different column names, the build script will try to match them automatically. It supports:
- `Identifier`, `ID`, `id`, `Google Play Store Link ID`
- `Title`, `title`
- `Format`, `Book Format`, `format`
- etc.

## Step 3: Build Catalog Locally (Optional)

Test the build before committing:

```bash
# Generate catalog.json
python tools/build_catalog.py

# Generate sitemap.xml
python tools/build_sitemap.py
```

You should see:
```
📖 Reading catalog from: data/catalog.csv
✅ Successfully wrote 269 items to: data/catalog.json
   📚 eBooks: 166
   🎧 Audiobooks: 103
```

## Step 4: Commit and Push

```bash
git add .
git commit -m "Add eBooks and Audiobooks catalog"
git push origin main
```

GitHub Actions will automatically:
1. Build `data/catalog.json`
2. Generate `sitemap.xml`
3. Commit them back to your repository

## Step 5: Verify It's Live

Visit your new pages:
- **eBooks**: https://id01t.github.io/ebooks.html
- **Audiobooks**: https://id01t.github.io/audiobooks.html
- **Example Detail**: https://id01t.github.io/book.html?id=GGKEY:...

## 🎨 Customization

### Update Colors

Edit the Tailwind config in `ebooks.html`, `audiobooks.html`, and `book.html`:

```javascript
tailwind.config = {
  theme: {
    extend: {
      colors: {
        brand: {
          500: '#2aa7ff',  // ← Change this to your brand color
          600: '#008ef6',  // ← Hover state (slightly darker)
          // ...
        }
      }
    }
  }
}
```

### Add Logo

Replace the logo path in all HTML files:

```html
<img src="/assets/img/brand/logo.svg" alt="iD01t Productions logo" class="h-8 w-8" />
```

With your actual logo file.

### Update Site Info

In each HTML file, update the meta tags:
- `<title>` - Page title
- `<meta name="description">` - Page description
- Open Graph tags
- Twitter Card tags

## 📊 Monitoring

### Check Build Status

1. Go to your repository on GitHub
2. Click "Actions" tab
3. See the latest workflow runs

### View Catalog Stats

After the build:
```bash
# Check how many items
python -c "import json; print(len(json.load(open('data/catalog.json'))))"

# Check sitemap URLs
grep -c "<loc>" sitemap.xml
```

## 🐛 Troubleshooting

### "No items in catalog"

1. Check your CSV file is at `data/catalog.csv`
2. Verify it has a header row
3. Check column names match expected format
4. Run `python tools/build_catalog.py` to see errors

### "GitHub Actions failed"

1. Check the Actions tab for error logs
2. Verify the CSV is valid (no special characters in paths)
3. Ensure workflow has write permissions

### "Pages not loading"

1. Clear browser cache
2. Check browser console for errors
3. Verify GitHub Pages is enabled
4. Wait 2-3 minutes for Pages deployment

## 📝 Next Steps

1. **Submit sitemap to Google**: Search Console → Sitemaps → Add `https://id01t.github.io/sitemap.xml`
2. **Test mobile**: Use Chrome DevTools mobile emulation
3. **Customize styling**: Edit `assets/css/site.css`
4. **Add more filters**: Modify `assets/js/app.js`

## 🎯 Production Checklist

Before going live:

- [ ] Real catalog data added
- [ ] Logo updated
- [ ] Meta tags customized
- [ ] Brand colors configured
- [ ] Tested on mobile
- [ ] Verified all links work
- [ ] Checked dark mode
- [ ] Sitemap submitted to Google
- [ ] Analytics added (optional)

---

**Need help?** Check the main [README.md](README.md) for detailed documentation.
