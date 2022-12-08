import streamlit as st
import pandas as pd
import numpy as np
import datetime
from utilities import *

#####
#Título
st.title('Fallecidos, hospitalizados y vacunados por COVID-19')

st.image("https://imagenes.20minutos.es/files/image_656_370/uploads/imagenes/2021/03/06/uci.jpeg", width=600)
st.subheader("Miembros del equipo")
st.markdown("""
- Lorena Belen Cerda Rioja 
- Anel Schantal Ortiz Camargo
- Flor Estefany Chuchullo Mosqueta
- Victoria Justa Navarro Valdiviezo
- Licie Solainch Paredes Bedoya
""")
st.subheader("Contexto Nacional e Internacional")
st.markdown("La pandemia debida a enfermedad por coronavirus 2019 (COVID-19) ha producido más de 70 mil muertes en el mundo.")

#DATASET
st.subheader("Dataset")
st.markdown("Toma como referencia el universo de fallecidos por covid, toma como referencia el universo de fallecidos por covid y si han recibido dosis de vacunas covid") 
st.markdown("Los datos analizados en esta página fueron recuperados de la ´Plataforma Nacional de Datos Abiertos´ del Ministerio de Salud (MINSA)")
st.markdown("Última fecha de modificación: 22 de diciembre del 2021")
st.markdown("https://www.datosabiertos.gob.pe/dataset/fallecidos-hospitalizados-y-vacunados-por-covid-19")



# Creación del dataframe con los datos "preprocesados"
download_data('data.csv')
df = pd.read_csv('data.csv', encoding='utf-8')
seleccion = ['fecha_fallecimiento',
        'edad', 'sexo', 'criterio_fallecido',
        'dpt_cdc', 'cdc_positividad', 'flag_vacuna',
        'flag_hospitalizado', 'flag_uci', 'con_oxigeno',
        'con_ventilacion', 'evolucion_hosp_ultimo']

df = df[seleccion]
df['fecha_fallecimiento'] = pd.to_datetime(df['fecha_fallecimiento']).dt.date
df = add_LatLong(df)

# Sistema de filtros
set_dep = np.sort(df['dpt_cdc'].dropna().unique())
dep_opt = st.selectbox('Departamento', set_dep)
df_dep = df[df['dpt_cdc'] == dep_opt]
num_filas = df_dep.shape[0]
num_hosp = df_dep[df_dep['flag_hospitalizado'] == 1].shape[0]

st.write('Número de Fallecidos en el Departamento: ', num_filas)
st.write('Número de Hospitalizados: ', num_hosp)


f_0 = st.date_input("Indique una fecha inferior: ", datetime.date(2020, 1, 1))
f_f = st.date_input("Indique una fecha superior: ", datetime.date(2021, 1, 1))

data = filtered_data(df, f_0, f_f)
Distribuciones(data)
plot_Criterio(data)

option = st.selectbox('Seleccione el sexo', ('M', 'F', 'Both'))
chart(data, option)
