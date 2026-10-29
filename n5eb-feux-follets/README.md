# Les Feux Follets de Kawabe

One-shot pour **Foundry VTT v13/v14** et le système **N5eB** (Naruto 5e).
Mission de rang C pour **5 genin de niveau 1**, environ 3 à 4 heures de jeu, pensée pour des joueurs et un MJ débutants.

> Le petit village de pêcheurs de Kawabe est hanté chaque nuit par un « fantôme du lac ». Les genin découvrent que le fantôme est en réalité un ninja déserteur de Kiri, payé par un marchand avide pour faire fuir les habitants et s'emparer d'un trésor caché sur une île.

## Contenu

| Type | Contenu |
|---|---|
| Prétirés | Akimichi Bunta (taijutsu), Hibana Kaito (ninjutsu, feu), Nara Shizuka (éclaireur, ombres), Fûma Tsumugi (armes), Sakuraba Momo (médecin) |
| PNJ | Inaba Shûhei (chûnin), la cheffe Oume, Sachi, Tetsu, Genji, Ayame, Kaneda, Mosuke |
| Adversaires | Brigand de la Gorge, Tonbi Gonza, Clone d'eau, Uramaru Hisame « le Fantôme du Lac » |
| Scènes | Carte du voyage, Le Pont de la Gorge (30×20), Le village de Kawabe (40×30), L'île des Lucioles (36×30) |
| Journaux | Lisez-moi (MJ), Scénario complet, PNJ, Aides de jeu, Guide du joueur, Fiches des prétirés |
| Objets | Onigiri, talismans de luciole, senbon empoisonnés, indices, trésor, insigne |
| Table | Rumeurs de Kawabe (1d8) |

## Installation

Dans l'onglet **Modules** de la configuration de Foundry, cliquez sur **Installer un module** et utilisez cette **URL du manifeste** :

```text
https://github.com/PrevotYann/one-shots-n5eb/releases/latest/download/module.json
```

Pour une installation manuelle :

1. Téléchargez `n5eb-feux-follets.zip` depuis les [releases GitHub](https://github.com/PrevotYann/one-shots-n5eb/releases) et extrayez son contenu dans `Data/modules/n5eb-feux-follets/`, ou copiez le dossier du même nom depuis le dépôt.
2. Lancez un monde utilisant le système **N5eB** et activez le module.
3. Au premier chargement, une fenêtre propose d'**importer le scénario**. Vous pouvez aussi le (ré)importer plus tard via *Paramètres → Configurer les paramètres → Les Feux Follets de Kawabe → Importer / réimporter le scénario*.
4. Ouvrez le journal **00 · Lisez-moi (MJ)**.

Après l'import, donnez à chaque joueur la propriété de son prétiré (clic droit sur l'acteur → *Configurer les droits*).

## Fonctionnement de l'import

- Les **classes, clans, historiques, techniques, armes et dons** des prétirés sont copiés depuis les compendiums du système `n5eb` au moment de l'import. Les fiches restent donc compatibles avec la version du système installée.
- Les avancements de niveau 1 sont appliqués automatiquement : maîtrises (sauvegardes, compétences, armes, armures, outils), capacités accordées par la classe, le clan et l'historique, points de vie et de chakra.
- Les noms sont affichés en français suivi du nom anglais, par exemple « Katon : Boule de feu (Fire Release Fireball) ». Chaque description commence par un résumé « En bref » en français.
- Tous les documents créés portent un drapeau du module. Réimporter **supprime puis recrée** ces documents.
- Depuis la console : `game.modules.get("n5eb-feux-follets").api.importAdventure({ replace: true })`.

## Illustrations finales

Le module comprend **46 visuels définitifs** : 17 portraits/jetons transparents, 4 cartes, 5 aides de jeu, 11 icônes d'objets et 9 épingles numérotées. Les personnages et les décors adoptent une direction artistique anime inspirée de Naruto ; les documents et les petites icônes restent en SVG pour garder leur netteté et leurs textes français exacts.

Les cartes conservent les dimensions des scènes et une échelle de **100 px par case**. Elles ne contiennent pas de grille intégrée : Foundry affiche la sienne. Les repères numérotés sont des notes Foundry, sans doublons dessinés sur les cartes.

| Fichier | Taille |
|---|---|
| `assets/maps/carte-voyage.webp` | 2400 × 1600 (sans grille) |
| `assets/maps/pont-gorge.webp` | 3000 × 2000 |
| `assets/maps/village-kawabe.webp` | 4000 × 3000 |
| `assets/maps/ile-lucioles.webp` | 3600 × 3000 |
| `assets/tokens/*.webp` | 17 portraits/jetons, 1024 × 1024, transparence conservée |
| `assets/handouts/*.svg` | ordre de mission, légende, registre, plan de l'île |
| `assets/handouts/bandeau-kiri.webp` | illustration du bandeau rayé |
| `assets/items/*.svg`, `assets/icons/note-*.svg` | icônes d'objets et épingles de carte |

Les cartes finales reprennent la disposition des lieux du scénario. `assets/art-manifest.json` inventorie les fichiers et leurs empreintes SHA-256. Le build du contenu conserve les illustrations finales et s'arrête si le manifeste ou un fichier manque.

Dans le dépôt source, `../art-source/preview.html` permet de parcourir les visuels. Les masters PNG, leurs dimensions natives et les prompts imagegen sont conservés dans `../art-source/`. Les cartes livrées sont redimensionnées aux dimensions Foundry indiquées ci-dessus ; les masters ne sont pas présentés comme des générations natives en 4K.

## Régénérer le module (développeurs)

Le contenu (`data/adventure.json`) est produit par les scripts Python de `../tools`. Les illustrations finales sont conservées :

```
pip install pillow
python tools/build.py
```

Pour réexporter les WebP à partir des masters PNG et reconstruire les SVG, utilisez `python tools/final_art.py`, puis `python tools/build.py`. Cette opération locale n'appelle aucun modèle et ne génère pas de nouvelles images.

- `tools/content_mj.py` : textes du MJ (lisez-moi, scénario, PNJ)
- `tools/content_joueurs.py` : guide du joueur, fiches des prétirés, liste des aides de jeu
- `tools/build.py` : acteurs, objets, scènes, tables, traductions des documents du système
- `tools/final_art.py` : exports des masters, SVG définitifs, manifeste et galerie
- `tools/art.py` : ancien générateur provisoire, conservé comme référence
