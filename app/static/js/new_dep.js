var confirmMessage = document.getElementById('confirmMessage');
var redirectLogin = document.getElementById('redirectLogin');

var valider = document.getElementById('valider');
valider.addEventListener("click", ajout_dep);

function ajout_dep() {
    var nom_departement = document.getElementById('nom_departement');

    $.ajax({
        type: "GET",
        headers: {"Access-Control-Allow-Origin": "*"},
        url: `/api/departements/new/`
                + `?nom_departement=${encodeURI(nom_departement.value)}`

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
