import hashlib

# Lista com as 4 casas de Hogwarts
HOUSES = ["Grifinória", "Sonserina", "Corvinal", "Lufa-Lufa"]

def normalize(name: str) -> str:
    """Remove espaços em branco nas pontas e deixa o texto limpo."""
    return name.strip() if name else ""

def sort_into_house(name: str) -> str:
    """
    Gera uma casa de Hogwarts determinística.
    O mesmo nome digitado sempre retornará a mesma casa.
    """
    clean_name = normalize(name).lower()
    if not clean_name:
        return ""
    
    # Gera um hash único a partir do nome
    hash_object = hashlib.md5(clean_name.encode())
    hash_digest = int(hash_object.hexdigest(), 16)
    
    # Usa o resto da divisão para escolher o índice da casa (0, 1, 2 ou 3)
    house_index = hash_digest % len(HOUSES)
    return HOUSES[house_index]