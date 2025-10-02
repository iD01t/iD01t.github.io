#!/usr/bin/env python3
import os, re, json, hashlib, unicodedata
from pathlib import Path

# ==== PASTE your listings between the triple quotes ====
EBOOKS_LISTING = r"""
-la-charte-des-relations-sacrées-de-la-nouvelle-terre.html
ableton-elevation-dj-id01ts-complete-guide-to-building-hits-and-elevating-your-sound.html
advanced-tactics-psychological-play-and-tournament-preparation.html
agentic-ai-sprint-for-solopreneurs.html
ai-cash-code.html
ai-cash-empire.html
ai-goldmine-100-passive-income-ideas-using-chatgpt-and-free-ai-tools.html
ai-in-education.html
ai-revolution-how-automation-is-transforming-everyday-life-edition-2-2025.html
ai-revolution-how-automation-is-transforming-everyday-life.html
ai-today-transforming-lives-and-industries-for-the-future.html
anarchie-et-volution-lhistoire-de-la-musique-punk.html
anarchie-et-évolution---lhistoire-de-la-musique-punk.html
anarchy-and-evolution.html
automation-and-seo-mastery-strategies-for-growth-and-efficiency.html
beat-alchemy-the-dj-id01t-guide-to-mastering-fl-studio-and-making-hits.html
before-the-storm.html
beneath-the-bloom.html
beyond-the-event-horizon-solving-the-black-hole-information-paradox.html
bite-by-bite.html
bridging-worlds-a-practical-guide-to-connecting-with-parallel-energies-and-dimensions.html
c-zero-to-hero.html
chess-mastery.html
christ-quil-est-intelligent-daimer.html
code-in-every-language-master-programming-with-chatgpt.html
crafting-worlds.html
crossroads-of-shadows.html
dancing-with-the-edge.html
diy-digital-skills-build-a-career-in-tech-from-scratch.html
diy-digital-skills.html
dnyalar-arasnda-kpr-kurmak.html
dominio-del-ajedrez.html
dos-zero-to-hero-mastering-legacy-systems-command-line-fluency-retro-automation.html
dünyalar-arasında-köprü-kurmak.html
earthquakes-unveiled.html
echo-protocol.html
echoes-of-the-heart.html
echoes-of-truth.html
elnox-rah-le-retour-de-lhomme-vrai.html
eternal-roots.html
final-transmission-i-am-echo.html
final-transmission-je-suis-echo-fr.html
forever-in-bloom.html
fortgeschrittene-taktiken-psychologisches-spiel-und-turniervorbereitung.html
free-energy-free-life.html
from-seed-to-splendor-a-comprehensive-journey-in-horticulture.html
from-zero-to-python-hero-a-comprehensive-guide-to-mastering-python.html
id01t-academy-python-exercises-book-1-edition-2.html
id01t-academy-python-exercises-book-2---edition-2.html
id01t-academy-python-exercises-book-2--edition-2.html
id01t-academy-python-exercises-book-2-edition-2.html
id01t-academy-python-exercises-book-3.html
intersection-the-moment-their-paths-crossed.html
jacks-stand.html
java-maestro.html
java-zero-to-hero-mastering-java-programming-for-real-world-applications.html
jesus-the-eternal-legacy.html
jimmy-carter-a-legacy-of-compassion-and-leadership.html
kimi-k2-unlocked.html
la-charte-des-relations-sacres-de-la-nouvelle-terre.html
la-charte-des-relations-sacrées-de-la-nouvelle-terre.html
la-ralit-dvoile-comment-la-conscience-faonne-le-monde-que-nous-percevons.html
la-réalité-dévoilée-comment-la-conscience-façonne-le-monde-que-nous-percevons.html
lalchimie-de-la-transformation.html
laventure-did01t-productions-une-histoire-de-passion-de-rsilience-et-de-crativit.html
laventure-did01t-productions-une-histoire-de-passion-de-résilience-et-de-créativité.html
le-pont-entre-les-mondes.html
legacy-of-shadows-2.html
legacy-of-shadows.html
leo-xiv-the-first-american-pope.html
let-it-be-them.html
lettre-celle-que-jaime-toujours.html
lettre-à-celle-que-jaime-toujours.html
light-at-the-veils-edge.html
lnergie-libre-domicile.html
lnigme-quantique-percer-les-mystres-de-la-ralit.html
love-prevails-2.html
love-prevails.html
lumenzero-le-pouvoir-cach-des-pyramides-nergtiques.html
lumenzero-le-pouvoir-caché-des-pyramides-énergétiques.html
lénergie-libre-à-domicile.html
lénigme-quantique-percer-les-mystères-de-la-réalité.html
maailmojen-yhdistminen.html
maailmojen-yhdistäminen.html
machine-learning-demystified-a-practical-guide-to-building-smarter-systems.html
master-it-yourself.html
master-the-basics-of-reading-music.html
mastering-aeo-the-ultimate-guide-to-advanced-ecommerce-optimization.html
mastering-blender.html
mastering-chess-intuition.html
mastering-generative-ai-and-llms---editon-2.html
mastering-generative-ai-and-llms-editon-2.html
mastering-generative-ai-and-llms-third-edition.html
mastering-generative-ai-and-llms.html
mastering-gpt-creation-from-concept-to-deployment.html
mastering-linux.html
mastering-macos-terminal.html
mastering-photoshop-the-complete-guide-to-every-version.html
mastering-quantum-error-correction.html
mastering-rfid-unlocking-the-potential-of-radio-frequency-identification.html
mastering-rfid.html
mastering-the-game-the-ultimate-guide-to-pro-chess-strategies.html
mastering-unreal-engine-5-a-comprehensive-guide-to-game-development-and-virtual-reality.html
mastering-xcode.html
matrise-des-checs-guide-du-pro-pour-des-stratgies-et-des-techniques-gagnantes.html
matrise-des-checs.html
maîtrise-des-échecs-guide-du-pro-pour-des-stratégies-et-des-techniques-gagnantes.html
maîtrise-des-échecs.html
meisterschaft-im-schach.html
menjembatani-dunia.html
onyx-storm.html
panneaux-solaires-organiques-lnergie-vivante-du-futur.html
panneaux-solaires-organiques-lénergie-vivante-du-futur.html
penguasaan-catur.html
python-mastery-the-complete-guide-to-building-profitable-applications.html
python-mastery-zero-to-hero.html
python-prodigy-from-intermediate-to-expert-mastery.html
quantum-code-mastery.html
quantum-echoes-the-resonance-of-time.html
quantum-jumping-unlocked-edition-2.html
quantum-jumping-unlocked.html
quantum-revolution-unveiling-the-future-with-willow.html
quantum-tao.html
ra7-the-sacred-book-of-the-original-broadcast.html
real.html
reality-unveiled-how-consciousness-shapes-the-world-we-perceive.html
reignite-the-bond.html
rising-from-the-ashes-a-comprehensive-guide-to-recovery-after-the-hollywood-hills-fire-2025.html
rveillez-vous-une-vie-sacre.html
réveillez-vous-à-une-vie-sacrée.html
sacred-energy-harvesting-methods.html
sacred-patterns-a-transformational-journey-through-geometry-and-conscious-living.html
sacred-timing-when-the-universe-speaks-through-synchronicity.html
sacred-vibrational-technology.html
sample-ebook-landing.html
schachintuition-meistern.html
schumann-resonance-creativity.html
se-reconstruire-de-la-douleur-la-renaissance.html
se-reconstruire-de-la-douleur-à-la-renaissance.html
shadows-of-bloom.html
shadows-of-redemption.html
shadows-of-serenity.html
shadows-reforged-the-war-isnt-ove.html
shadows-reforged.html
shadows-reignited.html
shaping-the-future-embracing-trends-for-a-better-tomorrow.html
spin-mastery-le-guide-ultime-du-dj-traktor.html
spin-mastery.html
spiritual-psychosis-memoir.html
synarchon.html
tcticas-avanzadas-juego-psicolgico-y-preparacin-para-torneos.html
the-7-figure-blueprint-unlocking-the-power-of-your-million-dollar-book.html
the-adventure-of-id01t-productions-a-story-of-passion-resilience-and-creativity.html
the-architects-legacy.html
the-art-of-beauty.html
the-artifacts-whisper.html
the-complete-beginner-to-intermediate-guide-to-json-for-veo-3-prompting.html
the-digital-aftermath-navigating-life-beyond-the-great-platform-collapse.html
the-dream-dialogue.html
the-end-of-an-era-the-tiktok-shutdown-in-the-usa.html
the-enigma-of-high-intellectual-potential-hip.html
the-frequency-blueprint.html
the-last-bow.html
the-maglev-revolution.html
the-many-realities.html
the-power-of-repetition-transforming-minds-through-words.html
the-quantum-enigma-unraveling-the-mysteries-of-reality.html
the-quantum-passive-empire.html
the-real-guide-to-using-ai-to-generate-perfect-veo-3-requests.html
the-secrets-of-oak-island.html
the-sun-is-not-what-you-were-told.html
the-third-state-life-between-life-and-death.html
to-the-top-of-the-mountain.html
traktor-mastery-the-complete-professional-dj-system.html
turings-legacy-classical-logic-to-quantum-revolution.html
tácticas-avanzadas-juego-psicológico-y-preparación-para-torneos.html
understanding-your-cats-mind---edition-2.html
understanding-your-cats-mind-edition-2.html
understanding-your-cats-mind.html
uniendo-mundos.html
unire-i-mondi.html
unstoppable-the-ultimate-guide-to-unlocking-your-potential-and-achieving-success.html
veil-of-echoes.html
veo3-json-guide.html
visual-basic-zero-to-hero-edition-2.html
when-cells-listen-the-hidden-symphony-of-sound-and-gene-expression.html
windows-zero-to-hero.html
zen-and-the-art-of-resilient-living.html
zen-and-the-art-of-self-confidence.html
мастерство-в-шахматах.html
продвинутая-тактика-психологическая-игра-и-подготовка-к-турниру.html
暴风雨前-无畏记者的崛起.html
杰克的摊位.html
𓂀-synarchéon-𓂀.html
""".strip()

