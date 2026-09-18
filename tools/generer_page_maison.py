"""Génère une page maison (grimaud.html, vars.html) à partir d'un descriptif.

La page Île Maurice sert de gabarit : en-tête, formulaire de séjour, pied,
visionneuse et scripts en sont repris tels quels ; seul le contenu entre le
héros et « Séjourner ici » est produit ici.

    python tools/generer_page_maison.py grimaud
    python tools/generer_page_maison.py vars
"""
import html
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- descriptifs
MAISONS = {
    "grimaud": {
        "page": "grimaud.html",
        "titre": "Grimaud — La Cachette",
        "description": "La Cachette Grimaud : quatre chambres face au golfe de Saint-Tropez, piscine à débordement, jacuzzi, tennis.",
        "classe": "h-grimaud",
        "index": "01 — Golfe de Saint-Tropez",
        "nom": "Grimaud",
        "lieu": "Quatre chambres · piscine à débordement · vue sur le golfe",
        "valeur": "Grimaud — Golfe de Saint-Tropez",
        "hero": [
            ("piscine-et-mer-1", "La piscine à débordement et le golfe", "center 55%"),
            ("maison-depuis-la-piscine", "La maison vue depuis la piscine", "center 50%"),
            ("mer-depuis-le-canape-ext", "Le golfe depuis le canapé extérieur", "center 50%"),
            ("salle-a-manger-exterieure-5", "La salle à manger extérieure", "center 50%"),
            ("chambre-1-vers-la-mer", "La chambre 1, ouverte sur la mer", "center 50%"),
            ("vue-de-la-maison-depuis-le-lit-balinais", "La maison depuis le lit balinais", "center 50%"),
        ],
        "intro": [
            "Une maison contemporaine posée sur les hauteurs de Grimaud, tournée vers "
            "le golfe de Saint-Tropez. Devant elle, une pelouse, une piscine à "
            "débordement dont le bord se confond avec la mer, un jacuzzi, un lit "
            "balinais sous les pins. La salle à manger extérieure, sous sa pergola de "
            "bois, regarde le même horizon.",
            "À l'intérieur, un grand séjour ouvert sur la terrasse, une cuisine "
            "équipée et quatre chambres — trois avec vue sur la mer — chacune avec "
            "sa salle de bains. Un court de tennis complète la propriété, et la "
            "plage est à quelques minutes.",
        ],
        "enbref": [
            ("Chambres", "4, dont trois face à la mer — chacune avec sa salle de bains"),
            ("Pièces de vie", "Salon-séjour, salle à manger, cuisine équipée"),
            ("Extérieur", "Piscine à débordement, jacuzzi, lit balinais, salle à manger sous pergola, canapé extérieur"),
            ("Aussi", "Court de tennis"),
            ("Plage", "À quelques minutes"),
        ],
        "sections": [
            ("exterieurs", "Dehors", "La piscine, le jardin et le golfe", [
                ("maison-depuis-la-piscine", "La maison depuis la piscine", True),
                ("piscine-et-mer-1", "Piscine et mer"),
                ("piscine-et-mer-2", "Piscine et mer, depuis la pelouse"),
                ("jaccuzzi-et-mer", "Le jacuzzi et la mer"),
                ("piscine-jardin", "La piscine depuis le jardin"),
                ("mer-depuis-le-canape-ext", "La mer depuis le canapé extérieur", True),
                ("canape-exterieur", "Le canapé extérieur"),
                ("vue-de-la-maison-depuis-la-terrasse-du-jaccuzzi", "La maison depuis la terrasse du jacuzzi"),
                ("vue-de-la-maison-depuis-le-lit-balinais", "La maison depuis le lit balinais"),
                ("vue-jardin-depuis-la-terrasse-ch2", "Le jardin depuis la terrasse de la chambre 2"),
                ("salle-a-manger-exterieure", "La salle à manger extérieure", True),
                ("salle-a-manger-exterieure-2", "Salle à manger extérieure, vers la mer"),
                ("salle-a-manger-exterieure-3", "Salle à manger extérieure, sous la pergola"),
                ("salle-a-manger-exterieure-4", "Salle à manger extérieure, la table de pierre"),
                ("salle-a-manger-exterieure-5", "Salle à manger extérieure, au soleil couchant"),
                ("vue-mer-depuis-table-pierre", "La mer depuis la table de pierre"),
                ("tennis", "Le court de tennis"),
            ]),
            ("vie", "Dedans", "Le séjour, la table et la cuisine", [
                ("salon-et-sejour", "Le salon et le séjour", True),
                ("salle-a-manger-1", "La salle à manger"),
                ("table-a-manger-interieure", "La table, ouverte sur la terrasse"),
                ("table-a-manger-interieure-2", "La table à manger intérieure"),
                ("cuisine", "La cuisine"),
                ("cuisine-2", "La cuisine, plan de travail"),
                ("couloir", "Le couloir, vers le jardin"),
                ("poissons", "Détail du salon"),
            ]),
            ("chambres", "Dormir", "Les quatre chambres", [
                ("chambre-1-vers-la-mer", "Chambre 1, vers la mer", True),
                ("chambre-1-vers-le-mur", "Chambre 1"),
                ("sdb-1-vue-mer", "Salle de bains 1, vue mer"),
                ("sdb-1-vue-douche", "Salle de bains 1, la douche"),
                ("chambre-2-vers-la-mer", "Chambre 2, vers la mer"),
                ("chambre-2-vers-le-lit", "Chambre 2"),
                ("chambre-2-vers-sdb", "Chambre 2, vers la salle de bains"),
                ("chambre-2-depuis-la-salle-de-bains", "Chambre 2, depuis la salle de bains"),
                ("chambre-3-vue-mer", "Chambre 3, vue mer", True),
                ("sdb-3", "Salle de bains 3"),
                ("chambre-4", "Chambre 4"),
                ("sdb-4", "Salle de bains 4"),
                ("terrasse-des-chambres-3-et-4", "La terrasse des chambres 3 et 4"),
                ("sdb5", "Salle de bains 5"),
                ("chambre-nuit", "Une chambre, la nuit"),
            ]),
            ("plage", "Au bout du chemin", "La plage", [
                ("plage", "La plage"),
            ]),
        ],
    },
    "vars": {
        "page": "vars.html",
        "titre": "Vars — La Cachette",
        "description": "La Cachette Vars : un chalet de cinq chambres et un dortoir au pied des pistes, spa, cheminée, ski room.",
        "classe": "h-vars",
        "index": "03 — Hautes-Alpes",
        "nom": "Vars",
        "lieu": "Cinq chambres et un dortoir · spa · au pied des pistes",
        "valeur": "Vars — Hautes-Alpes",
        "hero": [
            ("t-chalet-sous-la-neige", "Le chalet sous la neige", "center 45%"),
            ("0-vue-de-la-chambre-4", "La vallée depuis la chambre 4", "center 50%"),
            ("sejour-2", "Le séjour et la cheminée", "center 50%"),
            ("chambre-4-1", "La chambre 4, sous le toit", "center 50%"),
            ("spa-2", "Le spa", "center 50%"),
            ("chambre-5-3", "Les sommets depuis la chambre 5", "center 50%"),
        ],
        "intro": [
            "Un chalet de bois et de pierre, à Vars, dans les Hautes-Alpes, à quelques "
            "pas des remontées mécaniques. Les balcons donnent sur la vallée et les "
            "mélèzes ; l'hiver, la neige monte jusqu'aux fenêtres.",
            "Dedans, un grand séjour autour de la cheminée, une cuisine ouverte sur la "
            "salle à manger, cinq chambres et un dortoir pour les enfants. La chambre "
            "sous le toit a son balcon et sa longue-vue. Un spa extérieur et une ski "
            "room au retour des pistes.",
        ],
        "enbref": [
            ("Chambres", "5, plus un dortoir — la chambre 4 sous le toit, avec balcon"),
            ("Salles de bains", "4, dont une avec baignoire"),
            ("Pièces de vie", "Séjour avec cheminée, cuisine ouverte sur la salle à manger"),
            ("Extérieur", "Spa, balcons sur la vallée"),
            ("Aussi", "Ski room, longue-vue"),
            ("Pistes", "Remontées mécaniques à pied"),
        ],
        "sections": [
            ("exterieurs", "Dehors", "Le chalet, la neige et la vallée", [
                ("t-chalet-sous-la-neige", "Le chalet sous la neige", True),
                ("0-vue-de-la-salle-a-manger", "La vallée depuis la salle à manger"),
                ("0-vue-de-la-chambre-4", "La vallée depuis la chambre 4"),
                ("chambre-4-3", "Le balcon de la chambre 4"),
                ("chambre-5-3", "Les sommets depuis la chambre 5"),
                ("spa-1", "Le spa, face aux mélèzes"),
                ("spa-2", "Le spa"),
            ]),
            ("vie", "Dedans", "Le séjour, la cheminée et la cuisine", [
                ("sejour-1", "Le séjour", True),
                ("sejour-2", "Le séjour et la cheminée"),
                ("sejour-3", "La cheminée"),
                ("sejour-4", "Le feu"),
                ("cuisine-et-salle-a-manger", "La cuisine et la salle à manger"),
                ("cuisine", "La cuisine"),
                ("cuisine-2", "Détail de la cuisine"),
                ("ski-room-1", "La ski room"),
                ("ski-room-2", "La ski room, vers la vallée"),
            ]),
            ("chambres", "Dormir", "Les cinq chambres et le dortoir", [
                ("chambre-4-1", "Chambre 4, sous le toit", True),
                ("chambre-4-2", "Chambre 4, vers le balcon"),
                ("chambre-4-5", "Chambre 4, le mur de pierre"),
                ("chambre-4-6", "Chambre 4, détail"),
                ("chambre-4-7", "Chambre 4, la longue-vue"),
                ("chambre-1", "Chambre 1"),
                ("chambre-2", "Chambre 2"),
                ("chambre-3", "Chambre 3"),
                ("chambre-5-1", "Chambre 5"),
                ("chambre-5-2", "Chambre 5, vers la fenêtre"),
                ("dortoir", "Le dortoir"),
                ("salle-de-bains-1", "Salle de bains 1"),
                ("salle-de-bains-1-2", "Salle de bains 1, la douche"),
                ("salle-de-bains-3", "Salle de bains 3"),
                ("salle-de-bains-4-1", "Salle de bains 4, la baignoire", True),
                ("salle-de-bains-4-2", "Salle de bains 4, détail"),
                ("salle-de-bains-4-3", "Salle de bains 4, les vasques"),
                ("salle-de-bains-4-4", "Salle de bains 4, détail"),
                ("salle-de-bains-5", "Salle de bains 5"),
                ("salle-de-bains-51", "Salle de bains 5, la vasque"),
            ]),
            ("pistes", "Au pied des pistes", "Le chalet et les remontées mécaniques", [
                ("t-exterieur", "Le chalet, à gauche les remontées mécaniques"),
            ]),
        ],
    },
}


