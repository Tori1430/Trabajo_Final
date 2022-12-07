import streamlit as st
import pandas as pd
import numpy as np
import datetime
from utilities import *

#####
#Título
st.title('FALLECIDOS Y HOSPITALIZADOS DE COVID')
st.image("https://imagenes.20minutos.es/files/image_656_370/uploads/imagenes/2021/03/06/uci.jpeg", width=600)

st.subheader("Miembros del equipo")
st.markdown("""
- Lorena Cerda Rioja 
- Anel 
- Flor
- Victoria
- Licie Solainch Paredes Bedoya
""")

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

st.write('Número de fallecidos en el departamento: ', num_filas)

f_0 = st.date_input("Indique una fecha inferior: ", datetime.date(2020, 1, 1))
f_f = st.date_input("Indique una fecha superior: ", datetime.date(2021, 1, 1))
option = st.selectbox('Seleccione el sexo', ('M', 'F', 'Both'))

data = filtered_data(df, f_0, f_f)

chart(data, option)
Distribuciones(data)
