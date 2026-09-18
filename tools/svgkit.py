"""Outils communs : binarisation, recadrage sur l'encre, vectorisation, nettoyage SVG.

Même chaîne pour les trois logos, pour qu'ils aient exactement la même
texture de trait : LANCZOS -> normalisation -> seuil 135 -> vtracer spline.
"""
import os
import re
import tempfile

import numpy as np
import vtracer
from PIL import Image

SEUIL = 135          # seuil d'encre commun aux trois logos
NOIR, BLANC = "#111110", "#ffffff"


def binariser(img_gris, seuil=SEUIL, lo=30.0, hi=235.0):
    """Image en niveaux de gris -> masque booléen (True = encre)."""
    a = np.asarray(img_gris).astype(np.float32)
    a = np.clip((a - lo) / (hi - lo) * 255.0, 0, 255)
    return a < seuil


def recadrer(masque, marge=0.0):
    """Recadre sur la boîte englobante de l'encre. marge en fraction de largeur."""
    ys, xs = np.where(masque)
    if len(xs) == 0:
        raise ValueError("aucune encre trouvée")
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    m = int(round((x1 - x0) * marge))
    if m:
        h, w = masque.shape
        x0, x1 = max(0, x0 - m), min(w, x1 + m)
        y0, y1 = max(0, y0 - m), min(h, y1 + m)
    return masque[y0:y1, x0:x1]


def vectoriser(masque, speckle=4):
    """Masque booléen -> liste de <path .../> bruts (chaînes)."""
    png = os.path.join(tempfile.gettempdir(), "_cachette_trace.png")
    svg = os.path.join(tempfile.gettempdir(), "_cachette_trace.svg")
    Image.fromarray(np.where(masque, 0, 255).astype(np.uint8)).save(png)
    vtracer.convert_image_to_svg_py(
        png, svg,
        colormode="binary", hierarchical="stacked", mode="spline",
        filter_speckle=speckle, corner_threshold=60,
        length_threshold=4.0, splice_threshold=45, path_precision=2,
    )
    brut = open(svg, encoding="utf-8").read()
    return re.findall(r"<path\b[^>]*/>", brut)


_NOMBRE = re.compile(r"-?\d+\.\d+")


def _alleger(path):
    """Retire le fill par path et arrondit les coordonnées à 1 décimale."""
    path = re.sub(r'\s*fill="[^"]*"', "", path)
    return _NOMBRE.sub(lambda m: f"{float(m.group()):.1f}".rstrip("0").rstrip("."), path)


def ecrire_svg(chemin, paths, largeur, hauteur, titre, couleur="currentColor"):
    corps = "\n  ".join(_alleger(p) for p in paths)
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {largeur} {hauteur}" role="img" aria-labelledby="t">\n'
        f"<title id=\"t\">{titre}</title>\n"
        f'<g fill="{couleur}" fill-rule="evenodd">\n  {corps}\n</g>\n</svg>\n'
    )
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(svg)
    return len(svg)
