"""Compose la planche de contact des signatures (logos-planche.png).

    python tools/planche_logos.py

Les logos à montrer sont listés ci-dessous : fichier bitmap d'origine et
légende. La planche sert d'aperçu dans BRAND.md et sur la page « L'esprit ».
"""
import os

from PIL import Image, ImageChops, ImageDraw, ImageFont

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOND = (242, 241, 237)
ENCRE = (120, 118, 112)

SIGNATURES = [
    ("la-cachette-golfe-saint-tropez.jpg", "Golfe de Saint-Tropez"),
    ("la-cachette-ile-maurice.jpg", "Île Maurice"),
]

# Les gravures sont normalisées à la même hauteur. 260 px est la taille
# native de la plus petite (Île Maurice) : on ne l'agrandit donc jamais.
CASE, HAUTEUR, GRAVURE = 640, 430, 260


def police(taille):
    for nom in ("seguiui.ttf", "segoeui.ttf", "arial.ttf"):
        chemin = os.path.join(r"C:\Windows\Fonts", nom)
        if os.path.exists(chemin):
            return ImageFont.truetype(chemin, taille)
    return ImageFont.load_default()


def rogner(im, seuil=235):
    """Enlève le fond clair autour de la gravure."""
    gris = im.convert("L")
    boite = gris.point(lambda v: 255 if v < seuil else 0).getbbox()
    return im.crop(boite) if boite else im


def blanchir(im, seuil=232):
    """Pousse le papier de la gravure au blanc pur, pour qu'il disparaisse
    complètement dans le fond de la planche une fois multiplié."""
    return im.point(lambda v: 255 if v >= seuil else round(v * 255 / seuil))


def main():
    planche = Image.new("RGB", (CASE * len(SIGNATURES), HAUTEUR), FOND)
    dessin = ImageDraw.Draw(planche)
    f = police(17)

    for i, (fichier, legende) in enumerate(SIGNATURES):
        im = rogner(Image.open(os.path.join(RACINE, "assets", "logos", fichier)).convert("RGB"))
        im = blanchir(im.resize((round(im.width * GRAVURE / im.height), GRAVURE), Image.LANCZOS))
        x = i * CASE + (CASE - im.width) // 2
        y = (HAUTEUR - 90 - im.height) // 2
        # fondu « multiplier » : le papier des gravures disparaît dans le fond
        case = planche.crop((x, y, x + im.width, y + im.height))
        planche.paste(ImageChops.multiply(case, im), (x, y))
        l, t, r, b = dessin.textbbox((0, 0), legende, font=f)
        dessin.text((i * CASE + (CASE - (r - l)) // 2, HAUTEUR - 62), legende, font=f, fill=ENCRE)

    sortie = os.path.join(RACINE, "logos-planche.png")
    planche.save(sortie)
    print(f"{sortie} — {planche.width}x{planche.height}, {len(SIGNATURES)} signatures")


if __name__ == "__main__":
    main()
