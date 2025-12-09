import streamlit as st
import pandas as pd

st.title("✅ Dashboard Test - Basic Packages")
st.success("If you see this, installation worked!")

# Simple test
data = {
    "Staff": ["Ali", "Bilal", "Farhan", "Hassan"],
    "Visits": [45, 32, 67, 23],
    "Dealers": [12, 8, 15, 9]
}

df = pd.DataFrame(data)
st.dataframe(df)
st.bar_chart(df.set_index("Staff"))
