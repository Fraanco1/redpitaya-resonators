import numpy as np
import matplotlib.pyplot as plt
from redpitaya_resonators.redpitaya_driver import RedPitaya

redpitaya = RedPitaya(ip='192.168.1.12')
redpitaya.generate(frequency=1e5, amplitude=0.05)
ch1, ch2 = redpitaya.acquire()

plt.plot(ch1)
plt.plot(ch2)
plt.show()
