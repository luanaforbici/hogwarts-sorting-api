import base64
import json
import functions_framework
from house import sort_into_house, normalize

@functions_framework.cloud_event
def house_sorting_pubsub(cloud_event):
    pubsub_data = cloud_event.data.get("message", {}).get("data")
    if not pubsub_data:
        print("[ERRO] Nenhuma mensagem recebida.")
        return

    raw_message = base64.b64decode(pubsub_data).decode("utf-8").strip()
    name = raw_message
    try:
        json_payload = json.loads(raw_message)
        if isinstance(json_payload, dict) and "nome" in json_payload:
            name = json_payload["nome"]
    except json.JSONDecodeError:
        pass

    clean_name = normalize(name)
    if not clean_name:
        print("[AVISO] Nome inválido.")
        return

    house = sort_into_house(clean_name)
    print(f"[CHAPÉU SELETOR] Processado com sucesso! Nome: {clean_name.capitalize()} | Casa: {house}")
