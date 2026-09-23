import json
import base64
import logging
import functions_framework
import vertexai
from vertexai.generative_models import GenerativeModel

logging.basicConfig(level=logging.INFO)

# Inicialização da Vertex AI na região us-central1
vertexai.init(project="hogwarts-sorting-api", location="us-central1")
model = GenerativeModel("gemini-1.5-flash")

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
        # Extração e decodificação da mensagem do Pub/Sub
        pubsub_data = cloud_event.data.get("message", {}).get("data", "")
        if not pubsub_data:
            log_structured("WARNING", "Mensagem recebida sem payload válido.")
            return

        student_name = base64.b64decode(pubsub_data).decode("utf-8").strip()

        if not student_name:
            log_structured("WARNING", "Nome do estudante está vazio.")
            return

        # Chamada à Vertex AI (Gemini)
        prompt = (
            f"Atue como o Chapéu Seletor de Hogwarts. Analise o nome '{student_name}' "
            f"e selecione uma das quatro casas (Gryffindor, Slytherin, Ravenclaw, Hufflepuff). "
            f"Responda estritamente no formato JSON com as chaves 'house' e 'reason'."
        )
        response = model.generate_content(prompt)

        # Log estruturado de sucesso com a resposta do Gemini
        log_structured(
            severity="INFO",
            message="[CHAPÉU SELETOR - IA] Seleção de casa realizada com sucesso via Vertex AI.",
            payload={
                "student_name": student_name,
                "ia_response": response.text,
                "status": "SUCCESS"
            }
        )

    except Exception as e:
        log_structured(
            severity="ERROR",
            message=f"Falha ao processar mensagem no Chapéu Seletor: {str(e)}",
            payload={"error_detail": str(e), "status": "ERROR"}
        )
        raise e