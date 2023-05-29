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
image = Image.open(r'C:\Users\breno\Desktop\TESTE_SRICPT\SCRIPT_CURVAS_FENOLOGICAS\Logo-Escuro.png')
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
tabela['CENA'] = tabela['system:index'].str[-1]
tabela = tabela.loc[tabela['CENA'] == '0']
tabela = tabela.drop(['system:index','CENA'], axis=1)
tabela = tabela.dropna()
tabela = tabela.drop_duplicates(subset='DATA')
tabela['NDVI'] = round(tabela['NDVI'],4)
tabela.head()
print(tabela)


# ##  Salvar Dataframe em Excel: 

# In[14]:


# DataFrame para Planilha Excel em xlsx

def to_excel(tabela):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    tabela.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

tabela_xls = to_excel(tabela)
st.download_button(label=' ⬇️ Download Planilha Arrumada', data=tabela_xls,file_name= 'Planilha_IVs.xlsx')


# ##  Calculo do Score: 

# In[15]:


ordered_dataframe = tabela.sort_values(by=["DATA"])
means_array = np.array(ordered_dataframe['NDVI'].array, dtype="float")
peak_vals = [means_array[peak] for peak in find_peaks(means_array)[0]]
valor_p90 = np.percentile(peak_vals, 90, method="midpoint")
valor_p90 = round(valor_p90,2)
print(valor_p90)


# In[16]:


st.metric(label="O valor do Score é:", value= valor_p90)


# In[ ]:



