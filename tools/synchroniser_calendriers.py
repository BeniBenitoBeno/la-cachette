"""Lit les calendriers iCal des plateformes et en tire les dates prises.

Configuration dans `calendriers.json`, à la racine :

    {
      "maurice": [
        {"source": "airbnb",  "url": "https://www.airbnb.fr/calendar/ical/….ics"},
        {"source": "booking", "url": "https://ical.booking.com/v1/export?t=…"}
      ],
      "grimaud": [],
      "vars": []
    }

Produit `disponibilites/<maison>.json` :

    {"maj": "2026-09-18T14:02:00Z",
     "pris": [{"de": "2026-10-03", "a": "2026-10-10", "source": "airbnb"}, …]}

`de` = première nuit prise, `a` = jour du départ (libre pour une arrivée),
comme DTSTART / DTEND en iCal. Le calendrier du site lit ce fichier.

Aucune dépendance : urllib + un parseur iCal minimal (DTSTART/DTEND, dates
ou date-heure, lignes repliées). Lancer à la main :

    python tools/synchroniser_calendriers.py

ou laisser GitHub Actions le faire (.github/workflows/calendriers.yml).
"""
import datetime as dt
import json
import os
import re
import sys
import urllib.request

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(RACINE, "calendriers.json")
SORTIE = os.path.join(RACINE, "disponibilites")


def deplier(texte):
    """iCal replie les longues lignes : une ligne qui commence par un espace
    ou une tabulation continue la précédente."""
    return re.sub(r"\r?\n[ \t]", "", texte)


def lire_date(valeur):
    """DTSTART;VALUE=DATE:20261003  ->  2026-10-03
       DTSTART:20261003T140000Z    ->  2026-10-03 (on ignore l'heure)"""
    v = valeur.strip()[:8]
    return dt.date(int(v[:4]), int(v[4:6]), int(v[6:8]))


def evenements(ics):
    """Rend (debut, fin) pour chaque VEVENT ; fin exclusive.
    Un événement sans DTEND dure une journée."""
    for bloc in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", deplier(ics), re.S):
        debut = fin = None
        for ligne in bloc.splitlines():
            if ligne.startswith("DTSTART"):
                debut = lire_date(ligne.split(":", 1)[1])
            elif ligne.startswith("DTEND"):
                fin = lire_date(ligne.split(":", 1)[1])
        if debut is None:
            continue
        if fin is None or fin <= debut:
            fin = debut + dt.timedelta(days=1)
        yield debut, fin


def fusionner(plages):
    """Fusionne les plages qui se touchent ou se chevauchent, toutes sources
    confondues ; garde la source de la première."""
    plages = sorted(plages, key=lambda p: p[0])
    fusion = []
    for debut, fin, source in plages:
        if fusion and debut <= fusion[-1][1]:
            fusion[-1][1] = max(fusion[-1][1], fin)
        else:
            fusion.append([debut, fin, source])
    return fusion


def telecharger(url):
    req = urllib.request.Request(url, headers={"User-Agent": "la-cachette-calendrier/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def main():
    if not os.path.exists(CONFIG):
        print("pas de calendriers.json — rien à faire")
        return 0
    config = json.load(open(CONFIG, encoding="utf-8"))
    os.makedirs(SORTIE, exist_ok=True)
    aujourdhui = dt.date.today()
    horizon = aujourdhui - dt.timedelta(days=30)   # on garde un mois de passé
    erreurs = 0

    for maison, flux in config.items():
        plages = []
        for f in flux:
            if not f.get("url"):
                continue
            try:
                ics = telecharger(f["url"])
            except Exception as e:                       # un flux en panne ne bloque pas les autres
                print(f"  {maison}/{f.get('source', '?')} : échec ({e})")
                erreurs += 1
                continue
            n = 0
            for debut, fin in evenements(ics):
                if fin < horizon:
                    continue
                plages.append((debut, fin, f.get("source", "")))
                n += 1
            print(f"  {maison}/{f.get('source', '?')} : {n} période(s)")

        chemin = os.path.join(SORTIE, maison + ".json")
        contenu = {
            "maj": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "pris": [{"de": d.isoformat(), "a": f.isoformat(), "source": s}
                     for d, f, s in fusionner(plages)],
        }
        # on ne réécrit (et donc ne commit) que si les dates ont changé
        ancien = None
        if os.path.exists(chemin):
            try:
                ancien = json.load(open(chemin, encoding="utf-8")).get("pris")
            except Exception:
                pass
        if ancien == contenu["pris"]:
            print(f"  {maison} : inchangé")
            continue
        with open(chemin, "w", encoding="utf-8") as out:
            json.dump(contenu, out, ensure_ascii=False, indent=1)
        print(f"  {maison} : {len(contenu['pris'])} période(s) écrites")

    return 1 if erreurs and erreurs == sum(len(v) for v in config.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
