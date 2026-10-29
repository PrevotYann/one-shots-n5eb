"""Génère les visuels provisoires du one-shot : cartes (WebP), jetons/portraits et aides de jeu (SVG).

Tout est volontairement sommaire : ces images seront remplacées plus tard par des versions définitives.
Garder les mêmes noms de fichiers permet de les remplacer sans réimporter le scénario.
"""
import math
import os
import random
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

G = 100  # taille d'une case en pixels (1 case = 1,5 m / 5 ft)

FONT_DIR = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts")


def font(size, bold=False):
    for name in (["arialbd.ttf"] if bold else ["arial.ttf"]) + ["DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
        except OSError:
            continue
    return ImageFont.load_default()


# --------------------------------------------------------------------------- #
#  Outils de dessin                                                            #
# --------------------------------------------------------------------------- #

def cell_rect(c0, r0, c1, r1):
    return [c0 * G, r0 * G, c1 * G, r1 * G]


def speckle(draw, box, colors, n, size=(4, 14), rng=None):
    rng = rng or random
    x0, y0, x1, y1 = box
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        s = rng.uniform(*size)
        draw.ellipse([x - s, y - s, x + s, y + s], fill=rng.choice(colors))


def tree(draw, cx, cy, r, rng):
    draw.ellipse([cx - r + 8, cy - r + 10, cx + r + 8, cy + r + 10], fill=(20, 45, 20))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rng.choice([(38, 92, 40), (46, 105, 46), (32, 80, 36)]))
    draw.ellipse([cx - r * .55, cy - r * .6, cx + r * .2, cy - r * .05], fill=(70, 130, 60))


def rock(draw, cx, cy, r):
    pts = [(cx + r * math.cos(a) * (0.75 + 0.25 * math.sin(a * 3)), cy + r * math.sin(a) * 0.8)
           for a in [i * math.pi / 4 for i in range(8)]]
    draw.polygon([(x + 6, y + 8) for x, y in pts], fill=(50, 50, 50))
    draw.polygon(pts, fill=(130, 128, 120), outline=(70, 70, 70))


def house(draw, box, roof=(120, 60, 45), label=None, ruined=False):
    x0, y0, x1, y1 = box
    draw.rectangle([x0 + 10, y0 + 12, x1 + 10, y1 + 12], fill=(40, 35, 30))
    draw.rectangle(box, fill=roof, outline=(40, 25, 20), width=6)
    # faîtage
    if (x1 - x0) >= (y1 - y0):
        draw.line([x0, (y0 + y1) / 2, x1, (y0 + y1) / 2], fill=(60, 30, 25), width=8)
    else:
        draw.line([(x0 + x1) / 2, y0, (x0 + x1) / 2, y1], fill=(60, 30, 25), width=8)
    if ruined:
        draw.polygon([(x0 + 30, y0 + 20), (x0 + 120, y0 + 40), (x0 + 60, y0 + 140)], fill=(70, 60, 50))


def label(draw, xy, text, size=44, fill=(255, 255, 255), stroke=(0, 0, 0)):
    f = font(size, bold=True)
    draw.text(xy, text, font=f, fill=fill, stroke_width=max(2, size // 12), stroke_fill=stroke, anchor="mm")


def number_marker(draw, cx, cy, n, r=38):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(180, 30, 30), outline=(255, 240, 200), width=5)
    draw.text((cx, cy), str(n), font=font(int(r * 1.2), bold=True), fill=(255, 255, 255), anchor="mm")


def save(img, path, quality=82):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "WEBP", quality=quality, method=6)


def water_texture(draw, box, rng, base=(40, 90, 140)):
    x0, y0, x1, y1 = box
    for _ in range(int((x1 - x0) * (y1 - y0) / 9000)):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        w = rng.uniform(20, 60)
        c = tuple(min(255, v + rng.randint(10, 35)) for v in base)
        draw.arc([x - w, y - 8, x + w, y + 8], 200, 340, fill=c, width=3)


# --------------------------------------------------------------------------- #
#  Cartes                                                                      #
# --------------------------------------------------------------------------- #

