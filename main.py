import random
import uuid
from pprint import pprint

class Meal:
    def __init__(self, slots):
        self.id = str(uuid.uuid4())
        self.slots : list = random.choices([False, True], k=slots)

    def __repr__(self) -> str:
        return f'Meal {self.id}'

def generate_menu(meal_choices : int, meal_slots : int = 4):
    return [ Meal(4) for m in range(meal_choices) ]

def get_possibilities(menu : list, slot_i):
    return list(filter(lambda m : m.slots[slot_i], menu))

def generate_permutations(menu, slot_i = 0):

    possibilities = get_possibilities(menu, slot_i)
    if slot_i == len(menu[0].slots) - 1:
        return [ [p] for p in possibilities]

    current_permutations = generate_permutations(menu, slot_i + 1)

    permutations = []

    for p in possibilities:
        for c_p in current_permutations:
            next_permutation = [p]
            next_permutation.extend(c_p)
            permutations.append(next_permutation)
    
    return permutations

menu = generate_menu(5)
for meal in menu:
    print('-' * 20)
    print(meal)
    pprint(meal.slots)
permutations = generate_permutations(menu)
print(len(permutations))
pprint(permutations)