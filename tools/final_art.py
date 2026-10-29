"""Package final imagegen masters and render the module's native SVG artwork.

No image generation/API calls: only format/size conversion of saved masters.
Usage: python tools/final_art.py, then python tools/build.py.
"""
import hashlib
import json
from html import escape
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "art-source"
MODULE = ROOT / "n5eb-feux-follets"
ASSETS = MODULE / "assets"
MAPS = {"carte-voyage": (2400, 1600), "pont-gorge": (3000, 2000),
        "village-kawabe": (4000, 3000), "ile-lucioles": (3600, 3000)}
TOKENS = "bunta kaito shizuka tsumugi momo shuhei oume sachi tetsu genji ayame kaneda mosuke brigand gonza clone uramaru".split()
ITEMS = "onigiri talisman bandeau registre carte_ile tresor insigne poison eau lumiere capacite".split()
INK = "#19282c"


def write_svg(relative, body, w=256, h=256):
    path = ASSETS / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{body}\n</svg>\n', encoding="utf-8", newline="\n")


def path(d, fill="none", stroke=INK, sw=4, **attrs):
    extra = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def circle(x, y, r, fill, stroke=INK, sw=3):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def text(x, y, value, size=24, fill="#352b23", anchor="start", **attrs):
    family = attrs.pop("font_family", "Georgia, serif")
    extra = " ".join(f'{k.replace("_", "-")}="{escape(str(v), quote=True)}"' for k, v in attrs.items())
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-family="{family}" {extra}>{escape(value)}</text>'


def firefly(x=128, y=130, scale=1):
    return f'<g transform="translate({x} {y}) scale({scale})">' + \
        path("M-6 -4 C-55 -58 -66 -10 -14 14 M6 -4 C55 -58 66 -10 14 14", "#e7d9a3", "#8d7139", 3) + \
        '<ellipse cx="0" cy="18" rx="11" ry="26" fill="#efd277" stroke="#66552b" stroke-width="3"/>' + \
        circle(0, -16, 9, "#282e24", "#66552b", 3) + path("M-4 -23 L-14 -36 M4 -23 L14 -36", stroke="#66552b", sw=3) + '</g>'


ICON_DEFS = '''<defs>
<linearGradient id="frame" x2=".8" y2="1"><stop stop-color="#f2dca2"/><stop offset=".45" stop-color="#a98140"/><stop offset="1" stop-color="#e1c68a"/></linearGradient>
<radialGradient id="ground"><stop stop-color="#385057"/><stop offset="1" stop-color="#14262d"/></radialGradient>
<linearGradient id="steel" x2=".6" y2="1"><stop stop-color="#f4f7ef"/><stop offset=".4" stop-color="#9eafb1"/><stop offset=".5" stop-color="#d2dcda"/><stop offset="1" stop-color="#657d87"/></linearGradient>
<linearGradient id="paper" x2=".5" y2="1"><stop stop-color="#fff2cd"/><stop offset="1" stop-color="#c9af76"/></linearGradient>
<linearGradient id="water" x2=".7" y2="1"><stop stop-color="#b5f5ee"/><stop offset=".5" stop-color="#45afcb"/><stop offset="1" stop-color="#185c9b"/></linearGradient>
</defs>'''


