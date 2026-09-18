"""Dessine le logo « La Cachette — Vars » dans la grammaire des deux autres.

Même composition que le logo Golfe de Saint-Tropez : un bassin rectangulaire en
perspective, son reflet, un arbre du lieu de chaque côté, un soleil bas sur
l'horizon, trois oiseaux, puis le nom. Ici : mélèzes et crête des Hautes-Alpes.

Le dessin est produit en niveaux de gris à 3x, réduit, puis passé dans
exactement la même chaîne de vectorisation que les deux logos existants
(svgkit) pour que la texture du trait soit identique.
"""
import math
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
import svgkit  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGOS = os.path.join(RACINE, "assets", "logos")
GARAMOND = r"C:\Windows\Fonts\GARA.TTF"

# Repères repris du logo Golfe de Saint-Tropez (source 1536 x 1024)
W, H = 1536, 1024
S = 3                       # suréchantillonnage
EP = 1.75                   # épaisseur de référence du burin

HORIZON = 438
BASSIN = dict(xl_loin=566, xr_loin=970, y_loin=452,
              xl_pres=302, xr_pres=1234, y_pres=596)
EAU_BAS = 622

rng = random.Random(20260910)

img = Image.new("L", (W * S, H * S), 255)
d = ImageDraw.Draw(img)


# ----------------------------------------------------------------- primitives

def _p(x, y):
    return (x * S, y * S)


def trait(p0, p1, ep=1.0, dessin=None):
    (dessin or d).line([_p(*p0), _p(*p1)], fill=0,
                       width=max(1, round(ep * EP * S)))


def polyligne(pts, ep=1.0, dessin=None):
    for a, b in zip(pts, pts[1:]):
        trait(a, b, ep, dessin)


def hachurer(polygone, angle, pas, ep=0.8, densite=1.0, decoupe=None):
    """Hachures parallèles découpées à l'intérieur d'un polygone.

    `decoupe` : polygone supplémentaire, l'encre ne sort pas de l'intersection.
    """
    masque = Image.new("L", img.size, 0)
    ImageDraw.Draw(masque).polygon([_p(*p) for p in polygone], fill=255)
    if decoupe is not None:
        limite = Image.new("L", img.size, 0)
        ImageDraw.Draw(limite).polygon([_p(*p) for p in decoupe], fill=255)
        masque = ImageChops.multiply(masque, limite)

    lignes = Image.new("L", img.size, 0)
    dl = ImageDraw.Draw(lignes)
    a = math.radians(angle)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    diag = math.hypot(W, H)
    for i in range(-int(diag / pas) - 2, int(diag / pas) + 2):
        if rng.random() > densite:
            continue
        t = i * pas + rng.uniform(-pas * 0.16, pas * 0.16)
        cx, cy = W / 2 + nx * t, H / 2 + ny * t
        dl.line([_p(cx - dx * diag, cy - dy * diag),
                 _p(cx + dx * diag, cy + dy * diag)],
                fill=255, width=max(1, round(ep * EP * S)))

    img.paste(0, (0, 0), ImageChops.multiply(masque, lignes))


def masse(cx, cy, rx, ry, n, lg=(4, 11), ep=0.75, angle=None):
    """Amas de courts traits : le feuillage sombre des gravures."""
    for _ in range(n):
        while True:
            u, v = rng.uniform(-1, 1), rng.uniform(-1, 1)
            if u * u + v * v <= 1:
                break
        x, y = cx + u * rx, cy + v * ry
        a = rng.uniform(0, math.pi) if angle is None else \
            math.radians(angle + rng.uniform(-24, 24))
        l = rng.uniform(*lg)
        trait((x - math.cos(a) * l / 2, y - math.sin(a) * l / 2),
              (x + math.cos(a) * l / 2, y + math.sin(a) * l / 2), ep)


