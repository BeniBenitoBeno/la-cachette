"""Prépare les photos d'une maison pour le web.

Convertit tout en JPEG progressif, largeur max 2200 px, et produit deux tailles :
la pleine (galerie et visionneuse) et une vignette 700 px.
Les noms de fichiers de la source servent de légendes — ce sont ceux du
photographe, donc la seule information fiable dont on dispose sur les pièces.

    python tools/preparer_photos.py "<dossier source>" maurice
"""
import os
import re
import sys
import unicodedata

from PIL import Image, ImageOps

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LARGE, VIGNETTE, QUALITE = 2200, 700, 82


def slug(nom):
    nom = unicodedata.normalize("NFKD", nom).encode("ascii", "ignore").decode()
    nom = re.sub(r"[^a-zA-Z0-9]+", "-", nom).strip("-").lower()
    return re.sub(r"-+", "-", nom)


def legende(nom):
    """Nettoie le nom de fichier pour en faire une légende présentable."""
    t = re.sub(r"\s*-\s*copie$", "", nom.strip(), flags=re.I)
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"\bsdb\b", "salle de bains", t, flags=re.I)
    t = re.sub(r"\bwc\b", "WC", t, flags=re.I)
    t = re.sub(r"\bext\b\.?", "extérieure", t, flags=re.I)
    t = re.sub(r"\bvue\b", "vue", t, flags=re.I)
    return t[0].upper() + t[1:]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    source, maison = sys.argv[1], sys.argv[2]
    dest = os.path.join(RACINE, "assets", "img", maison)
    os.makedirs(dest, exist_ok=True)

    fiches = []
    for nom in sorted(os.listdir(source)):
        base, ext = os.path.splitext(nom)
        if ext.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        if base.lower().endswith("- copie"):
            continue
        im = Image.open(os.path.join(source, nom))
        im = ImageOps.exif_transpose(im).convert("RGB")
        s = slug(base)
        for suffixe, large in (("", LARGE), ("-v", VIGNETTE)):
            copie = im.copy()
            copie.thumbnail((large, large), Image.LANCZOS)
            copie.save(os.path.join(dest, s + suffixe + ".jpg"),
                       "JPEG", quality=QUALITE, optimize=True, progressive=True)
        fiches.append((s, legende(base), im.width, im.height))

    total = sum(os.path.getsize(os.path.join(dest, f))
                for f in os.listdir(dest)) / 1024 / 1024
    print(f"{len(fiches)} photos -> {dest}  ({total:.1f} Mo au total)")
    with open(os.path.join(dest, "manifeste.txt"), "w", encoding="utf-8") as f:
        for s, l, w, h in fiches:
            f.write(f"{s}\t{l}\t{w}x{h}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
