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

Justificativa das Escolhas Arquiteturais
Arquitetura Event-Driven (GCP Pub/Sub + Eventarc)

Por quê: Garante o desacoplamento entre os produtores de eventos e o processamento backend. O Pub/Sub lida com picos de tráfego (resiliência), enquanto o Eventarc roteia a mensagem via gatilhos nativos diretamente para o ambiente Serverless.

GCP Cloud Functions (2ª Geração / Cloud Run)

Por quê: Modelo de bilhetagem scale-to-zero (custo zero quando ocioso). A 2ª geração roda sobre a infraestrutura do Cloud Run, permitindo maior tempo de execução (timeout) e melhor concorrência para chamadas à API de IA.

Vertex AI com Modelo gemini-2.5-flash

Por quê: O modelo Flash oferece baixíssima latência e excelente custo-benefício para tarefas de geração de texto criativo.

Structured Outputs (response_mime_type: "application/json"): Garante que o modelo retorne estritamente um schema JSON pré-definido, evitando respostas truncadas e elimina falhas de parsing no backend.

Observabilidade e Logs Estruturados (Cloud Logging)

Por quê: A aplicação emite logs formatados em JSON (severity, message, payload), permitindo auditoria simples, rastreabilidade dos retornos da IA e criação de alertas/métricas na nuvem.

🛠️ Tecnologias e SDKs
Linguagem: Python 3.11

Plataforma Nuvem: Google Cloud Platform (GCP)

Serviços Utilizados: Cloud Pub/Sub, Cloud Functions v2, Eventarc, Vertex AI, Cloud Logging

Bibliotecas Python principais: google-genai, functions-framework, cloudevents

🔒 Segurança e Boas Práticas
Conforme as diretrizes de segurança adotadas no projeto:

Autenticação Nativa (IAM): Nenhuma chave de API (API Keys) ou Service Account Key em formato .json foi versionada no repositório.

Service Accounts Dedicadas: A aplicação utiliza a Service Account nativa do ambiente Google Cloud, gerenciada com permissões mínimas no IAM (como o papel de executor da Vertex AI).

Gitignore Configurado: Todos os arquivos de ambiente (.env), dados locais de desenvolvimento e credenciais temporárias foram estritamente excluídos do controle de versão.

📁 Estrutura do Repositório
.
├── main.py              # Código principal da Cloud Function e integração com Vertex AI
├── requirements.txt     # Dependências do projeto Python
├── .gitignore           # Exclusão de credenciais e arquivos sensíveis
└── README.md            # Documentação técnica da arquitetura

💻 Código da Aplicação (main.py)
import json
import base64
import logging
import functions_framework
from google import genai

logging.basicConfig(level=logging.INFO)

# Inicializa o cliente GenAI apontando para Vertex AI
client = genai.Client(
    vertexai=True,
    project="hogwarts-sorting-api",
    location="us-central1"
)


def log_structured(severity: str, message: str, payload: dict = None):
    log_entry = {
        "severity": severity,
        "message": message,
        "service": "hogwarts-sorting-api",
        "payload": payload or {}
    }
    print(json.dumps(log_entry))


@functions_framework.cloud_event
def subscribe(cloud_event):
    try:
        # 1. Extração do Payload do Pub/Sub
        pubsub_data = cloud_event.data.get("message", {}).get("data", "")
        if not pubsub_data:
            log_structured("WARNING", "Mensagem recebida sem dados no payload.")
            return

        student_name = base64.b64decode(pubsub_data).decode("utf-8").strip()
        if not student_name:
            log_structured("WARNING", "Nome do estudante está vazio.")
            return

        # 2. Chamada da Vertex AI Gemini
        try:
            prompt = (
                f"Atue como o Chapéu Seletor de Hogwarts. Analise o nome '{student_name}' "
                "e selecione uma das quatro casas (Grifinória, Sonserina, Corvinal, Lufa-Lufa). "
                "Seja extremamente criativo, único e persuasivo no seu discurso. "
                "Responda OBRIGATORIAMENTE em português do Brasil. "
                "Retorne um JSON contendo as chaves 'house' e 'reason'."
            )

            # Configuração otimizada para ser ultrarrápida e desativar o AFC automático
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "temperature": 0.8,
                    "response_mime_type": "application/json",
                    "tools": []  # Desativa o Automatic Function Calling (AFC) que estava atrasando
                }
            )
            ia_output = response.text

        except Exception as ia_err:
            log_structured("ERROR", f"Falha na chamada da Vertex AI: {str(ia_err)}")
            ia_output = json.dumps({
                "house": "Grifinória",
                "reason": f"Seleção de contingência devido a erro na IA: {str(ia_err)}"
            })

        # 3. Log estruturado do resultado
        log_structured(
            severity="INFO",
            message="[CHAPÉU SELETOR - IA] Processamento de seleção concluído.",
            payload={
                "student_name": student_name,
                "ia_response": ia_output,
                "status": "SUCCESS"
            }
        )

    except Exception as e:
        log_structured(
            severity="ERROR",
            message=f"Falha crítica na função: {str(e)}",
            payload={"error_detail": str(e)}
        )

🧪 Como Testar a Aplicação
Os testes da aplicação foram realizados diretamente pela interface gráfica do Google Cloud Console:

Acesse o console do Cloud Pub/Sub e selecione o tópico hogwarts-sorting-topic.

Vá até a aba Mensagens e clique em Publicar Mensagem.

No campo do corpo da mensagem, informe o nome do estudante (ex: Harry Potter) e clique em Publicar.

O evento é processado pela Cloud Function v2 e o resultado fica disponível no Cloud Logging.

📑 Exemplo de Saída nos Logs (Cloud Logging)
Exemplo real extraído dos logs da aplicação após o processamento da mensagem de teste:

jsonPayload: {
message: "[CHAPÉU SELETOR - IA] Processamento de seleção concluído."
payload: {
ia_response: "{
  "house": "Grifinória",
  "reason": "Ah, Potter... um nome que ecoa através dos salões de Hogwarts com a força de um trovão. Sinto sua mente, um caldeirão borbulhante de emoções e um potencial colossal. Vejo o peso de um legado imenso, a sombra de um destino que você carrega com uma resiliência notável. Muitos pensariam na astúcia, na sede de provar-se, na capacidade de sobrevivência que roça o ardiloso... sim, há um toque ali, uma conexão profunda com um poder que poderia ter levado a outro caminho. Poderia florescer onde a ambição e a determinação são a moeda mais forte, e a sua linhagem, por mais que negue, tem raízes profundas ali. A tentação é forte, oh, sim, muito forte para a Sonserina. Mas não é só isso. Sinto a lealdade inabalável aos seus amigos, um coração que busca a justiça e a verdade, mesmo que isso signifique dor e sacrifício. E a inteligência, a sagacidade para desvendar segredos e a curiosidade para entender o mundo, não são desprezíveis. Contudo, no fundo do seu ser, mais profundo que qualquer astúcia ou desejo de conhecimento, reside uma coragem que arde como um braseiro inextinguível. Não é uma coragem temerária, mas a bravura de enfrentar o que é certo, mesmo quando o medo é paralisante. É a audácia de se levantar contra a escuridão, a tenacidade de proteger aqueles que ama, a vontade inquebrantável de fazer o bem. É a sua escolha, Potter, que o define, e essa escolha aponta para um único lugar. Onde os corações valentes encontram seu lar, onde a ousadia é celebrada e a cavalaria é honrada. Não há dúvida, não há sombra de incerteza. GRYFFINDOR!"
}"
status: "SUCCESS"
student_name: "Harry Potter"