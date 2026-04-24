import numpy as np
import matplotlib.pyplot as plt
import h5py
import os 
import shutil
from redpitaya_resonators.redpitaya_driver import RedPitaya

def acquire(redpitaya, frequency_array, filename, amplitude, lo, power, attenuation):
    h5file  = filename + ".h5"
    tmpfile = filename + ".tmp"

    for freq in frequency_array:
        redpitaya.generate(frequency=freq, amplitude=amplitude)
        ch1, ch2 = redpitaya.acquire()

        key = f"freq_{freq}Hz"

        # Copy current h5 to tmp, or create fresh if it doesn't exist
        if os.path.exists(h5file):
            shutil.copy2(h5file, tmpfile)
        
        with h5py.File(tmpfile, "a") as f:
            f.attrs["filename"]    = filename
            f.attrs["amplitude"]   = f"{amplitude} V"
            f.attrs["lo"]          = f"{lo} GHz"
            f.attrs["power"]       = f"{power} dBm"
            f.attrs["attenuation"] = f"{attenuation} dB"

            if key in f:
                del f[key]
            grp = f.create_group(key)
            grp.create_dataset("channel1", data=np.array(ch1))
            grp.create_dataset("channel2", data=np.array(ch2))

        # Atomically replace readable file
        os.replace(tmpfile, h5file)

if __name__ == "__main__":
    os.chdir('../../data')
    redpitaya = RedPitaya(ip='192.168.1.12')
    frequency_array = np.arange(0.1e6, 4e6, 10e3)

    # data entered by user
    filename = input("Enter the filename to save the data (e.g., 'data.dat'): ")
    amplitude = float(input("Enter the amplitude for the signal (e.g., 0.05 V): "))
    lo = float(input("Enter the local oscillator frequency (e.g., 5.096 GHz): "))
    power = float(input("Enter the power level for the signal (e.g., -20 dBm): "))
    attenuation = float(input("Enter the attenuation level for the signal (e.g., 10 dB): "))

    # acquire data
    acquire(redpitaya, frequency_array, filename, amplitude, lo, power, attenuation)
