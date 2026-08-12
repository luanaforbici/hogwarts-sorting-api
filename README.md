# Chapéu Seletor Serverless API (GCP)

API desenvolvida para a disciplina de Serverless Computing.
A aplicação recebe um nome via requisição HTTP e retorna a casa de Hogwarts correspondente em formato JSON.

## 🔗 Endpoint em Produção
- **URL Base**: `<COLE_AQUI_A_URL_GERADA_PELO_GCP>`
- **Exemplo 1**: `<SUA_URL>/Luana`
- **Exemplo 2**: `<SUA_URL>/?nome=Luana`

## 🛠️ Tecnologias
- **Linguagem**: Python 3.11
- **Plataforma**: Google Cloud Platform (GCP)
- **Serviço**: Cloud Run functions (FaaS Gen 2)

## 📁 Estrutura do Projeto
- `main.py`: Entrada da requisição HTTP do GCP.
- `house.py`: Lógica de validação e hashing para ordenação das casas.
- `requirements.txt`: Dependências do ambiente Python.