import numpy as np
import time
import acquire
from redpitaya_resonators.redpitaya_driver import RedPitaya
from qcodes.instrument_drivers.Keysight import KeysightN5173B

if __name__ == "__main__":
    redpitaya = RedPitaya(ip='192.168.1.12')
    rf = KeysightN5173B('cgx', 'TCPIP0::192.168.1.23::inst0::INSTR')

    # data entered by user
    filename = input("Enter the filename to save the data (e.g., 'data.dat'): ")
    amplitude = float(input("Enter the amplitude for the signal (e.g., 0.05 V): "))
    power = float(input("Enter the power level for the signal (e.g., -20 dBm): "))
    attenuation = float(input("Enter the attenuation level for the signal (e.g., 10 dB): "))

    # resonator f0 positions
    f0 = [1, 2, 3, 4] # Hz
    spans = [2, 2, 2, 2] # Hz

    # performs acquisition for each resonator
    for i in range(len(f0)):
        filename = f"resonator_{i+1}.dat"
        lo = f0[i] - 0.1e6 - spans[i]/2
        rf.frequency(lo)
        frequency_array = np.arange(0.1e6, 0.1e6 + spans[i], 1e3)

        time.sleep(0.2)
        acquire.acquire(redpitaya, frequency_array, filename, amplitude, lo, power, attenuation)
    