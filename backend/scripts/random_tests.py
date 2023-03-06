import random
import matplotlib.pyplot as plt
import numpy as np

iterations = 100_000

randint_values = []
random_values = []

max_value = 72
for i in range(iterations):
    randint_values.append(random.randint(0, max_value))
    random_values.append(int(random.random() * (max_value+1)))

# plt.hist(randint_values)
# plt.hist(random_values)

randint_x, randint_counts = np.unique(np.array(randint_values), return_counts=True)
random_x, random_counts = np.unique(np.array(random_values), return_counts=True)

x = [i for i in range(max_value)]
plt.bar(randint_x, randint_counts, width=0.3)
plt.bar(random_x+0.3, random_counts, width=0.3)
plt.show()
