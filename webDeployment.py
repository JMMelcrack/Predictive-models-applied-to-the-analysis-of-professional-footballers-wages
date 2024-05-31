import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Set the title and description of the web app
st.title("FindTheSalary")
st.write("""
Esta aplicación estima el salario semanal de un futbolista basándose en distintas estadísticas.
A continuación, actualice las estadísticas como desee y pulse aceptar para obtener el salario estimado.
""")

# Initial data
df = pd.DataFrame(
    [
       {"Nombre": "Guido Rodríguez (2022/2023)", 
        "Edad": 28, 
        "Valor liga ini": 3300, 
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
        "Valor liga fin": 3300,
        "Valor equipo ini": 246.4, 
        "Valor equipo fin": 246.4, 
        "Defensa": False,
        },
   ]
)

# Create a form for user input with tooltips
with st.form(key='stats_form'):
    nombre = st.text_input('Nombre', df['Nombre'][0], help='Nombre del jugador')
    edad = st.number_input('Edad', value=df['Edad'][0], help='Edad del jugador')
    titularidades = st.number_input('Titularidades', value=df['Titularidades'][0], help='Número de partidos en los que fue titular')
    minutos = st.number_input('Minutos', value=df['Minutos'][0], help='Número de Minutos totales jugados')
    penaltis_lanzados = st.number_input('Penaltis lanzados', value=df['Penaltis lanzados'][0], help='Total penaltis intentados, incluye marcados y fallados')
    xG = st.number_input('xG', value=df['xG'][0], help='Número de goles que el jugador debería haber marcado en realidad (expected goals)')
    disparos = st.number_input('Disparos', value=df['Disparos'][0], help='Total de disparos efectuados por el jugador')
    tiros_a_puerta = st.number_input('Tiros a puerta', value=df['Tiros a puerta'][0], help='Disparos que van entre los tres palos')
    faltas_lanzadas = st.number_input('Faltas lanzadas', value=df['Faltas lanzadas'][0], help='Número de faltas lanzadas')
    pases_cortos_intentados = st.number_input('Pases cortos intentados', value=df['Pases cortos intentados'][0], help='Pases entre 5 y 15 yardas intentados')
    pases_largos_completados = st.number_input('Pases largos completados', value=df['Pases largos completados'][0], help='Pases de más de 30 yardas completados')
    pases_clave = st.number_input('Pases clave', value=df['Pases clave'][0], help='Número de pases que conducen a un disparo dados')
    toques = st.number_input('Toques', value=df['Toques'][0], help='Número de veces que el jugador toca el balón')
    controles = st.number_input('Controles', value=df['Controles'][0], help='Veces que el jugador controló el balón')
    dist_con_balon = st.number_input('Dist con balon', value=df['Dist con balon'][0], help='Distancia total de los desplazamientos del jugador con balón en yardas')
    conducciones_ultimo_tercio = st.number_input('Conducciones ultimo tercio', value=df['Conducciones ultimo tercio'][0], help='Conducciones que entran en el último tercio del campo')
    valor_liga_ini = st.number_input('Beneficio liga ini', value=df['Valor liga ini'][0], help='Beneficio de la liga en la que el jugador empieza la temporada, el beneficio se corresponde con el de la actual temporada. Las unidades están en millones.')
    valor_liga_fin = st.number_input('Beneficio liga fin', value=df['Valor liga fin'][0], help='Beneficio total de la liga en la que el jugador milita al final de temporada, es decir si ficha por un equipo de otra liga en verano es esa la liga que aparece, el beneficio se corresponde con el de la actual temporada. Las unidades están en millones.')
    valor_equipo_ini = st.number_input('Valor equipo ini', value=df['Valor equipo ini'][0], help='Valor del equipo por el que juega el jugador en la presente temporada, el valor es el de la temporada actual. Las unidades están en millones.')
    valor_equipo_fin = st.number_input('Valor equipo fin', value=df['Valor equipo fin'][0], help='Valor del equipo en el que jugará el jugador en la siguiente campaña, el valor es el de la presente temporada. Las unidades están en millones.')
    defensa = st.checkbox('Defensa', value=df['Defensa'][0], help='Indica si el jugador es defensor')

    submit_button = st.form_submit_button(label='Aceptar')

# Update the DataFrame with the new values
if submit_button:
    df = pd.DataFrame({
        "Nombre": [nombre], 
        "Edad": [edad], 
        "Valor liga ini": [valor_liga_ini], 
        "Titularidades": [titularidades],
        "Minutos": [minutos],
        "Penaltis lanzados": [penaltis_lanzados],
        "xG": [xG],
        "Disparos": [disparos],
        "Tiros a puerta": [tiros_a_puerta],
        "Faltas lanzadas": [faltas_lanzadas], 
        "Pases cortos intentados": [pases_cortos_intentados], 
        "Pases largos completados": [pases_largos_completados],
        "Pases clave": [pases_clave],
        "Toques": [toques],
        "Controles": [controles], 
        "Dist con balon": [dist_con_balon], 
        "Conducciones ultimo tercio": [conducciones_ultimo_tercio],
        "Valor liga fin": [valor_liga_fin],
        "Valor equipo ini": [valor_equipo_ini], 
        "Valor equipo fin": [valor_equipo_fin], 
        "Defensa": [defensa],
    })

    # Prepare to scale the data
    categoricas_indices = ['Nombre', 'Defensa']
    continuas_indices = [col for col in df.columns if col not in categoricas_indices]

    # Load the scaler and model using absolute paths
    scaler_path = 'web_deploy/MinMaxScaler.pkl'
    model_path = 'web_deploy/best_model.pkl'

    try:
        with open(scaler_path, 'rb') as file:
            scaler = pickle.load(file)

        with open(model_path, 'rb') as file:
            model = pickle.load(file)

        # If both files are loaded, perform the scaling and prediction
        df[continuas_indices] = scaler.transform(df[continuas_indices])
        predicted_salary = model.predict(df.drop(columns=['Nombre']).to_numpy())

        st.write(f"El salario estimado que cobra {df['Nombre'].iloc[0]}, es de {round(np.expm1(predicted_salary)[0], 2)} euros.")
    except FileNotFoundError as e:
        st.error(f"File not found: {e.filename}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