# ------------------------------------------------------------------ rendu
def e(t):
    return html.escape(t, quote=True)


def figure(maison, item):
    slug, legende = item[0], item[1]
    large = len(item) > 2 and item[2]
    base = f"assets/img/{maison}/{slug}"
    classe = ' class="large"' if large else ""
    return (
        f'      <figure{classe}>\n'
        f'        <button type="button" data-large="{base}.jpg" data-legende="{e(legende)}">\n'
        f'          <img src="{base}-v.jpg" alt="{e(legende)}" loading="lazy" decoding="async">\n'
        f'        </button>\n'
        f'        <figcaption>{e(legende)}</figcaption>\n'
        f'      </figure>\n'
    )


def corps(maison, m):
    out = []
    out.append(f'  <section class="hero {m["classe"]}" id="hero">\n    <div class="hero__diapos">\n')
    for i, (slug, alt, pos) in enumerate(m["hero"]):
        eager = ' loading="eager"' if i == 0 else ""
        out.append(f'      <img src="assets/img/{maison}/{slug}.jpg" alt="{e(alt)}" decoding="async"{eager}'
                   f' style="object-position:{pos}">\n')
    out.append(
        '    </div>\n'
        '    <div class="hero__texte">\n'
        f'      <span class="hero__index">{e(m["index"])}</span>\n'
        f'      <h1>{e(m["nom"])}</h1>\n'
        f'      <span class="hero__lieu" id="hero-lieu">{e(m["lieu"])}</span>\n'
        '      <a class="hero__cta" href="#reserver">Demander un séjour</a>\n'
        '    </div>\n'
        '  </section>\n\n'
    )
    out.append('  <section class="bloc intro" id="maison" data-sommaire="La maison">\n    <div>\n')
    for p in m["intro"]:
        out.append(f'      <p>{e(p)}</p>\n')
    out.append('    </div>\n    <ul class="enbref">\n')
    for b, s in m["enbref"]:
        out.append(f'      <li><b>{e(b)}</b><span>{e(s)}</span></li>\n')
    out.append('    </ul>\n  </section>\n\n')
    for ident, surtitre, h2, items in m["sections"]:
        out.append(
            f'  <section class="bloc" id="{ident}" data-sommaire="{e(surtitre)}">\n'
            f'    <p class="surtitre">{e(surtitre)}</p>\n'
            f'    <h2>{e(h2)}</h2>\n'
            '    <div class="grille">\n'
        )
        for it in items:
            chemin = os.path.join(RACINE, "assets", "img", maison, it[0] + ".jpg")
            if not os.path.exists(chemin):
                raise SystemExit(f"photo absente : {chemin}")
            out.append(figure(maison, it))
        out.append('    </div>\n  </section>\n\n')
    return "".join(out)


