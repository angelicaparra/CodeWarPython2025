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

1. **Crie o ambiente virtual e ative:**
```bash
python -m venv .venv
# Ative conforme seu sistema:
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute as migrações:**
```bash
alembic upgrade head
```

4. **Inicie o servidor FastAPI:**
```bash
uvicorn Api_Carros.app:app --reload
```

5. **Acesse a documentação da API:**
- Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- Dashbord: [http://127.0.0.1:8050/](http://127.0.0.1:8050/)

---

## 📘 Sobre o Projeto

Este projeto é uma **API RESTful completa** para o gerenciamento de veículos — simulando um sistema de frotas com carros antigos. Desenvolvido com **FastAPI** e **SQLite**, o objetivo principal é oferecer uma base sólida e performática para aprendizado, testes e prototipagem.

Criado como parte do desafio **"CodeWar Python + Análise de Dados 2025"**, ele abrange:

✅ Criação de API do zero  
✅ Integração com banco de dados  
✅ Consumo de APIs externas  
✅ Processos de ETL  
✅ Visualização de dados

---

## ⚡ Por que FastAPI?

Inicialmente, o projeto seria feito em Flask, mas após estudos mais aprofundados, foi escolhido o **FastAPI** por oferecer:

- Alta performance comparável ao **NodeJS** e **Golang**
- Base em **Starlette** e execução com **Uvicorn**
- Suporte nativo a código assíncrono com **uvloop** (libuv em C)

💡 *Uvicorn é o servidor padrão do FastAPI, utilizando o mesmo event loop usado em tecnologias modernas como NodeJS, Julia e Luvit.*

---

## 📌 Funcionalidades da API

A API disponibiliza os principais endpoints para CRUD de veículos, seguindo padrões REST:

| Método | Endpoint              | Descrição                                 |
|--------|-----------------------|-------------------------------------------|
| GET    | `/carros`             | Lista todos os carros                     |
| GET    | `/carros/{id}`        | Detalha um carro específico               |
| POST   | `/carros`             | Adiciona um novo carro                    |
| PUT    | `/carros/{id}`        | Atualiza um carro existente               |
| DELETE | `/carros/{id}`        | Remove um carro do sistema                |


### 🧩 Estrutura de um carro:
```json
{
  "id": "ID",
  "marca": "Volkswagen",
  "modelo": "Fusca",
  "cor": "Vermelho",
  "ano": "1964",
  "tipo_combustivel": "Gasolina",
  "modificacao": "Original",
  "descricao": "Clássico carro popular da VW"
}
```
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