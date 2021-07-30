from random import uniform
days_to_flower = 91
total_branches = 74

rate_of_bifurication = 0
good_enough = False
cycles = 10

while not good_enough:
    cumulative_days = 0
    for i in range(cycles):
        day = 0
        branches = 1
        while branches < total_branches:
            for i in range(branches):
                branch_chance = uniform(0, 1)
                if branch_chance > rate_of_bifurication:
                    branches += 1
            day += 1
        cumulative_days += day
    average_days = cumulative_days / cycles
    if average_days > days_to_flower:
        good_enough = True
    rate_of_bifurication += 0.0001

print(average_days, 1 - rate_of_bifurication)