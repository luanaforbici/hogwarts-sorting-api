import random

def get_house(student_name: str) -> str:
    houses = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]
    # Retorna uma casa baseada em hash determinístico ou aleatório
    return houses[len(student_name) % 4]