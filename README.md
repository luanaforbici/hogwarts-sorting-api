## 5. Checkpoint 5 - Pipeline de CI/CD (GitHub Actions)

A integração e implantação contínuas da aplicação foram automatizadas via **GitHub Actions**. Qualquer alteração enviada para a branch `main` dispara o pipeline de build e deploy automático.

### Fluxo do Pipeline (`.github/workflows/deploy.yml`):
1. **Checkout Code:** Baixa o código fonte atualizado.
2. **Set up Python:** Prepara o ambiente em Python 3.11.
3. **Install Dependencies:** Valida as dependências descritas no `requirements.txt`.
4. **Authenticate to GCP:** Autentica com o Google Cloud de forma segura utilizando a Secret `GCP_SA_KEY`.
5. **Deploy Cloud Function:** Realiza o deploy da função `hogwarts-sorting-pubsub` com gatilho Pub/Sub.

### Evidência Visual:
* O print da execução com sucesso do job no GitHub Actions está salvo em [`docs/deploy_success.png`](./docs/deploy_success.png).