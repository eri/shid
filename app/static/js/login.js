var username = document.getElementById("username");
var password = document.getElementById("password");

var box = document.getElementById("ErrorMessage");

var valider = document.getElementById('connexion');
valider.addEventListener("click", login);

function login() {

  $.ajax({
    type: "GET",
    headers: { "Access-Control-Allow-Origin": "*" },
    url:
      `/api/auth/login/` +
      `?username=${encodeURI(username.value)}` +
      `&password=${encodeURI(password.value)}`,
  }).done(function (data) {

    if (data["success"] == true) {
        window.location.href = "/"
    } else {
      box.innerHTML = data['error']
      box.classList.replace("hidden", "block");
    }
  });
}