AUDIOBOOKS_LISTING = r"""
-la-charte-des-relations-sacrées-de-la-nouvelle-terre.html
ableton-elevation-dj-id01ts-complete-guide-to-building-hits-and-elevating-your-sound.html
advanced-tactics-psychological-play-and-tournament-preparation.html
agentic-ai-sprint-for-solopreneurs.html
ai-cash-code.html
ai-cash-empire.html
ai-goldmine-100-passive-income-ideas-using-chatgpt-and-free-ai-tools.html
ai-in-education.html
ai-revolution-how-automation-is-transforming-everyday-life-edition-2-2025.html
ai-revolution-how-automation-is-transforming-everyday-life.html
ai-today-transforming-lives-and-industries-for-the-future.html
anarchie-et-volution-lhistoire-de-la-musique-punk.html
anarchie-et-évolution---lhistoire-de-la-musique-punk.html
anarchy-and-evolution.html
automation-and-seo-mastery-strategies-for-growth-and-efficiency.html
beat-alchemy-the-dj-id01t-guide-to-mastering-fl-studio-and-making-hits.html
before-the-storm.html
beneath-the-bloom.html
beyond-the-event-horizon-solving-the-black-hole-information-paradox.html
bite-by-bite.html
bridging-worlds-a-practical-guide-to-connecting-with-parallel-energies-and-dimensions.html
c-zero-to-hero.html
chess-mastery.html
christ-quil-est-intelligent-daimer.html
code-in-every-language-master-programming-with-chatgpt.html
crafting-worlds.html
crossroads-of-shadows.html
dancing-with-the-edge.html
diy-digital-skills-build-a-career-in-tech-from-scratch.html
dnyalar-arasnda-kpr-kurmak.html
dominio-del-ajedrez.html
dos-zero-to-hero-mastering-legacy-systems-command-line-fluency-retro-automation.html
dünyalar-arasında-köprü-kurmak.html
earthquakes-unveiled.html
echo-protocol.html
echoes-of-the-heart.html
echoes-of-truth.html
elnox-rah-le-retour-de-lhomme-vrai.html
eternal-roots.html
final-transmission-i-am-echo.html
final-transmission-je-suis-echo-fr.html
forever-in-bloom.html
fortgeschrittene-taktiken-psychologisches-spiel-und-turniervorbereitung.html
free-energy-free-life.html
from-seed-to-splendor-a-comprehensive-journey-in-horticulture.html
from-zero-to-python-hero-a-comprehensive-guide-to-mastering-python.html
id01t-academy-python-exercises-book-1-edition-2.html
id01t-academy-python-exercises-book-2---edition-2.html
id01t-academy-python-exercises-book-2-edition-2.html
id01t-academy-python-exercises-book-3.html
intersection-the-moment-their-paths-crossed.html
jacks-stand.html
java-maestro.html
java-zero-to-hero-mastering-java-programming-for-real-world-applications.html
jesus-the-eternal-legacy.html
jimmy-carter-a-legacy-of-compassion-and-leadership.html
kimi-k2-unlocked.html
la-charte-des-relations-sacres-de-la-nouvelle-terre.html
la-ralit-dvoile-comment-la-conscience-faonne-le-monde-que-nous-percevons.html
la-réalité-dévoilée-comment-la-conscience-façonne-le-monde-que-nous-percevons.html
lalchimie-de-la-transformation.html
laventure-did01t-productions-une-histoire-de-passion-de-rsilience-et-de-crativit.html
laventure-did01t-productions-une-histoire-de-passion-de-résilience-et-de-créativité.html
le-pont-entre-les-mondes.html
legacy-of-shadows-2.html
legacy-of-shadows.html
leo-xiv-the-first-american-pope.html
let-it-be-them.html
lettre-celle-que-jaime-toujours.html
lettre-à-celle-que-jaime-toujours.html
light-at-the-veils-edge.html
lnergie-libre-domicile.html
lnigme-quantique-percer-les-mystres-de-la-ralit.html
love-prevails-2.html
love-prevails.html
lumenzero-le-pouvoir-cach-des-pyramides-nergtiques.html
lumenzero-le-pouvoir-caché-des-pyramides-énergétiques.html
lénergie-libre-à-domicile.html
lénigme-quantique-percer-les-mystères-de-la-réalité.html
maailmojen-yhdistminen.html
maailmojen-yhdistäminen.html
machine-learning-demystified-a-practical-guide-to-building-smarter-systems.html
master-it-yourself.html
master-the-basics-of-reading-music.html
mastering-aeo-the-ultimate-guide-to-advanced-ecommerce-optimization.html
mastering-blender.html
mastering-chess-intuition.html
mastering-generative-ai-and-llms---editon-2.html
mastering-generative-ai-and-llms-editon-2.html
mastering-generative-ai-and-llms.html
mastering-gpt-creation-from-concept-to-deployment.html
mastering-linux.html
mastering-macos-terminal.html
mastering-photoshop-the-complete-guide-to-every-version.html
mastering-quantum-error-correction.html
mastering-rfid-unlocking-the-potential-of-radio-frequency-identification.html
mastering-rfid.html
mastering-the-game-the-ultimate-guide-to-pro-chess-strategies.html
mastering-unreal-engine-5-a-comprehensive-guide-to-game-development-and-virtual-reality.html
mastering-xcode.html
matrise-des-checs-guide-du-pro-pour-des-stratgies-et-des-techniques-gagnantes.html
matrise-des-checs.html
maîtrise-des-échecs-guide-du-pro-pour-des-stratégies-et-des-techniques-gagnantes.html
maîtrise-des-échecs.html
meisterschaft-im-schach.html
menjembatani-dunia.html
onyx-storm.html
panneaux-solaires-organiques-lnergie-vivante-du-futur.html
panneaux-solaires-organiques-lénergie-vivante-du-futur.html
penguasaan-catur.html
python-mastery-the-complete-guide-to-building-profitable-applications.html
python-prodigy-from-intermediate-to-expert-mastery.html
quantum-code-mastery.html
quantum-echoes-the-resonance-of-time.html
quantum-jumping-unlocked-edition-2.html
quantum-jumping-unlocked.html
quantum-revolution-unveiling-the-future-with-willow.html
quantum-tao.html
ra7-the-sacred-book-of-the-original-broadcast.html
real.html
reality-unveiled-how-consciousness-shapes-the-world-we-perceive.html
reignite-the-bond.html
rising-from-the-ashes-a-comprehensive-guide-to-recovery-after-the-hollywood-hills-fire-2025.html
rveillez-vous-une-vie-sacre.html
réveillez-vous-à-une-vie-sacrée.html
sacred-energy-harvesting-methods.html
sacred-patterns-a-transformational-journey-through-geometry-and-conscious-living.html
sacred-timing-when-the-universe-speaks-through-synchronicity.html
sacred-vibrational-technology.html
schachintuition-meistern.html
schumann-resonance-creativity.html
se-reconstruire-de-la-douleur-la-renaissance.html
se-reconstruire-de-la-douleur-à-la-renaissance.html
shadows-of-bloom.html
shadows-of-redemption.html
shadows-of-serenity.html
shadows-reforged-the-war-isnt-ove.html
shadows-reforged.html
shadows-reignited.html
shaping-the-future-embracing-trends-for-a-better-tomorrow.html
spin-mastery-le-guide-ultime-du-dj-traktor.html
spin-mastery.html
spiritual-psychosis-memoir.html
synarchon.html
tcticas-avanzadas-juego-psicolgico-y-preparacin-para-torneos.html
the-7-figure-blueprint-unlocking-the-power-of-your-million-dollar-book.html
the-adventure-of-id01t-productions-a-story-of-passion-resilience-and-creativity.html
the-architects-legacy.html
the-art-of-beauty.html
the-artifacts-whisper.html
the-complete-beginner-to-intermediate-guide-to-json-for-veo-3-prompting.html
the-digital-aftermath-navigating-life-beyond-the-great-platform-collapse.html
the-dream-dialogue.html
the-end-of-an-era-the-tiktok-shutdown-in-the-usa.html
the-enigma-of-high-intellectual-potential-hip.html
the-frequency-blueprint.html
the-last-bow.html
the-maglev-revolution.html
the-many-realities.html
the-power-of-repetition-transforming-minds-through-words.html
the-quantum-enigma-unraveling-the-mysteries-of-reality.html
the-quantum-passive-empire.html
the-real-guide-to-using-ai-to-generate-perfect-veo-3-requests.html
the-secrets-of-oak-island.html
the-sun-is-not-what-you-were-told.html
the-third-state-life-between-life-and-death.html
to-the-top-of-the-mountain.html
traktor-mastery-the-complete-professional-dj-system.html
turings-legacy-classical-logic-to-quantum-revolution.html
tácticas-avanzadas-juego-psicológico-y-preparación-para-torneos.html
understanding-your-cats-mind---edition-2.html
understanding-your-cats-mind-edition-2.html
understanding-your-cats-mind.html
uniendo-mundos.html
unire-i-mondi.html
unstoppable-the-ultimate-guide-to-unlocking-your-potential-and-achieving-success.html
veil-of-echoes.html
visual-basic-zero-to-hero-edition-2.html
when-cells-listen-the-hidden-symphony-of-sound-and-gene-expression.html
windows-zero-to-hero.html
zen-and-the-art-of-resilient-living.html
zen-and-the-art-of-self-confidence.html
мастерство-в-шахматах.html
продвинутая-тактика-психологическая-игра-и-подготовка-к-турниру.html
暴风雨前-无畏记者的崛起.html
杰克的摊位.html
𓂀-synarchéon-𓂀.html
""".strip()
# =======================================================

