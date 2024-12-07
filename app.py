import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tmm import (coh_tmm, inc_tmm, inc_absorp_in_each_layer)
from scipy.interpolate import interp1d
import os

hc = 1239.84193  # Planck constant times speed of light in eV*nm
q = 1.602e-19   # elementary charge in Coulombs
h = 6.626e-34   # Planck constant in Joule-seconds
c = 2.998e8     # speed of light in meters/secon


def nk_convert(fname):
    df = pd.read_csv(fname)
    E = hc / df['λ,n (nm)'].to_numpy()
    nk = df['n'].to_numpy() + 1j * df['k'].to_numpy()
    return interp1d(E, nk, bounds_error=False, fill_value='extrapolate')

def setup_layers(n_func_list, lambda_vac):
    energy = hc / lambda_vac
    return [1] + [n_func(energy) for n_func in n_func_list] + [1]

def setup_thicknesses(d_list):
    return [np.inf] + d_list + [np.inf]

# Keeping calculate_tmm unchanged
def calculate_tmm(lambda_list, d_list, c_list, n_func_list, plot=True):
    results = {'lambda': lambda_list, 'R': [], 'T': [], 'A': []}
    A_in_each_layer = []

    for lambda_vac in lambda_list:
        n_list = setup_layers(n_func_list, lambda_vac)
        d_list_full = setup_thicknesses(d_list)
        s_polar = inc_tmm('s', n_list, d_list_full, c_list, 0, lambda_vac)
        p_polar = inc_tmm('p', n_list, d_list_full, c_list, 0, lambda_vac)

        R = (s_polar['R'] + p_polar['R']) / 2
        T = (s_polar['T'] + p_polar['T']) / 2

        results['R'].append(R)
        results['T'].append(T)
        A_s = np.array(inc_absorp_in_each_layer(s_polar))
        A_p = np.array(inc_absorp_in_each_layer(p_polar))
        
        A_tot = 0.5 * (A_s + A_p)
        A_in_each_layer.append(A_tot[1:-1])  # Excluding infinite layers

    results['A'] = np.mean(A_in_each_layer, axis=0)
    results.setdefault('A_breakdown', []).append(np.array(A_in_each_layer).T)
    return results

# Streamlit interface
st.set_page_config(page_title="Optical Loss Analyzer", page_icon="🔬☀️", layout="wide")


st.write('## Optical Loss Analysis')

st.sidebar.header('Configuration Settings')

with st.sidebar:
    light_source_file = {'AM1.5G': './data/AM15G-spectrum.csv'}
    selected_light = st.selectbox('Select light source', ["AM1.5G"])

    lambda_start = st.number_input('Wavelength Start (nm)', min_value=200, max_value=1000, value=280)
    lambda_end = st.number_input('Wavelength End (nm)', min_value=200, max_value=1500, value=900)


    layer_number = st.number_input('Number of Layers', min_value=1, max_value=10, value=3)

 # Dynamically generate the material_files dictionary from the './data' folder
    data_folder = './data'

    material_files = {}
    if os.path.exists(data_folder):
        for filename in os.listdir(data_folder):
            if filename.endswith('.csv') and "spectrum" not in filename.lower():
                # Remove '.csv' from the filename to use as the material name
                material_name = os.path.splitext(filename)[0]
                # Add to the material_files dictionary
                material_files[material_name] = os.path.join(data_folder, filename)
    else:
        print(f"Data folder '{data_folder}' does not exist.")


    cols = st.columns(2)  # Create two columns

    layer_materials = [cols[0].selectbox(f'Material {i+1}', list(material_files.keys())) for i in range(layer_number)]
    layer_thicknesses = [cols[1].number_input(f'Thickness {i+1} (nm)', 10, 2000, 100) for i in range(layer_number)]


if st.button('Calculate and Plot'):
    n_func_list = [nk_convert(material_files[mat]) for mat in layer_materials]
    lambda_list = np.linspace(lambda_start, lambda_end, 500)
    c_list = ['i'] * (layer_number + 2)
    results = calculate_tmm(lambda_list, layer_thicknesses, c_list, n_func_list)

    A_breakdown = np.array(*results['A_breakdown'])
    optical_breakdown= [*reversed(A_breakdown), results['T'], results['R']]
    all_layer_names = [*reversed(layer_materials), 'Transmission', 'Reflection']

    fig, ax = plt.subplots()

    ax.stackplot(results['lambda'], optical_breakdown, labels=all_layer_names)

    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('Absorption per Layer')
    ax.set_ylim(0,1)
    ax.legend()
    st.pyplot(fig)

    # Improved J reporting
    df_sun = pd.read_csv(light_source_file[selected_light])
    wl = lambda_list
    pw = df_sun['pw']
    x1 = df_sun['wl']
    phi = interp1d(x1, pw)(wl)

    j_list = []
    for index,item in enumerate(optical_breakdown):
        integrand = ((q*wl*10**-9)/(h*c))* np.multiply(phi, item)

        j_layer = np.trapz(integrand, wl)

        j_list.append(j_layer)
    formatted_j_list = [f"{j:.2f}" for j in j_list] 

    st.write(f'### Light Source: {selected_light}')
    st.write('### \( J \) values for each layer:')
    st.table(pd.DataFrame(zip(all_layer_names, formatted_j_list), columns=['Layer', 'J (mA/cm²)']))