def tirets(p0, p1, ep=0.8, couverture=0.5, longueur=(10, 34)):
    """Une ride : suite de tirets entre deux points.

    `couverture` est la part réellement encrée de la distance parcourue,
    de 0 (rien) à 1 (trait plein).
    """
    x0, y0 = p0
    x1, y1 = p1
    total = x1 - x0
    if total <= 2 or couverture <= 0.01:
        return
    c = min(0.97, couverture)
    x = x0 - rng.uniform(0, longueur[1])
    while x < x1:
        lg = rng.uniform(*longueur)
        blanc = lg * (1 - c) / c * rng.uniform(0.6, 1.4)
        a, b = max(x, x0), min(x + lg, x1)
        if b - a > 1.5:
            u0, u1 = (a - x0) / total, (b - x0) / total
            trait((a, y0 + (y1 - y0) * u0), (b, y0 + (y1 - y0) * u1), ep)
        x += lg + blanc


# -------------------------------------------------------------------- montagne

# Chaîne lointaine : deux hauts sommets, trait fin, presque en réserve
CRETE_LOIN = [
    (196, HORIZON), (268, 356), (330, 332), (398, 288), (462, 316),
    (536, 244), (604, 214), (668, 274), (726, 300), (790, 276),
    (856, 240), (918, 230), (982, 286), (1046, 258), (1112, 296),
    (1178, 268), (1242, 320), (1310, 352), (1372, HORIZON),
]
# Chaîne proche : le col central laisse passer le soleil
CRETE_PRES = [
    (150, HORIZON), (238, 392), (300, 410), (356, 330), (398, 352),
    (462, 250), (530, 318), (582, 292), (640, 352), (700, 386),
    (768, 402), (836, 380), (890, 340), (948, 300), (1010, 328),
    (1076, 262), (1140, 330), (1196, 306), (1256, 358), (1320, 392),
    (1400, HORIZON),
]


def _etaler(sommets, x0, x1):
    """Ramène une crête dans l'empreinte horizontale du logo Grimaud."""
    a = sommets[0][0]
    b = sommets[-1][0]
    return [(x0 + (x - a) * (x1 - x0) / (b - a), y) for x, y in sommets]


# empreinte de la scène reprise du logo Golfe de Saint-Tropez : x 232 -> 1304
CRETE_LOIN = _etaler(CRETE_LOIN, 246, 1292)
CRETE_PRES = _etaler(CRETE_PRES, 232, 1304)


def silhouette(sommets):
    return list(sommets) + [(sommets[-1][0], HORIZON + 8), (sommets[0][0], HORIZON + 8)]


def crete(sommets, ep, pas, densite, ombre, ravines):
    limite = silhouette(sommets)
    polyligne(sommets, ep)
    for (x0, y0), (x1, y1) in zip(sommets, sommets[1:]):
        if y1 <= y0:                       # versant éclairé : réserve
            continue
        flanc = [(x0, y0), (x1, y1),
                 (x1 - ombre * 0.22, y1 + ombre),
                 (x0 - ombre * 0.12, y0 + ombre * 0.5)]
        hachurer(flanc, 62, pas, 0.68, densite, decoupe=limite)
    if ravines:
        for (x0, y0), (x1, y1) in zip(sommets, sommets[1:]):
            if y1 > y0:
                continue
            for _ in range(2):
                u = rng.uniform(0.3, 0.8)
                px, py = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
                trait((px, py), (px + rng.uniform(-3, 3), py + rng.uniform(12, 26)), 0.55)


def montagnes():
    crete(CRETE_LOIN, 0.85, 7.5, 0.4, 34, False)
    crete(CRETE_PRES, 1.5, 3.4, 0.95, 56, True)


# ---------------------------------------------------------------------- arbres

