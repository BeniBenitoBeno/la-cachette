"""Vectorise les deux logos existants (JPG gravure) en SVG propres."""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import svgkit  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGOS = os.path.join(RACINE, "assets", "logos")

SOURCES = [
    ("la-cachette-ile-maurice", 4, "La Cachette — Ile Maurice"),
    ("la-cachette-golfe-saint-tropez", 2, "La Cachette — Golfe de Saint Tropez"),
]


def main():
    for nom, echelle, titre in SOURCES:
        src = os.path.join(LOGOS, nom + ".jpg")
        im = Image.open(src)
        if im.mode != "RGB":
            im = im.convert("RGB")
        g = im.convert("L").resize(
            (im.width * echelle, im.height * echelle), Image.LANCZOS)

        masque = svgkit.recadrer(svgkit.binariser(g))
        h, w = masque.shape
        paths = svgkit.vectoriser(masque)

        for suffixe, couleur in (("", "currentColor"), ("-blanc", svgkit.BLANC)):
            dest = os.path.join(LOGOS, nom + suffixe + ".svg")
            taille = svgkit.ecrire_svg(dest, paths, w, h, titre, couleur)
            print(f"{os.path.basename(dest):48s} {w}x{h}  "
                  f"{len(paths):3d} tracés  {taille/1024:6.0f} Ko")


if __name__ == "__main__":
    main()
