import random
import uuid
from pprint import pprint

class Meal:
    def __init__(self, slots):
        self.id = str(uuid.uuid4())
        self.slots : list = random.choices([False, True], k=slots)

    def __repr__(self) -> str:
        return f'Meal {self.id}'

class Constraint:
    def __init__(self, period, max_repetitions):
        self.period = period
        self.max_repetitions = max_repetitions

    def __repr__(self) -> str:
        return f'[{self.period}, {self.max_repetitions}]'

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

def check_permutation_constraint(permutation : list, constraint : Constraint):
    stop_i = (len(permutation) - constraint.period) + 1
    for i in range(stop_i):
        upper = i + constraint.period
        cur_slice = permutation[i:upper]
        id_counts = dict()
        for meal in cur_slice:
            if meal.id not in id_counts:
                id_counts[meal.id] = 1
            else:
                id_counts[meal.id] += 1
            
            if id_counts[meal.id] > constraint.max_repetitions:
                return False

    # note that returning True is actually pretty tough here
    return True

def filter_permutations(permutations : list, hard_constraints : list = []):
    final_permutations = []
    for p in permutations:
        include_permutation = True
        for c in hard_constraints:    
            if not check_permutation_constraint(p,c):
                include_permutation = False
                break
        if include_permutation:
            final_permutations.append(p)
    return final_permutations

def rank_permutations(permutations : list, soft_constraints : list = []):
    pass

menu = generate_menu(5)
for meal in menu:
    print('-' * 20)
    print(meal)
    pprint(meal.slots)
permutations = generate_permutations(menu)
print(f'Permutation number: {len(permutations)}')

hard_constraints = [
    Constraint(2,1), # no two meals in a row can be the same
    Constraint(4,2) # no more than 2 identical meals in a single day
]

valid_permutations = filter_permutations(permutations, hard_constraints)
print(f"Valid permutations: {len(valid_permutations)}")
pprint(valid_permutations)