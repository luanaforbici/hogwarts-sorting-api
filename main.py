import json
import functions_framework
from house import sort_into_house, normalize

@functions_framework.http
def house_sorting(request):
    """
    Função HTTP para Cloud Run functions.
    Aceita o nome enviado de duas formas na URL:
    1. Query Parameter: ?nome=Luana
    2. Direto na URL: /Luana
    """
    # 1. Tenta pegar o nome se a pessoa digitou ?nome=Luana
    request_args = request.args
    name = request_args.get('nome') if request_args else None

    # 2. Se não achou em ?nome=, tenta pegar do final da URL (ex: /Luana)
    if not name:
        path = request.path.strip('/')
        if path:
            name = path

    clean_name = normalize(name) if name else ""

    # 3. Se a pessoa não informou um nome, retorna erro
    if not clean_name:
        response_data = {
            "error": "Por favor, informe um nome. Exemplo: /Luana ou /?nome=Luana"
        }
        return (
            json.dumps(response_data, ensure_ascii=False),
            400,
            {'Content-Type': 'application/json; charset=utf-8'}
        )

    # 4. Executa a lógica de seleção da casa
    house = sort_into_house(clean_name)

    # 5. Monta o resultado JSON
    response_data = {
        "nome": clean_name.capitalize(),
        "casa": house,
        "mensagem": f"O Chapéu Seletor definiu que {clean_name.capitalize()} pertence à {house}!"
    }

    return (
        json.dumps(response_data, ensure_ascii=False),
        200,
        {'Content-Type': 'application/json; charset=utf-8'}
    )