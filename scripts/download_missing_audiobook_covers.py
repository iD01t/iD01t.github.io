import os
import requests
from urllib.parse import quote

# Directory for audiobook covers
audio_dir = "assets/harvested/audiobooks/"
os.makedirs(audio_dir, exist_ok=True)

# List of audiobooks (filenames, no extension)
audiobooks = [
    "ableton-elevation-dj-id01ts-complete-guide-to-building-hits-and-elevating-your-sound",
    "advanced-tactics-psychological-play-and-tournament-preparation",
    "agentic-ai-sprint-for-solopreneurs",
    "ai-cash-code",
    "ai-cash-empire",
    "ai-goldmine-100-passive-income-ideas-using-chatgpt-and-free-ai-tools",
    "ai-in-education",
    "ai-revolution-how-automation-is-transforming-everyday-life-edition-2-2025",
    "ai-revolution-how-automation-is-transforming-everyday-life",
    "ai-today-transforming-lives-and-industries-for-the-future",
    "anarchie-et-évolution---lhistoire-de-la-musique-punk",
    "anarchy-and-evolution",
    "automation-and-seo-mastery-strategies-for-growth-and-efficiency",
    "beat-alchemy-the-dj-id01t-guide-to-mastering-fl-studio-and-making-hits",
    "before-the-storm",
    "beneath-the-bloom",
    "beyond-the-event-horizon-solving-the-black-hole-information-paradox",
    "bite-by-bite",
    "bridging-worlds-a-practical-guide-to-connecting-with-parallel-energies-and-dimensions",
    "c-zero-to-hero",
    "chess-mastery",
    "christ-quil-est-intelligent-daimer",
    "code-in-every-language-master-programming-with-chatgpt",
    "crafting-worlds",
    "crossroads-of-shadows",
    "dancing-with-the-edge",
    "diy-digital-skills-build-a-career-in-tech-from-scratch",
    "dominio-del-ajedrez",
    "dos-zero-to-hero-mastering-legacy-systems-command-line-fluency-retro-automation",
    "dünyalar-arasında-köprü-kurmak",
    "earthquakes-unveiled",
    "echo-protocol",
    "echoes-of-the-heart",
    "echoes-of-truth",
    "elnox-rah-le-retour-de-lhomme-vrai",
    "eternal-roots",
    "final-transmission-i-am-echo",
    "final-transmission-je-suis-echo-fr",
    "forever-in-bloom",
    "fortgeschrittene-taktiken-psychologisches-spiel-und-turniervorbereitung",
    "free-energy-free-life",
    "from-seed-to-splendor-a-comprehensive-journey-in-horticulture",
    "from-zero-to-python-hero-a-comprehensive-guide-to-mastering-python",
    "id01t-academy-python-exercises-book-1-edition-2",
    "id01t-academy-python-exercises-book-2---edition-2",
    "id01t-academy-python-exercises-book-3",
    "intersection-the-moment-their-paths-crossed",
    "jacks-stand",
    "java-maestro",
    "java-zero-to-hero-mastering-java-programming-for-real-world-applications",
    "jesus-the-eternal-legacy",
    "jimmy-carter-a-legacy-of-compassion-and-leadership",
    "kimi-k2-unlocked",
    "la-réalité-dévoilée-comment-la-conscience-façonne-le-monde-que-nous-percevons",
    "lalchimie-de-la-transformation",
    "laventure-did01t-productions-une-histoire-de-passion-de-résilience-et-de-créativité",
    "le-pont-entre-les-mondes",
    "legacy-of-shadows-2",
    "legacy-of-shadows",
    "leo-xiv-the-first-american-pope",
    "let-it-be-them",
    "lettre-à-celle-que-jaime-toujours",
    "light-at-the-veils-edge",
    "love-prevails-2",
    "love-prevails",
    "lumenzero-le-pouvoir-caché-des-pyramides-énergétiques",
    "lénergie-libre-à-domicile",
    "lénigme-quantique-percer-les-mystères-de-la-réalité",
    "maailmojen-yhdistäminen",
    "machine-learning-demystified-a-practical-guide-to-building-smarter-systems",
    "master-it-yourself",
    "master-the-basics-of-reading-music",
    "mastering-aeo-the-ultimate-guide-to-advanced-ecommerce-optimization",
    "mastering-blender",
    "mastering-chess-intuition",
    "mastering-generative-ai-and-llms---editon-2",
    "mastering-generative-ai-and-llms",
    "mastering-gpt-creation-from-concept-to-deployment",
    "mastering-linux",
    "mastering-macos-terminal",
    "mastering-photoshop-the-complete-guide-to-every-version",
    "mastering-quantum-error-correction",
    "mastering-rfid-unlocking-the-potential-of-radio-frequency-identification",
    "mastering-rfid",
    "mastering-the-game-the-ultimate-guide-to-pro-chess-strategies",
    "mastering-unreal-engine-5-a-comprehensive-guide-to-game-development-and-virtual-reality",
    "mastering-xcode",
    "maîtrise-des-échecs-guide-du-pro-pour-des-stratégies-et-des-techniques-gagnantes",
    "maîtrise-des-échecs",
    "meisterschaft-im-schach",
    "menjembatani-dunia",
    "onyx-storm",
    "panneaux-solaires-organiques-lénergie-vivante-du-futur",
    "penguasaan-catur",
    "python-mastery-the-complete-guide-to-building-profitable-applications",
    "python-prodigy-from-intermediate-to-expert-mastery",
    "quantum-code-mastery",
    "quantum-echoes-the-resonance-of-time",
    "quantum-jumping-unlocked-edition-2",
    "quantum-jumping-unlocked",
    "quantum-revolution-unveiling-the-future-with-willow",
    "quantum-tao",
    "ra7-the-sacred-book-of-the-original-broadcast",
    "real",
    "reality-unveiled-how-consciousness-shapes-the-world-we-perceive",
    "reignite-the-bond",
    "rising-from-the-ashes-a-comprehensive-guide-to-recovery-after-the-hollywood-hills-fire-2025",
    "réveillez-vous-à-une-vie-sacrée",
    "sacred-energy-harvesting-methods",
    "sacred-patterns-a-transformational-journey-through-geometry-and-conscious-living",
    "sacred-timing-when-the-universe-speaks-through-synchronicity",
    "sacred-vibrational-technology",
    "schachintuition-meistern",
    "schumann-resonance-creativity",
    "se-reconstruire-de-la-douleur-à-la-renaissance",
    "shadows-of-bloom",
    "shadows-of-redemption",
    "shadows-of-serenity",
    "shadows-reforged-the-war-isnt-ove",
    "shadows-reforged",
    "shadows-reignited",
    "shaping-the-future-embracing-trends-for-a-better-tomorrow",
    "spin-mastery-le-guide-ultime-du-dj-traktor",
    "spin-mastery",
    "spiritual-psychosis-memoir",
    "the-7-figure-blueprint-unlocking-the-power-of-your-million-dollar-book",
    "the-adventure-of-id01t-productions-a-story-of-passion-resilience-and-creativity",
    "the-architects-legacy",
    "the-art-of-beauty",
    "the-artifacts-whisper",
    "the-complete-beginner-to-intermediate-guide-to-json-for-veo-3-prompting",
    "the-digital-aftermath-navigating-life-beyond-the-great-platform-collapse",
    "the-dream-dialogue",
    "the-end-of-an-era-the-tiktok-shutdown-in-the-usa",
    "the-enigma-of-high-intellectual-potential-hip",
    "the-frequency-blueprint",
    "the-last-bow",
    "the-maglev-revolution",
    "the-many-realities",
    "the-power-of-repetition-transforming-minds-through-words",
    "the-quantum-enigma-unraveling-the-mysteries-of-reality",
    "the-quantum-passive-empire",
    "the-real-guide-to-using-ai-to-generate-perfect-veo-3-requests",
    "the-secrets-of-oak-island",
    "the-sun-is-not-what-you-were-told",
    "the-third-state-life-between-life-and-death",
    "to-the-top-of-the-mountain",
    "traktor-mastery-the-complete-professional-dj-system",
    "turings-legacy-classical-logic-to-quantum-revolution",
    "tácticas-avanzadas-juego-psicológico-y-preparación-para-torneos",
    "understanding-your-cats-mind---edition-2",
    "understanding-your-cats-mind",
    "uniendo-mundos",
    "unire-i-mondi",
    "unstoppable-the-ultimate-guide-to-unlocking-your-potential-and-achieving-success",
    "veil-of-echoes",
    "visual-basic-zero-to-hero-edition-2",
    "when-cells-listen-the-hidden-symphony-of-sound-and-gene-expression",
    "windows-zero-to-hero",
    "zen-and-the-art-of-resilient-living",
    "zen-and-the-art-of-self-confidence",
    "мастерство-в-шахматах",
    "продвинутая-тактика-психологическая-игра-и-подготовка-к-турниру",
    "暴风雨前-无畏记者的崛起",
    "杰克的摊位",
    "𓂀-synarchéon-𓂀"
]

