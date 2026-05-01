console.log("JS funcionando!")
const botaoCadastro = document.querySelector("#cadastro-box button")
botaoCadastro.addEventListener("click", function(){
    console.log("botão clicado")
    const nome = document.querySelector("#nome").value
    const email = document.querySelector("#email").value
    const senha = document.querySelector("#senha").value
    console.log(nome)
    console.log(email)
    console.log(senha)

    fetch("http://localhost:8000/cadastro",{
    method: "POST",
    headers: {
                "Content-Type": "application/json"
            },
    body: JSON.stringify({
        nome: nome,
        email: email,
        senha: senha
    })
    })
    .then(function(response){
        return response.json()
    })
    .then(function(data){
        console.log(data)
        const msgOK = document.getElementById("mensagem")
        msgOK.textContent = "Usuário criado com Sucesso!"
        setTimeout(function(){
            window.location.href = "index.html"
                }, 2000)
    })
})