def map_travel(path):
    """Carte régionale (sans grille) : Konoha -> la gorge -> Kawabe -> lac Kagami."""
    rng = random.Random(1)
    W, H = 2400, 1600
    img = Image.new("RGB", (W, H), (226, 208, 160))
    d = ImageDraw.Draw(img)
    speckle(d, [0, 0, W, H], [(214, 196, 150), (232, 216, 172), (220, 200, 150)], 2500, (3, 10), rng)
    # forêts
    for _ in range(260):
        x, y = rng.uniform(0, 1500), rng.uniform(0, H)
        if 650 < y < 900 and x < 1500:
            continue
        r = rng.uniform(16, 30)
        d.ellipse([x - r, y - r, x + r, y + r], fill=rng.choice([(90, 130, 70), (70, 115, 60), (105, 140, 80)]))
    # montagnes au nord
    for i in range(9):
        x = 1300 + i * 120 + rng.uniform(-30, 30)
        d.polygon([(x - 90, 330), (x, 150 + rng.uniform(-30, 30)), (x + 90, 330)], fill=(140, 125, 105), outline=(90, 80, 70))
    # lac Kagami
    lake = [(1700, 650), (1900, 560), (2150, 600), (2330, 760), (2350, 1050), (2200, 1300), (1950, 1380), (1760, 1250), (1680, 980)]
    d.polygon(lake, fill=(90, 150, 190), outline=(50, 100, 140))
    water_texture(d, [1700, 600, 2330, 1330], rng, (90, 150, 190))
    d.ellipse([2040, 900, 2180, 1010], fill=(110, 150, 90), outline=(70, 100, 60), width=4)
    # rivière qui coupe la route
    d.line([(1150, 0), (1110, 300), (1180, 600), (1120, 900), (1160, 1200), (1100, 1600)], fill=(90, 150, 190), width=26)
    # route
    road = [(240, 760), (600, 790), (900, 760), (1135, 770), (1400, 800), (1640, 830)]
    d.line(road, fill=(150, 110, 70), width=16)
    for a, b in zip(road, road[1:]):
        pass
    # Konoha
    d.ellipse([90, 620, 390, 900], fill=(200, 170, 120), outline=(120, 80, 40), width=6)
    d.polygon([(240, 560), (200, 640), (280, 640)], fill=(170, 40, 40))
    label(d, (240, 950), "KONOHA", 56)
    # pont
    d.rectangle([1105, 750, 1175, 790], fill=(120, 80, 40), outline=(60, 40, 20), width=4)
    label(d, (1140, 690), "Pont de la Gorge", 36)
    label(d, (1140, 860), "(embuscade)", 28, fill=(255, 220, 200))
    # Kawabe
    for i, (x, y) in enumerate([(1600, 790), (1650, 860), (1580, 880), (1690, 790), (1620, 940)]):
        d.rectangle([x - 22, y - 18, x + 22, y + 18], fill=(150, 80, 60), outline=(60, 30, 20), width=3)
    label(d, (1620, 1030), "KAWABE", 50)
    label(d, (2110, 870), "Île des Lucioles", 34)
    label(d, (2050, 1200), "Lac Kagami", 40, fill=(230, 245, 255), stroke=(30, 60, 90))
    label(d, (1500, 120), "Montagnes du Nord", 36)
    label(d, (700, 1450), "Forêts du Pays du Feu", 44)
    # distances
    label(d, (700, 720), "1 jour de marche", 30, fill=(255, 250, 220))
    label(d, (1400, 740), "½ jour", 30, fill=(255, 250, 220))
    # rose des vents
    cx, cy = 170, 200
    d.polygon([(cx, cy - 110), (cx - 25, cy), (cx + 25, cy)], fill=(160, 30, 30))
    d.polygon([(cx, cy + 110), (cx - 25, cy), (cx + 25, cy)], fill=(80, 60, 40))
    label(d, (cx, cy - 140), "N", 40)
    d.rectangle([10, 10, W - 10, H - 10], outline=(110, 80, 40), width=12)
    label(d, (W / 2, 60), "Mission : Les Feux Follets de Kawabe", 54, fill=(255, 240, 210), stroke=(90, 50, 20))
    save(img, path)


