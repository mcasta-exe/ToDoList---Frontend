console.log("JS funcionando!")
// document = a página HTML inteira
// querySelector = "encontre pra mim o elemento..."
// "#login-box button" = dentro do #login-box, o button
const botaoLogin = document.querySelector("#login-box button")

// botaoLogin = o elemento que encontramos
// addEventListener = "fique escutando esse evento..."
// "click" = o evento é um clique
// function() {} = execute essa função quando acontecer
botaoLogin.addEventListener("click", function() {
    console.log("Botão Login Clicado!")
    const email = document.querySelector("#email").value
    const senha = document.querySelector("#senha").value
    console.log(email)
    console.log(senha)

    const formdata = new FormData()
    formdata.append("username", email)
    formdata.append("password", senha)

    if (email === "" || senha === "") {
        console.log("Preencha os campos em branco")
        return 
    }

    fetch("http://localhost:8000/login", {
        method: "POST",
        body: formdata //formato exigido pelo OAuth2
    })
    .then(function(response){
        return response.json()
    })
    .then(function(data){
        console.log(data)
        console.log(data.access_token)
        localStorage.setItem("token", data.access_token) //acess_token é o token de autenticação gerado pelo meu backend, é possível visualizar através do console no browser
        localStorage.setItem("id_usuario", data.id_usuario)
        window.location.href = "tasks.html"
})
})



