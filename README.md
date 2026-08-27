# Checkpoint 2 - Arquitetura Event-Driven com GCP Pub/Sub (Hogwarts Sorting API)

Este projeto evolui a API Serverless para uma arquitetura orientada a eventos (*Event-Driven*). A função deixa de responder a chamadas HTTP diretas e passa a ser acionada assincronamente por mensagens publicadas em um tópico do Google Cloud Pub/Sub.

## Provedor Utilizado
* **Google Cloud Platform (GCP)** - Cloud Run functions & Cloud Pub/Sub

## Arquitetura
1. Uma mensagem (nome do bruxo/a) é publicada no tópico do Pub/Sub `hogwarts-sorting-topic`.
2. O evento dispara a Cloud Function acionada por `CloudEvent`.
3. A função decodifica o payload em Base64, processa a casa de Hogwarts e registra o resultado nos logs de execução.

## Como rodar localmente

### Pré-requisitos
* Python 3.11 ou superior
* Gerenciador de pacotes `pip`
* Terminal de comandos

### Passo a passo
1. Clone o repositório:
   ```bash
   git clone [https://github.com/luanaforbici/hogwarts-sorting-api.git](https://github.com/luanaforbici/hogwarts-sorting-api.git)