def item_shapes(key):
    if key == "onigiri":
        rice = ''.join(path(f'M{x} {y} l4 -2', stroke="#cfbd94", sw=2) for x,y in [(94,89),(124,73),(139,97),(80,117),(174,143),(63,153),(101,120),(155,121),(117,97)])
        return '<ellipse cx="128" cy="195" rx="84" ry="12" fill="#0a171a" opacity=".6"/>' + path("M49 174 Q40 163 49 147 L109 60 Q126 35 145 62 L207 151 Q223 182 199 190 Q124 203 58 190 Z", "#eee1bd") + path("M51 173 Q128 186 208 169 L199 190 Q120 203 58 190 Z", "#c9b98c", sw=2) + rice + path("M99 134 Q128 128 157 134 L166 195 Q130 201 94 194 Z", "#263b2a") + path("M105 143 L151 140 M103 154 L153 152 M102 168 L155 165 M101 181 L157 179", stroke="#486044", sw=2)
    if key == "talisman":
        return path("M81 54 L173 44 L190 190 L94 204 Z", "url(#paper)") + path("M91 64 L163 56 L178 181 L105 191 Z", stroke="#b64a35", sw=3) + circle(127, 49, 5, "#8b4d32", sw=1) + path("M127 49 Q82 15 98 27 Q112 36 121 22 Q145 8 140 32 L127 49", stroke="#c34c36", sw=5) + firefly(137, 120, .7) + path("M119 173 L151 169 M123 181 L148 178", stroke="#b64a35", sw=3)
    if key == "bandeau":
        return path("M34 93 L210 78 L225 165 L40 181 Z", "#233b59") + path("M39 159 L219 143 L225 165 L40 181 Z", "#12233c", sw=2) + '<rect x="61" y="87" width="133" height="78" rx="13" fill="url(#steel)" stroke="#19282c" stroke-width="4"/>' + ''.join(circle(x,y,3,"#56676c",sw=1) for x in (70,185) for y in (98,153)) + ''.join(path(f'M88 {y} q10 -12 20 0 t20 0 t20 0 t20 0',stroke="#354c57",sw=3) for y in (111,126,141)) + path("M80 157 L177 94",stroke="#182731",sw=6)
    if key == "registre":
        return path("M65 58 L171 44 L198 185 L83 208 Z", "#6a3d2a") + path("M76 62 L171 52 L191 180 L91 198 Z", "url(#paper)") + path("M65 58 L79 56 L103 205 L83 208 Z", "#a05237") + path("M89 88 L166 77 M93 107 L169 96 M96 126 L173 114 M100 145 L177 134 M103 164 L180 152 M137 78 L154 169",stroke="#916f4b",sw=2) + path("M65 80 L89 76 M71 111 L95 107 M76 142 L100 138 M81 173 L106 169",stroke="#dfc28e",sw=4) + path("M113 174 L155 167 L160 181 L117 188 Z","#ad4936",sw=1)
    if key == "carte_ile":
        return path("M42 65 L96 79 L157 51 L211 66 L205 190 L155 177 L93 206 L39 189 Z", "url(#paper)") + path("M96 79 L93 206 M157 51 L155 177",stroke="#a68b59",sw=3) + path("M72 136 Q72 90 128 95 Q184 94 177 143 Q159 182 108 173 Q72 172 72 136 Z","#9da46f","#59664d",2) + path("M63 157 Q91 143 102 132 T150 131",stroke="#8d4932",sw=3,stroke_dasharray="5 6") + path("M142 139 L163 159 M163 139 L142 159",stroke="#b13f2d",sw=5) + path("M50 87 L55 81 L60 87 M187 83 L192 77 L197 83",stroke="#75878a",sw=2)
    if key == "tresor":
        coins = ''.join(circle(x,y,r,"#e7bf57","#79542a",2) for x,y,r in [(77,158,12),(98,148,13),(120,159,12),(142,145,13),(162,155,13),(188,191,12),(62,203,9)])
        return path("M52 142 L202 142 L192 203 L62 203 Z","#7b4428") + path("M51 134 Q51 73 91 65 L176 65 Q210 73 204 135 Z","#985a30") + path("M69 96 L191 96 M57 118 L200 118",stroke="#542e23",sw=3) + path("M77 69 L86 133 M174 68 L179 134 M77 147 L82 202 M173 147 L168 203",stroke="#d2a448",sw=9) + path("M52 139 L203 139 L198 159 L57 159 Z","#3c2922") + coins + path("M55 166 L198 166 L192 203 L62 203 Z","#8c4b2b") + path("M78 170 L82 201 M173 170 L168 201",stroke="#d2a448",sw=9) + '<rect x="118" y="164" width="23" height="27" rx="3" fill="#ddb85c" stroke="#684827" stroke-width="3"/>' + circle(129,175,3,"#392a20",sw=1)
    if key == "insigne":
        return path("M91 44 L124 44 L135 106 L107 119 Z","#b94a3d") + path("M133 44 L165 44 L149 117 L119 105 Z","#d9c08b") + circle(128,156,58,"url(#frame)") + circle(128,156,47,"#244d61","#f0d69a",2) + firefly(128,145,.72) + path("M95 193 Q128 211 160 193",stroke="#dbbf7d",sw=3)
    if key == "poison":
        needles = ''.join('<g transform="rotate('+str(angle)+' 128 128)">'+path("M126 49 L132 49 L131 177 L127 195 L125 177 Z","url(#steel)",sw=2)+path("M127 157 L130 157 L130 176 L128 189 Z","#91bd69","#416441",1)+path("M126 68 L131 68 M126 74 L131 74 M126 80 L131 80",stroke="#53666b",sw=2)+'</g>' for angle in (-27,0,27))
        return needles + path("M181 166 Q196 186 190 195 Q181 205 174 194 Q169 185 181 166 Z","#a8c86c","#3e6040",3)
    if key == "eau":
        return path("M126 39 Q116 80 80 119 Q43 160 77 194 Q109 227 157 208 Q203 191 194 153 Q184 118 153 120 Q128 122 133 147 Q143 168 159 153 Q158 183 127 183 Q91 181 102 150 Q115 126 137 101 Q147 74 126 39 Z","url(#water)") + path("M127 70 Q115 105 91 132 Q65 164 88 186 M148 196 Q182 186 181 165",stroke="#c4ffff",sw=5) + path("M58 79 Q66 94 61 100 Q51 109 49 98 Q47 90 58 79 Z","#9de1e1",sw=2)
    if key == "lumiere":
        flame = path("M128 57 C117 95 83 110 99 145 C110 165 146 163 158 142 C175 111 142 96 151 72 C134 83 137 98 128 108 C118 95 132 80 128 57 Z","url(#water)","#b9f7ec",2)
        return '<g opacity=".16">'+circle(128,128,86,"#7bd3d8","none",0)+'</g>'+flame+'<g transform="translate(-49 60) scale(.64)">'+flame+'</g><g transform="translate(113 66) scale(.58)">'+flame+'</g>'+path("M61 183 Q112 214 196 174",stroke="#78bac3",sw=2)+''.join(circle(x,y,2,"#e2fff3","none",0) for x,y in [(76,65),(184,93),(169,191),(45,142),(158,42)])
    # Generic shinobi technique: four-bladed shuriken with a chakra orbit.
    return path("M129 43 L149 101 L212 127 L152 148 L127 212 L105 151 L43 127 L103 105 Z","url(#steel)") + path("M129 43 L128 128 L212 127 M127 212 L128 128 L43 127",stroke="#506770",sw=3) + circle(128,128,17,"#213c48","#d3ded7",3) + path("M59 101 C77 48 164 37 198 96 M58 157 C81 212 174 214 200 153",stroke="#71d0d0",sw=5)


