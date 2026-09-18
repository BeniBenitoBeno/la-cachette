# La Cachette — le site

Sept pages statiques, une feuille de style commune. Aucune dépendance, aucun
build, aucun framework.

```
index.html          les trois maisons, en trois colonnes
index-bandes.html   la même page en bandes horizontales (ancienne version, gardée)
grimaud.html        01 — Golfe de Saint-Tropez   (complète, 41 photos)
ile-maurice.html    02 — Océan Indien            (complète)
vars.html           03 — Hautes-Alpes            (complète, 37 photos)
esprit.html         ce qui relie les trois maisons
sejours.html        le déroulé d'un séjour, le tableau comparatif
contact.html        nous écrire (les demandes de séjour sont sur les pages maison)
assets/style.css    toute la mise en forme
assets/logos/       les trois signatures, en SVG, EPS et bitmap
assets/img/         les photos
tools/              les scripts qui ont produit les logos et les photos
```

## Lancer

```bash
python -m http.server 5177 --directory la-cachette
```

puis http://localhost:5177. Un double-clic sur `index.html` marche aussi, mais
le serveur local évite les surprises de cache sur les images.

---

## Les trois bandes de la page d'accueil

- **Repos** : les trois bandes en noir et blanc, assombries.
- **Survol** : la bande passe en couleur, l'image zoome de 7 %, le nom remonte
  et « Découvrir la maison » apparaît. Les deux autres s'assombrissent encore.
- **Sortie / passage à une autre** : retour au noir et blanc en 900 ms.
- **Clic** : la page de la maison.
- **Clavier** : `Tab` déclenche le même effet (`:focus-visible`).
- **Tactile** : pas de survol — la bande la plus proche du centre de l'écran
  s'active au défilement.
- **`prefers-reduced-motion`** : zoom et transitions désactivés.

Le noir et blanc est réservé à cette page. À l'intérieur d'une maison, les
photos sont en couleur : le clic a déjà été récompensé.

## Une page de maison

Ouverture pleine hauteur, deux paragraphes, un bloc « en bref », puis les
galeries par thème et le plan. Chaque photo s'ouvre dans une visionneuse
(flèches ← → et Échap au clavier, clic hors de l'image pour fermer).

## L'esprit, Séjours

**L'esprit** ouvre en clair, sans photo — c'est le contrepoint des pages maison :
le sens du nom, le fil qui relie les trois emblèmes, et pourquoi une gravure
plutôt qu'un logotype. Le dernier bloc, « Comment tout a commencé », est laissé
vide : ce paragraphe ne peut venir que des propriétaires.

**Séjours** explique le déroulé en trois temps (demander, échanger, venir) et
pose un tableau comparatif des trois maisons. Seule la colonne Île Maurice est
remplie — et uniquement avec ce qui se lit sur le plan. Les conditions
(saisons, tarifs, ce qui est compris, acompte, annulation) sont un bloc « à
renseigner » : aucun chiffre n'a été inventé.

## Grimaud et Vars : pages générées

`tools/generer_page_maison.py grimaud` (ou `vars`) écrit la page entière à partir
du descriptif en tête du script — textes, « en bref », photos du héros,
sections et légendes — en reprenant en-tête, formulaire, pied et visionneuse
de la page Île Maurice. Pour changer une légende ou déplacer une photo, on
modifie le descriptif et on relance ; on ne retouche pas le HTML à la main.
Les textes d'intro ne disent que ce que les photos montrent.

## Le héros d'une page maison

Les photos défilent d'elles-mêmes (fondu toutes les 6,5 s, lent zoom pendant
l'affichage) et se font défiler à la main : flèches, points, flèches du
clavier, glissement au doigt. Tout est dans `assets/hero.js` ; la liste des
photos est le simple bloc `<div class="hero__diapos">` en haut de la page —
ajouter ou retirer un `<img>` suffit. Une seule photo : pas de commandes. Aucune
photo qui charge : l'emblème gravé prend la place.

**Sur la qualité** : les originaux Île Maurice font 1 100 à 1 600 px de large.
Un héros pleine largeur les agrandit ; on a donc retenu les cadrages paysage
les plus grands. Le héros occupe tout l'écran sous le bandeau ; sur un très
grand écran, les photos sont donc agrandies d'un facteur 1,3 à 1,8.
Pour un rendu net sur grand écran, il faudrait les fichiers d'origine du
photographe en 2 400 px ou plus.

## Les dates prises sur les plateformes (iCal)

Chaque annonce Airbnb / Booking / Abritel exporte un lien `.ics`. On les
colle dans `calendriers.json` :

```json
"maurice": [
  {"source": "airbnb",  "url": "https://www.airbnb.fr/calendar/ical/….ics"},
  {"source": "booking", "url": "https://ical.booking.com/v1/export?t=…"}
]
```

Où les trouver : Airbnb → *Calendrier → Disponibilités → Synchronisation des
calendriers → Exporter* ; Booking → *Extranet → Tarifs et disponibilités →
Synchroniser les calendriers → Exporter* ; Abritel/Vrbo → *Calendrier →
Importer/Exporter*.

`tools/synchroniser_calendriers.py` lit ces flux (aucune dépendance), fusionne
les périodes prises et écrit `disponibilites/<maison>.json`. GitHub Actions le
lance **toutes les 30 minutes** (`.github/workflows/calendriers.yml`) et ne
commit que si les dates ont changé ; on peut aussi le lancer à la main depuis
l'onglet *Actions* (« Run workflow »), ou en local.

Le calendrier de chaque page maison lit ce fichier : les nuits prises sont
hachurées et barrées, on ne peut ni arriver dessus ni les enjamber. Le jour
du départ d'un autre client reste libre pour une arrivée, comme partout.

Limites de l'iCal : délai (les plateformes publient leurs `.ics` avec un
peu de retard, et nous relisons toutes les 30 min), et dates seulement — pas
de nom de client ni de prix. Les liens `.ics` sont secrets : qui les a voit
les dates prises. Ils sont dans un dépôt public, c'est le compromis assumé ;
si ça gêne, les passer en *secrets* GitHub Actions.

