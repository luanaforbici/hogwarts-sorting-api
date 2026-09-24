# 🧙‍♂️ Hogwarts Sorting Hat API (Serverless + GenAI)

API Serverless orientada a eventos implantada na Google Cloud Platform (GCP) que simula o **Chapéu Seletor de Hogwarts**. A aplicação processa requisições de estudantes via mensageria assíncrona e utiliza **IA Generativa (Vertex AI)** para classificar o aluno em uma casa e gerar uma justificativa única.

---

## 🏛️ Arquitetura e Decisões Técnicas

### Fluxo de Dados

```text
[ Cliente / Evento ] 
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
         ├───► [ Vertex AI / Gemini 2.5 Flash ] (Seleção + Justificativa em JSON)
         │
         ▼
 ┌──────────────────────┐
 │ Cloud Logging (Logs) │  (Log Estruturado em JSON)
 └──────────────────────┘

 ---

 ### Justificativa das Escolhas Arquiteturais

* **Arquitetura Event-Driven (GCP Pub/Sub + Eventarc)**
  * **Por quê:** Garante o desacoplamento total entre os produtores de eventos e o backend de processamento. O Pub/Sub absorve picos de tráfego de forma resiliente e o Eventarc entrega os eventos de maneira automática para a Cloud Function.

* **GCP Cloud Functions (2ª Geração / Cloud Run)**
  * **Por quê:** Adota o modelo *scale-to-zero* (custo zero quando ocioso). A 2ª geração roda sobre a infraestrutura do Cloud Run, proporcionando maior tempo limite de execução (*timeout*) e melhor capacidade de concorrência para chamadas à API de IA.

* **Vertex AI com Modelo `gemini-2.5-flash`**
  * **Por quê:** O modelo Flash foi escolhido por sua baixíssima latência e excelente custo-benefício para geração de texto criativo.
  * **Otimização do Tempo de Resposta (`tools: []`):** O parâmetro `tools: []` desativa expressamente o *Automatic Function Calling* (AFC) da SDK, evitando processamentos desnecessários e garantindo a resposta mais rápida possível.
  * **Structured Outputs (`response_mime_type: "application/json"`):** Garante que o modelo retorne estritamente um schema JSON válido, eliminando falhas de parsing no backend.

* **Observabilidade e Logs Estruturados (Cloud Logging)**
  * **Por quê:** A aplicação emite logs formatados em JSON (`severity`, `message`, `payload`), facilitando a auditoria, a rastreabilidade dos retornos da IA e a criação de alertas ou métricas no GCP.

--- 

## 🛠️ Tecnologias e SDKs

* **Linguagem:** Python 3.11
* **Plataforma Nuvem:** Google Cloud Platform (GCP)
* **Serviços Utilizados:** Cloud Pub/Sub, Cloud Functions v2, Eventarc, Vertex AI, Cloud Logging
* **Bibliotecas Python principais:** `google-genai`, `functions-framework`, `cloudevents`

---

## 🔒 Segurança e Boas Práticas

Conforme as diretrizes de segurança adotadas no projeto:

* **Autenticação Nativa (IAM):** Nenhuma chave de API (*API Keys*) ou *Service Account Key* em formato `.json` foi versionada no repositório.
* **Service Accounts Dedicadas:** A aplicação utiliza a Service Account nativa do ambiente Google Cloud, gerenciada com permissões mínimas no IAM (como o papel de executor da Vertex AI).
* **Gitignore Configurado:** Todos os arquivos de ambiente (`.env`), dados locais de desenvolvimento e credenciais temporárias foram estritamente excluídos do controle de versão.

📁 Estrutura do Repositório
.
├── main.py              # Código principal da Cloud Function e integração com Vertex AI
├── requirements.txt     # Dependências do projeto Python
├── .gitignore           # Exclusão de credenciais e arquivos sensíveis
└── README.md            # Documentação técnica da arquitetura

---

## 🧪 Como Testar a Aplicação

Os testes foram realizados diretamente via interface gráfica do **Google Cloud Console**:

1. Acesse o console do **Cloud Pub/Sub** e selecione o tópico `hogwarts-sorting-topic`.
2. Na aba **Mensagens**, clique em **Publicar mensagem**.
3. No corpo da mensagem, envie o nome do estudante (ex: `Harry Potter`).
4. O evento será processado de forma assíncrona e o resultado registrado no **Cloud Logging**.

<details>
<summary>🔍 <b>Clique aqui para ver o log real extraído do Cloud Logging</b></summary>

```json
{
  "insertId": "6ab5194d00003d495e340c2b",
  "jsonPayload": {
    "message": "[CHAPÉU SELETOR - IA] Processamento de seleção concluído.",
    "service": "hogwarts-sorting-api",
    "payload": {
      "student_name": "Harry Potter",
      "status": "SUCCESS",
      "ia_response": "{\n  \"house\": \"Grifinória\",\n  \"reason\": \"Ah, Potter... um nome que ecoa através dos salões de Hogwarts com a força de um trovão. Sinto sua mente, um caldeirão borbulhante de emoções e um potencial colossal. Vejo o peso de um legado imenso, a sombra de um destino que você carrega com uma resiliência notável. Muitos pensariam na astúcia, na sede de provar-se, na capacidade de sobrevivência que roça o ardiloso... sim, há um toque ali, uma conexão profunda com um poder que poderia ter levado a outro caminho. Poderia florescer onde a ambição e a determinação são a moeda mais forte, e a sua linhagem, por mais que negue, tem raízes profundas ali. A tentação é forte, oh, sim, muito forte para a Sonserina. Mas não é só isso. Sinto a lealdade inabalável aos seus amigos, um coração que busca a justiça e a verdade, mesmo que isso signifique dor e sacrifício. E a inteligência, a sagacidade para desvendar segredos e a curiosidade para entender o mundo, não são desprezíveis. Contudo, no fundo do seu ser, mais profundo que qualquer astúcia ou desejo de conhecimento, reside uma coragem que arde como um braseiro inextinguível. Não é uma coragem temerária, mas a bravura de enfrentar o que é certo, mesmo quando o medo é paralisante. É a audácia de se levantar contra a escuridão, a tenacidade de proteger aqueles que ama, a vontade inquebrantável de fazer o bem. É a sua escolha, Potter, que o define, e essa escolha aponta para um único lugar. Onde os corações valentes encontram seu lar, onde a ousadia é celebrada e a cavalaria é honrada. Não há dúvida, não há sombra de incerteza. GRYFFINDOR!\"\n}"
    }
  }
}