def map_bridge(path):
    """Le Pont de la Gorge : 30 x 20 cases."""
    rng = random.Random(2)
    C, R = 30, 20
    img = Image.new("RGB", (C * G, R * G), (70, 120, 55))
    d = ImageDraw.Draw(img)
    speckle(d, [0, 0, C * G, R * G], [(80, 132, 60), (62, 110, 50), (90, 140, 70)], 5000, (5, 16), rng)
    # route
    d.rectangle(cell_rect(0, 9, 13, 11), fill=(165, 135, 95))
    d.rectangle(cell_rect(17, 9, 30, 11), fill=(165, 135, 95))
    speckle(d, cell_rect(0, 9, 13, 11), [(150, 120, 85), (175, 145, 105)], 500, (3, 8), rng)
    speckle(d, cell_rect(17, 9, 30, 11), [(150, 120, 85), (175, 145, 105)], 500, (3, 8), rng)
    # gorge
    d.rectangle(cell_rect(13, 0, 17, 20), fill=(60, 50, 45))
    d.rectangle(cell_rect(13, 0, 13.4, 20), fill=(110, 95, 80))
    d.rectangle(cell_rect(16.6, 0, 17, 20), fill=(110, 95, 80))
    d.rectangle(cell_rect(14.3, 0, 15.7, 20), fill=(50, 100, 150))
    water_texture(d, cell_rect(14.3, 0, 15.7, 20), rng, (50, 100, 150))
    # pont de cordes
    d.rectangle(cell_rect(13, 9.1, 17, 10.9), fill=(130, 90, 50))
    for i in range(17):
        x = 13 * G + i * 25
        d.line([x, 9.1 * G, x, 10.9 * G], fill=(80, 55, 30), width=5)
    d.line([13 * G, 9.1 * G, 17 * G, 9.1 * G], fill=(220, 200, 150), width=8)
    d.line([13 * G, 10.9 * G, 17 * G, 10.9 * G], fill=(220, 200, 150), width=8)
    # arbres (hors route et gorge)
    for _ in range(95):
        c, r = rng.uniform(0, C), rng.uniform(0, R)
        if 8.3 < r < 11.7 or 12.3 < c < 17.7:
            continue
        tree(d, c * G, r * G, rng.uniform(45, 85), rng)
    # rochers de couverture côté Kawabe et arbre creux côté Konoha
    for c, r in [(18.5, 7.5), (19.5, 12.5), (21.5, 7.8), (23.5, 12.3)]:
        rock(d, c * G, r * G, 60)
    # tronc couché (barricade)
    d.rounded_rectangle(cell_rect(25, 8.6, 26, 11.4), 30, fill=(100, 70, 40), outline=(50, 30, 15), width=6)
    label(d, (2 * G, 8 * G), "← Konoha", 48)
    label(d, (28 * G, 8 * G), "Kawabe →", 48)
    label(d, (15 * G, 1 * G), "Gorge (chute = 3d6)", 36)
    save(img, path)