# Google Books API template (search by title)
GB_API = "https://www.googleapis.com/books/v1/volumes?q=intitle:{}&maxResults=1"

# Download image helper
def download_image(url, path):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                f.write(r.content)
            print(f"Downloaded: {path}")
            return True
    except Exception as e:
        print(f"Failed: {url} -> {e}")
    return False

# Main logic
for ab in audiobooks:
    # Expected cover filename
    base = ab.replace(' ', '_').replace('/', '_')
    cover_path = os.path.join(audio_dir, f"{base}_cover.jpg")
    if os.path.exists(cover_path):
        continue
    # Try Google Books API
    resp = requests.get(GB_API.format(quote(ab)))
    if resp.status_code == 200:
        data = resp.json()
        if 'items' in data and data['items']:
            info = data['items'][0]['volumeInfo']
            image_url = info.get('imageLinks', {}).get('thumbnail')
            if image_url:
                # Use high-res if available
                image_url = image_url.replace('&edge=curl', '').replace('zoom=1', 'zoom=2')
                if download_image(image_url, cover_path):
                    continue
    # Fallback: placeholder
    placeholder = os.path.join('..', '..', 'assets', 'placeholder-cover.svg')
    if os.path.exists(placeholder):
        with open(placeholder, 'rb') as src, open(cover_path, 'wb') as dst:
            dst.write(src.read())
        print(f"Used placeholder for: {cover_path}")
    else:
        print(f"No cover found for: {ab}")
