/* ------------------------------------------------------------------------
   Sommaire d'une page maison : une colonne fixe, à droite, au milieu de
   l'écran, qui apparaît une fois le héros passé et suit la lecture.

   Il se construit tout seul à partir des sections marquées :
     <section id="dehors" data-sommaire="Dehors">
   ------------------------------------------------------------------------ */
(function () {
  var sections = Array.prototype.slice.call(document.querySelectorAll('[data-sommaire]'));
  var hero = document.getElementById('hero');
  if (sections.length < 2 || !hero) return;

  var nav = document.createElement('nav');
  nav.className = 'sommaire';
  nav.setAttribute('aria-label', 'Sommaire de la page');
  var liste = document.createElement('ol');
  var liens = sections.map(function (s) {
    var li = document.createElement('li');
    var a = document.createElement('a');
    a.href = '#' + s.id;
    a.innerHTML = '<i aria-hidden="true"></i><span>' + s.dataset.sommaire + '</span>';
    li.appendChild(a);
    liste.appendChild(li);
    return a;
  });
  nav.appendChild(liste);
  document.body.appendChild(nav);
  document.body.classList.add('a-sommaire');

  var enAttente = false;
  function mettreAJour() {
    enAttente = false;
    /* visible seulement une fois le héros passé */
    nav.classList.toggle('est-visible', window.scrollY > hero.offsetTop + hero.offsetHeight - 120);

    /* la section active est celle qui contient le tiers haut de l'écran */
    var repere = window.scrollY + window.innerHeight * 0.34;
    var actif = 0;
    sections.forEach(function (s, i) { if (s.offsetTop <= repere) actif = i; });
    /* tout en bas de page, c'est forcément la dernière */
    if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 2) actif = sections.length - 1;
    liens.forEach(function (a, i) {
      if (i === actif) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
  }
  function planifier() {
    if (enAttente) return;
    enAttente = true;
    requestAnimationFrame(mettreAJour);
  }

  window.addEventListener('scroll', planifier, { passive: true });
  window.addEventListener('resize', planifier);
  window.addEventListener('load', planifier);
  mettreAJour();
})();
