import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import h5py
import os
import time

fig, ax = plt.subplots(2, 1)
filename = '../../data/test.h5'
moddate = None

def read_h5(retries=5, delay=0.2):
    for attempt in range(retries):
        try:
            with h5py.File(filename, "r") as f:
                keys = list(f.keys())
                if len(keys) == 0:
                    return None, None, None
                frequencies = sorted([float(key.replace("freq_", "").replace("Hz", "")) for key in keys])
                channel1 = [f[f"freq_{freq}Hz"]["channel1"][:] for freq in frequencies]
                channel2 = [f[f"freq_{freq}Hz"]["channel2"][:] for freq in frequencies]
                i_all = np.array([np.max(np.abs(np.fft.rfft(ch))) for ch in channel1])
                q_all = np.array([np.max(np.abs(np.fft.rfft(ch))) for ch in channel2])

                return frequencies, i_all, q_all
        except OSError:
            print(f"File busy, retrying ({attempt+1}/{retries})...")
            time.sleep(delay)
    return None, None, None

def plot_data():
    frequencies, i_all, q_all = read_h5()
    if frequencies is None:
        print("Could not read file, skipping frame")
        return

    print(i_all, q_all)
    freq  = np.array(frequencies)
    power = (i_all**2 + q_all**2)/ 50
    #mag   = 10 * np.log10(power / 0.001)
    mag = i_all
    phase = np.arctan2(q_all, i_all)

    #ax[0].clear()
    ax[0].scatter(freq, mag, c='black', marker='s', s=20, label='Magnitude')
    ax[0].legend()
    ax[0].set_xlabel('Frequency [Hz]')
    ax[0].set_ylabel('Mag [dBm]')
    ax[0].grid()

    #ax[1].clear()
    ax[1].scatter(freq, phase, c='black', marker='s', s=20, label='Phase')
    ax[1].legend()
    ax[1].set_xlabel('Frequency [Hz]')
    ax[1].set_ylabel('Phase [rad]')
    ax[1].grid()

    plt.xticks(rotation=45, ha='right')
    plt.suptitle('Frequency sweep FPGA')
    plt.tight_layout()
    fig.canvas.draw()

def animate(frame):
    global moddate
    try:
        moddate2 = os.stat(filename)[8]
        if moddate != moddate2:
            moddate = moddate2
            plot_data()
    except FileNotFoundError:
        print("Waiting for file...")
    except OSError as e:
        print(f"OSError in animate: {e}")

ani = animation.FuncAnimation(fig, animate, interval=500, cache_frame_data=False)
plt.tight_layout()
plt.show()