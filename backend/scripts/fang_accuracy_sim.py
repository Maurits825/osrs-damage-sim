import random

max_attack_role = 10000
max_defence_role = 15000
iterations = 500000

accuracy = max_attack_role / (2 * (max_defence_role + 1))
dps_calc_accuracy = (accuracy + ((1 - accuracy) * accuracy)) * 100

hit = 0
for i in range(iterations):
    attack_role = random.randint(0, max_attack_role)
    defence_role = random.randint(0, max_defence_role)

    if attack_role >= defence_role:
        hit += 1
    else:
        attack_role = random.randint(0, max_attack_role)
        if attack_role >= defence_role:
            hit += 1

only_attack_roll_accuracy = (hit / iterations) * 100

hit = 0
for i in range(iterations):
    attack_role = random.randint(0, max_attack_role)
    defence_role = random.randint(0, max_defence_role)

    if attack_role >= defence_role:
        hit += 1
    else:
        attack_role = random.randint(0, max_attack_role)
        defence_role = random.randint(0, max_defence_role)
        if attack_role >= defence_role:
            hit += 1

att_and_def_roll_accuracy = (hit / iterations) * 100

print("Dps calc: " + str(round(dps_calc_accuracy, 4)))
print("Only att roll: " + str(round(only_attack_roll_accuracy, 4)))
print("Both att and def roll: " + str(round(att_and_def_roll_accuracy, 4)))
