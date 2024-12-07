# optical-loss-calc
An interactive web application built with Streamlit for simulating optical properties in thin-film material stacks. The app allows users to configure multi-layer systems, calculate reflection, transmission, and absorption, and visualize optical losses.

### Features:
- Configure materials and thicknesses for each layer in a stack.
- Calculate reflection, transmission, and absorption using the Transfer Matrix Method (TMM).
- Visualize results with intuitive plots.
- Analyze absorption per layer and compute photocurrent density.
  
### Usage:
1. Select materials from the pre-loaded library.
2. Configure the thickness and order of layers.
3. Click "Calculate and Plot" to generate results.

### References:
- Solar Spectrum: [AM1.5G Solar Spectrum](https://rredc.nrel.gov/solar/spectra/am1.5/)
- Refractive Index Library ([PV Lighthouse](https://www.pvlighthouse.com.au/refractive-index-library))
- Thin-film optics modeling: `tmm` Python library ([GitHub link](https://github.com/sbyrnes321/tmm))
