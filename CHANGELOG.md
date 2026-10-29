# v1.0.1 — Import via le compendium d'aventure

- Import via l'importeur d'aventure standard de Foundry (compendium « Les Feux Follets de Kawabe (Aventure) »).
- Correction : l'import échouait avec N5eB 3.x (`buildActor`), dont les avancements de classe sont un objet et non un tableau.

# v1.0.0 — Les Feux Follets de Kawabe

Première publication du module Foundry VTT en français pour N5eB (Naruto 5e).

- Mission de rang C pour 5 genin de niveau 1, prévue pour 3 à 4 heures.
- 5 prétirés, 12 PNJ et adversaires, 4 scènes, 6 journaux et 43 pages.
- 8 objets et une table de rumeurs ; import du scénario depuis les paramètres du module.
- 46 illustrations finales : 17 jetons transparents, 4 cartes, 5 aides de jeu, 11 icônes d'objets et 9 épingles.
- Sources Python, masters PNG et prompts imagegen inclus dans le dépôt.

## Installation

Prérequis déclarés : Foundry VTT v13/v14 et N5eB 3.0.0 ou supérieur.

Dans **Modules → Installer un module**, utilisez l'URL du manifeste :

```text
https://github.com/PrevotYann/one-shots-n5eb/releases/latest/download/module.json
```

Pour une installation manuelle, extrayez `n5eb-feux-follets.zip` dans `Data/modules/n5eb-feux-follets/`.

Fichiers joints : `module.json`, `n5eb-feux-follets.zip` et `SHA256SUMS.txt`.

## Validation

Build du contenu, 46 références graphiques, dimensions des scènes, transparence des jetons, syntaxe SVG, conservation des textes français et syntaxe JavaScript vérifiés. Le ZIP est contrôlé et accompagné d'empreintes SHA-256. L'import dans un monde Foundry réel n'a pas encore été testé.
