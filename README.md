# Checkpoint 4 - Observabilidade e Otimização de Performance (Hogwarts Sorting API)

Este repositório contém a solução final do **Checkpoint 4**, focada em estabelecer **observabilidade completa (Logging Estruturado e Métricas)** no pipeline serverless da **Hogwarts Sorting API** no **Google Cloud Platform (GCP)** e documentar uma **análise crítica de performance e custo** com oportunidades de melhoria técnica.

---

## 1. Instrumentação e Evidências Visuais de Observabilidade

A aplicação foi instrumentada em Python (`main.py`) para emitir registros estruturados e monitorar o desempenho dos serviços no GCP. Todas as evidências visuais solicitadas estão armazenadas na pasta [`docs/`](./docs/):

### 📸 Evidência 1: Cloud Logging Estruturado (`docs/logging_estruturado.png`)
* **Ferramenta:** Google Cloud Logging / Logs Explorer.
* **Filtro de Consulta:** `resource.type="cloud_run_revision"` e `textPayload:"[CHAPÉU SELETOR]"`.
* **Detalhes do Registro:**
  * **Timestamp:** `2026-09-02T23:45:32.508212Z`
  * **Severity / Gravidade:** `INFO` (Padrão)
  * **Payload Emitido:** `[CHAPÉU SELETOR] Processado com sucesso! Nome: Luana | Casa: Sonserina`
  * **Análise:** Demonstra a capacidade de busca indexada e estruturação de mensagens para auditoria de execuções do Chapéu Seletor.

### 📸 Evidência 2: Dashboard de Métricas e Performance (`docs/metricas_gcp.png`)
* **Ferramenta:** Google Cloud Monitoring / Painel de Observabilidade do Cloud Run (`hogwarts-sorting-pubsub`).
* **Região / URL:** `us-central1` | `https://hogwarts-sorting-pubsub-1014335313570.us-central1.run.app`
* **Métricas Analisadas:**
  * **Contagem de Solicitações:** Monitoramento do volume de requisições por segundo (status HTTP `2xx`).
  * **Latências da Solicitação (p50, p95, p99):** Tempos de resposta na faixa de ~15ms a 20ms.
  * **Latência de Ponta a Ponta:** Processamento completo da requisição serverless em cerca de 1s.
  * **Contagem e Tempo de Instâncias:** Alocação dinâmica de contêineres e tempo faturável (*GB-segundo*).

### 📸 Evidência 3: Execução e Orquestração do Workflow (`docs/workflow_success.png`)
* **Ferramenta:** Google Cloud Workflows (`hogwarts-sorting-workflow`).
* **ID da Execução:** `f501eb08-b4ec-4e5e-b5e5-934c4ba4c39b`
* **Métricas da Execução:**
  * **Estado:** `Concluído` (Status verde)
  * **Duração Total:** `0,911 segundo`
  * **Entrada (Input):** `{"nome": "Luana"}`
  * **Saída (Output):** `{"message_id": "21657452411974050", "status": "SUCCESS", "student": "Luana"}`
  * **Grafo do Fluxo:** Etapas `init`, `validate_input` e `publish_to_pubsub` executadas sem falhas.

---

## 2. Relatório de Análise Crítica (Otimizações de Performance e Custo)

Com base no comportamento observado nas métricas e logs do GCP, foram identificadas **3 oportunidades reais de otimização técnica**:

### Otimização 1: Transição do Pub/Sub para Invocação Direta via HTTP (Redução de Latência)
* **Diagnóstico:** A arquitetura atual utiliza o Cloud Workflows para publicar no Pub/Sub, que por sua vez dispara a Cloud Function. A latência de ponta a ponta registrada no Cloud Workflows foi de `0,911s`, enquanto o tempo de execução da função foi de apenas `~20ms`.
* **Proposta:** Para fluxos de seleção síncronos que exigem resposta rápida, conectar o Workflows diretamente à Cloud Function via HTTPS com autenticação IAM.
* **Impacto:** Elimina o overhead do broker de mensageria, reduz a latência da requisição em até 500ms e remove custos operacionais do Pub/Sub.

### Otimização 2: Ajuste Fino de Memória e Concorrência (Redução de Custos)
* **Diagnóstico:** A Cloud Function executa uma lógica leve de manipulação de strings em Python (`house.py`), subutilizando a CPU e RAM alocadas por padrão (512 MB).
* **Proposta:** Reduzir a alocação de memória da função para **128 MB** ou **256 MB** e configurar **Min Instances = 0** para evitar cobrança por ociosidade.
* **Impacto:** Redução de até 40% nos custos de computação (*GB-segundos* e *GHz-segundos*) sem impactar o tempo de resposta.

### Otimização 3: Implementação de Dead-Letter Queue (DLQ) no Pub/Sub (Resiliência)
* **Diagnóstico:** Caso uma mensagem chegue malformatada ou com erro de payload, o Pub/Sub tenta reentregar indeterminadamente, gerando chamadas repetidas e custos desnecessários.
* **Proposta:** Configurar um **Dead-Letter Topic** no Pub/Sub limitando o número máximo de tentativas de entrega (*Max Delivery Attempts*) a 5.
* **Impacto:** Evita *loops* infinitos de execução, protegendo o orçamento da conta GCP e isolando dados inválidos para auditoria no Cloud Logging.

---

## 3. Estrutura do Repositório

```text
.
├── docs/
│   ├── logging_estruturado.png  # Print do Cloud Logging (Log JSON do Chapéu Seletor)
│   ├── metricas_gcp.png         # Print do Cloud Monitoring (Métricas do Cloud Run)
│   └── workflow_success.png     # Print do Cloud Workflows (Execução concluída)
├── workflows/
│   └── workflow.yaml            # Definição do fluxo de trabalho no Cloud Workflows
├── .gitignore                   # Proteção para não expor credenciais
├── README.md                    # Documentação do projeto e relatório crítico
├── house.py                     # Regra de negócio do Chapéu Seletor
├── main.py                      # Código Python instrumentado com logging em JSON
└── requirements.txt             # Dependências do projeto