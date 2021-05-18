var confirmMessage = document.getElementById('confirmMessage');
var redirectLogin = document.getElementById('redirectLogin');

var valider = document.getElementById('valider');
valider.addEventListener("click", ajout_role);

function ajout_role() {
    var nom_role = document.getElementById('nom_role');
    var afficher_stats = document.querySelector('input[name="afficher_stats"]:checked')
    var ajouter_dossier = document.querySelector('input[name="ajouter_dossier"]:checked')
    var afficher_dossier = document.querySelector('input[name="afficher_dossier"]:checked')
    var editer_dossier = document.querySelector('input[name="editer_dossier"]:checked')
    var supprimer_dossier = document.querySelector('input[name="supprimer_dossier"]:checked')

    $.ajax({
        type: "GET",
        headers: {"Access-Control-Allow-Origin": "*"},
        url: `/api/roles/new/`
                + `?nom_role=${encodeURI(nom_role.value)}`
                + `&afficher_stats=${encodeURI(afficher_stats.value)}`
                + `&ajouter_dossier=${encodeURI(ajouter_dossier.value)}`
                + `&afficher_dossier=${encodeURI(afficher_dossier.value)}`
                + `&editer_dossier=${encodeURI(editer_dossier.value)}`
                + `&supprimer_dossier=${encodeURI(supprimer_dossier.value)}`

    }).done(function (data) {
        if (data['success'] == true) {
            confirmMessage.innerHTML = data['message'];
            confirmMessage.classList.replace('hidden', 'block')
            redirectLogin.classList.replace('hidden', 'block')
        } else {
            confirmMessage.innerHTML = data['error'];
            confirmMessage.classList.replace('bg-green-600', 'bg-red-700')
            confirmMessage.classList.replace('hidden', 'block')
        }
    });

}
