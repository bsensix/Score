#!/usr/bin/env python
# coding: utf-8

# ##  Bibliotecas:

# In[1]:


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
import base64


# ##  Barra Lateral: 

# In[2]:


#Barra Lateral
barra_lateral = st.sidebar.empty()
image = Image.open('Logo-Escuro.png')
st.sidebar.image(image)
st.sidebar.markdown('### Calculo Score Sentinel-2')
# Upload Arquivo csv 
uploaded_files = st.sidebar.file_uploader("Upload Planilha dados Sentinel 📥")


# ##  ETL no CSV: 

# In[4]:


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


tabela.head()


# ##  Salvar Dataframe em Excel: 

# In[5]:


def to_excel(tabela):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    tabela.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
   
    processed_data = output.getvalue()
    return processed_data

df = to_excel(tabela)
st.download_button(label=' ⬇️ Download Planilha IVs', data= df, file_name= 'Planilha_IVs.xls')

# In[ ]:


