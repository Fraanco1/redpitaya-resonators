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
    f0 = np.array([
        5.030102224804392,
        5.036716901416831,
        5.056617747157971,
        5.062328182922382,
        5.096449020022729,
        5.098645793631314,
        5.1070293715518815,
        5.123789919393869,
        5.126262514423809,
        5.139484151238095,
        5.150227404419456,
        5.151213062005093,
        5.195578372016454,
        5.208324326418811,
        5.2104631047256085]) * 1e9 # Hz
    spans = np.ones(len(f0)) * 2e6 # Hz

    # performs acquisition for each resonator
    for i in range(len(f0)):
        filename = f"/../../data/resonator_{i+1}.dat"
        lo = f0[i] - 1e6 - spans[i]/2
        rf.frequency(lo)
        frequency_array = np.arange(1e6, 1e6 + spans[i], 2.5e3)

        time.sleep(0.2)
        acquire.acquire(redpitaya, frequency_array, filename, amplitude, lo/1e9, power, attenuation)
    