var nom = document.getElementById('nom');
var prenom = document.getElementById('prenom');
var date_naissance = document.getElementById('date_naissance');
var numero_ss = document.getElementById('numero_ss');
var numero_telephone = document.getElementById('numero_telephone');
var adresse_email = document.getElementById('adresse_email');
var departement = document.getElementById('departement');
var role = document.getElementById('role');

var confirmMessage = document.getElementById('confirmMessage');
var valider = document.getElementById('valider');
valider.addEventListener("click", register);

function get_sexe_personne() {
    var masculin = document.getElementById('masculin').checked;
    var feminin = document.getElementById('feminin').checked;

    if (masculin == true) {
        return "masculin"
    } else if (feminin == true) {
        return "feminin"
    } else {
        return null
    }
}

function register() {
    $.ajax({
        type: "GET",
        headers: {"Access-Control-Allow-Origin": "*"},
        url: `/api/auth/register/`
                + `?sexe=${encodeURI(get_sexe_personne())}`
                + `&nom=${encodeURI(nom.value)}`
                + `&prenom=${encodeURI(prenom.value)}`
                + `&date_naissance=${encodeURI(date_naissance.value)}`
                + `&numero_ss=${encodeURI(numero_ss.value)}`
                + `&numero_telephone=${encodeURI(numero_telephone.value)}`
                + `&adresse_email=${encodeURI(adresse_email.value)}`
                + `&departement=${encodeURI(departement.value)}`
                + `&role=${encodeURI(role.value)}`

    }).done(function (data) {
        if (data['success'] == true) {
            confirmMessage.innerHTML = data['message'];
            confirmMessage.classList.replace('hidden', 'block')
        } else {
            confirmMessage.innerHTML = data['error'];
            confirmMessage.classList.replace('bg-green-700', 'bg-red-700')
            confirmMessage.classList.replace('hidden', 'block')
        }
    });

}