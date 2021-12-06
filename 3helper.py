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

def neigborhood(interpretation, search_order = None):
    if not search_order:
        search_order = interpretation.keys()
    neig = []
    for key in search_order:
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
            return False
    return True


def local_search(interpretation, search_order):
    best_interpretation = interpretation
    best_val = count_sat(get_clauses(interpretation))
    nh = neigborhood(interpretation, search_order=search_order)
    for neighbor in nh:
        objective_value = count_sat(get_clauses(neighbor))
        if objective_value > best_val:
            return local_search(neighbor, search_order)
    return best_interpretation


print(f"x1 x2 x3 x4| (x1 v x2) ∧ (x1 v x3) ∧ (x1 v ~x3) ∧ (~x1 v x4) ∧ (~x2 v ~x3) ∧ (x2 v ~x4) ∧ (~x3 v ~x4) | nr of sat clauses | global | local")
print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------")
for i in interpretations:
    clauses = get_clauses(i)
    str_for_clauses = "            ".join([v(c) for c in clauses])
    print(f"{v(i['x1'])}  {v(i['x2'])}  {v(i['x3'])}  {v(i['x4'])} |     {str_for_clauses}      |         {count_sat(clauses)}         |    {v(evaluate(clauses))}   |   {v(is_local_opt(i))}")


def get_as_string(i):
    return f"{v(i['x1'])}{v(i['x2'])}{v(i['x3'])}{v(i['x4'])}"

search_order1  = ['x1', 'x2', 'x3', 'x4']
search_order2  = ['x4', 'x3', 'x2', 'x1']
for search_order in [search_order1, search_order2]:
    count_local_optima = dict()
    for i in interpretations:
        loc_opt = local_search(i, search_order)
        str_local_opt = get_as_string(loc_opt)
        print("interp", get_as_string(i), "leads to", str_local_opt)
        count_local_optima[str_local_opt] = 0 if not (str_local_opt in count_local_optima) else (count_local_optima[str_local_opt] +1)
    print("for search_order", search_order, ":",count_local_optima)

def calc_distance_to_global_opt(i):
    global_opt = {
                    'x1': True,
                    'x2': True,
                    'x3': False,
                    'x4': True                
                }
    hamming_distance = 0
    for key in global_opt.keys():
        if global_opt[key] != i[key]: hamming_distance += 1
    return hamming_distance

correlation = []
for i in interpretations:
    print("distance of", get_as_string(i), "to global opt", calc_distance_to_global_opt(i), "with a objective value of", count_sat(get_clauses(i))) 
    correlation.append((count_sat(get_clauses(i)), calc_distance_to_global_opt(i)))

import numpy as np
objective= np.array([i[0] for i in correlation])
distances= np.array([i[1] for i in correlation])
corr = np.corrcoef(objective, distances)
print(corr)

import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

dataFrame = pd.DataFrame({"objective value":objective, "distances":distances})
# dataFrame.plot("objective value", "distances", kind='scatter')
sns.regplot(data=dataFrame, x="distances", y="objective value")
plt.show()

