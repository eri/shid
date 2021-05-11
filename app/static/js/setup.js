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