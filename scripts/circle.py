import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

filename = 'sweep_50MHz.dat'
data = pd.read_csv(filename)

min_, max_= 10, 100
freq = data['freq'].to_numpy()[min_:max_]
i = data['i'].to_numpy()[min_:max_]
q = data['q'].to_numpy()[min_:max_]

plt.scatter(i, q)
plt.axis('equal')
plt.show()