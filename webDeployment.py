import streamlit as st
import pandas as pd
import pickle
import numpy as np
import os

df = pd.DataFrame(
    [
       {"Nombre": "Declan Rice", 
        "Edad": 23, 
        "Valor liga ini": 11320, 
        "Titularidades": 36,
        "Minutos": 3273,
        "Penaltis lanzados": 0,
        "xG": 2.4,
        "Disparos": 35,
        "Tiros a puerta": 8,
        "Faltas lanzadas": 1, 
        "Pases cortos intentados": 944, 
        "Pases largos completados": 223,
        "Pases clave": 37,
        "Toques": 2475,
        "Controles": 1642, 
        "Dist con balon": 9170, 
        "Conducciones ultimo tercio": 76,
        "Valor liga fin": 11320,
        "Valor equipo ini": 465.75, 
        "Valor equipo fin": 1000, 
        "Defensa": True,
        },
   ]
)
edited_df = st.data_editor(df.transpose(), height=770)
df = edited_df.transpose()

# Prepare to scale the data
categoricas_indices = ['Nombre', 'Defensa']
continuas_indices = [col for col in df.columns if col not in categoricas_indices]

# Load the scaler to transform the data and the ML model to make the predictions
# with open('model_weights/MinMaxScaler.pkl', 'rb') as file:
#     scaler = pickle.load(file)

# with open('model_weights/best_model.pkl', 'rb') as file:
#     model = pickle.load(file)

# Option 2: Use file uploader for user to upload files
uploaded_scaler = st.file_uploader("Upload MinMaxScaler.pkl", type="pkl")
uploaded_model = st.file_uploader("Upload best_model.pkl", type="pkl")

if uploaded_scaler is not None:
    scaler = pickle.load(uploaded_scaler)
    st.success("Scaler loaded successfully.")

if uploaded_model is not None:
    model = pickle.load(uploaded_model)
    st.success("Model loaded successfully.")

# If both files are loaded, perform the scaling
if 'scaler' in locals() and 'model' in locals():
    df[continuas_indices] = scaler.transform(df[continuas_indices])
    df['Defensa'] = (df['Defensa'] == 'True') | (df['Defensa'] == 'true')
    predicted_salary = model.predict(df.drop(columns=['Nombre']).to_numpy())

    st.write(f"El salario estimado que cobra {df['Nombre']}, es de {np.expm1(predicted_salary)} euros.")
else:
    st.warning("Scaler and/or model not loaded. Please upload the necessary files.")

# scaled_df = scaler.transform(df)