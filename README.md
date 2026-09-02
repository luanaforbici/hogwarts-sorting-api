# Checkpoint 3 - Orquestração Serverless com Google Cloud Workflows (Hogwarts Sorting API)

Este repositório contém a solução do Checkpoint 3, evoluindo o pipeline das entregas anteriores para uma arquitetura orquestrada de serviços serverless no **Google Cloud Platform (GCP)**.

## Provedores e Serviços Utilizados
* **Google Cloud Workflows:** Orquestração do fluxo de execução.
* **Google Cloud Pub/Sub:** Mensageria assíncrona baseada em eventos.
* **Cloud Run functions:** Execução do código de ordenação das casas de Hogwarts.

## Arquitetura e Fluxo de Execução
1. O **Cloud Workflows** recebe os parâmetros de entrada (ex: nome do estudante) e valida o payload.
2. O workflow publica a mensagem codificada em Base64 no tópico `hogwarts-sorting-topic` do **Pub/Sub**.
3. A **Cloud Function** acionada por `CloudEvent` processa a mensagem, sorteia a casa e grava o resultado nos logs do GCP.
4. O workflow possui mecanismos nativos de resiliência, com tratamento de exceções e regras de retentativas (*retry*) para falhas transitórias de rede ou serviço.

## Estrutura do Repositório
* `main.py`: Código principal da Cloud Function.
* `house.py`: Lógica do Chapéu Seletor.
* `requirements.txt`: Dependências do projeto.
* `workflows/workflow.yaml`: Definição da orquestração do Cloud Workflows em YAML.

## Segurança
Este repositório não contém chaves privadas, credenciais, segredos ou arquivos `.json` confidenciais. Toda a autenticação entre os serviços do GCP é realizada nativamente via IAM e contas de serviço autorizadas.