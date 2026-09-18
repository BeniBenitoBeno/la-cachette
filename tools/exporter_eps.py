"""Convertit les logos SVG en EPS vectoriel (pour l'imprimeur).

Les SVG produits par la chaîne de vectorisation n'utilisent que trois
commandes — M, C, Z — ce qui se traduit directement en PostScript.
L'axe Y est inversé (SVG vers le bas, PostScript vers le haut) et chaque
tracé est rempli en règle pair-impair, comme dans le SVG.
"""
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGOS = os.path.join(RACINE, "assets", "logos")

NOMS = {
    "la-cachette-golfe-saint-tropez": "La Cachette - Golfe de Saint Tropez",
    "la-cachette-ile-maurice": "La Cachette - Ile Maurice",
    "la-cachette-vars": "La Cachette - Vars",
}

_PATH = re.compile(r'<path\b[^>]*?d="([^"]*)"[^>]*?(?:transform="translate\(([^)]*)\)")?\s*/>')
_JETON = re.compile(r"[MCZ]|-?\d*\.?\d+")


def _tracer(d, tx, ty):
    """Un `d` SVG -> lignes PostScript. Retourne aussi les points, pour contrôle."""
    jetons = _JETON.findall(d)
    lignes, points = [], []
    i = 0
    while i < len(jetons):
        j = jetons[i]
        if j == "M":
            x, y = float(jetons[i + 1]) + tx, float(jetons[i + 2]) + ty
            lignes.append(f"{x:.2f} {y:.2f} m")
            points.append((x, y))
            i += 3
        elif j == "C":
            v = [float(n) for n in jetons[i + 1:i + 7]]
            x1, y1, x2, y2, x3, y3 = (v[0] + tx, v[1] + ty, v[2] + tx,
                                      v[3] + ty, v[4] + tx, v[5] + ty)
            lignes.append(f"{x1:.2f} {y1:.2f} {x2:.2f} {y2:.2f} {x3:.2f} {y3:.2f} c")
            points.append((x3, y3))
            i += 7
        elif j == "Z":
            lignes.append("h")
            i += 1
        else:                                   # coordonnée orpheline : ignorée
            i += 1
    return lignes, points


def convertir(base):
    src = os.path.join(LOGOS, base + ".svg")
    svg = open(src, encoding="utf-8").read()
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg)
    larg, haut = int(vb.group(1)), int(vb.group(2))

    corps, tous = [], []
    for d, tr in _PATH.findall(svg):
        tx, ty = (0.0, 0.0)
        if tr:
            a, b = tr.split(",")
            tx, ty = float(a), float(b)
        lignes, points = _tracer(d, tx, ty)
        if not lignes:
            continue
        corps.append("n\n" + "\n".join(lignes) + "\nf")
        tous.extend(points)

    eps = f"""%!PS-Adobe-3.0 EPSF-3.0
%%Creator: La Cachette - tools/exporter_eps.py
%%Title: {NOMS[base]}
%%BoundingBox: 0 0 {larg} {haut}
%%HiResBoundingBox: 0 0 {larg}.0 {haut}.0
%%DocumentData: Clean7Bit
%%LanguageLevel: 2
%%EndComments
%%BeginProlog
/n {{ newpath }} bind def
/m {{ moveto }} bind def
/c {{ curveto }} bind def
/h {{ closepath }} bind def
/f {{ eofill }} bind def
%%EndProlog
gsave
0 setgray
0 {haut} translate
1 -1 scale
{chr(10).join(corps)}
grestore
showpage
%%EOF
"""
    dest = os.path.join(LOGOS, base + ".eps")
    with open(dest, "w", encoding="ascii", newline="\n") as f:
        f.write(eps)

    xs = [p[0] for p in tous]
    ys = [p[1] for p in tous]
    print(f"{base + '.eps':44s} {larg}x{haut} pt  {len(corps):3d} tracés  "
          f"{len(eps)/1024:6.0f} Ko  "
          f"points x[{min(xs):.0f},{max(xs):.0f}] y[{min(ys):.0f},{max(ys):.0f}]")
    return larg, haut, min(xs), max(xs), min(ys), max(ys)


def main():
    for base in NOMS:
        larg, haut, x0, x1, y0, y1 = convertir(base)
        # contrôle : les points doivent tenir dans le viewBox
        assert -2 <= x0 and x1 <= larg + 2, f"{base}: débordement en X"
        assert -2 <= y0 and y1 <= haut + 2, f"{base}: débordement en Y"
    print("\nContrôle : tous les tracés tiennent dans leur boîte englobante.")


if __name__ == "__main__":
    main()