def meleze(x, ybase, hauteur, envergure, ep=0.85):
    """Mélèze : cône élancé, étages de feuillage sombre, cime effilée."""
    ytop = ybase - hauteur
    trait((x, ybase + 4), (x, ytop + hauteur * 0.06), ep * 1.9)

    etages = max(8, int(hauteur / 7.5))
    for i in range(etages):
        t = (i + 1) / etages
        y = ytop + hauteur * (t ** 0.9)
        port = envergure * (t ** 1.12)
        if port < 2.5:
            continue
        for sens in (-1, 1):
            bout = (x + sens * port * rng.uniform(0.88, 1.12),
                    y + port * rng.uniform(0.30, 0.52))
            trait((x, y), bout, ep)
            masse((x + bout[0]) / 2, (y + bout[1]) / 2 + port * 0.10,
                  port * 0.52, max(2.4, port * 0.24),
                  int(6 + port * 1.5), lg=(3, 7 + port * 0.16), ep=0.62,
                  angle=90 + sens * 26)
        if t > 0.25:
            masse(x, y + port * 0.16, port * 0.30, port * 0.15,
                  int(4 + port), lg=(3, 8), ep=0.6, angle=90)

    masse(x, ytop + hauteur * 0.05, envergure * 0.10 + 2, hauteur * 0.05,
          14, lg=(3, 7), ep=0.6, angle=90)


def bosquet(xc, ybase):
    """Bosquet de mélèzes à droite, pendant du pin parasol de Grimaud."""
    meleze(xc - 74, ybase + 4, 118, 27)
    meleze(xc + 78, ybase + 5, 136, 31)
    meleze(xc + 8, ybase, 208, 46)


# ------------------------------------------------------------- herbe et rochers

def touffe(x, y, taille, brins=15):
    for _ in range(brins):
        h = taille * rng.uniform(0.4, 1.0)
        pente = rng.uniform(-0.6, 0.6)
        polyligne([(x, y),
                   (x + pente * h * 0.34, y - h * 0.56),
                   (x + pente * h * 1.2, y - h)], 0.72)


def berge(x0, x1, y):
    x = x0
    while x < x1:
        touffe(x + rng.uniform(-4, 4), y + rng.uniform(-4, 4), rng.uniform(16, 40))
        x += rng.uniform(5.5, 10)
    masse((x0 + x1) / 2, y + 5, (x1 - x0) / 2, 7,
          int((x1 - x0) * 0.9), lg=(4, 14), ep=0.7, angle=0)


def rocher(x, y, l, h):
    pts = [(x - l / 2, y), (x - l * 0.36, y - h * 0.74),
           (x - l * 0.02, y - h), (x + l * 0.32, y - h * 0.62), (x + l / 2, y)]
    polyligne(pts + [pts[0]], 1.1)
    hachurer(pts, 66, 4.0, 0.7, densite=0.9)


# ------------------------------------------------------------------------- eau

def bassin():
    b = BASSIN
    reflets = [(392, 0.70, 46), (1080, 0.60, 52), (768, 0.40, 34)]

    y = b["y_loin"] + 2.5
    while y < b["y_pres"]:
        t = (y - b["y_loin"]) / (b["y_pres"] - b["y_loin"])
        xl = b["xl_loin"] + (b["xl_pres"] - b["xl_loin"]) * t
        xr = b["xr_loin"] + (b["xr_pres"] - b["xr_loin"]) * t
        ondul = math.sin(t * 6.4 + 0.7) * 1.4
        fond = 0.24 + 0.10 * math.sin(t * 8.3) + t * 0.10
        tirets((xl + 5, y + ondul), (xr - 5, y + ondul),
               ep=0.62, couverture=fond, longueur=(26, 110))
        for cx, prof, demi0 in reflets:
            if t > prof:
                continue
            k = 1 - t / prof
            demi = demi0 * (0.70 + t * 1.35)
            cxx = 768 + (cx - 768) * (1 - t * 0.16)
            tirets((max(xl + 3, cxx - demi), y + ondul),
                   (min(xr - 3, cxx + demi), y + ondul),
                   ep=0.9, couverture=0.62 + 0.36 * k, longueur=(36, 120))
        y += 3.9 + t * 1.9

    trait((b["xl_loin"], b["y_loin"]), (b["xl_pres"], b["y_pres"]), 1.15)
    trait((b["xr_loin"], b["y_loin"]), (b["xr_pres"], b["y_pres"]), 1.15)
    trait((b["xl_loin"], b["y_loin"]), (b["xr_loin"], b["y_loin"]), 1.0)
    trait((b["xl_pres"], b["y_pres"]), (b["xr_pres"], b["y_pres"]), 1.35)

    y = b["y_pres"] + 5
    while y < EAU_BAS:
        t = (y - b["y_pres"]) / (EAU_BAS - b["y_pres"])
        marge = 60 * t
        tirets((b["xl_pres"] - marge - 52, y), (b["xr_pres"] + marge + 52, y),
               ep=0.7, couverture=0.46 - t * 0.28, longueur=(34, 140))
        y += 3.8 + t * 3.0


