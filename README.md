# 🏰 Hogwarts Sorting API - Event-Driven & IA (Projeto Final)

Esta aplicação implementa um sistema serverless e orientado a eventos (*event-driven*) no Google Cloud Platform (GCP) para a seleção das casas de Hogwarts. A solução utiliza o **Pub/Sub** para ingestão assíncrona, uma **Cloud Function (2ª Geração)** para o processamento e o modelo de IA **Vertex AI (Gemini 1.5 Flash)** para tomar as decisões de seleção com base no perfil do estudante.

---

## 🏗️ Arquitetura do Sistema
[ Ingestão / Pub/Sub ] ──( CloudEvent )──> [ Cloud Function v2 ] ──( API Call )──> [ Vertex AI / Gemini ]
│
└──( Logs JSON )──> [ Cloud Logging ]

### Fluxo de Funcionamento:
1. Um evento com os dados do estudante é publicado no tópico Pub/Sub `hogwarts-sorting-topic`.
2. O Pub/Sub aciona a Cloud Function de 2ª Geração (`hogwarts-sorting-pubsub`) via gatilho de CloudEvent.
3. A função envia o prompt com as informações do aluno para a **Vertex AI (Gemini)**.
4. O Gemini determina a casa correta e gera uma justificativa em formato JSON estruturado.
5. Os dados e métricas são registados no **Google Cloud Logging**.

---

## 🧠 Decisões Arquiteturais & Justificativas Técnicas

* **Arquitetura Event-Driven Assíncrona (Pub/Sub)**:
  * **Justificativa**: Desacopla a ingestão de dados do processamento do modelo de IA. Isso permite absorver picos de tráfego sem sobrecarregar a API do modelo e garante resiliência com retentativas automáticas (*retries*) em caso de falha.
* **Cloud Functions 2ª Geração (engine Cloud Run)**:
  * **Justificativa**: Proporciona um tempo limite (*timeout*) estendido para aguardar a resposta da IA, suporte nativo ao padrão CloudEvents e escalonamento automático até zero (*scale-to-zero*), otimizando custos.
* **Vertex AI (Gemini 1.5 Flash)**:
  * **Justificativa**: Modelo escolhido pelo baixo tempo de resposta (latência reduzida), excelente capacidade de inferência e suporte a saídas estruturadas em JSON.
* **Structured Logging (JSON)**:
  * **Justificativa**: Facilita a observabilidade e a análise das decisões tomadas pela IA diretamente no Google Cloud Logging.

---

## 🚀 Pipeline de CI/CD (GitHub Actions)

A integração e implantação contínuas da aplicação são automatizadas via GitHub Actions. Qualquer alteração enviada para a branch `main` dispara o pipeline de build e deploy automático.

### Fluxo do Pipeline (`.github/workflows/deploy.yml`):

1. **Checkout Code**: Baixa o código-fonte atualizado do repositório.
2. **Set up Python**: Prepara o ambiente com Python 3.11.
3. **Install Dependencies**: Instala os pacotes descritos no `requirements.txt`.
4. **Authenticate to GCP**: Autentica de forma segura no Google Cloud usando a Secret `GCP_SA_KEY`.
5. **Set up Cloud SDK**: Configura as ferramentas da CLI do Google Cloud.
6. **Enable GCP APIs**: Garante a ativação automática das APIs necessárias (`cloudresourcemanager`, `cloudfunctions`, `cloudbuild`, `artifactregistry`, `run`, `aiplatform`).
7. **Deploy Cloud Function**: Executa a implantação da função `hogwarts-sorting-pubsub` (gen2) com gatilho no Pub/Sub.

### Evidências Visuais:

* **Execução do Pipeline**: [Visualizar Log do GitHub Actions](docs/deploy_serverless_function.png)
* **Serviço Ativo no GCP**: [Visualizar Status do Serviço no GCP Console](docs/hogwarts_sorting_pubsub.png)