def map_village(path):
    """Le village de Kawabe : 40 x 30 cases."""
    rng = random.Random(3)
    C, R = 40, 30
    img = Image.new("RGB", (C * G, R * G), (95, 140, 70))
    d = ImageDraw.Draw(img)
    speckle(d, [0, 0, C * G, R * G], [(100, 146, 74), (88, 132, 64), (108, 152, 82)], 7000, (5, 16), rng)
    # lac à l'est
    shore = [(31 * G, 0)]
    for r in range(0, R + 1, 2):
        shore.append(((30.5 + math.sin(r * .7) * 1.2) * G, r * G))
    shore += [(C * G, R * G), (C * G, 0)]
    d.polygon(shore, fill=(50, 105, 150))
    water_texture(d, [29 * G, 0, C * G, R * G], rng, (50, 105, 150))
    for _ in range(160):  # roseaux
        r = rng.uniform(0, R)
        c = 30.5 + math.sin(r * .7) * 1.2 + rng.uniform(-0.6, 0.6)
        x, y = c * G, r * G
        d.line([x, y, x + rng.uniform(-8, 8), y - 30], fill=(120, 150, 70), width=4)
    # chemins
    d.rectangle(cell_rect(0, 14, 30, 16), fill=(170, 140, 100))
    d.rectangle(cell_rect(17, 5, 19, 14), fill=(170, 140, 100))
    d.rectangle(cell_rect(9, 16, 10.5, 23), fill=(170, 140, 100))
    d.rectangle(cell_rect(25, 9, 26.5, 14), fill=(170, 140, 100))
    # rizières
    for c in range(12, 28, 4):
        for r in range(19, 28, 3):
            d.rectangle(cell_rect(c + .15, r + .15, c + 3.85, r + 2.85), fill=(120, 170, 160), outline=(90, 120, 70), width=8)
            for k in range(6):
                for m in range(4):
                    x, y = (c + .5 + k * .6) * G, (r + .6 + m * .6) * G
                    d.line([x, y, x, y - 18], fill=(70, 140, 60), width=3)
    # place du village et puits
    d.ellipse(cell_rect(15.5, 12.5, 21.5, 18.5), fill=(180, 155, 115))
    d.ellipse(cell_rect(17.6, 14.6, 19.4, 16.4), fill=(90, 90, 95), outline=(50, 50, 55), width=8)
    d.ellipse(cell_rect(18.1, 15.1, 18.9, 15.9), fill=(30, 60, 90))
    # bâtiments
    house(d, cell_rect(6, 10, 12, 13.6))                       # 1 auberge
    house(d, cell_rect(15.5, 6.5, 21.5, 11.2), roof=(140, 70, 50))  # 2 cheffe
    house(d, cell_rect(22, 3, 29, 8.6), roof=(110, 100, 80))   # 4 entrepôt
    d.rectangle(cell_rect(29, 5, 32.5, 6), fill=(130, 95, 60))  # quai entrepôt
    house(d, cell_rect(25, 17, 28.6, 20.4), roof=(130, 80, 55))  # 5 Genji
    d.rectangle(cell_rect(29.5, 16, 37, 17.2), fill=(130, 95, 60), outline=(70, 50, 30), width=4)  # ponton
    for i in range(30, 37):
        d.line([i * G, 16 * G, i * G, 17.2 * G], fill=(70, 50, 30), width=4)
    d.ellipse(cell_rect(36.2, 14.6, 38.6, 15.8), fill=(110, 80, 50), outline=(50, 30, 20), width=4)  # barque
    # maisons abandonnées
    for box in [(2, 3, 5.5, 6), (8, 3, 11.5, 6.4), (2, 18, 5, 21), (12, 9.5, 14.8, 12.6), (21, 17, 23.8, 19.6)]:
        house(d, cell_rect(*box), roof=(105, 95, 90), ruined=True)
    # sanctuaire sur la colline
    d.ellipse(cell_rect(1.5, 20.5, 10, 28.5), fill=(110, 150, 80))
    house(d, cell_rect(4, 22, 7.4, 25.4), roof=(170, 40, 40))
    d.rectangle(cell_rect(8.2, 22.8, 8.5, 25), fill=(200, 40, 30))
    d.rectangle(cell_rect(9.5, 22.8, 9.8, 25), fill=(200, 40, 30))
    d.rectangle(cell_rect(7.9, 22.6, 10.1, 23.0), fill=(200, 40, 30))
    # arbres
    for _ in range(70):
        c, r = rng.uniform(0, 29), rng.uniform(0, R)
        if (11.5 < c < 28.5 and 18.5 < r < 28.5) or (13 < r < 17) or (5.5 < c < 22 and 2.5 < r < 13.8) \
                or (21.5 < c < 29.5 and 2.5 < r < 9) or (1 < c < 10.5 and 20 < r < 26) or (24.5 < c < 29 and 16.5 < r < 21):
            continue
        tree(d, c * G, r * G, rng.uniform(40, 70), rng)
    # marqueurs numérotés
    for n, (c, r) in enumerate([(9, 9.3), (18.5, 5.8), (20.5, 13.2), (25.5, 2.3), (33, 15.4), (5.7, 21.3), (20, 23.3), (3.5, 2.3)], start=1):
        number_marker(d, c * G, r * G, n)
    label(d, (1.6 * G, 13.3 * G), "← route", 38)
    label(d, (35 * G, 27 * G), "Lac Kagami", 56, fill=(220, 240, 255), stroke=(20, 50, 80))
    save(img, path)


