import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ️")

st.title("About")
st.write("### Guide")
st.write("""
This app helps you analyze optical losses in thin-film materials. You can:
- Configure the material stack with thicknesses.
- Calculate and visualize optical properties like reflection, transmission, and absorption.

**Steps to Use:**
1. Configure the material layers in the sidebar.
2. Click 'Calculate and Plot' to generate results.
""")

st.write("### About the Author")
st.write("""
Hi, I'm [Farshad Jafarzadeh](https://www.farshadj.ir/), a researcher and developer passionate about photovoltaics and optical materials.
This app is a result of my interest in making optical loss analysis accessible to everyone.
If you have questions or feedback, feel free to reach out!
""")

st.write("### References")
st.write("""
- Data source: [AM1.5G Solar Spectrum](https://rredc.nrel.gov/solar/spectra/am1.5/)
- Thin-film optics modeling: `tmm` Python library ([GitHub link](https://github.com/sbyrnes321/tmm))
- Refractive Index Library ([PV Lighthouse](https://www.pvlighthouse.com.au/refractive-index-library))  
""")
