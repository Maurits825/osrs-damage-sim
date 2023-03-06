import math
from itertools import permutations, combinations

# dhl, inq top+bot, slayer helm
gear_bonus = [1.2, 1.01, 1.2]

for base_dmg in range(1, 100):
    print("\nbase dmg: " + str(base_dmg))
    for gear_bonus_count in range(2, len(gear_bonus)):
        all_combinations = combinations(gear_bonus, gear_bonus_count)
        for comb in all_combinations:
            all_perms = permutations(comb)
            previous_max_hit = 0
            for perm in all_perms:
                current_max_hit = base_dmg
                for bonus in perm:
                    current_max_hit = math.floor(current_max_hit * bonus)

                if previous_max_hit != 0 and current_max_hit != previous_max_hit:
                    print("Not matching!")
                    print(perm)

                previous_max_hit = current_max_hit
