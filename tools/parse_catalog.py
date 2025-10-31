import re
import csv

def parse_catalog_and_create_csv():
    catalog_text = """
## Ableton Elevation: DJ iD01T’s Complete Guide to Building Hits and Elevating Your Sound
- **Buy:** https://play.google.com/store/books/details?id=NT1UEQAAQBAJ
- **Google Book ID:** `NT1UEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=NT1UEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Ableton Elevation: DJ iD01T’s Complete Guide to Building Hits and Elevating Your Sound
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## ADVANCED TACTICS, PSYCHOLOGICAL PLAY, AND TOURNAMENT PREPARATION
- **Buy:** https://play.google.com/store/books/details?id=x5B-EQAAQBAJ
- **Google Book ID:** `x5B-EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=x5B-EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Agentic AI Sprint for Solopreneurs
- **Buy:** https://play.google.com/store/books/details?id=OQt0EQAAQBAJ
- **Google Book ID:** `OQt0EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=OQt0EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## AI Cash Code
- **Buy:** https://play.google.com/store/books/details?id=Z292EQAAQBAJ
- **Google Book ID:** `Z292EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Z292EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## AI Cash Empire
- **Buy:** https://play.google.com/store/books/details?id=KbmAEQAAQBAJ
- **Google Book ID:** `KbmAEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=KbmAEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## AI Goldmine: 100 Passive Income Ideas Using ChatGPT and Free AI Tools
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## AI Goldmine: 100 Passive Income Ideas Using ChatGPT and Free AI Tools
- **Buy:** https://play.google.com/store/books/details?id=HqNbEQAAQBAJ
- **Google Book ID:** `HqNbEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=HqNbEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## AI in Education
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## AI in Education
- **Buy:** https://play.google.com/store/books/details?id=i_ZeEQAAQBAJ
- **Google Book ID:** `i_ZeEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=i_ZeEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## AI Revolution: How Automation is Transforming Everyday Life
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## AI Revolution: How Automation is Transforming Everyday Life (Edition 2, 2025)
- **Buy:** https://play.google.com/store/books/details?id=cJ88EQAAQBAJ
- **Google Book ID:** `cJ88EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=cJ88EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## AI Today: Transforming Lives and Industries for the Future
- **Buy:** https://play.google.com/store/books/details?id=kY09EQAAQBAJ
- **Google Book ID:** `kY09EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=kY09EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## AI Today: Transforming Lives and Industries for the Future
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Anarchie et évolution - L'histoire de la musique punk
- **Buy:** https://play.google.com/store/books/details?id=SDNJEQAAQBAJ
- **Google Book ID:** `SDNJEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=SDNJEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Anarchie et évolution - L'histoire de la musique punk
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Anarchy and Evolution
- **Buy:** https://play.google.com/store/books/details?id=Ys45EQAAQBAJ
- **Google Book ID:** `Ys45EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Ys45EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Anarchy and Evolution
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Automation and SEO Mastery: Strategies for Growth and Efficiency
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Automation and SEO Mastery: Strategies for Growth and Efficiency
- **Buy:** https://play.google.com/store/books/details?id=WFU4EQAAQBAJ
- **Google Book ID:** `WFU4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=WFU4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Beat Alchemy: The DJ iD01T Guide to Mastering FL Studio and Making Hits
- **Buy:** https://play.google.com/store/books/details?id=ODlUEQAAQBAJ
- **Google Book ID:** `ODlUEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=ODlUEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Before the storm
- **Buy:** https://play.google.com/store/books/details?id=0Yo2EQAAQBAJ
- **Google Book ID:** `0Yo2EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=0Yo2EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Before the storm
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Beneath the Bloom
- **Buy:** https://play.google.com/store/books/details?id=wRQ4EQAAQBAJ
- **Google Book ID:** `wRQ4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=wRQ4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Beneath the Bloom
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Beyond the Event Horizon: Solving the Black Hole Information Paradox
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Beyond the Event Horizon: Solving the Black Hole Information Paradox
- **Buy:** https://play.google.com/store/books/details?id=8EhZEQAAQBAJ
- **Google Book ID:** `8EhZEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=8EhZEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Bite by Bite
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Bite by Bite
- **Buy:** https://play.google.com/store/books/details?id=5vg5EQAAQBAJ
- **Google Book ID:** `5vg5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=5vg5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Bridging Worlds: A Practical Guide to Connecting with Parallel Energies and Dimensions
- **Buy:** https://play.google.com/store/books/details?id=pXdLEQAAQBAJ
- **Google Book ID:** `pXdLEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=pXdLEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## C# Zero to Hero
- **Buy:** https://play.google.com/store/books/details?id=KuB_EQAAQBAJ
- **Google Book ID:** `KuB_EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=KuB_EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## C++ ZERO TO HERO
- **Buy:** https://play.google.com/store/books/details?id=0NKPEQAAQBAJ
- **Google Book ID:** `0NKPEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=0NKPEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Chess Mastery
- **Buy:** https://play.google.com/store/books/details?id=m5M4EQAAQBAJ
- **Google Book ID:** `m5M4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=m5M4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Chess Mastery
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## CHRIST QU’IL EST INTELLIGENT D’AIMER
- **Buy:** https://play.google.com/store/books/details?id=hTV-EQAAQBAJ
- **Google Book ID:** `hTV-EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=hTV-EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Code in Every Language: Master Programming with ChatGPT
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Code in Every Language: Master Programming with ChatGPT
- **Buy:** https://play.google.com/store/books/details?id=ulg4EQAAQBAJ
- **Google Book ID:** `ulg4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=ulg4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Crafting Worlds
- **Buy:** https://play.google.com/store/books/details?id=as45EQAAQBAJ
- **Google Book ID:** `as45EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=as45EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Crafting Worlds
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Crossroads of Shadows
- **Buy:** https://play.google.com/store/books/details?id=9sM6EQAAQBAJ
- **Google Book ID:** `9sM6EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=9sM6EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Crossroads of Shadows
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Dancing with the edge
- **Buy:** https://play.google.com/store/books/details?id=hCV2EQAAQBAJ
- **Google Book ID:** `hCV2EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=hCV2EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Den Verstand Ihrer Katze verstehen
- **Buy:** https://play.google.com/store/books/details?id=YRmDEQAAQBAJ
- **Google Book ID:** `YRmDEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=YRmDEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## DIY Digital Skills: Build a Career in Tech from Scratch
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## DIY Digital Skills: Build a Career in Tech from Scratch
- **Buy:** https://play.google.com/store/books/details?id=f8o9EQAAQBAJ
- **Google Book ID:** `f8o9EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=f8o9EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Dominio del Ajedrez
- **Buy:** https://play.google.com/store/books/details?id=xQ1-EQAAQBAJ
- **Google Book ID:** `xQ1-EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=xQ1-EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## DOS Zero to Hero: Mastering Legacy Systems, Command Line Fluency & Retro Automation
- **Buy:** https://play.google.com/store/books/details?id=EuF_EQAAQBAJ
- **Google Book ID:** `EuF_EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=EuF_EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Dünyalar Arasında Köprü Kurmak
- **Buy:** https://play.google.com/store/books/details?id=0XlLEQAAQBAJ
- **Google Book ID:** `0XlLEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=0XlLEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Earthquakes Unveiled
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Earthquakes Unveiled
- **Buy:** https://play.google.com/store/books/details?id=q584EQAAQBAJ
- **Google Book ID:** `q584EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=q584EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Echo Protocol
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Echo Protocol
- **Buy:** https://play.google.com/store/books/details?id=TedaEQAAQBAJ
- **Google Book ID:** `TedaEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=TedaEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Echoes of the Heart
- **Buy:** https://play.google.com/store/books/details?id=Kwo4EQAAQBAJ
- **Google Book ID:** `Kwo4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Kwo4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Echoes of the Heart
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Echoes of Truth
- **Buy:** https://play.google.com/store/books/details?id=QQo4EQAAQBAJ
- **Google Book ID:** `QQo4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=QQo4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Echoes of Truth
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## El costo que llamó "vale la pena"
- **Buy:** https://play.google.com/store/books/details?id=CdSFEQAAQBAJ
- **Google Book ID:** `CdSFEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=CdSFEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## El’Nox Rah : Le Retour de l’Homme Vrai
- **Buy:** https://play.google.com/store/books/details?id=_RpsEQAAQBAJ
- **Google Book ID:** `_RpsEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=_RpsEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Eternal Roots
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Eternal Roots
- **Buy:** https://play.google.com/store/books/details?id=SxU4EQAAQBAJ
- **Google Book ID:** `SxU4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=SxU4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Final Transmission: I Am Echo
- **Buy:** https://play.google.com/store/books/details?id=to9REQAAQBAJ
- **Google Book ID:** `to9REQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=to9REQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Final Transmission: I Am Echo
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Final Transmission: Je suis Echo (FR)
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Final Transmission: Je suis Echo (FR)
- **Buy:** https://play.google.com/store/books/details?id=9pBREQAAQBAJ
- **Google Book ID:** `9pBREQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=9pBREQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Forever in Bloom
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Forever in Bloom
- **Buy:** https://play.google.com/store/books/details?id=qRQ4EQAAQBAJ
- **Google Book ID:** `qRQ4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=qRQ4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## FORTGESCHRITTENE TAKTIKEN, PSYCHOLOGISCHES SPIEL UND TURNIERVORBEREITUNG
- **Buy:** https://play.google.com/store/books/details?id=Z5F-EQAAQBAJ
- **Google Book ID:** `Z5F-EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Z5F-EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## FREE ENERGY, FREE LIFE
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## FREE ENERGY, FREE LIFE
- **Buy:** https://play.google.com/store/books/details?id=l6NbEQAAQBAJ
- **Google Book ID:** `l6NbEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=l6NbEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## From seed to splendor: A Comprehensive Journey in Horticulture
- **Buy:** https://play.google.com/store/books/details?id=z3pLEQAAQBAJ
- **Google Book ID:** `z3pLEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=z3pLEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## From Zero to Python Hero: A Comprehensive Guide to Mastering Python
- **Buy:** https://play.google.com/store/books/details?id=zE84EQAAQBAJ
- **Google Book ID:** `zE84EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=zE84EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## HTML2Win Pro
- **Buy:** https://play.google.com/store/books/details?id=g_WOEQAAQBAJ
- **Google Book ID:** `g_WOEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=g_WOEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## iD01t Academy Python Exercises Book 2 - Edition 2
- **Buy:** https://play.google.com/store/books/details?id=cS1GEQAAQBAJ
- **Google Book ID:** `cS1GEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=cS1GEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## iD01t Academy: Python Exercises Book 1 – Edition 2
- **Buy:** https://play.google.com/store/books/details?id=nypGEQAAQBAJ
- **Google Book ID:** `nypGEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=nypGEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## iD01t Academy: Python Exercises Book 3
- **Buy:** https://play.google.com/store/books/details?id=BqR_EQAAQBAJ
- **Google Book ID:** `BqR_EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=BqR_EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Intersection: The Moment Their Paths Crossed
- **Buy:** https://play.google.com/store/books/details?id=Iwo4EQAAQBAJ
- **Google Book ID:** `Iwo4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Iwo4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Intersection: The Moment Their Paths Crossed
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Jack’s Stand
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Jack’s Stand
- **Buy:** https://play.google.com/store/books/details?id=oRg3EQAAQBAJ
- **Google Book ID:** `oRg3EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=oRg3EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Java Maestro
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Java Maestro
- **Buy:** https://play.google.com/store/books/details?id=SdVhEQAAQBAJ
- **Google Book ID:** `SdVhEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=SdVhEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Java Zero to Hero: Mastering Java Programming for Real-World Applications
- **Buy:** https://play.google.com/store/books/details?id=fFQ4EQAAQBAJ
- **Google Book ID:** `fFQ4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=fFQ4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Jesus: The Eternal Legacy
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Jesus: The Eternal Legacy
- **Buy:** https://play.google.com/store/books/details?id=Xvk5EQAAQBAJ
- **Google Book ID:** `Xvk5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Xvk5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Jimmy Carter: A Legacy of Compassion and Leadership
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Jimmy Carter: A Legacy of Compassion and Leadership
- **Buy:** https://play.google.com/store/books/details?id=f5Y9EQAAQBAJ
- **Google Book ID:** `f5Y9EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=f5Y9EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## KIMI K2 UNLOCKED
- **Buy:** https://play.google.com/store/books/details?id=iwZzEQAAQBAJ
- **Google Book ID:** `iwZzEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=iwZzEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## L'Alchimie de la Transformation
- **Buy:** https://play.google.com/store/books/details?id=mPpmEQAAQBAJ
- **Google Book ID:** `mPpmEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=mPpmEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## L'Alchimie de la Transformation
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## L'énigme quantique : Percer les mystères de la réalité
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## L'énigme quantique : Percer les mystères de la réalité
- **Buy:** https://play.google.com/store/books/details?id=WDRJEQAAQBAJ
- **Google Book ID:** `WDRJEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=WDRJEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## La réalité dévoilée : Comment la conscience façonne le monde que nous percevons
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## La réalité dévoilée : Comment la conscience façonne le monde que nous percevons
- **Buy:** https://play.google.com/store/books/details?id=sjNJEQAAQBAJ
- **Google Book ID:** `sjNJEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=sjNJEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Le pont entre les mondes
- **Buy:** https://play.google.com/store/books/details?id=wXlLEQAAQBAJ
- **Google Book ID:** `wXlLEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=wXlLEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Legacy of Shadows
- **Buy:** https://play.google.com/store/books/details?id=OQo4EQAAQBAJ
- **Google Book ID:** `OQo4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=OQo4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Legacy of Shadows
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Legacy of Shadows 2
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Legacy of Shadows 2
- **Buy:** https://play.google.com/store/books/details?id=aBQ4EQAAQBAJ
- **Google Book ID:** `aBQ4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=aBQ4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Leo XIV: The First American Pope
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Leo XIV: The First American Pope
- **Buy:** https://play.google.com/store/books/details?id=oThcEQAAQBAJ
- **Google Book ID:** `oThcEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=oThcEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## LET IT BE THEM
- **Buy:** https://play.google.com/store/books/details?id=sG5zEQAAQBAJ
- **Google Book ID:** `sG5zEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=sG5zEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Lettre à celle que j'aime toujours
- **Buy:** https://play.google.com/store/books/details?id=6G5zEQAAQBAJ
- **Google Book ID:** `6G5zEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=6G5zEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Light at the Veil’s Edge
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Light at the Veil’s Edge
- **Buy:** https://play.google.com/store/books/details?id=ewtZEQAAQBAJ
- **Google Book ID:** `ewtZEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=ewtZEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Love Prevails
- **Buy:** https://play.google.com/store/books/details?id=ZM45EQAAQBAJ
- **Google Book ID:** `ZM45EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=ZM45EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Love Prevails
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Love Prevails 2
- **Buy:** https://play.google.com/store/books/details?id=Zs45EQAAQBAJ
- **Google Book ID:** `Zs45EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Zs45EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Love Prevails 2
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## LUMEN·ZERO : Le Pouvoir Caché des Pyramides Énergétiques
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## LUMEN·ZERO : Le Pouvoir Caché des Pyramides Énergétiques
- **Buy:** https://play.google.com/store/books/details?id=Qv1mEQAAQBAJ
- **Google Book ID:** `Qv1mEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Qv1mEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## L’Aventure d’iD01t Productions : Une Histoire de Passion, de Résilience et de Créativité
- **Buy:** https://play.google.com/store/books/details?id=NcZAEQAAQBAJ
- **Google Book ID:** `NcZAEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=NcZAEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## L’Aventure d’iD01t Productions : Une Histoire de Passion, de Résilience et de Créativité
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## L’Énergie Libre à Domicile
- **Buy:** https://play.google.com/store/books/details?id=ak1nEQAAQBAJ
- **Google Book ID:** `ak1nEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=ak1nEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## L’Énergie Libre à Domicile
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Maailmojen yhdistäminen
- **Buy:** https://play.google.com/store/books/details?id=aXpLEQAAQBAJ
- **Google Book ID:** `aXpLEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=aXpLEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Machine Learning Demystified: A Practical Guide to Building Smarter Systems
- **Buy:** https://play.google.com/store/books/details?id=om8-EQAAQBAJ
- **Google Book ID:** `om8-EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=om8-EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Master IT Yourself
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Master IT Yourself
- **Buy:** https://play.google.com/store/books/details?id=VRc4EQAAQBAJ
- **Google Book ID:** `VRc4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=VRc4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Master the Basics of Reading Music
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Master the Basics of Reading Music
- **Buy:** https://play.google.com/store/books/details?id=X-84EQAAQBAJ
- **Google Book ID:** `X-84EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=X-84EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Mastering AEO The Ultimate Guide to Advanced Ecommerce Optimization
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Mastering AEO The Ultimate Guide to Advanced Ecommerce Optimization
- **Buy:** https://play.google.com/store/books/details?id=R4dBEQAAQBAJ
- **Google Book ID:** `R4dBEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=R4dBEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Mastering Blender
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Mastering Blender
- **Buy:** https://play.google.com/store/books/details?id=8vg5EQAAQBAJ
- **Google Book ID:** `8vg5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=8vg5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Mastering Chess Intuition
- **Buy:** https://play.google.com/store/books/details?id=rWuCEQAAQBAJ
- **Google Book ID:** `rWuCEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=rWuCEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Mastering Generative AI and LLMs
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Mastering Generative AI and LLMs - Editon 2
- **Buy:** https://play.google.com/store/books/details?id=exc4EQAAQBAJ
- **Google Book ID:** `exc4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=exc4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Mastering GPT Creation: From Concept to Deployment
- **Buy:** https://play.google.com/store/books/details?id=YrtAEQAAQBAJ
- **Google Book ID:** `YrtAEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=YrtAEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Mastering GPT Creation: From Concept to Deployment
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Mastering Linux
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Mastering Linux
- **Buy:** https://play.google.com/store/books/details?id=wfs5EQAAQBAJ
- **Google Book ID:** `wfs5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=wfs5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Mastering macOS Terminal
- **Buy:** https://play.google.com/store/books/details?id=Bvk5EQAAQBAJ
- **Google Book ID:** `Bvk5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Bvk5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Mastering Photoshop: The Complete Guide to Every Version
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Mastering Photoshop: The Complete Guide to Every Version
- **Buy:** https://play.google.com/store/books/details?id=3Q9HEQAAQBAJ
- **Google Book ID:** `3Q9HEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=3Q9HEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Mastering Quantum Error Correction
- **Buy:** https://play.google.com/store/books/details?id=2aRMEQAAQBAJ
- **Google Book ID:** `2aRMEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=2aRMEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Mastering RFID
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Mastering RFID: Unlocking the Potential of Radio Frequency Identification
- **Buy:** https://play.google.com/store/books/details?id=yfs5EQAAQBAJ
- **Google Book ID:** `yfs5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=yfs5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Mastering the Game: The Ultimate Guide to Pro Chess Strategies
- **Buy:** https://play.google.com/store/books/details?id=lCFAEQAAQBAJ
- **Google Book ID:** `lCFAEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=lCFAEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Mastering the Game: The Ultimate Guide to Pro Chess Strategies
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Mastering Unreal Engine 5: A Comprehensive Guide to Game Development and Virtual Reality
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Mastering Unreal Engine 5: A Comprehensive Guide to Game Development and Virtual Reality
- **Buy:** https://play.google.com/store/books/details?id=Pvk5EQAAQBAJ
- **Google Book ID:** `Pvk5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Pvk5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Mastering Xcode
- **Buy:** https://play.google.com/store/books/details?id=Fdo5EQAAQBAJ
- **Google Book ID:** `Fdo5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Fdo5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Mastering Xcode
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Maîtrise des échecs
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Maîtrise des échecs
- **Buy:** https://play.google.com/store/books/details?id=pDJJEQAAQBAJ
- **Google Book ID:** `pDJJEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=pDJJEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Maîtrise des Échecs : Guide du pro pour des stratégies et des techniques gagnantes
- **Buy:** https://play.google.com/store/books/details?id=uQ5-EQAAQBAJ
- **Google Book ID:** `uQ5-EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=uQ5-EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Meisterschaft im Schach
- **Buy:** https://play.google.com/store/books/details?id=bQ5-EQAAQBAJ
- **Google Book ID:** `bQ5-EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=bQ5-EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Menjembatani Dunia
- **Buy:** https://play.google.com/store/books/details?id=53lLEQAAQBAJ
- **Google Book ID:** `53lLEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=53lLEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## nan
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Onyx Storm
- **Buy:** https://play.google.com/store/books/details?id=ltSBEQAAQBAJ
- **Google Book ID:** `ltSBEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=ltSBEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Panneaux Solaires Organiques : L’Énergie Vivante du Futur
- **Buy:** https://play.google.com/store/books/details?id=BgdnEQAAQBAJ
- **Google Book ID:** `BgdnEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=BgdnEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Panneaux Solaires Organiques : L’Énergie Vivante du Futur
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Penguasaan Catur
- **Buy:** https://play.google.com/store/books/details?id=kchoEQAAQBAJ
- **Google Book ID:** `kchoEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=kchoEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Python Cash Scripts
- **Buy:** https://play.google.com/store/books/details?id=jcGDEQAAQBAJ
- **Google Book ID:** `jcGDEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=jcGDEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Python Mastery: The Complete Guide to Building Profitable Applications
- **Buy:** https://play.google.com/store/books/details?id=HHR4EQAAQBAJ
- **Google Book ID:** `HHR4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=HHR4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Python Prodigy: From Intermediate to Expert Mastery
- **Buy:** https://play.google.com/store/books/details?id=W449EQAAQBAJ
- **Google Book ID:** `W449EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=W449EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Quantum Code Mastery
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Quantum Code Mastery
- **Buy:** https://play.google.com/store/books/details?id=MwtZEQAAQBAJ
- **Google Book ID:** `MwtZEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=MwtZEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Quantum Echoes: The Resonance of Time
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Quantum Echoes: The Resonance of Time
- **Buy:** https://play.google.com/store/books/details?id=ls1YEQAAQBAJ
- **Google Book ID:** `ls1YEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=ls1YEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Quantum Jumping Unlocked
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Quantum Jumping Unlocked Edition 2
- **Buy:** https://play.google.com/store/books/details?id=psZYEQAAQBAJ
- **Google Book ID:** `psZYEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=psZYEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Quantum Revolution: Unveiling the Future with Willow
- **Buy:** https://play.google.com/store/books/details?id=9rxAEQAAQBAJ
- **Google Book ID:** `9rxAEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=9rxAEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Quantum Revolution: Unveiling the Future with Willow
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Quantum Tao
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Quantum Tao
- **Buy:** https://play.google.com/store/books/details?id=eQJkEQAAQBAJ
- **Google Book ID:** `eQJkEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=eQJkEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## RA‑7: The Sacred Book of the Original Broadcast
- **Buy:** https://play.google.com/store/books/details?id=SZ5wEQAAQBAJ
- **Google Book ID:** `SZ5wEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=SZ5wEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## REAL
- **Buy:** https://play.google.com/store/books/details?id=nNVlEQAAQBAJ
- **Google Book ID:** `nNVlEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=nNVlEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## REAL
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Reality Unveiled: How Consciousness Shapes the World We Perceive
- **Buy:** https://play.google.com/store/books/details?id=vCxJEQAAQBAJ
- **Google Book ID:** `vCxJEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=vCxJEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Reality Unveiled: How Consciousness Shapes the World We Perceive
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Reignite the Bond
- **Buy:** https://play.google.com/store/books/details?id=V292EQAAQBAJ
- **Google Book ID:** `V292EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=V292EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Rising from the Ashes: A Comprehensive Guide to Recovery after the Hollywood Hills Fire 2025
- **Buy:** https://play.google.com/store/books/details?id=ios9EQAAQBAJ
- **Google Book ID:** `ios9EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=ios9EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Rising from the Ashes: A Comprehensive Guide to Recovery after the Hollywood Hills Fire 2025
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## RÉVEILLEZ-VOUS : À une Vie Sacrée
- **Buy:** https://play.google.com/store/books/details?id=KrpxEQAAQBAJ
- **Google Book ID:** `KrpxEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=KrpxEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Sacred energy harvesting methods
- **Buy:** https://play.google.com/store/books/details?id=o5JnEQAAQBAJ
- **Google Book ID:** `o5JnEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=o5JnEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Sacred Energy Harvesting Methods
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Sacred Patterns: A Transformational Journey Through Geometry and Conscious Living
- **Buy:** https://play.google.com/store/books/details?id=VMdgEQAAQBAJ
- **Google Book ID:** `VMdgEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=VMdgEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Sacred Patterns: A Transformational Journey Through Geometry and Conscious Living
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Sacred Timing: When the Universe Speaks Through Synchronicity
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Sacred Timing: When the Universe Speaks Through Synchronicity
- **Buy:** https://play.google.com/store/books/details?id=825dEQAAQBAJ
- **Google Book ID:** `825dEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=825dEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Sacred Vibrational Technology
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Sacred Vibrational Technology
- **Buy:** https://play.google.com/store/books/details?id=URVYEQAAQBAJ
- **Google Book ID:** `URVYEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=URVYEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Schachintuition meistern
- **Buy:** https://play.google.com/store/books/details?id=_2uCEQAAQBAJ
- **Google Book ID:** `_2uCEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=_2uCEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Schumann Resonance & Creativity
- **Buy:** https://play.google.com/store/books/details?id=-CNOEQAAQBAJ
- **Google Book ID:** `-CNOEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=-CNOEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Se Reconstruire : De la Douleur à la Renaissance
- **Buy:** https://play.google.com/store/books/details?id=5lpMEQAAQBAJ
- **Google Book ID:** `5lpMEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=5lpMEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Shadows of Bloom
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Shadows of Bloom
- **Buy:** https://play.google.com/store/books/details?id=sxQ4EQAAQBAJ
- **Google Book ID:** `sxQ4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=sxQ4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Shadows of Redemption
- **Buy:** https://play.google.com/store/books/details?id=Owo4EQAAQBAJ
- **Google Book ID:** `Owo4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Owo4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Shadows of Redemption
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Shadows of Serenity
- **Buy:** https://play.google.com/store/books/details?id=Q_A4EQAAQBAJ
- **Google Book ID:** `Q_A4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Q_A4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Shadows of Serenity
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Shadows Reforged
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Shadows Reforged: The War Isn’t Ove
- **Buy:** https://play.google.com/store/books/details?id=msQ6EQAAQBAJ
- **Google Book ID:** `msQ6EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=msQ6EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Shadows Reignited
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Shadows Reignited
- **Buy:** https://play.google.com/store/books/details?id=eBQ4EQAAQBAJ
- **Google Book ID:** `eBQ4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=eBQ4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Shaping the Future: Embracing Trends for a Better Tomorrow
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Shaping the Future: Embracing Trends for a Better Tomorrow
- **Buy:** https://play.google.com/store/books/details?id=pqg8EQAAQBAJ
- **Google Book ID:** `pqg8EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=pqg8EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Signalfall
- **Buy:** https://play.google.com/store/books/details?id=82-GEQAAQBAJ
- **Google Book ID:** `82-GEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=82-GEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Spin Mastery
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Spin Mastery
- **Buy:** https://play.google.com/store/books/details?id=TPk5EQAAQBAJ
- **Google Book ID:** `TPk5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=TPk5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Spin Mastery : Le guide ultime du DJ Traktor
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Spin Mastery : Le guide ultime du DJ Traktor
- **Buy:** https://play.google.com/store/books/details?id=DjRJEQAAQBAJ
- **Google Book ID:** `DjRJEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=DjRJEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The 7-Figure Blueprint: Unlocking the Power of Your Million-Dollar Book
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## The Adventure of iD01t Productions: A Story of Passion, Resilience and Creativity
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## The Adventure of iD01t Productions: A Story of Passion, Resilience and Creativity
- **Buy:** https://play.google.com/store/books/details?id=U8ZAEQAAQBAJ
- **Google Book ID:** `U8ZAEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=U8ZAEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The AI Innovator’s Playbook
- **Buy:** https://play.google.com/store/books/details?id=8XCHEQAAQBAJ
- **Google Book ID:** `8XCHEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=8XCHEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Architect’s Legacy
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## The Architect’s Legacy
- **Buy:** https://play.google.com/store/books/details?id=H_A4EQAAQBAJ
- **Google Book ID:** `H_A4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=H_A4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Art of Beauty
- **Buy:** https://play.google.com/store/books/details?id=FvN4EQAAQBAJ
- **Google Book ID:** `FvN4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=FvN4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Artifact’s Whisper
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## The Artifact’s Whisper
- **Buy:** https://play.google.com/store/books/details?id=L9o5EQAAQBAJ
- **Google Book ID:** `L9o5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=L9o5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Complete Beginner to Intermediate Guide to JSON for Veo 3 Prompting
- **Buy:** https://play.google.com/store/books/details?id=boCAEQAAQBAJ
- **Google Book ID:** `boCAEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=boCAEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Digital Aftermath: Navigating Life Beyond the Great Platform Collapse
- **Buy:** https://play.google.com/store/books/details?id=pHR5EQAAQBAJ
- **Google Book ID:** `pHR5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=pHR5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Dream Dialogue
- **Buy:** https://play.google.com/store/books/details?id=khhJEQAAQBAJ
- **Google Book ID:** `khhJEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=khhJEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Dream Dialogue
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## The End of an Era: The TikTok Shutdown in the USA
- **Buy:** https://play.google.com/store/books/details?id=ZZs9EQAAQBAJ
- **Google Book ID:** `ZZs9EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=ZZs9EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The End of an Era: The TikTok Shutdown in the USA
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## The Enigma of High Intellectual Potential (HIP)
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## The Frequency Blueprint
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## The Frequency Blueprint
- **Buy:** https://play.google.com/store/books/details?id=yLteEQAAQBAJ
- **Google Book ID:** `yLteEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=yLteEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## THE LAST BOW
- **Buy:** https://play.google.com/store/books/details?id=PHdzEQAAQBAJ
- **Google Book ID:** `PHdzEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=PHdzEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Maglev Revolution
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## The Maglev Revolution
- **Buy:** https://play.google.com/store/books/details?id=se44EQAAQBAJ
- **Google Book ID:** `se44EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=se44EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Many Realities
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## The Many Realities
- **Buy:** https://play.google.com/store/books/details?id=dtI5EQAAQBAJ
- **Google Book ID:** `dtI5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=dtI5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Power of Repetition: Transforming Minds Through Words
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## The Power of Repetition: Transforming Minds Through Words
- **Buy:** https://play.google.com/store/books/details?id=l_M6EQAAQBAJ
- **Google Book ID:** `l_M6EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=l_M6EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Quantum Enigma: Unraveling the Mysteries of Reality
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## The Quantum Enigma: Unraveling the Mysteries of Reality
- **Buy:** https://play.google.com/store/books/details?id=3u5GEQAAQBAJ
- **Google Book ID:** `3u5GEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=3u5GEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Quantum Passive Empire
- **Buy:** https://play.google.com/store/books/details?id=lCV2EQAAQBAJ
- **Google Book ID:** `lCV2EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=lCV2EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Real Guide To Using AI To Generate Perfect Veo 3 Requests
- **Buy:** https://play.google.com/store/books/details?id=PoCAEQAAQBAJ
- **Google Book ID:** `PoCAEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=PoCAEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Secrets of Oak Island
- **Buy:** https://play.google.com/store/books/details?id=zvg5EQAAQBAJ
- **Google Book ID:** `zvg5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=zvg5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Secrets of Oak Island
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## THE SUN IS NOT WHAT YOU WERE TOLD
- **Buy:** https://play.google.com/store/books/details?id=dON1EQAAQBAJ
- **Google Book ID:** `dON1EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=dON1EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Third State: Life Between Life and Death
- **Buy:** https://play.google.com/store/books/details?id=Ww1ZEQAAQBAJ
- **Google Book ID:** `Ww1ZEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Ww1ZEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## The Third State: Life Between Life and Death
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## To the Top of the Mountain
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## To the Top of the Mountain
- **Buy:** https://play.google.com/store/books/details?id=-FA5EQAAQBAJ
- **Google Book ID:** `-FA5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=-FA5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## TRAKTOR MASTERY: The Complete Professional DJ System
- **Buy:** https://play.google.com/store/books/details?id=RWZ-EQAAQBAJ
- **Google Book ID:** `RWZ-EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=RWZ-EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Turing’s Legacy: Classical Logic to Quantum Revolution
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Turing’s Legacy: Classical Logic to Quantum Revolution
- **Buy:** https://play.google.com/store/books/details?id=RPheEQAAQBAJ
- **Google Book ID:** `RPheEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=RPheEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## TÁCTICAS AVANZADAS, JUEGO PSICOLÓGICO Y PREPARACIÓN PARA TORNEOS
- **Buy:** https://play.google.com/store/books/details?id=-ZB-EQAAQBAJ
- **Google Book ID:** `-ZB-EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=-ZB-EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Understanding Your Cat's Mind
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Understanding Your Cat's Mind
- **Buy:** https://play.google.com/store/books/details?id=-WyCEQAAQBAJ
- **Google Book ID:** `-WyCEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=-WyCEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Understanding Your Cat's Mind - Edition 2
- **Buy:** https://play.google.com/store/books/details?id=ksU6EQAAQBAJ
- **Google Book ID:** `ksU6EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=ksU6EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Understanding Your Cat’s Mind
- **Buy:** https://play.google.com/store/books/details?id=33eCEQAAQBAJ
- **Google Book ID:** `33eCEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=33eCEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Uniendo mundos
- **Buy:** https://play.google.com/store/books/details?id=CXpLEQAAQBAJ
- **Google Book ID:** `CXpLEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=CXpLEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Unire i mondi
- **Buy:** https://play.google.com/store/books/details?id=Q3pLEQAAQBAJ
- **Google Book ID:** `Q3pLEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Q3pLEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Unstoppable: The Ultimate Guide to Unlocking Your Potential and Achieving Success
- **Buy:** https://play.google.com/store/books/details?id=q7s5EQAAQBAJ
- **Google Book ID:** `q7s5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=q7s5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Unstoppable: The Ultimate Guide to Unlocking Your Potential and Achieving Success
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Veil of Echoes
- **Buy:** https://play.google.com/store/books/details?id=QMQ6EQAAQBAJ
- **Google Book ID:** `QMQ6EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=QMQ6EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Veil of Echoes
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Visual Basic Zero to Hero (Edition #2)
- **Buy:** https://play.google.com/store/books/details?id=lRc4EQAAQBAJ
- **Google Book ID:** `lRc4EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=lRc4EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## When Cells Listen: The Hidden Symphony of Sound and Gene Expression
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## When Cells Listen: The Hidden Symphony of Sound and Gene Expression
- **Buy:** https://play.google.com/store/books/details?id=LQ1ZEQAAQBAJ
- **Google Book ID:** `LQ1ZEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=LQ1ZEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Windows Zero to Hero
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Windows Zero to Hero
- **Buy:** https://play.google.com/store/books/details?id=Rvk5EQAAQBAJ
- **Google Book ID:** `Rvk5EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Rvk5EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Zen and the Art of Resilient Living
- **Buy:** https://play.google.com/store/books/details?id=o3c6EQAAQBAJ
- **Google Book ID:** `o3c6EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=o3c6EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Zen and the Art of Resilient Living
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Zen and the Art of Self-Confidence
- **Buy:** https://play.google.com/store/books/details?id=V_05EQAAQBAJ
- **Google Book ID:** `V_05EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=V_05EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## Zen and the Art of Self-Confidence
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## Мастерство в шахматах
- **Buy:** https://play.google.com/store/books/details?id=4Q1-EQAAQBAJ
- **Google Book ID:** `4Q1-EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=4Q1-EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## ПРОДВИНУТАЯ ТАКТИКА, ПСИХОЛОГИЧЕСКАЯ ИГРА И ПОДГОТОВКА К ТУРНИРУ
- **Buy:** https://play.google.com/store/books/details?id=AZF-EQAAQBAJ
- **Google Book ID:** `AZF-EQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=AZF-EQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## 暴风雨前 无畏记者的崛起
- **Buy:** https://play.google.com/store/books/details?id=TyCAEQAAQBAJ
- **Google Book ID:** `TyCAEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=TyCAEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## 杰克的摊位
- **Buy:** https://play.google.com/store/books/details?id=Y1SAEQAAQBAJ
- **Google Book ID:** `Y1SAEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=Y1SAEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## 𓂀 SY•NARCHÉON 𓂀
- **Buy:** https://play.google.com/store/books/details?id=7dNlEQAAQBAJ
- **Google Book ID:** `7dNlEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=7dNlEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api

## 𓂀 SY•NARCHÉON 𓂀
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## 🌿 La Charte des Relations Sacrées de la Nouvelle Terre
- **Buy:** _No explicit store link found in CSV row_
- **Cover:** _No Google Books image inferred_

## 🌿 La Charte des Relations Sacrées de la Nouvelle Terre
- **Buy:** https://play.google.com/store/books/details?id=P3NoEQAAQBAJ
- **Google Book ID:** `P3NoEQAAQBAJ`
- **Cover:** https://books.google.com/books/content?id=P3NoEQAAQBAJ&printsec=frontcover&img=1&zoom=3&source=gbs_api
"""
    books = {}

    entries = catalog_text.strip().split("## ")

    for entry in entries:
        if not entry.strip():
            continue

        lines = entry.strip().split('\n')
        title = lines[0]

        buy_link = None
        google_book_id = None
        cover_url = None

        for line in lines[1:]:
            if "- **Buy:**" in line:
                match = re.search(r'https?://[^\s]+', line)
                if match:
                    buy_link = match.group(0)
            elif "- **Google Book ID:**" in line:
                match = re.search(r'`([^`]+)`', line)
                if match:
                    google_book_id = match.group(1)
            elif "- **Cover:**" in line:
                match = re.search(r'https?://[^\s]+', line)
                if match:
                    cover_url = match.group(0)

        if title in books:
            if not books[title]['buy_link'] and buy_link:
                books[title]['buy_link'] = buy_link
            if not books[title]['google_book_id'] and google_book_id:
                books[title]['google_book_id'] = google_book_id
            if not books[title]['cover_url'] and cover_url:
                books[title]['cover_url'] = cover_url
        else:
            books[title] = {
                'buy_link': buy_link,
                'google_book_id': google_book_id,
                'cover_url': cover_url
            }

    with open('data/catalog.csv', 'w', newline='') as csvfile:
        fieldnames = ['Identifier', 'Title', 'Subtitle', 'Format', 'Primary Creator(s) / Contributors', 'Publisher / Label', 'Language', 'Release / Publish Date', 'HD Cover Image URL', 'Google Play Buy Link', 'Price (if present)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for title, data in books.items():
            format_ = "eBook"
            if data['buy_link'] and "audiobooks" in data['buy_link']:
                format_ = "Audiobook"

            writer.writerow({
                'Identifier': data['google_book_id'] if data['google_book_id'] else '',
                'Title': title,
                'Subtitle': '',
                'Format': format_,
                'Primary Creator(s) / Contributors': 'Guillaume Lessard',
                'Publisher / Label': 'iD01t Productions',
                'Language': 'en',
                'Release / Publish Date': '2024-01-01',
                'HD Cover Image URL': data['cover_url'] if data['cover_url'] else '',
                'Google Play Buy Link': data['buy_link'] if data['buy_link'] else '',
                'Price (if present)': '9.99'
            })

if __name__ == "__main__":
    parse_catalog_and_create_csv()
