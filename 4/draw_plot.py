import json
import matplotlib.pyplot as plt
import numpy as np

json_data = open('plot_data.json')
data = json.load(json_data)

x = np.arange(1.0,6.5,0.5)

plt.figure()
plt.xlabel('lambda')
plt.ylabel('denial probability')
potk, = plt.plot(x, data[2], 'g^', label="Potk")
potk1, = plt.plot(x, data[0], 'ro', label="Potk1")
potk2, = plt.plot(x, data[1], 'bs', label="Potk2")
plt.legend(loc=2)
plt.show()