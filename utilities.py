import streamlit as st
import pandas as pd
import numpy as np
import requests
import urllib.request
import os
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import pydeck as pdk

@st.experimental_memo
def download_data(filename = 'data.csv'):
    url = 'https://cloud.minsa.gob.pe/s/8EsmTzyiqmaySxk/download'
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'whatever')
    filename, headers = opener.retrieve(url, filename)


