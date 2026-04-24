import h5py
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(2, 1)
index = 100

with h5py.File('../data/test.h5', "r") as f:
    # Get all frequencies
    frequencies = sorted([float(key.replace("freq_", "").replace("Hz", "")) for key in f.keys()])
    ch1 = f[f"freq_{frequencies[index]}Hz"]["channel1"][:]
    ch2 = f[f"freq_{frequencies[index]}Hz"]["channel2"][:]

    fft_freqs = np.fft.rfftfreq(len(ch1), d=1/125e6)
    fft_ch1 = np.fft.rfft(ch1)
    ax[0].plot(ch1)
    ax[1].plot(fft_freqs, np.abs(fft_ch1))
    plt.show()