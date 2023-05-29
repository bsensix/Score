#!/usr/bin/env python
# coding: utf-8

# ##  Bibliotecas:

# In[8]:


import argparse
import pandas as pd 
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline as ius
from scipy.signal import find_peaks
import xlsxwriter 
import streamlit as st
from PIL import Image
from io import BytesIO


# ##  Barra Lateral: 

# In[9]:


#Barra Lateral
barra_lateral = st.sidebar.empty()
image = Image.open('Logo-Escuro.png')
st.sidebar.image(image)
st.sidebar.markdown('### Calculo Score Sentinel-2')
# Upload Arquivo csv 
uploaded_files = st.sidebar.file_uploader("Upload Planilha dados Sentinel 📥")


# ##  ETL no CSV: 

# In[13]:


tabela = pd.read_csv(uploaded_files)
tabela_filtro = ['system:index','NDVI','Nome']
tabela= tabela[tabela_filtro]
tabela['DATA'] = tabela['system:index'].apply(lambda x: x[:8])
tabela['DATA'] = pd.to_datetime(tabela['DATA'], format='%Y%m%d').dt.strftime('%d/%m/%Y')
tabela = tabela.dropna()

tabela['NDVI'] = round(tabela['NDVI'],4)

tabela = tabela.groupby(['DATA','Nome'])['NDVI'].min().reset_index()
tabela['DATA'] = pd.to_datetime(tabela['DATA'], format='%d/%m/%Y')
tabela = tabela.sort_values('DATA')
ordem = ['DATA','Nome','NDVI']
tabela = tabela[ordem]
print(tabela)


# ##  Salvar Dataframe em Excel: 

# In[14]:


# DataFrame para Planilha Excel em xlsx

def to_excel(tabela):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(tabela):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(tabela)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download csv file</a>' # decode b'abc' => abc

df = tabela
st.markdown(get_table_download_link(df), unsafe_allow_html=True)