def map_island(path):
    """L'île des Lucioles (nuit) : 36 x 30 cases."""
    rng = random.Random(4)
    C, R = 36, 30
    img = Image.new("RGB", (C * G, R * G), (35, 70, 110))
    d = ImageDraw.Draw(img)
    water_texture(d, [0, 0, C * G, R * G], rng, (35, 70, 110))
    # île
    pts = []
    for i in range(28):
        a = i / 28 * 2 * math.pi
        rx, ry = 13.5 + math.sin(a * 3) * .8, 11 + math.cos(a * 2) * .7
        pts.append(((19 + rx * math.cos(a)) * G, (15 + ry * math.sin(a)) * G))
    sand = [(x + (x - 19 * G) * .06, y + (y - 15 * G) * .06) for x, y in pts]
    d.polygon(sand, fill=(190, 170, 120))
    d.polygon(pts, fill=(70, 110, 60))
    speckle(d, [6 * G, 4 * G, 32 * G, 26 * G], [(78, 118, 66), (62, 100, 54)], 3000, (5, 14), rng)
    # plage d'accostage à l'ouest
    d.polygon([(5 * G, 11 * G), (10 * G, 12 * G), (10.5 * G, 18 * G), (5 * G, 19 * G)], fill=(195, 175, 125))
    # barques volées
    for r in (12.6, 17.0):
        d.ellipse(cell_rect(2.6, r, 5.4, r + 1.1), fill=(110, 80, 50), outline=(50, 30, 20), width=5)
    # sentier de pierres
    for i in range(14):
        c = 10.5 + i
        r = 15 - math.sin(i / 13 * math.pi) * 0.8
        d.ellipse(cell_rect(c, r - .35, c + .7, r + .35), fill=(150, 145, 135), outline=(90, 90, 85), width=3)
    # torii
    d.rectangle(cell_rect(12, 13.5, 12.3, 16.5), fill=(200, 40, 30))
    d.rectangle(cell_rect(13.7, 13.5, 14, 16.5), fill=(200, 40, 30))
    d.rectangle(cell_rect(11.6, 13.2, 14.4, 13.6), fill=(200, 40, 30))
    # vieux sanctuaire
    house(d, cell_rect(24, 9.5, 29.6, 15.6), roof=(90, 50, 40), ruined=True)
    d.rectangle(cell_rect(26, 15.6, 27.6, 16.6), fill=(110, 100, 90))  # marches
    # fosse de fouille
    d.rectangle(cell_rect(21.5, 17, 25.5, 21), fill=(80, 55, 35))
    d.rectangle(cell_rect(22, 17.5, 25, 20.5), fill=(45, 30, 20))
    d.rectangle(cell_rect(23, 18.3, 24, 19.1), fill=(150, 110, 40), outline=(230, 190, 80), width=5)  # coffre
    for k in range(5):
        d.line([25.2 * G, (17.4 + k * .7) * G, 25.8 * G, (17.4 + k * .7) * G], fill=(140, 100, 60), width=8)
    # camp : tentes et feu
    for c, r in [(14.5, 7.5), (17.5, 6.8)]:
        d.polygon([(c * G, (r - 1) * G), ((c - 1) * G, (r + 1) * G), ((c + 1) * G, (r + 1) * G)], fill=(150, 130, 90), outline=(70, 60, 40))
    d.ellipse(cell_rect(15.6, 9.4, 16.6, 10.4), fill=(240, 140, 30), outline=(120, 60, 20), width=6)
    # arbres et rochers
    for _ in range(45):
        c, r = rng.uniform(8, 31), rng.uniform(5, 25)
        if (math.hypot((c - 19) / 12, (r - 15) / 9.5) > 0.92) or (9.5 < c < 25 and 13.3 < r < 16.7) \
                or (21 < c < 30.2 and 9 < r < 21.5) or (13 < c < 19 and 5.5 < r < 11):
            continue
        tree(d, c * G, r * G, rng.uniform(40, 65), rng)
    for c, r in [(18, 19), (11, 20), (20, 11.5), (29, 19.5), (15, 21.5)]:
        rock(d, c * G, r * G, 50)
    # nappes de brume
    fog = Image.new("RGBA", img.size, (0, 0, 0, 0))
    fd = ImageDraw.Draw(fog)
    for _ in range(40):
        x, y = rng.uniform(0, C * G), rng.uniform(0, R * G)
        w = rng.uniform(150, 420)
        fd.ellipse([x - w, y - w * .45, x + w, y + w * .45], fill=(220, 230, 240, 45))
    fog = fog.filter(ImageFilter.GaussianBlur(25))
    img = Image.alpha_composite(img.convert("RGBA"), fog).convert("RGB")
    d = ImageDraw.Draw(img)
    for n, (c, r) in enumerate([(7.5, 10.5), (13, 12.2), (16.1, 11.6), (26.8, 8.6), (23.5, 22)], start=1):
        number_marker(d, c * G, r * G, n)
    save(img, path)


