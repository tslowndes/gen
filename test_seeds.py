import numpy as np
working_seeds = []
for i in range(0,100):
    np.random.seed(i)
    start_locs = [(np.random.randint(475, 525), np.random.randint(475, 525)) for j in range(30)]
    if len(set(start_locs)) == len(start_locs):
        working_seeds.append(i)

print(working_seeds[:50])

