import numpy
import matplotlib.pyplot as plt
import random
from numpy.random import normal

gaussian_numbers = normal(size=1000)


arr = [random.random()*100 for i in range(100)]
plt.hist(gaussian_numbers, bins=100)
plt.show()