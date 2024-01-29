import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# https://www.ncei.noaa.gov/access/crn/qcdatasets.html
# https://www.ncei.noaa.gov/pub/data/uscrn/products/soil/soilanom01/readme.txt
# https://www.ncei.noaa.gov/pub/data/uscrn/products/soil/soilanom01/

DATE_COLUMN = 'DATE_TIME'
DATA_URL = 'data/CRNSSM0101-CO_Boulder_14_W.csv'

def load_data(nrows: int | None = None):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    # lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN], format='%Y%m%d%H')
    return data

st.title ("NOAA Dataset Analysis")
st.header("Standardized Soil Moisture")
st.markdown("""    
    This standardized soil moisture product is derived using the soil moisture
    climatology from the SMC01 product series (described in a separate README file)
    in the following manner.  The soil moisture volumetric water content (SMVWC) is
    reported as observed for the layer in question. The soil moisture anomaly
    (SMANOM) is derived by subtracting the MEDIAN from the SMVWC value and dividing
    the difference by the interquartile range (IQR) for that hour:
""")
st.latex(r''' SMANOM = (SMVWC - MEDIAN) / (IQR) ''')


data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('Loading data...done!')

st.subheader('Raw data')
st.write(data)

# histogram for soil moisture anomaly at 5 cm depth
plt.figure(figsize=(10, 6))
plt.hist(data['SMANOM_5_CM'], bins=30, edgecolor='black')
plt.title('Histogram of Soil Moisture Anomaly at 5 cm Depth')
plt.xlabel('Soil Moisture Anomaly (IQR Deviations)')
plt.ylabel('Frequency')
plt.grid(True)
st.pyplot(plt)
plt.clf()

# vizualize soil moisture anomaly at 5 cm depth over time
plt.figure(figsize=(10, 6))
plt.plot(data['DATE_TIME'], data['SMANOM_5_CM'], marker='o')
plt.title('Soil Moisture Anomaly at 5 cm Depth Over Time')
plt.xlabel('Date Time')
plt.ylabel('Soil Moisture Anomaly (IQR Deviations)')
plt.grid(True)
st.pyplot(plt)
plt.clf()




