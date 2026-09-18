# La Cachette — repères de marque (v0)

Base de travail déduite des logos et appliquée telle quelle à la page
« Nos maisons ». À valider / corriger avant d'aller plus loin.

Aperçu des trois signatures : `logos-planche.png`.

---

## 1. Architecture de marque

Une marque mère, trois lieux. Le nom ne change pas, le lieu se pose en second.

```
La Cachette
├── La Cachette — Golfe de Saint-Tropez   (Grimaud, Var)
├── La Cachette — Île Maurice
└── La Cachette — Vars                    (Hautes-Alpes)
```

Sur le site, on écrit toujours le lieu seul en titre (**Grimaud**, **Île Maurice**,
**Vars**) et la précision géographique en sous-titre. « La Cachette » reste dans
l'en-tête : la marque n'a pas à être répétée trois fois dans la même page.

**À trancher** : le logo Maurice signe « Ile Maurice » sans accent, le logo Var
signe « Golfe de Saint Tropez » sans trait d'union. Sur le site j'ai typographié
en français correct — *Île Maurice*, *Golfe de Saint-Tropez*. Soit on aligne les
logos sur le site, soit l'inverse, mais il faut choisir.

---

## 2. Logos

Trois signatures, une seule grammaire : **gravure au trait noir, bassin
rectangulaire en perspective avec son reflet, un arbre du lieu de chaque côté,
un soleil bas sur l'horizon, trois oiseaux**, puis le nom.

| Lieu                  | Arbres                        | Fond            |
|-----------------------|-------------------------------|-----------------|
| Golfe de Saint-Tropez | pin parasol, pin d'Alep       | mer             |
| Île Maurice           | baobab, palmiers, pavillon    | lagon           |
| Vars                  | mélèzes                       | crête alpine    |

### Fichiers

Chaque logo existe en trois formes dans `assets/logos/` :

| Fichier                       | Usage                                                |
|-------------------------------|------------------------------------------------------|
| `<nom>.svg`                   | `fill="currentColor"` — SVG en ligne, prend la couleur du texte |
| `<nom>-blanc.svg`             | blanc en dur — pour `<img>` sur fond sombre           |
| `<nom>.eps`                   | noir plein, pour l'imprimeur — boîte en points, sans vignette |
| `<nom>.jpg` / `.png`          | bitmap d'origine, ou son équivalent pour Vars         |

Les SVG sont des vectorisations des gravures d'origine (chaîne commune :
`tools/svgkit.py`, seuil d'encre 135, tracé spline). Ils tiennent
l'agrandissement, la réserve blanche et l'impression.

**Vars** n'existait pas : il a été dessiné pour compléter la famille
(`tools/logo_vars.py`, dessin paramétrique passé dans la même chaîne de
vectorisation, donc même texture de trait). Le lettrage « La Cachette » y est
repris tel quel du logo Golfe de Saint-Tropez — les trois noms sont donc
rigoureusement identiques. Le mot « Vars » est composé en Garamond, comme le
sous-titre de Grimaud.

### Usage

- fond ivoire, blanc ou photo très sombre — jamais sur une photo claire ;
- zone de protection = hauteur du mot « La Cachette » sur les quatre côtés ;
- taille minimale à l'écran : **180 px de large** pour les deux logos paysage
  (Grimaud, Vars), 120 px pour le logo carré (Maurice) — en dessous, la gravure
  se referme ;
- monochrome uniquement, pas d'ombre, pas de dégradé, pas de rotation.

---

## 3. Couleurs

| Rôle              | Hex       | Usage                                        |
|-------------------|-----------|----------------------------------------------|
| Encre             | `#111110` | texte, filets, logos                         |
| Ivoire            | `#f4f2ed` | fond des pages claires, en-tête              |
| Nuit              | `#090908` | voile posé sur les photos                    |
| Or pâle *(prop.)* | `#b9a37e` | accent rare : focus clavier, filet actif     |

Trois couleurs suffisent. L'or n'est qu'une proposition — la marque tient très
bien en noir et ivoire seuls, et la couleur, dans ce système, vient uniquement
des photographies.

---

## 4. Typographie

| Rôle           | Police                    | Réglage                                   |
|----------------|---------------------------|-------------------------------------------|
| Titres, nom    | Cormorant Garamond Light  | interlignage 0.98, approche +0.02em        |
| Courant, menus | Jost Light / Regular      | capitales, approche +0.22em à +0.34em      |

Cormorant est un substitut libre proche du serif des logos. Si la marque acquiert
une licence, viser plutôt un Garamond premium (Adobe Garamond Pro, Sabon) pour
les titres.

Règles : jamais de gras, jamais d'italique hors citation, les surtitres et
libellés toujours en capitales espacées, le nom des maisons toujours en bas de
casse serif.

---

## 5. Photographie

C'est le seul apport de couleur, donc la règle est stricte.

- **Sur la page d'accueil, tout est en noir et blanc.** La couleur est une
  récompense, pas un état par défaut : elle n'apparaît qu'au survol de la bande.
- **À l'intérieur d'une maison, tout est en couleur.** Le clic a déjà été
  récompensé ; du noir et blanc à ce stade serait une coquetterie.
- Lumière naturelle, pas de HDR, pas de ciel sursaturé.
- Cadrages larges, sujet à droite, moitié gauche laissée respirante pour le texte.
- Pas de personnes identifiables, pas de nourriture en gros plan, pas de
  panneaux ni de logos tiers dans le champ.
- Traitement noir et blanc : `grayscale(1) contrast(1.02)`, aucun virage sépia.

---

## 6. Mouvement

| Paramètre     | Valeur                        |
|---------------|-------------------------------|
| Durée         | 900 ms                        |
| Courbe        | `cubic-bezier(.22,.61,.36,1)` |
| Zoom au survol| `scale(1.07)`                 |
| Décalage texte| 6 px vers le haut             |

Une seule chose bouge à la fois. Rien ne rebondit, rien ne clignote, rien ne
démarre tout seul. `prefers-reduced-motion` coupe le zoom.

---

## 7. Ton

Court, concret, jamais commercial. « Découvrir la maison », pas « Réservez dès
maintenant ». On nomme des lieux et des matières, on ne promet pas d'émotions.

Dans les formulaires : on ne demande que ce qui sert à répondre, on dit ce qui
est facultatif, et on ne promet rien qu'on ne tienne — « une demande n'est pas
une réservation » plutôt qu'une réponse garantie sous 24 h.

---

## À faire

### Tranché

- **Logo Vars** : validé. Les réglages restent ouverts dans `tools/logo_vars.py`.
- **Orthographe des signatures** : les logos gardent « Ile Maurice » et « Golfe
  de Saint Tropez » tels quels ; le site écrit « Île Maurice » et « Golfe de
  Saint-Tropez ». L'écart est assumé.
- **Sous-titre** : Maurice reste en italique, Grimaud et Vars en romain.
  L'irrégularité ne gêne pas, on n'y touche pas.
- **EPS** : produits pour les trois logos.

### Ouvert

1. **Photos Vars en 1 024 px seulement** — trop petites pour un héros plein
   écran sur grand moniteur ; demander les originaux.
2. **Or pâle** : entre-t-il dans la palette, oui ou non ? Il ne sert
   aujourd'hui qu'au contour de focus clavier.
3. **Envoi des demandes** — les formulaires (séjour sur chaque page maison,
   message sur la page contact) ne partent nulle part tant qu'une adresse ou un
   point de collecte n'est pas renseigné dans `assets/config.js`.
