import json
import base64
import logging
import functions_framework
from house import get_house

# Configuração de logging estruturado no formato JSON para o Google Cloud Logging
logging.basicConfig(level=logging.INFO)

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
        # Extração e decodificação do payload do Pub/Sub
        pubsub_data = cloud_event.data.get("message", {}).get("data", "")
        if not pubsub_data:
            log_structured("WARNING", "Mensagem recebida sem dados válidos no payload.")
            return

        student_name = base64.b64decode(pubsub_data).decode("utf-8").strip()

        if not student_name:
            log_structured("WARNING", "Nome do estudante está vazio após decodificação.")
            return

        # Lógica de negócio: Seleção da casa de Hogwarts
        selected_house = get_house(student_name)

        # Log estruturado de Sucesso
        log_structured(
            severity="INFO",
            message=f"[CHAPÉU SELETOR] Seleção concluída com sucesso.",
            payload={
                "student_name": student_name,
                "selected_house": selected_house,
                "status": "SUCCESS"
            }
        )

    except Exception as e:
        # Log estruturado de Erro
        log_structured(
            severity="ERROR",
            message=f"Falha ao processar mensagem no Chapéu Seletor: {str(e)}",
            payload={"error_detail": str(e), "status": "ERROR"}
        )
        raise e