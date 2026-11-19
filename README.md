# API de Avaliação de Filmes

API REST para cadastro de usuários e filmes, onde os usuários podem avaliar os filmes com notas de 0 a 5. Desenvolvida com **FastAPI**, **SQLAlchemy** e **PostgreSQL**.

## Funcionalidades

- Cadastro de usuários com senha criptografada (hash com **bcrypt**)
- Cadastro, listagem, atualização e remoção de filmes
- Avaliação de filmes por usuários (nota de 0 a 5, com uma casa decimal)
- Cada usuário só pode avaliar um mesmo filme uma única vez
- Validação de dados com **Pydantic**
- Documentação interativa automática (Swagger UI)

## Tecnologias

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/) (via `psycopg2`)
- [Pydantic](https://docs.pydantic.dev/)
- [bcrypt](https://pypi.org/project/bcrypt/)
- [Uvicorn](https://www.uvicorn.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Estrutura do projeto

```
.
├── main.py           # Rotas da API
├── models.py         # Modelos do banco de dados (SQLAlchemy)
├── schemas.py        # Schemas de validação (Pydantic)
├── database.py       # Conexão com o banco e sessão
├── requirements.txt  # Dependências
└── .env              # Variáveis de ambiente (não versionar)
```

## Como executar

### Pré-requisitos

- Python 3.10 ou superior
- PostgreSQL instalado e rodando

### Passo a passo

1. **Clone o repositório**

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. **Crie e ative um ambiente virtual**

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Crie o banco de dados no PostgreSQL**

```sql
CREATE DATABASE filmes;
```

5. **Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/filmes
```

6. **Inicie o servidor**

```bash
uvicorn main:app --reload
```

As tabelas são criadas automaticamente na primeira execução.

A API ficará disponível em `http://127.0.0.1:8000`.

## Documentação interativa

Com o servidor rodando, acesse:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## Endpoints

### Usuários

| Método | Rota        | Descrição                |
|--------|-------------|--------------------------|
| POST   | `/usuario/` | Cria um novo usuário     |
| GET    | `/usuario/` | Lista todos os usuários  |

**Exemplo de corpo (POST `/usuario/`):**

```json
{
  "nome_usuario": "joao",
  "email": "joao@email.com",
  "senha": "minhasenha123"
}
```

### Filmes

| Método | Rota                | Descrição                      |
|--------|---------------------|--------------------------------|
| POST   | `/filme/`           | Cadastra um novo filme         |
| GET    | `/filme/`           | Lista todos os filmes          |
| PUT    | `/filme/{filme_id}/`| Atualiza os dados de um filme  |
| DELETE | `/filme/{filme_id}/`| Remove um filme                |

**Exemplo de corpo (POST `/filme/`):**

```json
{
  "nome": "Interestelar",
  "ano_lancamento": 2014,
  "diretor": "Christopher Nolan"
}
```

### Avaliações

| Método | Rota                          | Descrição                     |
|--------|-------------------------------|-------------------------------|
| POST   | `/filme/{filme_id}/avaliacao` | Avalia um filme               |

**Exemplo de corpo:**

```json
{
  "usuario_id": 1,
  "nota": 4.5
}
```

## Modelo de dados

```
Usuario (1) ────< Avaliacao >──── (1) Filme
```

- **Usuario:** `id`, `nome_usuario` (único), `email`, `senha_hash`
- **Filme:** `id`, `nome` (único), `ano_lancamento`, `diretor`
- **Avaliacao:** `id`, `usuario_id`, `filme_id`, `nota`
  - Restrição: nota entre 0 e 5
  - Restrição: um usuário só avalia o mesmo filme uma vez

## Códigos de resposta

| Código | Significado                                              |
|--------|----------------------------------------------------------|
| 200    | Sucesso                                                  |
| 404    | Filme ou usuário não encontrado                          |
| 409    | Conflito (nome já existente ou avaliação duplicada)      |
| 422    | Dados inválidos na requisição                            |

## Próximos passos

- [ ] Autenticação com JWT
- [ ] Rota para listar os usuários que avaliaram um filme
- [ ] Média de notas por filme
- [ ] Migrações com Alembic
- [ ] Testes automatizados

## Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar e modificar.
