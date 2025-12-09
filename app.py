import streamlit as st
import pandas as pd
import numpy as np

st.title("Test Dashboard")
st.write("If you see this, packages are installed!")

# Create simple data
df = pd.DataFrame({
    'Name': ['Ali', 'Bilal', 'Farhan'],
    'Visits': [10, 20, 15]
})

st.dataframe(df)
st.bar_chart(df.set_index('Name'))
