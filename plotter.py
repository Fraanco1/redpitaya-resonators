import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.animation as animation
import os

fig, ax = plt.subplots(2)
filename = 'test.dat'
moddate = None  # Start as None to force first draw

def plot_data():
    data = pd.read_csv(filename)
    
    freq = data['freq'].to_numpy()
    i = data['i'].to_numpy()
    q = data['q'].to_numpy()
    
    power = (np.sqrt(i**2 + q**2)**2) / 50
    mag = 10 * np.log10(power / 0.001)
    phase = np.arctan2(q, i)
    
    ax[0].clear()
    ax[0].scatter(freq, mag, c='black', marker='s', s=10, label='Mag')
    ax[0].legend()
    ax[0].set_xlabel('Frequency [Hz]')
    ax[0].set_ylabel('Magnitude [dBm]')
    ax[0].grid()
    
    ax[1].clear()
    ax[1].scatter(freq, phase, c='black', marker='s', s=10, label='Phase')
    ax[1].legend()
    ax[1].set_xlabel('Frequency [Hz]')
    ax[1].set_ylabel('Phase [rad]')
    ax[1].grid()
    
    plt.xticks(rotation=45, ha='right')
    plt.suptitle('Frequency sweep FPGA')

def animate(frame):
    global moddate
    moddate2 = os.stat(filename)[8]
    
    if moddate != moddate2:  # Triggers on first call (None) and on file changes
        moddate = moddate2
        plot_data()

ani = animation.FuncAnimation(fig, animate)
plt.tight_layout()
plt.show()