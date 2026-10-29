# Les Feux Follets de Kawabe — final artwork

Open [preview.html](preview.html) to review all **46 final runtime assets**. The module uses the files in `../n5eb-feux-follets/assets/`; their complete paths, sizes and SHA-256 hashes are listed in `../n5eb-feux-follets/assets/art-manifest.json`.

- **17 transparent circular character portraits/tokens**, exported as 1024 × 1024 WebP.
- **4 illustrated maps**, exported at the existing Foundry scene dimensions: 2400 × 1600, 3000 × 2000, 4000 × 3000 and 3600 × 3000. Battle maps have no baked grid or numbered markers.
- **5 handouts**: an illustrated Kiri headband and four native SVG documents with exact French text.
- **11 native SVG item illustrations** and **9 numbered SVG map pins**.

## Raster generation

The **built-in `image_gen` tool** produced 22 individual final illustrations: 17 character tokens, 4 maps and the headband handout. No fallback CLI or image API key was used. Each complete final prompt is saved in [prompts.json](prompts.json), together with the corresponding master path and actual source pixel dimensions. Original PNG outputs are retained in `masters/maps/`, `masters/tokens/` and `masters/handouts/`.

The raster direction uses Naruto-inspired anime ink contours, cel shading, painted environments, original scenario characters and consistent brushed-brass token rings. Map edits used the original module maps as spatial references. Uramaru's final portrait served as the identity reference for his water clone.

Foundry map files are resized from the generated master resolutions to match the existing scenes. They are **not native 4K generations**. Transparent token alpha is preserved, including the masters' slightly translucent interior pixels. No semantic image edits or repainting were performed outside imagegen.

## Native artwork and reproducibility

`../tools/final_art.py` renders the native SVG item illustrations, map pins and handout documents. This keeps French accents, clue text and small icons crisp. [handout-text.json](handout-text.json) preserves the original three written handouts verbatim; the island plan preserves its original clues and relative geography.

From the repository root:

```powershell
python tools/final_art.py
python tools/build.py
python tools/validate_art.py
```

Only the first command reexports images; it reads the saved PNG masters and calls no image model. The normal content build validates the final-art manifest and does not regenerate placeholders. The legacy placeholder generator also refuses to overwrite installed final artwork. Superseded token/headband SVG placeholders are archived in `legacy-placeholders/` outside the runtime module.

Validation checks all 46 final file hashes, every local asset reference in the generated adventure, the 17 token alpha channels, all four scene sizes, SVG syntax and the original French handout text. A live Foundry world was not available for an import test.
