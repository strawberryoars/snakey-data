import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Constants
DATE_COLUMN = 'DATE_TIME'
DATA_URL =  'https://www.ncei.noaa.gov/pub/data/uscrn/products/soil/soilanom01/CRNSSM0101-CO_Boulder_14_W.csv'

@st.cache_data(show_spinner=False)
def load_data(nrows: int | None = None):
    """Loads data from the provided URL."""
    try:
        data = pd.read_csv(DATA_URL, nrows=nrows)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN], format='%Y%m%d%H')
        return data
    except Exception as e:
        st.error(f"An error occurred while loading the data: {str(e)}")
        return None

def plot_histogram(data):
    """Plots a histogram of soil moisture anomaly at  5 cm depth."""
    fig, ax = plt.subplots(figsize=(10,  6))
    ax.hist(data['SMANOM_5_CM'], bins=30, edgecolor='black', alpha=0.7)
    ax.set_title('Histogram of Soil Moisture Anomaly at  5 cm Depth')
    ax.set_xlabel('Soil Moisture Anomaly (IQR Deviations)')
    ax.set_ylabel('Frequency')
    ax.grid(True)
    return fig

def plot_over_time(data):
    """Plots soil moisture anomaly at  5 cm depth over time."""
    fig, ax = plt.subplots(figsize=(10,  6))
    ax.plot(data['DATE_TIME'], data['SMANOM_5_CM'], marker='o', alpha=0.7)
    ax.set_title('Soil Moisture Anomaly at  5 cm Depth Over Time')
    ax.set_xlabel('Date Time')
    ax.set_ylabel('Soil Moisture Anomaly (IQR Deviations)')
    ax.grid(True)
    return fig

def main():
    st.title("NOAA Dataset Analysis")
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

    # Load data with progress bar
    with st.spinner('Loading data...'):
        data = load_data(10000)
        if data is not None:
            st.success('Data loaded successfully!')
            st.subheader('Raw data')
            st.write(data)

            # Display plots side by side
            col1, col2 = st.columns(2)
            with col1:
                st.pyplot(plot_histogram(data))
            with col2:
                st.pyplot(plot_over_time(data))
        else:
            st.error('Failed to load data. Please check the URL or network connection.')

if __name__ == "__main__":
    main()
