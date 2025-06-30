# 🚗 **API de Carros** – Gerenciamento de Frotas Inteligente 🔧

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-009688?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

Em breve ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

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
  "nome": "Fusca",
  "descricao": "Clássico carro popular da VW",
  "marca": "Volkswagen",
  "ano": "1964",
  "cor": "Vermelho",
  "tipo_combustivel": "Gasolina",
  "preco": "1.000.000,00"
  "modificacao": "Original"
}
```
---

🤝 Contribuições
Fique à vontade para:
- Sugerir novas funcionalidades
- Reportar bugs
- Criar issues ou pull requests

💬 Toda contribuição é bem-vinda para aprimorar o projeto!

---

👩‍💻 Autora

Angélica Parra de Lima

🔗 github.com/angelicaparra