# --------------------------------------------------------------------------- #
#  Jetons / portraits (SVG)                                                    #
# --------------------------------------------------------------------------- #

def token_svg(path, initials, name, color, kanji="", ring="#f4e7c5", hostile=False):
    ring = "#c0392b" if hostile else ring
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">
  <defs>
    <radialGradient id="g" cx="40%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.25"/>
    </radialGradient>
  </defs>
  <circle cx="200" cy="200" r="190" fill="{ring}"/>
  <circle cx="200" cy="200" r="172" fill="{color}"/>
  <circle cx="200" cy="200" r="172" fill="url(#g)"/>
  <text x="200" y="150" font-family="Yu Gothic, Meiryo, sans-serif" font-size="70" fill="#ffffff" fill-opacity="0.55" text-anchor="middle">{escape(kanji)}</text>
  <text x="200" y="250" font-family="Arial, sans-serif" font-weight="bold" font-size="110" fill="#ffffff" stroke="#000000" stroke-width="4" text-anchor="middle">{escape(initials)}</text>
  <rect x="40" y="290" width="320" height="56" rx="28" fill="#000000" fill-opacity="0.55"/>
  <text x="200" y="330" font-family="Arial, sans-serif" font-size="32" fill="#ffffff" text-anchor="middle">{escape(name)}</text>
</svg>
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)


def item_icon_svg(path, glyph, color):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">
  <rect x="4" y="4" width="120" height="120" rx="18" fill="{color}" stroke="#f4e7c5" stroke-width="6"/>
  <text x="64" y="88" font-family="Yu Gothic, Meiryo, sans-serif" font-weight="bold" font-size="64" fill="#ffffff" text-anchor="middle">{escape(glyph)}</text>
</svg>
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)


def note_icon_svg(path, n):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">
  <circle cx="64" cy="64" r="58" fill="#b4231e" stroke="#fff0c8" stroke-width="8"/>
  <text x="64" y="86" font-family="Arial, sans-serif" font-weight="bold" font-size="64" fill="#ffffff" text-anchor="middle">{n}</text>
</svg>
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)


# --------------------------------------------------------------------------- #
#  Aides de jeu (SVG)                                                          #
# --------------------------------------------------------------------------- #

PARCHMENT = """<defs>
    <filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" seed="7"/>
      <feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.33  0 0 0 0 0.18  0 0 0 0.25 0"/>
      <feComposite in2="SourceGraphic" operator="in"/></filter>
  </defs>
  <rect x="20" y="20" width="760" height="{h}" rx="18" fill="#efe0b9" stroke="#8a6a3a" stroke-width="6"/>
  <rect x="20" y="20" width="760" height="{h}" rx="18" fill="#efe0b9" filter="url(#rough)"/>"""


def text_lines(lines, x, y, size=26, gap=40, family="Georgia, serif", color="#3b2a14", anchor="start"):
    out = []
    for i, line in enumerate(lines):
        weight = "normal"
        style = "normal"
        txt = line
        if txt.startswith("**"):
            weight, txt = "bold", txt[2:]
        elif txt.startswith("__"):
            style, txt = "italic", txt[2:]
        out.append(f'<text x="{x}" y="{y + i * gap}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
                   f'font-style="{style}" fill="{color}" text-anchor="{anchor}">{escape(txt)}</text>')
    return "\n  ".join(out)


