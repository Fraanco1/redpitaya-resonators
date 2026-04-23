import time
import sys
import redpitaya_resonators.redpitaya_scpi as scpi

class RedPitaya():
    def __init__(self, ip, dec=1):
        self.ip = ip
        self.dec = dec                          # sets decimation, default dec=1
        self.fs = 125e6 / dec                   # sampling rate after decimation
        
        self.rp = scpi.scpi(ip)                 # redpitaya interface
        print(f"Connecting to RedPitaya at {ip} ...")
        print(f"  Decimation : {dec}  →  Fs = {self.fs/1e6:.1f} MHz")

        # resets everything
        self.rp.tx_txt('GEN:RST')
        self.rp.tx_txt('ACQ:RST')

        # configure acquisition
        self.rp.tx_txt(f'ACQ:DEC {self.dec}')
        self.rp.tx_txt('ACQ:DATA:UNITS VOLTS')
        self.rp.tx_txt('ACQ:TRIG:LEV 0')        # trigger at 0 V crossing
        self.rp.tx_txt('ACQ:TRIG:DLY 0')

    def __del__(self):
        self.rp.close()

    def generate(self, amplitude, frequency):
        # OUT1 = cos = sine at 90°
        self.rp.tx_txt('SOUR1:FUNC SINE')
        self.rp.tx_txt(f'SOUR1:FREQ:FIX {frequency}')
        self.rp.tx_txt(f'SOUR1:VOLT {amplitude}')
        self.rp.tx_txt('SOUR1:PHAS 90')          # 90° → cosine

        # OUT2 = sine = sine at 0°
        self.rp.tx_txt('SOUR2:FUNC SINE')
        self.rp.tx_txt(f'SOUR2:FREQ:FIX {frequency}')
        self.rp.tx_txt(f'SOUR2:VOLT {amplitude}')
        self.rp.tx_txt('SOUR2:PHAS 0')           # 0°  → sine

        # Enable both outputs
        self.rp.tx_txt('OUTPUT:STATE ON')        # turns on both OUT1 and OUT2

        # Start both generators simultaneously (phase-locked)
        self.rp.tx_txt('SOUR:TRig:INT')

        print(f"Generators running. Frequency = {frequency/1e6} MHz, Amplitude = {amplitude} V")    

    def acquire(self, timeout=5.0):
        # arm and trigger acquisition
        self.rp.tx_txt('ACQ:START')
        time.sleep(0.02)                        # let the buffer fill a bit
        self.rp.tx_txt('ACQ:TRIG NOW')          # triggers now

        t0 = time.time()
        while True:
            self.rp.tx_txt('ACQ:TRIG:STAT?')
            if self.rp.rx_txt() == 'TD':
                break
            if time.time() - t0 > timeout:
                self.rp.close()
                sys.exit(1)
            time.sleep(0.005)
        
        # read both channels
        self.rp.tx_txt('ACQ:SOUR1:DATA?')
        raw1 = self.rp.rx_txt().strip('{}\n\r').replace(' ', '').split(',')
        ch1  = list(map(float, raw1))

        self.rp.tx_txt('ACQ:SOUR2:DATA?')
        raw2 = self.rp.rx_txt().strip('{}\n\r').replace(' ', '').split(',')
        ch2  = list(map(float, raw2))
        return ch1, ch2