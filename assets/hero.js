/* ------------------------------------------------------------------------
   Héros d'une page maison : les photos défilent d'elles-mêmes, et on peut
   les faire défiler à la main (flèches, points, clavier, glissement).

   Structure attendue :
     <section class="hero" id="hero">
       <div class="hero__diapos"><img …><img …></div>
       …
   Une seule photo -> pas de commandes, pas de défilement.
   Aucune photo qui charge -> le héros porte l'emblème gravé (.vide).
   ------------------------------------------------------------------------ */
(function () {
  var hero = document.getElementById('hero');
  if (!hero) return;
  var piste = hero.querySelector('.hero__diapos');
  var diapos = Array.prototype.slice.call(piste.querySelectorAll('img'));
  var DUREE = 6500;
  var reduit = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var courant = 0, minuterie = null, points = [], commandes = null;

  function vide() {
    hero.classList.add('vide');
    var lieu = document.getElementById('hero-lieu');
    if (lieu) lieu.textContent = 'Photos à venir';
    if (commandes) commandes.remove();
  }

  /* une photo qui ne charge pas sort du défilement ; plus aucune -> emblème */
  diapos.forEach(function (img) {
    function rater() {
      var i = diapos.indexOf(img);
      if (i < 0) return;
      diapos.splice(i, 1);
      img.remove();
      if (points[i]) { points[i].remove(); points.splice(i, 1); }
      if (!diapos.length) { vide(); return; }
      if (courant >= diapos.length) courant = 0;
      if (diapos.length < 2 && commandes) commandes.remove();
      montrer(courant, true);
    }
    img.addEventListener('error', rater);
    if (img.complete && img.naturalWidth === 0) rater();
  });

  function montrer(i, immediat) {
    courant = (i + diapos.length) % diapos.length;
    diapos.forEach(function (img, k) {
      var actif = k === courant;
      img.classList.toggle('est-visible', actif);
      if (actif && !reduit && !immediat) {
        /* relance le lent zoom à chaque passage */
        img.classList.remove('anime');
        void img.offsetWidth;
        img.classList.add('anime');
      }
    });
    points.forEach(function (p, k) {
      p.setAttribute('aria-current', k === courant ? 'true' : 'false');
    });
  }

  function suivant() { montrer(courant + 1); }
  function precedent() { montrer(courant - 1); }

  function lancer() {
    arreter();
    if (diapos.length < 2 || reduit) return;
    minuterie = setInterval(suivant, DUREE);
  }
  function arreter() { if (minuterie) { clearInterval(minuterie); minuterie = null; } }
  function relancer() { lancer(); }

  /* ------------------------------------------------------------ commandes */
  if (diapos.length > 1) {
    commandes = document.createElement('div');
    commandes.className = 'hero__commandes';

    var prec = document.createElement('button');
    prec.type = 'button'; prec.className = 'hero__fleche hero__fleche--prec';
    prec.setAttribute('aria-label', 'Photo précédente'); prec.innerHTML = '&lsaquo;';

    var suiv = document.createElement('button');
    suiv.type = 'button'; suiv.className = 'hero__fleche hero__fleche--suiv';
    suiv.setAttribute('aria-label', 'Photo suivante'); suiv.innerHTML = '&rsaquo;';

    var nav = document.createElement('div');
    nav.className = 'hero__points';
    nav.setAttribute('role', 'tablist');
    nav.setAttribute('aria-label', 'Photos de la maison');
    diapos.forEach(function (img, k) {
      var p = document.createElement('button');
      p.type = 'button';
      p.setAttribute('role', 'tab');
      p.setAttribute('aria-label', img.alt || ('Photo ' + (k + 1)));
      p.addEventListener('click', function () { montrer(k); relancer(); });
      nav.appendChild(p);
      points.push(p);
    });

    prec.addEventListener('click', function () { precedent(); relancer(); });
    suiv.addEventListener('click', function () { suivant(); relancer(); });

    commandes.appendChild(prec);
    commandes.appendChild(nav);
    commandes.appendChild(suiv);
    hero.appendChild(commandes);

    /* clavier, quand le héros ou l'une de ses commandes a le focus */
    hero.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); precedent(); relancer(); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); suivant(); relancer(); }
    });

    /* glissement au doigt */
    var x0 = null;
    hero.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      x0 = null;
      if (Math.abs(dx) < 40) return;
      if (dx < 0) suivant(); else precedent();
      relancer();
    });

    /* on ne défile pas dans un onglet caché */
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) arreter(); else lancer();
    });
  }

  if (diapos.length) {
    montrer(0, true);
    if (!reduit) diapos[0].classList.add('anime');
    lancer();
  } else {
    vide();
  }
})();
