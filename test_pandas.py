import pandas as pd
import numpy as np
import os

array = np.linspace(0,1,10)
df = pd.DataFrame({'frequency [Hz]': array})
file_exists = os.path.isfile('test.csv')
df.to_csv('test.csv', mode='a', index=False, header=not file_exists)