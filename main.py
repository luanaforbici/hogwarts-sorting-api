import json
import base64
import logging
import functions_framework

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
            from google import genai

            client = genai.Client(vertexai=True, project="hogwarts-sorting-api", location="us-central1")

            prompt = (
                f"Atue como o Chapéu Seletor de Hogwarts. Analise o nome '{student_name}' "
                f"e selecione uma das quatro casas (Gryffindor, Slytherin, Ravenclaw, Hufflepuff). "
                f"Responda estritamente em formato JSON com as chaves 'house' e 'reason'."
            )

            response = client.models.generate_content(
                model="gemini-1.5-flash-001",
                contents=prompt,
            )
            ia_output = response.text

        except Exception as ia_err:
            log_structured("ERROR", f"Falha na chamada da Vertex AI: {str(ia_err)}")
            ia_output = json.dumps({
                "house": "Gryffindor",
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