**Sens inverse** (bloquer Airbnb depuis une résa directe) : il faudrait que le
site produise son propre `.ics`, donc une base des résas directes — ça
n'existe pas tant que le formulaire part par courriel.

## Le sommaire d'une page maison

Une colonne fixe à droite, au milieu de l'écran, qui apparaît une fois le héros
passé et suit la lecture (`assets/sommaire.js`). Elle se construit à partir des
sections marquées `data-sommaire="Dehors"` — pour ajouter une entrée, il suffit
de marquer la section. Sous 1 100 px de large, elle disparaît ; au-dessus, les
sections lui réservent 230 px à droite pour qu'elle ne couvre rien.

## La demande de séjour (pages maison)

En bas de chaque page maison, section `#reserver` — le bouton « Demander un
séjour » du héros y mène. Le formulaire est en une colonne, avec une fiche qui
se remplit en direct à côté : l'emblème de la maison, les dates en toutes
lettres, le nombre de nuits, les voyageurs. La maison n'est plus à choisir :
elle est portée par la page (`<form data-maison="…">`), et le calendrier, la
fiche, les contrôles et le récapitulatif sont dans `assets/reservation.js`,
commun aux trois pages. En dessous de 900 px, la fiche passe au-dessus du
formulaire pour rester sous les yeux pendant la saisie.

**Les dates se prennent au calendrier**, pas dans deux champs `jj/mm/aaaa` :
deux mois côte à côte (un seul en dessous de 720 px), la semaine qui commence
le lundi, un clic pour l'arrivée, un second pour le départ, et la plage qui se
remplit entre les deux. Le survol montre la plage avant de la valider, un clic
avant l'arrivée repart de zéro, et « Effacer les dates » remet tout à plat. Le
passé est désactivé, donc un départ ne peut jamais précéder une arrivée.

Au clavier : `Tab` entre dans la grille, les flèches déplacent d'un jour ou
d'une semaine, `Origine`/`Fin` vont aux bords de la semaine, `Page préc.` et
`Page suiv.` changent de mois, `Entrée` choisit. Le calendrier fait défiler les
mois tout seul quand on sort de ceux qui sont affichés.

Deux champs cachés `arrivee` et `depart` restent la source de vérité — la fiche,
les contrôles et le récapitulatif n'ont pas eu à changer.

Les compteurs adultes / enfants fonctionnent au clavier comme à la
souris. Rien n'est obligatoire au sens du navigateur : à l'envoi, un seul
encadré liste ce qui manque encore, en français, sans faire clignoter les
champs un par un.

À la validation, le formulaire cède la place à un récapitulatif en clair — la
demande telle qu'elle partira — avec **Envoyer**, **Copier la demande** et
**Modifier**.

## La page contact

Réduite à l'essentiel : nom, courriel, téléphone facultatif, message. Un encart
à côté renvoie vers le calendrier de chaque maison pour les demandes de séjour.
Même récapitulatif avant envoi, même destination.

### Brancher l'envoi

Rien n'est envoyé pour l'instant, faute de destination. Deux constantes dans
`assets/config.js`, communes aux demandes de séjour et à la page contact :

```js
window.ADRESSE = '';            // ex. 'bonjour@…' -> ouvre le logiciel de courrier, prérempli
window.POINT_DE_COLLECTE = '';  // ex. une URL Formspree/Basin -> la demande est postée
```

- **`ADRESSE`** seule : zéro service tiers, mais le visiteur doit avoir un
  logiciel de courrier configuré et cliquer une seconde fois pour envoyer.
