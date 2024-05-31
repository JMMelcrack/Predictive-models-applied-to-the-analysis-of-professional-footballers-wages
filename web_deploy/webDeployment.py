import streamlit as st
import pandas as pd
import pickle
import numpy as np
import os

df = pd.DataFrame(
    [
       {"Nombre": "Guido Rodríguez", 
        "Edad": 28, 
        "Valor liga ini": 5260, 
        "Titularidades": 33,
        "Minutos": 2872,
        "Penaltis lanzados": 0,
        "xG": 1.2,
        "Disparos": 22,
        "Tiros a puerta": 6,
        "Faltas lanzadas": 0, 
        "Pases cortos intentados": 796, 
        "Pases largos completados": 129,
        "Pases clave": 11,
        "Toques": 2064,
        "Controles": 1033, 
        "Dist con balon": 3909, 
        "Conducciones ultimo tercio": 14,
        "Valor liga fin": 5260,
        "Valor equipo ini": 246.4, 
        "Valor equipo fin": 246.4, 
        "Defensa": False,
        },
   ]
)
edited_df = st.data_editor(df.transpose(), height=770, width=400)
df = edited_df.transpose()

# Prepare to scale the data
categoricas_indices = ['Nombre', 'Defensa']
continuas_indices = [col for col in df.columns if col not in categoricas_indices]

# Load the scaler to transform the data and the ML model to make the predictions
with open('./MinMaxScaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

with open('./best_model.pkl', 'rb') as file:
    model = pickle.load(file)

# If both files are loaded, perform the scaling and prediction
df[continuas_indices] = scaler.transform(df[continuas_indices])
df['Defensa'] = (df['Defensa'] == 'True') | (df['Defensa'] == 'true')
predicted_salary = model.predict(df.drop(columns=['Nombre']).to_numpy())

st.write(f"El salario estimado que cobra {df['Nombre'].iloc[0]}, es de {round(np.expm1(predicted_salary)[0], 2)} euros.")