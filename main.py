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
    return [ Meal(meal_slots) for m in range(meal_choices) ]

def get_possibilities(menu : list, slot_i):
    return list(filter(lambda m : m.slots[slot_i], menu))

def generate_permutations(menu, slot_i = 0, total_slots = 4):

    possibilities = get_possibilities(menu, slot_i % len(menu[0].slots))
    if slot_i == total_slots - 1: # menu slots shouldn't be controlling this; it should be independent
        return [ [p] for p in possibilities]

    current_permutations = generate_permutations(menu, slot_i + 1, total_slots)

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

def score_permutations(permutations : list, soft_constraints : list = []):
    failures = [ 0 for i in range(len(permutations)) ]
    for i, p in enumerate(permutations):
        for c in soft_constraints:
            if not check_permutation_constraint(p, c):
                failures[i] += 1
    return failures

def get_all_winners(ranked : list):
    if len(ranked) == 0:
        return []
    first_place = ranked[0][0]
    i = 0
    while i < len(ranked) and ranked[i][0] == first_place:
        i += 1
    return ranked[:i]

menu = generate_menu(5)
for meal in menu:
    print('-' * 20)
    print(meal)
    pprint(meal.slots)
permutations = generate_permutations(menu, total_slots=8)

if len(permutations) > 0:
    pprint(permutations[0])

print(f'Permutation number: {len(permutations)}')

hard_constraints = [
    Constraint(2,1), # no two meals in a row can be the same
    Constraint(4,2) # no more than 2 identical meals in a single day
]

soft_constraints = [
    Constraint(4,1) # no more than one of the same meal in a single day
]

# check_permutation_constraint(permutations[0], hard_constraints[0])

valid_permutations = filter_permutations(permutations, hard_constraints)
print(f"Valid permutations: {len(valid_permutations)}")
scores = score_permutations(valid_permutations, soft_constraints)
# print(scores)
zipped = [(s, p) for s, p in zip(scores, valid_permutations)]
# # pprint(zipped)
ranked = sorted(zipped, key=lambda pair : pair[0])
# pprint(ranked)
winners = get_all_winners(ranked)
print(f"Best permutations: {len(winners)}")
if len(winners) < 10:
    pprint(winners)

# ranking = [(s, p) for s, p in sorted(zip(scores, valid_permutations), key=lambda pair : pair[0])]
# ranked_permutations = [p for _, p in sorted(zip(scores, valid_permutations), key=lambda pair : pair[0])]
# pprint(ranking)
