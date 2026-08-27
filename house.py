import hashlib

def normalize(name: str) -> str:
    return name.strip().lower()

def sort_into_house(name: str) -> str:
    houses = ["Grifinória", "Sonserina", "Corvinal", "Lufa-Lufa"]
    hash_value = int(hashlib.md5(name.encode('utf-8')).hexdigest(), 16)
    return houses[hash_value % 4]