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
        "Valor liga ini": 3300.0, 
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
        "Dist con balon": 3574.39,
        "Conducciones ultimo tercio": 14,
        "Valor liga fin": 3300.0,
        "Valor equipo ini": 246.4,
        "Valor equipo fin": 246.4,
        "Defensa": False,
        },
   ]
)

# Create a form for user input with tooltips
with st.form(key='stats_form'):
    nombre = st.text_input('Nombre', df['Nombre'][0], help='Nombre del jugador')
    edad = st.number_input('Edad', value=int(df['Edad'][0]), min_value=0, help='Edad del jugador')
    titularidades = st.number_input('Titularidades', value=int(df['Titularidades'][0]), min_value=0, help='Número de partidos en los que fue titular')
    minutos = st.number_input('Minutos', value=int(df['Minutos'][0]), min_value=0, help='Número de minutos totales jugados en toda la temporada')
    penaltis_lanzados = st.number_input('Penaltis lanzados', value=int(df['Penaltis lanzados'][0]), min_value=0, help='Total penaltis intentados en toda la temporada, incluye marcados y fallados')
    xG = st.number_input('xG', value=float(df['xG'][0]), min_value=0.0, help='Número de goles que el jugador debería haber marcado en realidad en toda la temporada (expected goals)')
    disparos = st.number_input('Disparos', value=int(df['Disparos'][0]), min_value=0, help='Total de disparos efectuados por el jugador en toda la temporada')
    tiros_a_puerta = st.number_input('Tiros a puerta', value=int(df['Tiros a puerta'][0]), min_value=0, help='Disparos que van entre los tres palos en toda la temporada')
    faltas_lanzadas = st.number_input('Faltas lanzadas', value=int(df['Faltas lanzadas'][0]), min_value=0, help='Número de faltas lanzadas en toda la temporada')
    pases_cortos_intentados = st.number_input('Pases cortos intentados', value=int(df['Pases cortos intentados'][0]), min_value=0, help='Pases entre 4.6 y 13.7 metros intentados en toda la temporada')
    pases_largos_completados = st.number_input('Pases largos completados', value=int(df['Pases largos completados'][0]), min_value=0, help='Pases de más de 27.4 metros completados en toda la temporada')
    pases_clave = st.number_input('Pases clave', value=int(df['Pases clave'][0]), min_value=0, help='Número de pases que conducen a un disparo dados en toda la temporada')
    toques = st.number_input('Toques', value=int(df['Toques'][0]), min_value=0, help='Número de veces que el jugador toca el balón en toda la temporada')
    controles = st.number_input('Controles', value=int(df['Controles'][0]), min_value=0, help='Veces que el jugador controló el balón en toda la temporada')
    dist_con_balon = st.number_input('Dist con balon', value=float(df['Dist con balon'][0]), min_value=0.0, help='Distancia total de los desplazamientos del jugador con balón en metros en toda la temporada')
    conducciones_ultimo_tercio = st.number_input('Conducciones ultimo tercio', value=int(df['Conducciones ultimo tercio'][0]), min_value=0, help='Conducciones que entran en el último tercio del campo en toda la temporada')
    valor_liga_ini = st.number_input('Beneficio liga ini', value=float(df['Valor liga ini'][0]), min_value=0.0, help='Beneficio de la liga en la que el jugador empieza la temporada, el beneficio se corresponde con el de la actual temporada. Las unidades están en millones de euros.')
    valor_liga_fin = st.number_input('Beneficio liga fin', value=float(df['Valor liga fin'][0]), min_value=0.0, help='Beneficio total de la liga en la que el jugador milita al final de temporada, es decir si ficha por un equipo de otra liga en verano es esa la liga que aparece, el beneficio se corresponde con el de la actual temporada. Las unidades están en millones de euros.')
    valor_equipo_ini = st.number_input('Valor equipo ini', value=float(df['Valor equipo ini'][0]), min_value=0.0, help='Valor del equipo por el que juega el jugador en la presente temporada, el valor es el de la temporada actual. Las unidades están en millones de euros.')
    valor_equipo_fin = st.number_input('Valor equipo fin', value=float(df['Valor equipo fin'][0]), min_value=0.0, help='Valor del equipo en el que jugará el jugador en la siguiente campaña, el valor es el de la presente temporada. Las unidades están en millones de euros.')
    defensa = st.checkbox('Defensa', value=df['Defensa'][0], help='Indica si el jugador es defensor')

    submit_button = st.form_submit_button(label='Aceptar')

# Update the DataFrame with the new values if form is submitted
metro2yarda = 1.094 # Para pasar los inputs de metros a yardas

if submit_button:
    if not nombre:
        st.error("El campo 'Nombre' no puede estar vacío.")
    else:
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
            "Dist con balon": [dist_con_balon*metro2yarda], 
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