def render_icons():
    for key in ITEMS:
        frame = '<rect x="7" y="7" width="242" height="242" rx="31" fill="url(#frame)" stroke="#13242b" stroke-width="5"/><rect x="15" y="15" width="226" height="226" rx="24" fill="url(#ground)" stroke="#735e37" stroke-width="2"/>'
        corners = path("M27 58 L27 29 L57 29 M199 29 L228 29 L228 58 M27 198 L27 227 L57 227 M199 227 L228 227 L228 198",stroke="#ad9560",sw=2)
        write_svg(f"items/{key}.svg", ICON_DEFS + frame + corners + item_shapes(key))
    for n in range(1, 10):
        body = '<defs><radialGradient id="red" cx=".35" cy=".25"><stop stop-color="#c8624a"/><stop offset="1" stop-color="#7c2b25"/></radialGradient></defs>' + circle(64,64,59,"#14282e","#1a2228",3) + circle(64,61,53,"url(#red)","#dfc697",5) + circle(64,61,46,"none","#d59e70",1) + text(64,83,str(n),62,"#fff0cd","middle",font_weight="bold")
        write_svg(f"icons/note-{n}.svg", body, 128, 128)


def paper(w, h):
    fibers = ''.join(path(f'M{30+(i*71)%(w-60)} {35+(i*47)%(h-70)} l{15+i%22} {i%5-2}',stroke="#8e784f",sw=.6,opacity=".12") for i in range(170))
    return '<defs><linearGradient id="sheet" x2=".8" y2="1"><stop stop-color="#d2b77e"/><stop offset=".12" stop-color="#f6e9c8"/><stop offset=".78" stop-color="#ead8ad"/><stop offset="1" stop-color="#c6a775"/></linearGradient></defs>' + \
        f'<rect width="{w}" height="{h}" fill="#293c3b"/><path d="M22 23 L{w-26} 18 L{w-18} {h-30} L30 {h-17} Z" fill="url(#sheet)" stroke="#765e3d" stroke-width="3"/>' + fibers + \
        f'<rect x="44" y="42" width="{w-88}" height="{h-84}" fill="none" stroke="#9e7850" stroke-width="1"/>' + \
        path(f'M58 102 L58 56 L102 56 M{w-102} 56 L{w-58} 56 L{w-58} 102 M58 {h-102} L58 {h-56} L102 {h-56} M{w-102} {h-56} L{w-58} {h-56} L{w-58} {h-102}',stroke="#956a40",sw=3)


