export function normalizeCover(src) {
  if (!src) return src;
  let s = String(src).trim();

  // Strip accidental local prefix when an absolute URL was jammed after it
  s = s.replace(/^\/assets\/harvested\/(?:ebooks|audiobooks)\/(https?:\/\/.*)$/i, '$1');

  // If already absolute, keep it (but fix missing extension for Imgur)
  if (/^https?:\/\//i.test(s)) {
    const hasExt = /\.[a-z]{3,4}(\?.*)?$/i.test(s);
    const isImgurRaw = /^https?:\/\/i\.imgur\.com\/[^.\/\s?]+(?:\?.*)?$/i.test(s);
    if (isImgurRaw && !hasExt) s += '.png';
    return s;
  }

  // If it's a site-absolute path, trust it (png|jpg|jpeg|webp|avif|gif)
  if (/^\/.+\.(?:png|jpe?g|webp|avif|gif)(\?.*)?$/i.test(s)) return s;

  // If it's a stray relative and you host locally, choose one:
  // return `/assets/harvested/ebooks/${s}`;
  return s;
}