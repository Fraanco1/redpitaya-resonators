import h5py
import matplotlib.pyplot as plt

with h5py.File('../data/test.h5', "r") as f:
    # Get all frequencies
    frequencies = sorted([float(key.replace("freq_", "").replace("Hz", "")) for key in f.keys()])

    # Get ch1 and ch2 for every frequency
    for freq in frequencies:
        ch1 = f[f"freq_{freq}Hz"]["channel1"][:]
        ch2 = f[f"freq_{freq}Hz"]["channel2"][:]
        plt.plot(ch1)
        plt.show()