def main():
    maison = sys.argv[1]
    m = MAISONS[maison]
    gabarit = open(os.path.join(RACINE, "ile-maurice.html"), encoding="utf-8").read()

    tete = gabarit[: gabarit.index("<main>") + len("<main>\n")]
    queue = gabarit[gabarit.index('  <section class="reserver"'):]

    tete = tete.replace("<title>Île Maurice — La Cachette</title>", f"<title>{e(m['titre'])}</title>")
    tete = tete.replace(
        'content="La Cachette Île Maurice : sept chambres autour d\'un bassin, gazebo, jardin et plage de Belle Rivière."',
        f'content="{e(m["description"])}"')
    assert e(m["description"]) in tete

    queue = queue.replace('data-maison="Île Maurice"', f'data-maison="{e(m["valeur"])}"')
    queue = queue.replace('name="maison" value="Île Maurice"', f'name="maison" value="{e(m["valeur"])}"')
    queue = queue.replace('fiche__embleme f-maurice', f'fiche__embleme f-{maison}')
    queue = queue.replace('<h2>Île Maurice</h2>', f'<h2>{e(m["nom"])}</h2>')
    queue = queue.replace('<a href="ile-maurice.html" aria-current="page">Île Maurice</a>',
                          '<a href="ile-maurice.html">Île Maurice</a>')
    queue = queue.replace(f'<a href="{m["page"]}">{m["nom"]}</a>',
                          f'<a href="{m["page"]}" aria-current="page">{m["nom"]}</a>')
    assert f'f-{maison}' in queue and 'aria-current="page"' in queue

    page = tete + corps(maison, m) + queue
    with open(os.path.join(RACINE, m["page"]), "w", encoding="utf-8") as f:
        f.write(page)
    print(m["page"], "écrit —", sum(len(s[3]) for s in m["sections"]), "photos en galerie,",
          len(m["hero"]), "au héros")


if __name__ == "__main__":
    main()
