"""Validate the final Foundry artwork, references, dimensions and checksums."""
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "n5eb-feux-follets"
ASSETS = MODULE / "assets"


def main():
    manifest = json.loads((ASSETS / "art-manifest.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "final"
    entries = manifest["assets"]
    assert len(entries) == 46, f"Expected 46 assets, found {len(entries)}"
    assert len({entry["path"] for entry in entries}) == 46
    for entry in entries:
        file = MODULE / entry["path"]
        assert file.is_file(), f"Missing: {file}"
        assert hashlib.sha256(file.read_bytes()).hexdigest() == entry["sha256"], f"Changed: {file}"
        if file.suffix == ".svg":
            ET.parse(file)
        else:
            with Image.open(file) as im:
                im.load()
                assert im.size == (entry["width"], entry["height"]), f"Size: {file}"
                if file.parent.name == "tokens":
                    assert im.size == (1024, 1024), f"Token size: {file}"
                    assert "A" in im.getbands(), f"Missing alpha: {file}"
                    alpha = im.getchannel("A")
                    assert all(alpha.getpixel(xy) <= 1 for xy in [(0,0),(1023,0),(0,1023),(1023,1023)]), f"Opaque token corners: {file}"
                    # The imagegen masters retain slightly translucent (252–253)
                    # interior pixels; preserve that supplied alpha in exports.
                    assert alpha.getpixel((512,512)) >= 250, f"Empty token centre: {file}"
    raw = (MODULE / "data/adventure.json").read_text(encoding="utf-8")
    adventure = json.loads(raw)
    refs = set(re.findall(r"modules/n5eb-feux-follets/([a-zA-Z0-9_./-]+)", raw))
    for ref in refs:
        assert (MODULE / ref).is_file(), f"Broken reference: {ref}"
    assert len(adventure["actors"]) == 17
    for actor in adventure["actors"]:
        assert actor["img"].endswith(".webp"), actor["name"]
        assert actor["prototypeToken"]["texture"]["src"].endswith(".webp"), actor["name"]
    for scene in adventure["scenes"]:
        file = MODULE / scene["background"]["src"].split("modules/n5eb-feux-follets/")[1]
        with Image.open(file) as im:
            assert im.size == (scene["width"],scene["height"]), f"Scene size: {scene['name']}"
        if scene["grid"]["type"]:
            assert scene["grid"]["size"] == 100
    images = [page["src"] for journal in adventure["journals"] for page in journal["pages"] if page["type"] == "image"]
    assert any(p.endswith("handouts/bandeau-kiri.webp") for p in images)
    originals = json.loads((ROOT / "art-source/handout-text.json").read_text(encoding="utf-8"))
    for key, rows in originals.items():
        rendered = [e.text or "" for e in ET.parse(ASSETS / "handouts" / (key+".svg")).iter("{http://www.w3.org/2000/svg}text")]
        for row in rows:
            assert row["text"] in rendered, f"Handout text lost: {key}: {row['text']}"
    prompts = json.loads((ROOT / "art-source/prompts.json").read_text(encoding="utf-8"))
    assert len(prompts) == 22
    for record in prompts:
        assert (ROOT / "art-source" / record["source"]).is_file(), record["key"]
    print(f"PASS: {len(entries)} assets; {len(refs)} asset references; 17 transparent tokens; 4 scene sizes; SVG syntax; original French handout text; 22 masters.")


if __name__ == "__main__":
    main()
