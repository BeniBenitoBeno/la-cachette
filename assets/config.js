/* Où partent les demandes — commun à toutes les pages.

   ADRESSE vide            -> le récapitulatif s'affiche avec un bouton « copier ».
   ADRESSE remplie         -> le bouton ouvre le logiciel de courrier, prérempli.
   POINT_DE_COLLECTE remplie (Formspree, Basin, un script maison…) -> la demande
   est postée directement et le courrier n'est plus nécessaire. */
window.ADRESSE = '';
window.POINT_DE_COLLECTE = '';
