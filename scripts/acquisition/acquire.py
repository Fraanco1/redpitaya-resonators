import numpy as np
import matplotlib.pyplot as plt
from redpitaya_resonators.redpitaya_driver import RedPitaya

def acquire(redpitaya, frequency_array, filename, amplitude, lo, power, attenuation):
    # creates file
    with open(filename, 'w') as f:
        f.write(f"# Filename: {filename}\n")
        f.write(f"# Amplitude: {amplitude} V\n")
        f.write(f"# Local Oscillator: {lo} GHz\n")
        f.write(f"# Power: {power} dBm\n")
        f.write(f"# Attenuation: {attenuation} dB\n")
        f.write("Frequency (Hz)\tChannel 1 (V)\tChannel 2 (V)\n")

    for freq in frequency_array:
        redpitaya.generate(frequency=freq)
        ch1, ch2 = redpitaya.acquire()

        with open(filename, 'a') as f:
            f.write(f"{freq}\t{ch1}\t{ch2}\n")

if __name__ == "__main__":
    redpitaya = RedPitaya(ip='192.168.1.12')
    frequency_array = np.arange(2.5e6, 2.8e6, 1e3)

    # data entered by user
    filename = input("Enter the filename to save the data (e.g., 'data.dat'): ")
    amplitude = float(input("Enter the amplitude for the signal (e.g., 0.05 V): "))
    lo = float(input("Enter the local oscillator frequency (e.g., 2.65 GHz): "))
    power = float(input("Enter the power level for the signal (e.g., -20 dBm): "))
    attenuation = float(input("Enter the attenuation level for the signal (e.g., 10 dB): "))

    # acquire data
    acquire(redpitaya, frequency_array, filename, amplitude, lo, power, attenuation)
