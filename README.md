# 🧙‍♂️ Hogwarts Sorting Hat API

Aplicação **serverless e orientada a eventos**, desenvolvida em Python na Google Cloud Platform (GCP).

O projeto simula o **Chapéu Seletor de Hogwarts**: o nome de um estudante é enviado por meio do **Google Cloud Pub/Sub**, processado por uma **Cloud Function 2ª geração** e analisado pelo **Vertex AI (Gemini 2.5 Flash)**, que determina uma casa e gera uma justificativa.

---

## 🏗️ Arquitetura

```text
┌───────────────────┐
│  Publicação       │
│  da mensagem      │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│   Google Pub/Sub  │
│                   │
│ hogwarts-sorting- │
│ topic             │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Cloud Functions   │
│     2ª geração    │
│                   │
│    Python 3.11    │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│     Vertex AI     │
│                   │
│  Gemini 2.5 Flash │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  Cloud Logging    │
│                   │
│ Resultado/logs    │
└───────────────────┘
```

### Fluxo

1. O nome do estudante é publicado no tópico `hogwarts-sorting-topic`.
2. O Pub/Sub entrega a mensagem para a Cloud Function.
3. A função envia o nome para o Vertex AI.
4. O Gemini 2.5 Flash determina a casa e gera uma justificativa.
5. O resultado é estruturado em JSON e registrado no Cloud Logging.

---

## 🧠 Decisões Técnicas

### Google Cloud Pub/Sub

Foi utilizado para implementar a comunicação **assíncrona e orientada a eventos**.

A escolha permite desacoplar o envio da mensagem do processamento da aplicação, evitando que o produtor precise aguardar diretamente a execução da IA.

### Cloud Functions 2ª geração

A Cloud Function foi escolhida por ser uma solução **serverless**, adequada ao processamento de eventos do Pub/Sub.

A segunda geração utiliza a infraestrutura do Cloud Run, proporcionando escalabilidade automática sem a necessidade de gerenciar servidores.

### Vertex AI + Gemini 2.5 Flash

O **Vertex AI** foi utilizado para integrar a IA generativa à aplicação.

O **Gemini 2.5 Flash** realiza a classificação do estudante e gera a justificativa.

O modelo foi escolhido por ser adequado para tarefas de geração de texto com baixa latência.

A resposta é solicitada no formato JSON, facilitando o processamento pelo backend:

```json
{
  "house": "Grifinória",
  "reason": "A coragem e a determinação demonstradas indicam afinidade com a Grifinória."
}
```

O projeto não utiliza Function Calling, pois a tarefa não necessita de ferramentas ou funções externas para realizar a classificação.

### Cloud Logging

O Cloud Logging foi utilizado para registrar o resultado do processamento e facilitar o acompanhamento das execuções e eventuais erros.

---

## 🛠️ Tecnologias

- **Python 3.11**
- **Google Cloud Pub/Sub**
- **Cloud Functions 2ª geração**
- **Vertex AI**
- **Gemini 2.5 Flash**
- **Cloud Logging**

### Principais bibliotecas

- `google-genai`
- `functions-framework`
- `cloudevents`

---

## 📁 Estrutura do Projeto

```text
hogwarts-sorting-api/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

- `main.py` — código da aplicação e integração com Vertex AI.
- `requirements.txt` — dependências Python.
- `.gitignore` — arquivos que não devem ser enviados ao Git.
- `README.md` — documentação do projeto.

---

## 🧪 Como Testar

1. Acesse o **Google Cloud Console**.
2. Abra **Pub/Sub → Topics**.
3. Selecione `hogwarts-sorting-topic`.
4. Clique em **Publicar mensagem**.
5. Informe o nome de um estudante, por exemplo:

```text
Harry Potter
```

6. Após o processamento, consulte o resultado em **Cloud Logging**.

O log de sucesso apresenta a mensagem:

```text
[CHAPÉU SELETOR - IA] Processamento de seleção concluído.
```

---

## 🔒 Segurança

As credenciais não são armazenadas no código ou no repositório.

- Não são utilizadas API Keys no código.
- Credenciais de Service Account não são versionadas.
- Arquivos `.json` e `.env` são excluídos pelo `.gitignore`.
- O acesso aos serviços da GCP utiliza as permissões da identidade de execução da aplicação.

Exemplo do `.gitignore`:

```text
.env
*.json
__pycache__/
.venv/
venv/
```

---

## 🎯 Objetivo da Etapa

Este projeto demonstra a integração entre:

**Mensageria assíncrona + Serverless + IA Generativa + Observabilidade**

A arquitetura foi definida buscando **desacoplamento, escalabilidade, processamento orientado a eventos e integração segura com serviços de IA da Google Cloud**.