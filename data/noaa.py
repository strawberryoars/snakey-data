import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# https://www.ncei.noaa.gov/access/crn/qcdatasets.html
# https://www.ncei.noaa.gov/pub/data/uscrn/products/soil/soilanom01/readme.txt
# https://www.ncei.noaa.gov/pub/data/uscrn/products/soil/soilanom01/

st.title ("NOAA Quality Controlled Dataset Analysis")
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

data = pd.read_csv('data/CRNSSM0101-CO_Boulder_14_W.csv')
plt.plot(data['SMANOM_5_CM'])
st.pyplot(plt)
plt.clf()

