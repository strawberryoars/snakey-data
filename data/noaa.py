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

st.subheader('Samplings per hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)


plt.plot(data['SMANOM_5_CM'])

st.pyplot(plt)
plt.clf()




