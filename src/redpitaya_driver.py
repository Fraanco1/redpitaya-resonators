import csv
import sys
import time
import numpy as np
import src.redpitaya_scpi as scpi
import matplotlib.pyplot as plt
import pandas as pd

def acquire(rp, timeout=5.0):
    # ── 4. Arm and trigger acquisition ──────────────────────────────────────────
    rp.tx_txt('ACQ:START')
    time.sleep(0.02)                     # let the buffer fill a bit
    #rp.tx_txt('ACQ:TRIG CH2_PE')        # trigger on IN1 positive edge
    rp.tx_txt('ACQ:TRIG NOW')

    t0 = time.time()
    while True:
        rp.tx_txt('ACQ:TRIG:STAT?')
        if rp.rx_txt() == 'TD':
            break
        if time.time() - t0 > timeout:
            rp.close()
            sys.exit(1)
        time.sleep(0.005)


    # ── 5. Read both channels ────────────────────────────────────────────────────
    rp.tx_txt('ACQ:SOUR1:DATA?')
    raw1 = rp.rx_txt().strip('{}\n\r').replace(' ', '').split(',')
    ch1  = list(map(float, raw1))

    rp.tx_txt('ACQ:SOUR2:DATA?')
    raw2 = rp.rx_txt().strip('{}\n\r').replace(' ', '').split(',')
    ch2  = list(map(float, raw2))
    return ch1, ch2

# Global parameters
ip = '192.168.1.12'
dec = 1

# Sampling rate after decimation
FS = 125e6 / dec
print(f"Connecting to RedPitaya at {ip} ...")
print(f"  Decimation : {dec}  →  Fs = {FS/1e3:.1f} kHz")

rp = scpi.scpi(ip)

# ── 1. Reset everything ──────────────────────────────────────────────────────
rp.tx_txt('GEN:RST')
rp.tx_txt('ACQ:RST')

# ── 2. Configure acquisition ─────────────────────────────────────────────────
rp.tx_txt(f'ACQ:DEC {dec}')
rp.tx_txt('ACQ:DATA:UNITS VOLTS')
rp.tx_txt('ACQ:TRIG:LEV 0')         # trigger at 0 V crossing
rp.tx_txt('ACQ:TRIG:DLY 0')

# ── 3. Frequency sweep ──────────────────────────────────────────────────
filename = input('Nombre archivo: ')
power = input('Potencia (dBm): ')
ext_attenuation = input('Atenuación externa (dB): ')
lo_frequency = input('Frecuencia LO (GHz): ')
ampl = 0.05

df = pd.DataFrame()

with open(filename + '.dat', 'w') as file:
    file.writelines('freq,i,q\n')
frequency_array = np.arange(2.5e6, 2.8e6, 1e3)
i_, q_ = [], []
for freq in frequency_array:
    print('Frequency:', freq)
    # OUT1 = cosine = sine at +90°
    rp.tx_txt('SOUR1:FUNC SINE')
    rp.tx_txt(f'SOUR1:FREQ:FIX {freq}')
    rp.tx_txt(f'SOUR1:VOLT {ampl}')
    rp.tx_txt('SOUR1:PHAS 90')          # 90° → cosine

    # OUT2 = sine = sine at 0°
    rp.tx_txt('SOUR2:FUNC SINE')
    rp.tx_txt(f'SOUR2:FREQ:FIX {freq}')
    rp.tx_txt(f'SOUR2:VOLT {ampl}')
    rp.tx_txt('SOUR2:PHAS 0')           # 0°  → sine

    # Enable both outputs
    rp.tx_txt('OUTPUT:STATE ON')        # turns on both OUT1 and OUT2

    # Start both generators simultaneously (phase-locked)
    rp.tx_txt('SOUR:TRig:INT')

    print("Generators running (OUT1=cos, OUT2=sin).")
    channel1, channel2 = acquire(rp)
    i = np.max(channel1) - np.min(channel1)
    q = np.max(channel2) - np.min(channel2)
    with open(filename + '.dat', 'a') as file:
        file.writelines(f'{freq},{i},{q}\n')
    i_.append(i)
    q_.append(q)

rp.close()