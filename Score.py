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
import io
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


# buffer to use for excel writer
buffer = io.BytesIO()

with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Write each dataframe to a different worksheet.
    tabela.to_excel(writer, sheet_name='Sheet1', index=False)
    # Close the Pandas Excel writer and output the Excel file to the buffer
    writer.save()
    
st.download_button(label=' ⬇️ Download Planilha IVs',
    data=buffer,
    file_name='large_df.xlsx',
    mime='application/vnd.ms-excel'
    )

# In[ ]:


