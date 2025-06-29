# CRUD Python - Sistema Escolar

![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)
![Docker](https://img.shields.io/badge/docker-compose-blue.svg)

Sistema CRUD para gestão escolar desenvolvido em Python com Flask.

## 🚀 Funcionalidades

- ✅ CRUD de Alunos
- ✅ CRUD de Professores  
- ✅ CRUD de Usuários
- ✅ CRUD de Turmas
- ✅ CRUD de Pagamentos
- ✅ Sistema de Presença
- ✅ Monitoramento com Prometheus e Grafana

## 🛠️ Tecnologias

- **Backend**: Python, Flask
- **Banco**: PostgreSQL
- **Containerização**: Docker, Docker Compose
- **Monitoramento**: Prometheus, Grafana
- **Testes**: Pytest

## 📋 Pré-requisitos

- [Docker](https://www.docker.com/get-started) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado
- [Git](https://git-scm.com/) instalado

## 🚀 Como executar

### 1. Clone o repositório
```bash
git clone https://github.com/LucaasMartins/crud-python.git
cd crud-python
```

### 2. Execute a aplicação
```bash
docker-compose up --build
```

### 3. Acesse a aplicação
- **API**: http://localhost:5000
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

## 🧪 Testando

Verifique se a API está funcionando:
```bash
curl http://localhost:5000/
```

Resposta esperada:
```json
{
  "message": "API Sistema Escolar",
  "status": "running"
}
```

## 🛑 Parar a aplicação

```bash
docker-compose down
```