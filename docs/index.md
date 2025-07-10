# 🚗 API de Carros – Gerenciamento de Frotas Inteligente

**Versão:** 0.1.0  
**Criado por:** Angélica Parra – [angelicaparraa@gmail.com](mailto:angelicaparraa@gmail.com)  
**Desafio:** CodeWar Python + Análise de Dados 2025

---

## 🧾 Descrição

API desenvolvida com **FastAPI** e **SQLAlchemy**, criada para gerenciamento de frotas de veículos. Permite operações completas de CRUD (Create, Read, Update, Delete), com rotas organizadas e validação de dados via **Pydantic**.

---

## 📁 Estrutura do Projeto

```
Api_Carros/
├── app.py
├── database.py
├── models.py
├── routers.py  <-- Arquivo com as rotas da API
├── schemas.py
├── migrations/
└── __init__.py
```

---

## ⚙️ Configuração do Projeto (`pyproject.toml`)

```toml
[project]
name = "API de Carros – Gerenciamento de Frotas Inteligente"
version = "0.1.0"
description = "Criado como parte do desafio CodeWar Python + Análise de Dados 2025"
authors = [
    {name = "Angélica Parra", email = "angelicaparraa@gmail.com"}
]

[tool.ruff]
line-length = 79
extend-exclude = ['migrations']

[tool.ruff.lint]
preview = true
select = ['I', 'F', 'E', 'W', 'PL', 'PT']

[tool.ruff.format]
preview = true
quote-style = 'single'

[tool.taskipy.tasks]
lint = 'ruff check'
lint_fix = 'ruff check --fix'
format = 'ruff format'
run = 'fastapi dev Api_Carros/app.py'
```

---

## 🧪 Comandos Rápidos

```bash
# Executar o projeto
task run

# Checar lint com Ruff
task lint

# Corrigir lint automaticamente
task lint_fix

# Formatador de código
task format
```

---

## 🔌 Endpoints da API

### ✅ Criar Carro
- **POST** `/api/v1/carros/`
- **Body**: `CarSchema`
- **Response**: `CarPublic`
- **Status**: `201 Created`

### 📄 Listar Carros
- **GET** `/api/v1/carros/`
- **Query Params**: `offset`, `limit`
- **Response**: `CarList`
- **Status**: `200 OK`

### 🔍 Buscar Carro por ID
- **GET** `/api/v1/carros/{car_id}`
- **Response**: `CarPublic`
- **Status**: `200 OK`

### ✏️ Atualizar Carro (PUT)
- **PUT** `/api/v1/carros/{car_id}`
- **Body**: `CarSchema`
- **Response**: `CarPublic`
- **Status**: `201 Created`

### 🛠️ Atualização Parcial (PATCH)
- **PATCH** `/api/v1/carros/{car_id}`
- **Body**: `CarPartialUpdate`
- **Response**: `CarPublic`
- **Status**: `201 Created`

### ❌ Deletar Carro
- **DELETE** `/api/v1/carros/{car_id}`
- **Status**: `204 No Content`

---

## 🧠 Observações Técnicas

- Utiliza `Depends` para injeção de sessão com o banco (SQLAlchemy).
- `PATCH` utiliza `exclude_unset=True` para enviar apenas campos alterados.
- CRUD completo com boas práticas REST.

---

## 📫 Contato

- **Desenvolvedora:** Angélica Parra  
- **Email:** [angelicaparraa@gmail.com](mailto:angelicaparraa@gmail.com)