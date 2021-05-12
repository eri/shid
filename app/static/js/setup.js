var type_structure = document.querySelector('input[name="type_structure"]:checked')
var nom_structure = document.getElementById('nom_structure');
var adresse_structure = document.getElementById('adresse_structure');
var cp_structure = document.getElementById('cp_structure');
var ville_structure = document.getElementById('ville_structure');

var covid_structure = document.querySelector('input[name="covid_structure"]:checked')
var covid_dose = document.getElementById('covid_dose');
var capacite_lit = document.getElementById('capacite_lit');

var username_admin = document.getElementById('username_admin');
var password_admin = document.getElementById('password_admin');
var email_admin = document.getElementById('email_admin');
var public_stats = document.querySelector('input[name="public_stats"]:checked')

var confirmMessage = document.getElementById('confirmMessage');
var redirectLogin = document.getElementById('redirectLogin');
var valider = document.getElementById('valider');
valider.addEventListener("click", setup);

if (type_structure == null || type_structure.value == null) {
    type_structure = "hôpital"
} else { type_structure = type_structure.value }

if (public_stats == null || public_stats.value == null) {
    public_stats = "True"
} else { public_stats = public_stats.value }

if (covid_structure == null || covid_structure.value == null) {
    if (covid_dose == null || covid_dose.value == null) {
        covid_structure = "False"
    } else {
        covid_structure = "True"
    }
} else { covid_structure = covid_structure.value }

function setup() {
    $.ajax({
        type: "GET",
        headers: {"Access-Control-Allow-Origin": "*"},
        url: `/api/auth/setup/`
                + `?type_structure=${encodeURI(type_structure)}`
                + `&nom_structure=${encodeURI(nom_structure.value)}`
                + `&adresse_structure=${encodeURI(adresse_structure.value)}`
                + `&cp_structure=${encodeURI(cp_structure.value)}`
                + `&ville_structure=${encodeURI(ville_structure.value)}`
                + `&covid_structure=${encodeURI(covid_structure)}`
                + `&covid_dose=${encodeURI(covid_dose.value)}`
                + `&capacite_lit=${encodeURI(capacite_lit.value)}`
                + `&username_admin=${encodeURI(username_admin.value)}`
                + `&password_admin=${encodeURI(password_admin.value)}`
                + `&email_admin=${encodeURI(email_admin.value)}`
                + `&public_stats=${encodeURI(public_stats)}`

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

var suivant = document.getElementById('setup-continuer-1');
var suivant2 = document.getElementById('setup-continuer-2');

var retour2 = document.getElementById('setup-precedent-2');
var retour3 = document.getElementById('setup-precedent-3');

var etape1 = document.getElementById("setup-1");
var etape2 = document.getElementById("setup-2");
var etape3 = document.getElementById("setup-3");

retour2.addEventListener("click", RetourEtape1);
retour3.addEventListener("click", RetourEtape2);

suivant.addEventListener("click", PassageEtape2);
suivant2.addEventListener("click", PassageEtape3);

function RetourEtape1() {
    etape2.classList.replace("block", "hidden");
    etape1.classList.replace("hidden", "block");
}

function RetourEtape2() {
    etape3.classList.replace("block", "hidden");
    etape2.classList.replace("hidden", "block");
}

function PassageEtape2() {
    etape1.classList.replace("block", "hidden");
    etape2.classList.replace("hidden", "block");
}

function PassageEtape3() {
    etape2.classList.replace("block", "hidden");
    etape3.classList.replace("hidden", "block");
}
