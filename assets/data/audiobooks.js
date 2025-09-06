/*! Ultimate Audiobooks Fallback & Map (v2) — iD01t Productions
   - Exposes:
     • window.AUDIOBOOK_FALLBACK  → rich catalog used if API fails
     • window.AUDIOBOOK_MAP       → Google volumeId → local /audiobooks/*.html overrides
     • window.GB_API_KEY          → optional API key override for audiobooks.client.js
   - Safe to include on any page; keys are merged not replaced.
*/
;(function(w){
  var cat = {
  "schema": "https://id01t.store/schemas/audiobooks-fallback.v2.json",
  "generatedAt": "2025-09-06T20:05:12Z",
  "publisher": "iD01t Productions",
  "source": "ultimate-audiobooks.js",
  "notes": "This fallback is used when Google Books API is unavailable. You can safely add/edit items.",
  "items": [
    {
      "id": "ab-unstoppable",
      "title": "Unstoppable: Unlock Your Potential (Audiobook)",
      "authors": [
        "Guillaume Lessard"
      ],
      "narrators": [
        "AI Narrator"
      ],
      "year": "2025",
      "language": "en",
      "genre": "Self-Improvement",
      "description": "High-impact systems, mindset, and automation. Audiobook edition.",
      "googleBooks": "https://books.google.com/",
      "googlePlay": "",
      "url": "/audiobooks/unstoppable.html",
      "cover": "/assets/img/audiobooks/unstoppable.jpg"
    },
    {
      "id": "ab-python-hero",
      "title": "Python Zero to Hero (Audiobook Edition)",
      "authors": [
        "Guillaume Lessard"
      ],
      "narrators": [
        "Studio Voice"
      ],
      "year": "2025",
      "language": "en",
      "genre": "Programming",
      "description": "A narrated path from absolute beginner to productive Python dev.",
      "googleBooks": "https://books.google.com/",
      "googlePlay": "",
      "url": "/audiobooks/python-zero-to-hero.html",
      "cover": "/assets/img/audiobooks/python-hero.jpg"
    },
    {
      "id": "ab-healing-code-fr",
      "title": "Le Code de Gu\u00e9rison de la Nature (\u00c9dition Audio)",
      "authors": [
        "Guillaume Lessard",
        "Cynthia Martineau"
      ],
      "narrators": [
        "Narrateur FR"
      ],
      "year": "2024",
      "language": "fr",
      "genre": "Health & Wellness",
      "description": "Exploration francophone des fr\u00e9quences naturelles et de l'auto-gu\u00e9rison.",
      "googleBooks": "https://books.google.com/",
      "googlePlay": "",
      "url": "/audiobooks/le-code-de-guerison.html",
      "cover": "/assets/img/audiobooks/healing-code-fr.jpg"
    },
    {
      "id": "ab-producer-workflow",
      "title": "Music Producer Workflow (Audiobook)",
      "authors": [
        "Guillaume Lessard"
      ],
      "narrators": [
        "DJ iD01t"
      ],
      "year": "2025",
      "language": "en",
      "genre": "Music",
      "description": "Studio and live performance workflows powered by AI tools.",
      "googleBooks": "https://books.google.com/",
      "googlePlay": "",
      "url": "/audiobooks/music-producer-workflow.html",
      "cover": "/assets/img/audiobooks/producer-workflow.jpg"
    }
  ]
};

  // Merge without clobbering if already present
  try {
    w.AUDIOBOOK_FALLBACK = (function(prev, next){
      // accept array or object format; client handles both
      if (!prev) return next;
      try {
        var prevItems = Array.isArray(prev) ? prev : (prev.items || []);
        var nextItems = Array.isArray(next) ? next : (next.items || []);
        var byId = Object.create(null);
        prevItems.concat(nextItems).forEach(function(it){ if(!it) return; byId[it.id || it.title] = it; });
        return { schema: (next.schema||prev.schema), generatedAt: (next.generatedAt||prev.generatedAt), publisher: (next.publisher||prev.publisher), source: "merged", items: Object.values(byId) };
      } catch(e) {
        return next || prev;
      }
    })(w.AUDIOBOOK_FALLBACK, cat);
  } catch(e) { w.AUDIOBOOK_FALLBACK = cat; }

  // Manual overrides for tricky slugs: Google Books volumeId → local URL
  w.AUDIOBOOK_MAP = Object.assign(Object.create(null), w.AUDIOBOOK_MAP || {}, {
    // "GoogleVolumeIdExample": "/audiobooks/unstoppable.html",
  });

  // Optional: allow overriding client API key (can be set here or elsewhere)
  w.GB_API_KEY = w.GB_API_KEY || ""; // set if you want to override the client-embedded key
})(window);