def lantern(x, y, s=1):
    return f'<g transform="translate({x} {y}) scale({s})" opacity=".38">' + path("M-38 32 L38 32 L31 18 L-31 18 Z M-18 18 L18 18 L18 -27 L-18 -27 Z M-35 -28 L35 -28 L22 -45 L-22 -45 Z M-21 -44 L21 -44 L0 -60 Z M-29 45 L29 45 L24 32 L-24 32 Z","#8b8772","#526358",2) + path("M-8 -21 L8 -21 L8 8 L-8 8 Z","#e4ca7e","#526358",2) + '</g>'


def render_documents():
    originals = json.loads((SOURCE / "handout-text.json").read_text(encoding="utf-8"))
    for key, rows in originals.items():
        h = 1000 if key == "ordre-mission" else 820
        title, rest = rows[0]["text"], rows[1:]
        seal = rest.pop()["text"] if key != "registre-kaneda" else None
        body = paper(800, h) + text(400,100,title,32,"#713c2c","middle",font_weight="bold")
        body += path("M80 123 L720 123",stroke="#936d44",sw=2)
        # Original content, accents, spacing and information are preserved.
        for i,row in enumerate(rest):
            body += text(78,177+i*38,row["text"],23 if key != "registre-kaneda" else 21,
                         font_weight=row["weight"],font_style=row["style"])
        if seal:
            body += f'<g transform="translate(670 {h-111}) rotate(-9)"><rect x="-42" y="-43" width="84" height="86" rx="5" fill="none" stroke="#a34731" stroke-width="5"/><rect x="-35" y="-36" width="70" height="72" fill="none" stroke="#a34731" stroke-width="2"/>' + text(0,20,seal,52,"#a34731","middle",font_family="Yu Mincho, serif") + '</g>'
        if key == "legende-kagami":
            body += lantern(190,718,1.1) + '<g opacity=".35">'+firefly(290,688,.35)+firefly(338,722,.24)+'</g>'
        elif key == "ordre-mission":
            body += path("M104 893 C194 858 242 912 324 882 M104 904 C194 869 242 923 324 893",stroke="#a28c5d",sw=2)
        else:
            body += path("M139 260 L704 259 M145 335 L710 334",stroke="#aa3e2c",sw=2,opacity=".6")
            body += text(103,733,"K. J.",30,"#8b4a32",font_style="italic")
        write_svg(f"handouts/{key}.svg",body,800,h)


