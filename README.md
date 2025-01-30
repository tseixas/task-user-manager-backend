
# Projeto task-user-manager-backend

Este projeto é uma aplicação desenvolvido com Python, Flask, Redis e MongoDB.

## 💻 Funcionalidades
- Login e Logout
- Redefinição de senha (Em breve)
- Listagem de Tarefas
- Cadastro de Tarefas
- Atualização de Tarefas
- Visualização de Tarefas
- Remoção de Tarefas

## ⚙️ Endpoints
### Autenticação
- Login ```POST /auth/login```
- Logout ```POST /auth/logout```
- Cadastrar usuário ```POST auth/register```
```
Exemplo de payload POST auth/register
{
	"email": "user@mail.com",
	"password": "123456"
}
```

### Tarefas
- Cadastrar ```POST /tasks```
```
Exemplo de payload POST /tasks
{
	"title": "task title",
	"description": "description task",
	"due_date": "2025-01-30"
}
```
- Listagem ```POST /tasks/all```
- Detalhes ```POST /tasks/<id>```
- Atualizar ```PUT /tasks/<id>```
```
Exemplo de payload PUT tasks/<id>
{
	"title": "task title - update",
	"description": "description task - update",
	"due_date": "2025-01-20"
}
```
- Remoção ```POST /tasks/<id>```

## 🔍 Verificando integrações
### Redis
```
docker ps
docker exec -it <container> redis-cli 

Lista as chaves armazenadas:
127.0.0.1:6379> keys *

Obtendo o valor de uma chave:
127.0.0.1:6379> get <key>

Verificando os detalhes de uma chave:(será retornado um valor em segundos com o tempo restante)
127.0.0.1:6379> ttl <key>
```

### MongoDB
```
docker ps
docker exec -it <container> mongosh

Listar bancos de dados:
show databases

Selecionar um banco de dados:
use db_tsk

Listar coleções dentro de um banco de dados:
show collections

Listando os dados:
db.users.find().pretty()
db.tasks.find().pretty()

```

## 📥 Clonando o Repositório

Para baixar o código-fonte do projeto, execute o seguinte comando:

```sh
git clone git@github.com:tseixas/task-user-manager-backend.git
cd task-user-manager-backend
```

## 🐳 Executando a Aplicação via Docker

Antes de iniciar, certifique-se de ter o [Docker](https://www.docker.com/) e o [Docker Compose](https://docs.docker.com/compose/) instalados.

### 🚀 Passos para Rodar a Aplicação

1. **Copie o arquivo de variáveis de ambiente (se necessário)**
   ```sh
   cp .env.example .env
   ```
   
2. **Construa e inicie os containers**
   ```sh
   docker compose up --build
   ```
   
3. **Verifique se os containers estão rodando(Opcional)**
   ```sh
   docker ps
   ```

4. **Acesse a aplicação**
   - O frontend estará disponível em: `http://127.0.0.1:5000`

5. **Credenciais de acesso - (Criadas ao iniciar a aplicação)**
   - email: `admin@mail.com`
   - senha: `123456`

## 🛑 Parando a Aplicação
Para parar os containers, execute:
```sh
docker-compose down
```

---

Desenvolvido por [Thiago Seixas](https://github.com/tseixas) 🚀

