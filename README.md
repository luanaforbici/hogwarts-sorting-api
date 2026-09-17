## 5. Checkpoint 5 - Pipeline de CI/CD (GitHub Actions)

A integração e implantação contínuas da aplicação foram automatizadas via GitHub Actions. Qualquer alteração enviada para a branch `main` dispara o pipeline de build e deploy automático.

### Fluxo do Pipeline (`.github/workflows/deploy.yml`):

1. **Checkout Code**: Baixa o código-fonte atualizado do repositório.
2. **Set up Python**: Prepara o ambiente com Python 3.11.
3. **Install Dependencies**: Instala os pacotes descritos no `requirements.txt`.
4. **Authenticate to GCP**: Autentica de forma segura no Google Cloud usando a Secret `GCP_SA_KEY`.
5. **Set up Cloud SDK**: Configura as ferramentas de CLI do Google Cloud.
6. **Enable GCP APIs**: Garante a ativação automática das APIs necessárias (`cloudresourcemanager`, `cloudfunctions`, `cloudbuild`, `artifactregistry`, `run`).
7. **Deploy Cloud Function**: Executa a implantação da função `hogwarts-sorting-pubsub` (gen2) com gatilho no Pub/Sub.

### Evidências Visuais:

* **Execução do Pipeline**: [Visualizar Log do GitHub Actions](docs/deploy_serverless_function.png)
* **Serviço Ativo no GCP**: [Visualizar Status do Serviço no GCP Console](docs/hogwarts_sorting_pubsub.png)