# Sistema de Cadastro de Tarefas (Aplicação Web Containerizada)
Este projeto implementa uma aplicação web de lista de tarefas (To-Do list) utilizando uma arquitetura de microsserviços containerizada com Docker e Docker Compose.

## 🎯 Objetivo
O objetivo deste projeto é demonstrar o desenvolvimento e a implantação de uma aplicação web moderna, separando frontend e backend, e orquestrando os serviços com containers Docker, conforme solicitado no trabalho prático da disciplina de Engenharia de Software.

## 🛠️ Arquitetura e Tecnologias
A aplicação é composta por três serviços principais:

**1. Frontend:** Interface de usuário desenvolvida com HTML, CSS e JavaScript puros. É servida por um container Nginx leve e eficiente.

**2. Backend:** Uma API RESTful construída com Python e o micro-framework Flask. É responsável por toda a lógica de negócio e comunicação com o banco de dados.

**3. Banco de Dados:** Um banco de dados relacional PostgreSQL, rodando em seu próprio container, para persistir os dados das tarefas.

## 🏗️ Estrutura do Projeto
O código-fonte está organizado da seguinte maneira para manter a separação clara entre os serviços:

```
/sistema-de-tarefas
├── backend/
│   ├── app.py              # Lógica da API Flask
│   ├── requirements.txt    # Dependências Python
│   └── Dockerfile          # Instruções para construir a imagem do backend
├── frontend/
│   ├── index.html          # Estrutura da página
│   └── styles.css          # Folha de estilos
├── docker-compose.yml      # Orquestrador dos containers
└── README.md               # Este arquivo
```

## 🚀 Como Executar o Projeto 
### Pré-requisitos

* [Docker](https://www.docker.com/get-started)

* [Docker Compose](https://docs.docker.com/compose/install/)

### Passos para Execução
**1. Clone o repositório:**

```
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO
```

**2. Inicie os containers:**
Na pasta raiz do projeto, execute o comando a seguir. O ```--build``` garante que a imagem do backend seja construída a partir do Dockerfile.

```
docker-compose up --build
```

**3. Acesse a aplicação:**

Após os containers serem iniciados, a aplicação estará disponível nos seguintes endereços:

- **Interface Web (Frontend):** http://localhost:8080

- **API (Backend):** http://localhost:5000/tarefas

## ⚙️ Endpoints da API
A API do backend expõe os seguintes endpoints:

| Método     | Endpoint            | Descrição                                        | Corpo da Requisição                  |
| ---------- | ------------------- | ------------------------------------------------ | ------------------------------------ |
| ```GET```  | ```/tarefas```      | Retorna uma lista com todas as tarefas.          | N/A                                  |
| ```POST``` | ```/tarefas```      | Adiciona uma nova tarefa.                        | ```{ "descricao": "Comprar pão" }``` |
| ```PUT```  | ```/tarefas/<id>``` | Atualiza o status de uma tarefa (concluída/etc). | ```{ "concluida": true }```          |

## 🛑 Como Parar a Aplicação
1. Pressione Ctrl + C no terminal onde o docker-compose está sendo executado.

2. Para derrubar os containers e remover a rede criada, execute:

```
docker-compose down
```
Dica: Para remover também o volume de dados do PostgreSQL (apagando todas as tarefas salvas), use o comando docker-compose down -v.

## 📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤖 Desenvolvimento Assistido por IA
Parte do código, da estrutura e da documentação deste projeto foi gerada com o auxílio do Gemini, um modelo de linguagem grande do Google. A ferramenta foi utilizada para acelerar o desenvolvimento, gerar código boilerplate, depurar erros e refinar a documentação, servindo como uma assistente de programação.

## 👨‍💻 Autor

```
Lucas Dias Squinca
```
