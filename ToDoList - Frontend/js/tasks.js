document.addEventListener("DOMContentLoaded", function (){
    const id_usuario = localStorage.getItem("id_usuario")
    console.log("id_usuario:", id_usuario)
    const token = localStorage.getItem("token")
    console.log("token:", token)

    fetch(`http://localhost:8000/usuarios/${id_usuario}/tarefas`,
    //template literal usa crase e $ pra indicar um valor que será adicionado (definido nas linhas anteriores)
    {
        method: "GET",
        headers: {
        "Authorization": `Bearer ${token}` //padrão do protocolo OAuth2
    }
    }) 
    
    .then(function(response){
        return response.json()
    })

    .then(function(data){
        console.log(data)

        const lista_tasks = document.querySelector("#tasks") //id que eu atribui no tasks.html
        data.forEach(function(task) {   
            const li = document.createElement("li") //cria um elemento <li>
            li.textContent = task.descricao //pega a descrição da task e atribui a <li>
            lista_tasks.appendChild(li) //adiciona o <li> dentro da lista <ul> criada no tasks.html

            const task_actions = document.createElement("div")
            task_actions.className = "task-actions"
            li.appendChild(task_actions)

            const edit_button = document.createElement("button")
            edit_button.dataset.id_tarefa = task.id_tarefa //armazenou o id_tarefa no botão de edit
            edit_button.addEventListener("click", function(){
                const novaDesc = prompt("Editar Tarefa:", task.descricao)
                if (novaDesc === null){ // Retorna nada caso o usuario clique em cancelar
                    return
                }
                fetch(`http://localhost:8000/usuarios/${id_usuario}/tarefas/${edit_button.dataset.id_tarefa}`,
                    {
                        method: "PUT",
                        headers: {
                            "Authorization": `Bearer ${token}`,
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            descricao: novaDesc
                        })
                    })  
                    .then(function(response){
                            return response.json()
                    })      
                    .then(function(data){
                            console.log(data)  
                            li.firstChild.textContent = novaDesc                     
                    })     
            })
            edit_button.type = "button"
            edit_button.textContent = "Editar"
            task_actions.append(edit_button)

            const del_button = document.createElement("button")
            del_button.dataset.id_tarefa = task.id_tarefa //armazenou o id_tarefa da task criada e atribuiu ao botão de delete
            del_button.addEventListener("click", function(){
                console.log(del_button.dataset.id_tarefa)
                fetch(`http://localhost:8000/usuarios/${id_usuario}/tarefas/${del_button.dataset.id_tarefa}`,
                    {
                        method: "DELETE",
                        headers: {
                            "Authorization": `Bearer ${token}`
                        }
                    })       
                    
                    .then(function(response){
                        return response.json()
                    })

                    .then(function(data){
                        console.log(data)
                        li.remove()
                    })

            })
            del_button.type = "button"
            del_button.textContent = "Deletar"
            task_actions.append(del_button)
        })

        const botaoCriar = document.querySelector("#criar-task button")
        botaoCriar.addEventListener("click", function(){
            const novaTask = document.querySelector("#nova-task").value
            fetch(`http://localhost:8000/usuarios/${id_usuario}/tarefas/`,
                {
                method: "POST",
                headers: {
                            "Authorization": `Bearer ${token}`,
                            "Content-Type": "application/json"
                        },
                body: JSON.stringify({
                    descricao: novaTask
                })
            })
            .then(function(response){
                return response.json()
            })
            .then(function(data){
                console.log(data)
                const lista_tasks = document.querySelector("#tasks")
                const li = document.createElement("li")
                li.textContent = data.descricao
                lista_tasks.appendChild(li)
                
                const task_actions = document.createElement("div")
                task_actions.className = "task-actions"
                li.appendChild(task_actions)

                const edit_button = document.createElement("button")
                edit_button.dataset.id_tarefa = data.id_tarefa // Guarda no botão de editar, o id_tarefa que veio do backend
                edit_button.addEventListener("click", function(){
                    const li = edit_button.closest("li") //procurando o elemento pai mais próximo com aquela tag.
                    const novaDesc = prompt("Editar Tarefa:", data.descricao)
                    if (novaDesc === null){ // Retorna nada caso o usuario clique em cancelar
                    return
                }
                    fetch(`http://localhost:8000/usuarios/${id_usuario}/tarefas/${edit_button.dataset.id_tarefa}`,
                    {
                        method: "PUT",
                        headers: {
                            "Authorization": `Bearer ${token}`,
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            descricao: novaDesc
                        })
                    })  
                    .then(function(response){
                            return response.json()
                    })      
                    .then(function(data){
                            console.log(data)
                            li.firstChild.textContent = novaDesc                      
                    })     
                })
                edit_button.type = "button"
                edit_button.textContent = "Editar"
                task_actions.append(edit_button)

                const del_button = document.createElement("button")
                del_button.dataset.id_tarefa = data.id_tarefa
                del_button.addEventListener("click", function(){
                    console.log(del_button.dataset.id_tarefa)
                    fetch(`http://localhost:8000/usuarios/${id_usuario}/tarefas/${del_button.dataset.id_tarefa}`,
                    {
                        method: "DELETE",
                        headers: {
                            "Authorization": `Bearer ${token}`
                        }
                    })       
                    
                    .then(function(response){
                        return response.json()
                    })

                    .then(function(data){
                        console.log(data)
                        li.remove()
                    })
                })
                del_button.type = "button"
                del_button.textContent = "Deletar"
                task_actions.append(del_button)
            })  
        })
         
        const botaoSair = document.getElementById("sair")
        botaoSair.addEventListener("click", function(){
            window.location.href = "index.html"
        })

    })
})