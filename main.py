import json
import base64
import logging
import functions_framework
import vertexai
from vertexai.generative_models import GenerativeModel

logging.basicConfig(level=logging.INFO)

# Inicializa Vertex AI (ajuste para o seu project_id se necessário)
vertexai.init(project="hogwarts-sorting-api", location="us-central1")
model = GenerativeModel("gemini-1.5-flash")

def log_structured(severity: str, message: str, payload: dict = None):
    print(json.dumps({
        "severity": severity,
        "message": message,
        "service": "hogwarts-sorting-api",
        "payload": payload or {}
    }))

@functions_framework.cloud_event
def subscribe(cloud_event):
    try:
        pubsub_data = cloud_event.data.get("message", {}).get("data", "")
        if not pubsub_data:
            return

        student_name = base64.b64decode(pubsub_data).decode("utf-8").strip()

        # Chamada à Vertex AI (Gemini)
        prompt = f"Atue como o Chapéu Seletor de Hogwarts. Analise o nome '{student_name}' e escolha uma das quatro casas (Gryffindor, Slytherin, Ravenclaw, Hufflepuff). Responda estritamente em JSON no formato: {{\"house\": \"NOME_DA_CASA\", \"reason\": \"JUSTIFICATIVA_CURTA\"}}"
        response = model.generate_content(prompt)
        
        log_structured("INFO", "[CHAPÉU SELETOR - IA] Seleção realizada via Vertex AI", {
            "student_name": student_name,
            "ia_response": response.text
        })

    except Exception as e:
        log_structured("ERROR", f"Falha no processamento: {str(e)}")
        raise e