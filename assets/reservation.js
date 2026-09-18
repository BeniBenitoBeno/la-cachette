/* ------------------------------------------------------------------------
   Demande de séjour — commun aux trois pages maison.

   Le formulaire porte la maison en attribut : <form id="demande"
   data-maison="Île Maurice">. Le calendrier, la fiche en direct, les
   contrôles et le récapitulatif sont les mêmes partout. La destination de
   la demande (ADRESSE / POINT_DE_COLLECTE) se règle dans assets/config.js.
   ------------------------------------------------------------------------ */
(function () {
  var form = document.getElementById('demande');
  if (!form) return;
  var MAISON = form.dataset.maison;        // « Île Maurice », « Grimaud — … »
  var ADRESSE = window.ADRESSE || '';
  var POINT_DE_COLLECTE = window.POINT_DE_COLLECTE || '';
  var boiteErreurs = document.getElementById('erreurs');
  var listeErreurs = document.getElementById('liste-erreurs');
  var arrivee = document.getElementById('arrivee');
  var depart = document.getElementById('depart');

  var aujourdhui = new Date();
  aujourdhui.setHours(0, 0, 0, 0);

  var longue = new Intl.DateTimeFormat('fr-FR',
    { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  var courte = new Intl.DateTimeFormat('fr-FR', { day: 'numeric', month: 'long' });

  function date(v) { return v ? new Date(v + 'T12:00:00') : null; }
  function accord(n, mot) { return n + ' ' + mot + (n > 1 ? 's' : ''); }

  /* ------------------------------------------------------------ compteurs */
  function compteurs() {
    document.querySelectorAll('.compteur button').forEach(function (b) {
      b.addEventListener('click', function () {
        var champ = document.getElementById(b.dataset.cible);
        var mini = b.dataset.cible === 'adultes' ? 1 : 0;
        var n = Math.min(20, Math.max(mini, parseInt(champ.value, 10) + parseInt(b.dataset.pas, 10)));
        champ.value = n;
        document.getElementById('out-' + b.dataset.cible).textContent = n;
        b.parentElement.querySelector('button').disabled = n <= mini;
        rafraichir();
      });
    });
    document.querySelectorAll('.compteur__reglage').forEach(function (r) {
      var champ = document.getElementById(r.querySelector('button').dataset.cible);
      var mini = champ.id === 'adultes' ? 1 : 0;
      r.querySelector('button').disabled = parseInt(champ.value, 10) <= mini;
    });
  }

  /* --------------------------------------------------- la fiche en direct */
  function voyageurs() {
    var a = parseInt(document.getElementById('adultes').value, 10);
    var e = parseInt(document.getElementById('enfants').value, 10);
    return accord(a, 'adulte') + (e ? ' · ' + accord(e, 'enfant') : '');
  }

  function nuits() {
    var d1 = date(arrivee.value), d2 = date(depart.value);
    if (!d1 || !d2) return 0;
    return Math.round((d2 - d1) / 86400000);
  }

  function rafraichir() {
    ['arrivee', 'depart'].forEach(function (cle) {
      var v = document.getElementById(cle).value;
      var cible = document.getElementById('fiche-' + cle);
      cible.textContent = v ? courte.format(date(v)) : 'à choisir';
      cible.classList.toggle('attente', !v);
    });

    document.getElementById('fiche-voyageurs').textContent = voyageurs();

    var n = nuits();
    document.getElementById('fiche-nuits').textContent = n > 0 ? accord(n, 'nuit') : '';
  }

  /* ------------------------------------------------------------ contrôles */
  function verifier() {
    var manques = [];
    if (!arrivee.value) manques.push('la date d’arrivée');
    if (!depart.value) manques.push('la date de départ');
    if (arrivee.value && depart.value && nuits() < 1) {
      manques.push('un départ postérieur à l’arrivée');
    }
    if (!document.getElementById('nom').value.trim()) manques.push('votre nom');
    var courriel = document.getElementById('courriel');
    if (!courriel.value.trim() || !/^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(courriel.value.trim())) {
      manques.push('un courriel valide');
    }
    return manques;
  }

  /* ------------------------------------------------------- le récapitulatif */
  function texte() {
    var d = new FormData(form);
    var n = nuits();
    var lignes = [
      'Maison      : ' + d.get('maison'),
      'Arrivée     : ' + longue.format(date(d.get('arrivee'))),
      'Départ      : ' + longue.format(date(d.get('depart'))),
      'Durée       : ' + accord(n, 'nuit'),
      'Voyageurs   : ' + voyageurs(),
      '',
      'Nom         : ' + d.get('nom'),
      'Courriel    : ' + d.get('courriel')
    ];
    if (d.get('telephone').trim()) lignes.push('Téléphone   : ' + d.get('telephone'));
    if (d.get('message').trim()) lignes.push('', d.get('message').trim());
    return lignes.join('\n');
  }

  function confirmer() {
    var corps = texte();
    var objet = 'Demande de séjour — ' + MAISON;

    var bloc = document.createElement('section');
    bloc.className = 'recap';
    bloc.innerHTML =
      '<p class="surtitre">Dernière étape</p>' +
      '<h2>Votre demande est prête</h2>' +
      '<p>Relisez-la, puis envoyez-la. Nous vous répondons à l’adresse que vous ' +
      'venez d’indiquer.</p>' +
      '<pre></pre>' +
      '<div class="recap__actions">' +
      '  <button class="envoyer" type="button" id="r-envoyer">Envoyer</button>' +
      '  <button class="bouton-fin" type="button" id="r-copier">Copier la demande</button>' +
      '  <button class="bouton-fin" type="button" id="r-modifier">Modifier</button>' +
      '</div>' +
      '<p class="recap__etat" id="r-etat"></p>';
    bloc.querySelector('pre').textContent = corps;

    var colonne = form.parentElement;
    var entete = form.closest('.reserver').querySelector('.demande__titre');
    entete.hidden = true;
    form.hidden = true;
    boiteErreurs.hidden = true;
    colonne.appendChild(bloc);
    bloc.scrollIntoView({ behavior: 'smooth', block: 'start' });

    var etat = document.getElementById('r-etat');

    document.getElementById('r-envoyer').addEventListener('click', function () {
      if (POINT_DE_COLLECTE) {
        fetch(POINT_DE_COLLECTE, { method: 'POST', body: new FormData(form) })
          .then(function (r) {
            etat.textContent = r.ok
              ? 'Demande envoyée. Merci — nous revenons vers vous rapidement.'
              : 'L’envoi a échoué. Copiez la demande et écrivez-nous directement.';
          })
          .catch(function () {
            etat.textContent = 'L’envoi a échoué. Copiez la demande et écrivez-nous directement.';
          });
      } else if (ADRESSE) {
        window.location.href = 'mailto:' + ADRESSE +
          '?subject=' + encodeURIComponent(objet) +
          '&body=' + encodeURIComponent(corps);
        etat.textContent = 'Votre message vous attend dans votre logiciel de courrier — ' +
          'il reste à l’envoyer.';
      } else {
        etat.textContent = 'Aucune adresse de destination n’est encore configurée sur ce ' +
          'site. Copiez la demande en attendant. (À renseigner en haut du script de ' +
          'cette page : ADRESSE ou POINT_DE_COLLECTE.)';
      }
    });

    document.getElementById('r-copier').addEventListener('click', function () {
      navigator.clipboard.writeText(objet + '\n\n' + corps).then(function () {
        etat.textContent = 'Demande copiée dans le presse-papiers.';
      }, function () {
        etat.textContent = 'La copie automatique a été refusée par le navigateur — ' +
          'sélectionnez le texte ci-dessus.';
      });
    });

    document.getElementById('r-modifier').addEventListener('click', function () {
      bloc.remove();
      form.hidden = false;
      entete.hidden = false;
      entete.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }

  /* ------------------------------------------------------------- calendrier
     Deux mois affichés, la semaine commence le lundi. Un clic pose l'arrivée,
     le suivant le départ ; un clic avant l'arrivée repart de zéro. Les deux
     champs cachés `arrivee` et `depart` restent la source de vérité pour la
     fiche, les contrôles et le récapitulatif. */

  var JOURS = ['lun', 'mar', 'mer', 'jeu', 'ven', 'sam', 'dim'];
  var moisTitre = new Intl.DateTimeFormat('fr-FR', { month: 'long', year: 'numeric' });
  var jourLong = new Intl.DateTimeFormat('fr-FR',
    { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });

  var cal = document.getElementById('calendrier');
  var calEffacer = document.getElementById('cal-effacer');
  var calEtat = document.getElementById('cal-etat');
  var calPrec = document.getElementById('cal-prec');

  var debut = null, fin = null, survol = null;
  var premierMois = new Date(aujourdhui.getFullYear(), aujourdhui.getMonth(), 1);
  var moisVu = new Date(premierMois);
  var focusJour = new Date(aujourdhui);

  function cle(d) {
    return d.getFullYear() + '-' +
      String(d.getMonth() + 1).padStart(2, '0') + '-' +
      String(d.getDate()).padStart(2, '0');
  }
  function memeJour(a, b) { return !!(a && b && cle(a) === cle(b)); }
  function plus(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  function duJour(v) { return new Date(v + 'T00:00:00'); }

  function construireMois(base, grilleHote, titre) {
    titre.textContent = moisTitre.format(base);
    grilleHote.innerHTML = '';
    var grille = document.createElement('div');
    grille.className = 'cal-grille';

    JOURS.forEach(function (j) {
      var b = document.createElement('b');
      b.textContent = j;
      b.setAttribute('aria-hidden', 'true');
      grille.appendChild(b);
    });

    var decalage = (base.getDay() + 6) % 7;          // lundi en tête
    for (var i = 0; i < decalage; i++) grille.appendChild(document.createElement('span'));

    var dernier = new Date(base.getFullYear(), base.getMonth() + 1, 0).getDate();
    for (var n = 1; n <= dernier; n++) {
      var d = new Date(base.getFullYear(), base.getMonth(), n);
      var casier = document.createElement('div');
      casier.className = 'cal-case';
      casier.dataset.jour = cle(d);
      var bt = document.createElement('button');
      bt.type = 'button';
      bt.textContent = n;
      bt.dataset.jour = cle(d);
      bt.setAttribute('aria-label', jourLong.format(d));
      bt.tabIndex = -1;
      if (d < aujourdhui) bt.disabled = true;
      casier.appendChild(bt);
      grille.appendChild(casier);
    }
    grilleHote.appendChild(grille);
  }

  function construire() {
    var suivant = new Date(moisVu.getFullYear(), moisVu.getMonth() + 1, 1);
    construireMois(moisVu, document.getElementById('cal-grille-1'),
      document.getElementById('cal-titre-1'));
    construireMois(suivant, document.getElementById('cal-grille-2'),
      document.getElementById('cal-titre-2'));
    calPrec.disabled = moisVu <= premierMois;
    peindre();
  }

  function peindre() {
    /* pendant le choix du départ, le survol donne un aperçu de la plage */
    var borne = fin || (debut && survol && survol > debut ? survol : null);
    var porteFocus = false;

    cal.querySelectorAll('.cal-case').forEach(function (c) {
      var d = duJour(c.dataset.jour);
      var estDebut = memeJour(d, debut);
      var estFin = memeJour(d, borne);
      var dedans = !!(debut && borne && d > debut && d < borne);

      c.classList.toggle('dans', dedans || (estDebut && !!borne) || (estFin && !!debut));
      c.classList.toggle('bord-gauche', estDebut && !!borne);
      c.classList.toggle('bord-droite', estFin && !!debut);
      c.classList.toggle('extremite', estDebut || estFin);
      c.classList.toggle('aujourdhui', memeJour(d, aujourdhui));

      var bt = c.querySelector('button');
      bt.setAttribute('aria-pressed', estDebut || estFin ? 'true' : 'false');
      var aLeFocus = memeJour(d, focusJour) && !bt.disabled;
      bt.tabIndex = aLeFocus ? 0 : -1;
      if (aLeFocus) porteFocus = true;
    });

    if (!porteFocus) {
      var premier = cal.querySelector('.cal-case button:not(:disabled)');
      if (premier) premier.tabIndex = 0;
    }

    calEffacer.hidden = !debut;
    if (!debut) {
      calEtat.textContent = 'Choisissez votre date d’arrivée.';
    } else if (!fin) {
      calEtat.textContent = 'Arrivée le ' + jourLong.format(debut) +
        '. Choisissez maintenant le départ.';
    } else {
      calEtat.textContent = 'Du ' + jourLong.format(debut) + ' au ' +
        jourLong.format(fin) + ' — ' + accord(nuits(), 'nuit') + '.';
    }
  }

  function synchroniser() {
    arrivee.value = debut ? cle(debut) : '';
    depart.value = fin ? cle(fin) : '';
    rafraichir();
  }

  function allerA(d) {
    if (d < aujourdhui) d = new Date(aujourdhui);
    focusJour = d;
    var mois = new Date(d.getFullYear(), d.getMonth(), 1);
    var second = new Date(moisVu.getFullYear(), moisVu.getMonth() + 1, 1);
    if (mois < moisVu) moisVu = mois;
    else if (mois > second) moisVu = new Date(d.getFullYear(), d.getMonth() - 1, 1);
    if (moisVu < premierMois) moisVu = new Date(premierMois);
    construire();
    var cible = cal.querySelector('button[data-jour="' + cle(d) + '"]');
    if (cible) cible.focus();
  }

  cal.addEventListener('click', function (e) {
    var bt = e.target.closest('button[data-jour]');
    if (!bt || bt.disabled) return;
    var d = duJour(bt.dataset.jour);
    if (!debut || fin || d <= debut) { debut = d; fin = null; }
    else { fin = d; }
    focusJour = d;
    survol = null;
    synchroniser();
    peindre();
  });

  cal.addEventListener('mouseover', function (e) {
    if (!debut || fin) return;
    var bt = e.target.closest('button[data-jour]');
    var nouveau = bt && !bt.disabled ? duJour(bt.dataset.jour) : null;
    if (memeJour(nouveau, survol) || (!nouveau && !survol)) return;
    survol = nouveau;
    peindre();
  });

  cal.addEventListener('mouseleave', function () {
    if (!survol) return;
    survol = null;
    peindre();
  });

  cal.addEventListener('keydown', function (e) {
    var bt = e.target.closest('button[data-jour]');
    if (!bt) return;
    var d = duJour(bt.dataset.jour);
    var pas = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7 };
    if (e.key in pas) { e.preventDefault(); allerA(plus(d, pas[e.key])); }
    else if (e.key === 'PageUp') {
      e.preventDefault(); allerA(new Date(d.getFullYear(), d.getMonth() - 1, d.getDate()));
    } else if (e.key === 'PageDown') {
      e.preventDefault(); allerA(new Date(d.getFullYear(), d.getMonth() + 1, d.getDate()));
    } else if (e.key === 'Home') {
      e.preventDefault(); allerA(plus(d, -((d.getDay() + 6) % 7)));
    } else if (e.key === 'End') {
      e.preventDefault(); allerA(plus(d, 6 - ((d.getDay() + 6) % 7)));
    }
  });

  function decaler(n) {
    moisVu = new Date(moisVu.getFullYear(), moisVu.getMonth() + n, 1);
    if (moisVu < premierMois) moisVu = new Date(premierMois);
    construire();
  }
  calPrec.addEventListener('click', function () { decaler(-1); });
  document.getElementById('cal-suiv').addEventListener('click', function () { decaler(1); });
  calEffacer.addEventListener('click', function () {
    debut = fin = survol = null;
    synchroniser();
    peindre();
  });

  /* ------------------------------------------------------------- branchement */
  form.addEventListener('change', rafraichir);
  form.addEventListener('input', rafraichir);

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var manques = verifier();
    if (manques.length) {
      listeErreurs.innerHTML = '';
      manques.forEach(function (m) {
        var li = document.createElement('li');
        li.textContent = m;
        listeErreurs.appendChild(li);
      });
      boiteErreurs.hidden = false;
      boiteErreurs.scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }
    boiteErreurs.hidden = true;
    confirmer();
  });

  compteurs();
  construire();
  rafraichir();
})();
