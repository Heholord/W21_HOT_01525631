import math
interpretations = []

for x1 in [True, False]:
    for x2 in [True, False]:
        for x3 in [True, False]:
            for x4 in [True, False]:
                interpretations.append({
                    'x1': x1,
                    'x2': x2,
                    'x3': x3,
                    'x4': x4                    
                })

# print(interpretations)

def v(bool):
    if bool:
        return '1'
    else: 
        return '0'

def count_sat(clauses):
    counter = 0
    for c in clauses:
        if c: counter +=1
    return counter

def evaluate(clauses):
    ev = True
    for c in clauses:
        ev = ev and c
    return ev


def get_clauses(i):
    return [
        i['x1'] or i['x2'],
        i['x1'] or i['x3'],
        i['x1'] or not i['x3'],
        not i['x1'] or i['x4'],
        not i['x2'] or not i['x3'],
        i['x2'] or not i['x4'],
        not i['x3'] or not i['x4'],
    ]

def neigborhood(interpretation):
    neig = []
    for key in interpretation.keys():
        # new_interpretation = {
        #             'x1': interpretation['x1'],
        #             'x2': interpretation['x2'],
        #             'x3': interpretation['x3'],
        #             'x4': interpretation['x4']                    
        #         }
        new_interpretation = interpretation.copy()
        new_interpretation[key] = not interpretation[key]
        neig.append(new_interpretation)
    
    # print(f"interp {interpretation} created neighborhood {neig}")
    return neig



def is_local_opt(interpretation):
    local_opt = count_sat(get_clauses(interpretation))
    neighborh = neigborhood(interpretation)
    for neighbor in neighborh:
        pot_local_opt = count_sat(get_clauses(neighbor))
        # print(pot_local_opt)
        if pot_local_opt > local_opt:
            # print("sss")
            return False
    return True

print(f"x1 x2 x3 x4| (x1 v x2) ∧ (x1 v x3) ∧ (x1 v ~x3) ∧ (~x1 v x4) ∧ (~x2 v ~x3) ∧ (x2 v ~x4) ∧ (~x3 v ~x4) | nr of sat clauses | global | local")
print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------")
for i in interpretations:
    clauses = get_clauses(i)
    str_for_clauses = "            ".join([v(c) for c in clauses])
    print(f"{v(i['x1'])}  {v(i['x2'])}  {v(i['x3'])}  {v(i['x4'])} |     {str_for_clauses}      |         {count_sat(clauses)}         |    {v(evaluate(clauses))}   |   {v(is_local_opt(i))}")