def render_island_plan():
    body = paper(1000,1000)+text(500,105,"Plan de l'île — NE PAS MONTRER",36,"#713c2c","middle",font_weight="bold")
    coast = "M191 513 C172 330 312 222 528 236 C744 212 877 371 846 560 C844 737 643 818 437 789 C286 794 185 684 191 513 Z"
    body += path(coast,"#c3c99d","#59634a",4)
    body += '<g opacity=".45">'+path("M207 509 C186 346 322 244 528 258 C719 235 850 383 824 557 C820 712 634 793 440 766",stroke="#829378",sw=2)+'</g>'
    for x,y in [(293,337),(338,318),(385,309),(732,627),(685,698),(602,744),(317,698),(265,640),(731,365),(770,434)]:
        body += path(f'M{x-16} {y+15} L{x} {y-18} L{x+16} {y+15} Z',"#879673","#5c6d50",2)
    body += path("M220 510 Q378 491 431 509 T662 499",stroke="#775e3d",sw=3,stroke_dasharray="9 9")
    body += path("M166 484 L234 476 L253 618 L181 631 Z","#d5c28e","none",0)
    for y in (501,599):
        body += path(f'M119 {y} Q159 {y-27} 196 {y} Q158 {y+26} 119 {y} Z',"#af9567","#725b3c",2)+path(f'M134 {y} L183 {y}',stroke="#725b3c",sw=2)
    body += path("M341 488 L341 552 M390 488 L390 552 M330 479 L402 479 M337 490 L394 490",stroke="#9d4835",sw=8)
    body += path("M656 398 L766 398 L766 492 L656 492 Z","#ac9a6d","#5f5238",3)+path("M642 399 L780 399 L753 367 L669 367 Z","#8e8164","#5f5238",3)
    body += path("M652 574 L682 604 M682 574 L652 604",stroke="#ad4332",sw=6)+text(668,639,"creuser ici",27,"#a33f2f","middle",font_style="italic")
    body += lantern(670,555,.5)
    body += path("M401 357 L425 317 L448 357 Z M478 343 L501 303 L525 343 Z","#bcaa75","#6e5e3c",2)
    body += text(467,288,"camp",26,anchor="middle",font_style="italic")+text(711,348,"vieux sanctuaire",25,anchor="middle")
    body += path("M142 286 L142 216 L129 242 M142 216 L155 242",stroke="#765b3d",sw=3)+text(142,201,"N",23,anchor="middle")
    body += text(157,840,"Barques cachées ici (ouest)",25,font_style="italic")+path("M211 809 Q166 738 156 629",stroke="#765b3d",sw=2)
    body += text(500,898,"« Le brouillard tous les soirs. Le reste du village",23,anchor="middle",font_style="italic")+text(500,933,"partira d'ici dix jours. » — K.",23,anchor="middle",font_style="italic")
    write_svg("handouts/plan-ile.svg",body,1000,1000)


def export_masters():
    expected = ["maps/"+k for k in MAPS]+["tokens/"+k for k in TOKENS]+["handouts/bandeau-kiri"]
    missing = [k for k in expected if not (SOURCE / "masters" / (k+".png")).is_file()]
    if missing:
        raise FileNotFoundError("Masters missing: "+", ".join(missing))
    for key in expected:
        source = SOURCE / "masters" / (key+".png")
        with Image.open(source) as original:
            is_token = key.startswith("tokens/")
            if is_token and (original.mode != "RGBA" or original.getchannel("A").getextrema()[0] != 0):
                raise ValueError(f"Transparent master required: {key}")
            size = MAPS[key.split("/")[1]] if key.startswith("maps/") else (1024,1024) if is_token else (1600,round(original.height * 1600 / original.width))
            # Encoding and technical resizing only; no repainting, compositing or alpha removal.
            image = original.convert("RGBA" if is_token else "RGB").resize(size,Image.Resampling.LANCZOS)
            dest = ASSETS / (key+".webp")
            dest.parent.mkdir(parents=True,exist_ok=True)
            image.save(dest,"WEBP",quality=95,method=6,exact=True)


