# Checkpoint 4 - Observabilidade e Otimização de Performance (Hogwarts Sorting API)

Este repositório contém a solução final do Checkpoint 4, adicionando **observabilidade completa (Logging Estruturado e Métricas)** e uma **análise crítica de arquitetura** para otimização de custos e performance no **Google Cloud Platform (GCP)**.

---

## 1. Instrumentação e Observabilidade
* **Google Cloud Logging:** Logs convertidos para o formato JSON estruturado (`severity`, `message`, `service` e `payload`), permitindo consultas via Log Analytics/Logs Explorer.
* **Google Cloud Monitoring:** Acompanhamento de métricas nativas de execução de Cloud Run functions/Cloud Workflows (tempo de resposta, taxa de erro HTTP, invocação de instâncias e latência de mensageria).

---

## 2. Relatório de Otimizações Técnicas Propostas

### Otimização 1: Transição do Pub/Sub Push para Invocação Direta via HTTP (Redução de Latência e Custos)
* **Diagnóstico:** A arquitetura atual utiliza o Cloud Workflows para publicar no Pub/Sub, que por sua vez dispara a Cloud Function de forma assíncrona.
* **Proposta:** Para cenários de APIs síncronas que exigem resposta em tempo real, conectar o Workflows diretamente à Cloud Function via HTTPS/IAM.
* **Impacto:** Elimina o *overhead* de mensageria assíncrona, reduz a latência total da requisição em até 200ms-500ms e remove custos de operabilidade do Pub/Sub para fluxos de baixa/média volumetria.

### Otimização 2: Ajuste de Memória e Concorrência da Cloud Function (Cold Start & Custo)
* **Diagnóstico:** A função Python aloca a quantidade padrão de memória (256 MB ou 512 MB). Como a execução do algoritmo do Chapéu Seletor é extremamente leve, há subutilização de CPU/Memória.
* **Proposta:**
  1. Configurar o limite de memória para **128 MB** ou **256 MB**.
  2. Definir o parâmetro de **Min Instances = 1** apenas em horários de pico se houver gargalo de *Cold Start*.
* **Impacto:** Redução direta nos custos de computação (*GB-segundo* e *GHz-segundo*) da função em cerca de 30% a 50%.

### Otimização 3: Consolidação da Política de Retry e Dead-Letter Queue (DLQ) no Pub/Sub
* **Diagnóstico:** Em falhas persistentes (ex: erros 5xx contínuos), retentativas ilimitadas do Workflow/Pub/Sub podem gerar *loops* infinitos de execução e custos desnecessários.
* **Proposta:** Configurar um **Dead-Letter Topic** no Pub/Sub com limite máximo de 5 retentativas (*Max Delivery Attempts*).
* **Impacto:** Evita desperdício de recursos computacionais processando payloads corrompidos e garante isolamento para análise posterior de falhas sem impacto na fila principal.

---

## 3. Estrutura do Repositório
* `main.py`: Função Python com instrumentação de logs estruturados em JSON.
* `house.py`: Regra de negócio do Chapéu Seletor.
* `requirements.txt`: Dependências do projeto.
* `workflows/workflow.yaml`: Definição da orquestração no Cloud Workflows.
* `docs/`: Pasta contendo as evidências visuais de logs e métricas.

---

## 4. Diretrizes de Segurança
Este repositório cumpre integralmente as regras de segurança do GCP: não há credenciais, segredos, chaves `.json` ou variáveis de ambiente confidenciais no repositório público. As integrações utilizam identidades gerenciadas via **IAM e Service Accounts**.