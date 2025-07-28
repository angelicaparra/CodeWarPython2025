# 🚗 CodeWarPython2025 – API de Carros

API desenvolvida com **FastAPI** para gerenciamento de frotas de carros. O sistema oferece funcionalidades completas de CRUD, integração com API externa para consulta de dados automotivos e banco de dados relacional via SQLAlchemy.

---

## 📌 Funcionalidades

- ✅ Cadastro, leitura, atualização e exclusão de carros (CRUD)
- 🔄 Integração com API externa de veículos (API Ninjas)
- 🔐 Banco de dados relacional com SQLAlchemy
- 📥 Importação em lote de carros e via ETL

---

## 🚀 Como rodar o projeto

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/codewarpython2025.git
cd codewarpython2025
```

2. **Crie o ambiente virtual e ative:**
```bash
python -m venv .venv
# Ative conforme seu sistema:
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Execute as migrações:**
```bash
alembic upgrade head
```

5. **Inicie o servidor FastAPI:**
```bash
uvicorn Api_Carros.app:app --reload
```

6. **Acesse a documentação da API:**
- Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- Dashbord: [http://127.0.0.1:8050/](http://127.0.0.1:8050/)

---

## 🧱 Estrutura dos Arquivos

```
Api_Carros/
├── app.py          # Inicialização FastAPI
├── database.py     # Conexão SQLite com SQLAlchemy
├── models.py       # ORM - Modelo de dados Car
├── routers.py      # Endpoints da API
├── schemas.py      # Schemas Pydantic (entrada/saída)
├── migrations/     # Diretório Alembic
```

---

## 🔗 Endpoints Principais

- `GET /api/v1/carros`: Lista todos os carros
- `GET /api/v1/carros/todos`: Lista carros do banco e externos
- `POST /api/v1/carros`: Cadastra novo carro
- `GET /api/v1/carros/{id}`: Detalha um carro por ID
- `PUT /api/v1/carros/{id}`: Atualiza carro por ID
- `PATCH /api/v1/carros/{id}`: Atualização parcial
- `DELETE /api/v1/carros/{id}`: Deleta carro por ID
- `POST /api/v1/carros/importar-lote`: Importa vários carros de uma vez
- `POST /api/v1/carros/etl/importar_carros`: Importa dados da API externa

---

## 🛠️ Requisitos

- Python 3.10+
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic
- Pydantic
- Requests

---

## ✨ Créditos

Projeto desenvolvido para fins educacionais no **CodeWar Python 2025**.