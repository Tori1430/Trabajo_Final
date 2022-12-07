import streamlit as st
import pandas as pd
import numpy as np
import requests
import urllib.request
import os
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import pydeck as pdk

#####
#Título
st.title('Índices Soberanos 2010 - 2022')
st.image("https://diariocorreo.pe/resizer/Fc7YLo9pXk9ykDycNAg8OkQ58LE=/580x330/smart/filters:format(jpeg):quality(75)/cloudfront-us-east-1.images.arcpublishing.com/elcomercio/KXKXRKMB7NGKLE3ASDKUGPVDRI.jpg", width=600)

st.subheader("Miembros del equipo")
st.markdown("""
- Palacios Ninahuanca, Ninoska
- Orozco Chupos, Frank
- Quispe Laura, Jhorch
- Parillo Sanchez, Yassmin Diana
""")

@st.experimental_memo
def download_data(filename = 'data.csv'):
    url = 'https://cloud.minsa.gob.pe/s/8EsmTzyiqmaySxk/download'
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'whatever')
    filename, headers = opener.retrieve(url, filename)


    
@st.experimental_memo
def add_LatLong(df):
    mapeo = pd.read_excel('Tabla_Lat_Long.xlsx')
    data = df['dpt_cdc'].copy()
    Lat_Long = dict()
    for i, element  in enumerate(mapeo['Ciudad']):
        Lat_Long[element.lower()] = [mapeo['Latitud'][i], mapeo['Longitud'][i]]

    for i, element in enumerate(data):
        if element.lower() in Lat_Long.keys():
            data[i] = Lat_Long[element.lower()]
        else:
            print(element)

    Data = pd.DataFrame((i for i in data), columns =['lat', 'lon'])
    return pd.concat([df, Data], axis = 1)

def filtered_data(data, f_0, f_f):
    df = data.copy()
    df = df[(df['fecha_fallecimiento'] >= f_0) & (df['fecha_fallecimiento'] <= f_f)]
    return df

@st.experimental_memo
def chart(data, option):
    df = data.copy()
    if option == 'M':
        df = df[df['sexo'] == 'M']
    elif option == 'F':
        df = df[df['sexo'] == 'F']
    df = df[['lat', 'lon']]

    st.write('Número de fallecidos: ', df.shape[0])

    st.pydeck_chart(pdk.Deck(
        map_style= None,
        initial_view_state = pdk.ViewState(
            latitude=-12.046374,
            longitude=-77.042793,
            zoom=4,
            pitch=50,
        ),
        layers = [
            pdk.Layer(
                'HexagonLayer',
                data = df,
                get_position = '[lon, lat]',
                radius = 20*1e3,
                elevation_scale=500,
                elevation_range=[0, 5000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=20000,
            ),
        ],
    ))

def Distribuciones(data):
    df = data.copy()
    df_dep = df['dpt_cdc'].value_counts()
    df_male = df['dpt_cdc'][df['sexo'] == 'M'].value_counts()
    df_female = df['dpt_cdc'][df['sexo'] == 'F'].value_counts()
    df = pd.concat([df_male, df_female], axis = 1)
    df.columns = ['Hombres', 'Mujeres']
    print(df.head())

    st.bar_chart(df)
