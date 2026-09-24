# 🧙‍♂️ Hogwarts Sorting Hat API (Serverless + GenAI)

Uma API Serverless orientada a eventos criada no Google Cloud Platform (GCP) que simula o **Chapéu Seletor de Hogwarts**. A aplicação processa o nome de um estudante enviado via Pub/Sub e utiliza a **Vertex AI (Gemini 2.5 Flash)** para determinar a casa de Hogwarts e gerar uma justificativa única, criativa e persuasiva.

---

## 🏗️ Arquitetura do Projeto
[ Cliente / Mensagem ]
│
▼
┌──────────────┐
│ GCP Pub/Sub  │  (Tópico: hogwarts-sorting-topic)
└───────┬──────┘
│ (Eventarc / Cloud Event)
▼
┌──────────────────────┐
│ GCP Cloud Functions  │  (Python 3.11 / Cloud Run Backend)
│    (2ª Geração)      │
└───────┬──────────────┘
│
├───► [ Vertex AI / Gemini 2.5 Flash ] (Gera Seleção + Justificativa em JSON)
│
▼
┌──────────────────────┐
│ Cloud Logging (Logs) │  (Saída Estruturada)
└──────────────────────┘

1. **Pub/Sub**: Recebe a mensagem contendo o nome do estudante codificado em Base64.
2. **Eventarc & Cloud Functions (v2)**: Processa o evento de forma assíncrona usando o `functions-framework` com subscrição otimizada para evitar duplicidades de execução.
3. **Vertex AI SDK (`google-genai`)**: Consome o modelo `gemini-2.5-flash` configurado com `temperature: 0.9` e `response_mime_type: "application/json"` para garantir respostas criativas, ultrarrápidas e estritamente formatadas.
4. **Cloud Logging**: Armazena a resposta em formato JSON estruturado com a casa atribuída (*Grifinória, Sonserina, Corvinal ou Lufa-Lufa*) e a justificativa em Português do Brasil.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.11
- **Plataforma Cloud**: Google Cloud Platform (GCP)
- **Serviços Serverless**: Cloud Functions (2ª Geração) / Cloud Run / Eventarc
- **Mensageria**: Cloud Pub/Sub
- **IA Generativa**: Vertex AI API (`gemini-2.5-flash`)
- **SDK Oficial**: `google-genai`

---

🚀 Como Testar a Aplicação
Via Cloud Console (Interface Gráfica)
Acesse o Pub/Sub > Tópicos > selecione hogwarts-sorting-topic.

Vá à aba Mensagens e clique em Publicar Mensagem.

No corpo da mensagem, insira o nome de um estudante (ex: Luana Vitorino) e clique em Publicar.