def handout_svg(path, title, lines, extra="", height=1000, seal=None):
    h = height - 40
    seal_svg = ""
    if seal:
        seal_svg = (f'<circle cx="680" cy="{height - 110}" r="60" fill="#b4231e" fill-opacity="0.85"/>'
                    f'<text x="680" y="{height - 92}" font-family="Yu Gothic, Meiryo, sans-serif" font-size="54" '
                    f'fill="#fff3d6" text-anchor="middle">{escape(seal)}</text>')
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}" viewBox="0 0 800 {height}">
  {PARCHMENT.format(h=h)}
  <text x="400" y="100" font-family="Georgia, serif" font-size="40" font-weight="bold" fill="#5a1d10" text-anchor="middle">{escape(title)}</text>
  <line x1="80" y1="125" x2="720" y2="125" stroke="#8a6a3a" stroke-width="3"/>
  {text_lines(lines, 70, 180)}
  {extra}
  {seal_svg}
</svg>
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)


def handout_headband(path):
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500">
  <rect width="800" height="500" fill="#2b3a2a"/>
  <text x="400" y="60" font-family="Georgia, serif" font-size="34" font-weight="bold" fill="#f4e7c5" text-anchor="middle">Morceau de bandeau trouvé dans les roseaux</text>
  <path d="M60 160 L700 140 L740 360 L90 380 Z" fill="#26324a"/>
  <rect x="200" y="170" width="380" height="170" rx="16" fill="#b9c0c7" stroke="#6b7480" stroke-width="8"/>
  <path d="M250 255 q35 -40 70 0 t70 0 t70 0 t70 0" stroke="#4a525c" stroke-width="12" fill="none"/>
  <path d="M250 300 q35 -40 70 0 t70 0 t70 0 t70 0" stroke="#4a525c" stroke-width="12" fill="none"/>
  <path d="M250 210 q35 -40 70 0 t70 0 t70 0 t70 0" stroke="#4a525c" stroke-width="12" fill="none"/>
  <line x1="215" y1="330" x2="565" y2="185" stroke="#2a2a2a" stroke-width="14"/>
  <text x="400" y="440" font-family="Georgia, serif" font-size="26" fill="#f4e7c5" text-anchor="middle">Le symbole est rayé d'un grand trait : la marque d'un ninja déserteur.</text>
</svg>
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)


def handout_island_map(path):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800">
  {PARCHMENT.format(h=760)}
  <text x="400" y="90" font-family="Georgia, serif" font-size="38" font-weight="bold" fill="#5a1d10" text-anchor="middle">Plan de l'île — NE PAS MONTRER</text>
  <path d="M170 420 C150 250 330 180 470 200 C640 220 690 360 640 480 C590 600 400 650 280 600 C200 570 180 500 170 420 Z" fill="#c9d6a0" stroke="#5a4a2a" stroke-width="5"/>
  <path d="M90 300 C110 330 120 360 100 400" stroke="#6a8aa0" stroke-width="4" fill="none"/>
  <text x="120" y="660" font-family="Georgia, serif" font-size="24" fill="#3b2a14">Barques cachées ici (ouest)</text>
  <line x1="215" y1="420" x2="480" y2="410" stroke="#3b2a14" stroke-width="4" stroke-dasharray="12 10"/>
  <rect x="260" y="380" width="14" height="70" fill="#a02a1a"/><rect x="300" y="380" width="14" height="70" fill="#a02a1a"/>
  <rect x="250" y="372" width="74" height="12" fill="#a02a1a"/>
  <rect x="480" y="330" width="110" height="90" fill="#8a6a3a" stroke="#3b2a14" stroke-width="4"/>
  <text x="535" y="315" font-family="Georgia, serif" font-size="24" fill="#3b2a14" text-anchor="middle">vieux sanctuaire</text>
  <path d="M440 470 l40 40 m0 -40 l-40 40" stroke="#b4231e" stroke-width="10"/>
  <text x="470" y="550" font-family="Georgia, serif" font-size="26" font-weight="bold" fill="#b4231e" text-anchor="middle">creuser ici</text>
  <text x="300" y="250" font-family="Georgia, serif" font-size="22" fill="#3b2a14">camp</text>
  <text x="400" y="720" font-family="Georgia, serif" font-size="24" font-style="italic" fill="#3b2a14" text-anchor="middle">« Le brouillard tous les soirs. Le reste du village partira d'ici dix jours. » — K.</text>
</svg>
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)
