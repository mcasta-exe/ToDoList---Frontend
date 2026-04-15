# ToDo List - Frontend

Interface web para gerenciamento de tarefas, consumindo uma API REST com autenticação JWT.

## 🚀 Funcionalidades

- Cadastro de usuário
- Login com autenticação via token
- Criação de tarefas
- Listagem de tarefas
- Edição de tarefas
- Exclusão de tarefas
- Logout com redirecionamento
- Interface dinâmica com JavaScript puro

## 🛠 Tecnologias

- HTML5
- CSS3
- JavaScript (Vanilla)
- API REST (consumo via Fetch)

## 🔐 Autenticação

O sistema utiliza JWT (Bearer Token).  
O token é armazenado no `localStorage` e enviado nas requisições protegidas.

## 📁 Estrutura

- index.html → login
- cadastro.html → criação de usuário
- tasks.html → dashboard de tarefas
- script.js → lógica de requisições e manipulação do DOM
- style.css → estilização da interface

## ▶️ Como executar

1. Abrir o projeto em um servidor local (ex: Live Server no VS Code)
2. Garantir que o backend esteja rodando
3. Acessar o `index.html` ou `login.html`
4. Realizar login para acessar as tarefas

## ⚙️ Backend necessário

Este frontend depende de uma API construída com FastAPI + PostgreSQL.

## 📌 Observações

- Requer backend ativo para funcionamento
- Utiliza `fetch` para comunicação com API
- Dados de autenticação armazenados localmente no navegador