# --------------------------------------------------------------- soleil, oiseaux

def soleil(cx, cy, r):
    halo = Image.new("L", img.size, 0)
    ImageDraw.Draw(halo).ellipse(
        [_p(cx - r * 1.34, cy - r * 1.34), _p(cx + r * 1.34, cy + r * 1.34)], fill=255)
    ImageDraw.Draw(halo).rectangle([_p(cx - r * 1.4, cy), _p(cx + r * 1.4, cy + r * 1.4)], fill=0)
    img.paste(255, (0, 0), halo)
    arc = [(cx + r * math.cos(a), cy + r * math.sin(a))
           for a in [math.pi + i / 48 * math.pi for i in range(49)]]
    polyligne(arc, 0.85)
    hachurer([(cx - r, cy)] + arc + [(cx + r, cy)], 0, 4.2, 0.6, densite=0.7)


def oiseau(x, y, e):
    polyligne([(x - e, y), (x - e * 0.42, y - e * 0.62), (x, y - e * 0.10)], 0.85)
    polyligne([(x, y - e * 0.10), (x + e * 0.44, y - e * 0.66), (x + e, y - e * 0.02)], 0.85)


# ------------------------------------------------------------------------ texte

def coller_la_cachette(plan):
    """Reprend le lettrage « La Cachette » du logo Golfe de Saint-Tropez."""
    src = Image.open(os.path.join(LOGOS, "la-cachette-golfe-saint-tropez.jpg"))
    src = src.convert("RGB").convert("L")
    boite = (575, 686, 963, 758)
    mot = src.crop(boite)
    plan.paste(ImageChops.darker(plan.crop(boite), mot), boite[:2])
    return boite[3]


def poser_vars(plan, y_haut):
    police = ImageFont.truetype(GARAMOND, 52)
    dp = ImageDraw.Draw(plan)
    ecart = 4.0
    largeurs = [dp.textlength(c, font=police) for c in "Vars"]
    x = 768 - (sum(largeurs) + ecart * 3) / 2
    for c, lc in zip("Vars", largeurs):
        dp.text((x, y_haut), c, font=police, fill=0)
        x += lc + ecart


# ------------------------------------------------------------------------ scène

def dessiner():
    montagnes()
    soleil(768, HORIZON, 42)
    berge(238, 556, HORIZON + 10)
    berge(980, 1298, HORIZON + 10)
    meleze(392, HORIZON + 12, 268, 56)
    bosquet(1072, HORIZON + 12)
    for x, y, e in ((892, 300, 17), (946, 278, 12), (856, 268, 10)):
        oiseau(x, y, e)
    bassin()


def main():
    dessiner()
    plan = img.resize((W, H), Image.LANCZOS)
    bas = coller_la_cachette(plan)
    poser_vars(plan, bas + 10)

    masque = svgkit.recadrer(svgkit.binariser(plan))
    h, w = masque.shape
    paths = svgkit.vectoriser(masque)
    for suffixe, couleur in (("", "currentColor"), ("-blanc", svgkit.BLANC)):
        dest = os.path.join(LOGOS, "la-cachette-vars" + suffixe + ".svg")
        taille = svgkit.ecrire_svg(dest, paths, w, h, "La Cachette — Vars", couleur)
        print(f"{os.path.basename(dest):40s} {w}x{h}  {len(paths):3d} tracés  "
              f"{taille/1024:6.0f} Ko")

    png = os.path.join(LOGOS, "la-cachette-vars.png")
    Image.fromarray((~masque * 255).astype("uint8")).save(png)
    print(f"{os.path.basename(png):40s} {w}x{h}  (équivalent des JPG des deux autres)")


if __name__ == "__main__":
    main()