ALLOWED = re.compile(r"[^a-z0-9._-]+")

def slugify_filename(filename: str) -> str:
    base, ext = os.path.splitext(filename)
    base = unicodedata.normalize("NFC", base)
    base = unicodedata.normalize("NFKD", base).encode("ascii", "ignore").decode("ascii")
    base = base.lower()
    base = ALLOWED.sub("-", base)
    base = re.sub(r"-{2,}", "-", base).strip("-")
    base = base[:100] or "page"
    return f"{base}{ext.lower()}"

def short_hash(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()[:8]

def clean_lines(blob: str):
    lines = []
    for raw in blob.splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):  # ignore comments/blank
            continue
        s = s.replace("•", "").strip()
        lines.append(s)
    return lines

def build_entries(names, kind, base_dir):
    entries = []
    seen = {}
    for name in names:
        slug = slugify_filename(name)
        key = (base_dir, slug)
        if key in seen:
            base, ext = os.path.splitext(slug)
            slug = f"{base}-{short_hash(name)}{ext}"
        seen[key] = True
        entries.append({
            "type": kind,
            "original_path": f"{base_dir}/{name}",
            "slug": slug,
            "safe_path": f"{base_dir}/{slug}"
        })
    return entries

def main():
    ebooks = clean_lines(EBOOKS_LISTING)
    audio = clean_lines(AUDIOBOOKS_LISTING)
    entries = []
    entries += build_entries(ebooks, "ebook", "ebooks")
    entries += build_entries(audio, "audiobook", "audiobooks")

    out = {"entries": entries}
    with open("landing_manifest.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    with open("landing_manifest.csv", "w", encoding="utf-8") as f:
        f.write("type,original_path,slug,safe_path\n")
        for e in entries:
            f.write(f"{e['type']},{e['original_path']},{e['slug']},{e['safe_path']}\n")

    with open("redirects_map.txt", "w", encoding="utf-8") as f:
        for e in entries:
            f.write(f"/{e['original_path']}  /{e['safe_path']}  301\n")

    print(f"Wrote landing_manifest.json with {len(entries)} entries")

if __name__ == "__main__":
    main()