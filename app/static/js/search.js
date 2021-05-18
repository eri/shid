function recherche_dossiers() {
    var a, i, txtValue;

    var input = document.getElementById('recherche');
    var filter = input.value.toUpperCase();

    var ul = document.getElementById("resultats");
    var li = ul.getElementsByTagName('li');

    var search_num_box = document.getElementById("nombre_recherche")
    var nb_search = 0

    for (i = 0; i < li.length; i++) {
      a = li[i].getElementsByTagName("a")[0];
      txtValue = a.textContent || a.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
        nb_search = nb_search + 1
      } else {
        li[i].style.display = "none";
        nb_search = nb_search - 1
      }
    }
    if (nb_search < 0) {nb_search = 0}

    if (nb_search == 0) {
        search_num_box.innerHTML = "Liste pour votre recherche. Essayez avec d'autres termes de recherche si nécessaire."
    } else {
        search_num_box.innerHTML = "Nous avons trouvé " + nb_search + " résultats correspondant à votre recherche."
    }
  }
