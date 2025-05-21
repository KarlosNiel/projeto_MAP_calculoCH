# Projeto MAP - Cálculo de Carga Horária

Este projeto é uma aplicação Django que tem como objetivo calcular a Carga Horária (CH) de disciplinas a partir de dados organizados, permitindo a manipulação e visualização dessas informações por meio de uma API RESTful.

## 📌 Objetivo

Automatizar o processo de cálculo da carga horária de disciplinas com base em informações como horas teóricas, práticas e carga total, promovendo organização e facilidade na análise desses dados.

## 🧩 Estrutura do Projeto

```
projeto_map/
├── config/ # Configurações do Django
├── sistema_ch/ # Aplicação principal de cálculo de CH
│ ├── api/v1/ # API RESTful (viewsets, serializers, router)
│ ├── migrations/ # Migrações do banco de dados
│ ├── calculateCH.py # Script com a lógica de cálculo da carga horária
│ ├── models.py # Modelos de dados
│ ├── views.py # Views (caso sejam usadas)
│ ├── signals.py # Sinais conectados aos modelos
├── manage.py # Utilitário do Django
├── requirements.txt # Dependências do projeto
```

## ⚙️ Funcionalidades

- Criação e gerenciamento de registros de disciplinas com dados de carga horária.
- Cálculo automático da CH total.
- API RESTful para acesso e manipulação dos dados.
- Estrutura pronta para autenticação e administração via Django Admin.
- Modularização para facilitar a expansão futura do sistema.

## 🚀 Tecnologias Utilizadas

- Python 3
- Django
- Django REST Framework
- SQLite (default)

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/KarlosNiel/projeto_MAP_calculoCH.git
```

2. Acesse a pasta do projeto:
```bash
cd projeto_MAP_calculoCH/projeto_map
```

3. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Aplique as migrações do banco de dados:
```bash
python manage.py migrate
```

6. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```