- **`POINT_DE_COLLECTE`** : envoi direct, avec accusé à l'écran. C'est
  l'option à retenir pour un vrai site.
- **Aucune des deux** (état actuel) : le récapitulatif s'affiche et explique
  que la destination n'est pas configurée ; le bouton « Copier la demande »
  reste utilisable.

Une demande n'est pas une réservation : la fiche le dit explicitement, et rien
dans la page ne promet de délai de réponse. À ajuster quand vous saurez lequel
vous tenez.

---

## Ajouter les photos manquantes

### L'image d'ouverture d'une bande et d'un héros

| Bande | Fichier attendu            | État        |
|-------|----------------------------|-------------|
| 01    | `assets/img/grimaud.jpg`   | à fournir   |
| 02    | `assets/img/maurice.jpg`   | en place    |
| 03    | `assets/img/vars.jpg`      | à fournir   |

Tant que le fichier est absent, la bande **et** le héros de la page basculent
sur l'emblème gravé de la maison, avec la mention « Photos à venir ». Il suffit
de déposer le fichier au bon nom : tout s'allume, rien d'autre à modifier.

**Format conseillé** : paysage, 2400 × 1200 px minimum, JPG qualité 80, sujet
placé à droite du cadre — la moitié gauche porte le nom de la maison.

Le cadrage vertical se règle dans `assets/style.css` :

```css
#m-grimaud img{object-position:center 50%}
#m-maurice img{object-position:center 42%}
#m-vars    img{object-position:center 45%}
```

### Les galeries

```bash
python tools/preparer_photos.py "<dossier des photos>" grimaud
```

Le script convertit tout en JPEG progressif, produit deux tailles (2200 px pour
la visionneuse, 700 px pour la grille) et écrit un `manifeste.txt` où chaque
ligne donne le nom de fichier, la légende et les dimensions d'origine. **Les
légendes viennent des noms de fichiers du photographe** — c'est la seule
information fiable dont on dispose sur les pièces, donc mieux vaut des noms
soignés à la source.

Il reste ensuite à recopier dans `grimaud.html` le gabarit `<figure>` de
`ile-maurice.html`, section par section.

Pour l'Île Maurice, 61 photos ont été traitées (19 Mo au total). **Il n'y a
aucune photo de la chambre 3** — elle apparaît sur le plan mais pas dans le
dossier.

---

## Les logos

`assets/logos/` contient les trois signatures :

| Lieu                  | Vectoriel                            | Réserve blanche                            | Imprimeur | Bitmap |
|-----------------------|--------------------------------------|--------------------------------------------|-----------|--------|
| Golfe de Saint-Tropez | `la-cachette-golfe-saint-tropez.svg` | `la-cachette-golfe-saint-tropez-blanc.svg` | `.eps`    | `.jpg` |
| Île Maurice           | `la-cachette-ile-maurice.svg`        | `la-cachette-ile-maurice-blanc.svg`        | `.eps`    | `.jpg` |
| Vars                  | `la-cachette-vars.svg`               | `la-cachette-vars-blanc.svg`               | `.eps`    | `.png` |

Les `.svg` sont en `fill="currentColor"` : posés en SVG *en ligne*, ils prennent
la couleur du texte environnant. Les `-blanc.svg` sont blancs en dur, pour un
`<img>` ou un `background-image` sur fond sombre — c'est ce qu'utilisent les
bandes et les héros sans photo.

Les `.eps` sont en noir plein, sans vignette de prévisualisation intégrée
(normal, et sans conséquence : Illustrator, InDesign et les RIP les ouvrent).
Leur boîte est en points, à l'échelle du SVG.

Poids : Maurice 124 Ko, Vars 161 Ko, Grimaud 585 Ko en SVG. Le tracé de Grimaud
est lourd parce que la gravure d'origine est très fournie ; pour un usage web
léger (favicon, en-tête), préférer le bitmap.

### Régénérer

```bash
python tools/vectoriser_logos.py   # les deux gravures d'origine -> SVG
python tools/logo_vars.py          # dessine et vectorise le logo Vars
python tools/exporter_eps.py       # les trois SVG -> EPS
```

`tools/svgkit.py` porte la chaîne commune (seuil d'encre 135, tracé spline) :
les trois logos ont donc exactement la même texture de trait. Tous les réglages
du dessin de Vars — sommets des crêtes, mélèzes, densité de l'eau, position du
soleil dans le col — sont en haut de `tools/logo_vars.py`.

`logos-planche.png` est une planche de contact des trois, pour comparaison.

---

## Ce qui reste à brancher

- **La destination du formulaire** — voir « Brancher l'envoi » plus haut.
- Les entrées de menu **L'esprit** et **Séjours** pointent encore sur `#`.
- Les blocs « À renseigner » de Grimaud et Vars attendent le nombre de chambres,
  les pièces, les extérieurs et la saison d'ouverture.