def manifest_and_preview():
    files = [ASSETS / ("maps/"+k+".webp") for k in MAPS]+[ASSETS / ("tokens/"+k+".webp") for k in TOKENS]+[ASSETS / ("items/"+k+".svg") for k in ITEMS]+[ASSETS / ("icons/note-"+str(n)+".svg") for n in range(1,10)]+[ASSETS / ("handouts/"+k) for k in ["ordre-mission.svg","legende-kagami.svg","registre-kaneda.svg","plan-ile.svg","bandeau-kiri.webp"]]
    entries=[]
    for file in files:
        entry={"path":file.relative_to(MODULE).as_posix(),"sha256":hashlib.sha256(file.read_bytes()).hexdigest()}
        if file.suffix == ".webp":
            with Image.open(file) as im:
                entry.update(width=im.width,height=im.height,alpha="A" in im.getbands())
        entries.append(entry)
    manifest={"status":"final","generation":"Built-in image_gen (22 raster illustrations); native SVG for documents, item icons and numbered map pins.","raster_source_note":"Generated masters retained in ../art-source/masters. Maps resized to the existing 100-pixel grid dimensions; source dimensions are in art-source/prompts.json.","assets":entries}
    (ASSETS / "art-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    sections=[]
    labels={"tokens":"Personnages · 17 jetons transparents","maps":"Cartes · 4 scènes","handouts":"Aides de jeu · 5 documents","items":"Objets · 11 icônes","icons":"Épingles de carte · 9 repères"}
    for category,label in labels.items():
        figures=[]
        for entry in entries:
            p=Path(entry["path"])
            if p.parts[1] != category: continue
            url="../n5eb-feux-follets/"+entry["path"]
            figures.append(f'<figure><a href="{url}"><img loading="lazy" src="{url}" alt="{escape(p.stem)}"></a><figcaption>{escape(p.stem)}</figcaption></figure>')
        sections.append(f'<section class="{category}"><h2>{label}</h2><div class="grid">'+''.join(figures)+'</div></section>')
    html='''<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Les Feux Follets de Kawabe · Illustrations finales</title><style>body{margin:0;padding:40px max(24px,5vw);background:#142429;color:#eee2c4;font:16px/1.5 system-ui}h1,h2{font-family:Georgia,serif;font-weight:400}h1{font-size:42px}h2{margin-top:48px;border-bottom:1px solid #74613f;padding-bottom:12px}p{color:#c0baa9}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:20px}figure{margin:0;padding:12px;border:1px solid #435252;background:#1b2e33;border-radius:12px}img{display:block;width:100%;height:auto;aspect-ratio:1;object-fit:contain}figcaption{text-align:center;padding-top:10px;color:#d6c6a0}.maps .grid,.handouts .grid{grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}.maps img{aspect-ratio:1.5}.handouts img{aspect-ratio:.8}.items .grid,.icons .grid{grid-template-columns:repeat(auto-fill,minmax(100px,1fr))}a:focus{outline:2px solid #e5c987}</style><h1>Les Feux Follets de Kawabe</h1><p>Illustrations finales · Naruto / N5eB · Cliquez sur une illustration pour l'ouvrir.</p>'''+''.join(sections)+'</html>'
    (SOURCE / "preview.html").write_text(html,encoding="utf-8",newline="\n")
    print(f"Final art packaged: {len(entries)} assets. Preview: {SOURCE / 'preview.html'}")


def main():
    export_masters()
    render_icons()
    render_documents()
    render_island_plan()
    manifest_and_preview()


if __name__ == "__main__":
    main()
