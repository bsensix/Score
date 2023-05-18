#!/usr/bin/env python
# coding: utf-8

# ##  Bibliotecas:

# In[74]:


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


# ##  Barra Lateral: 

# In[75]:


#Barra Lateral
barra_lateral = st.sidebar.empty()
image = Image.open('Logo-Escuro.png')
st.sidebar.image(image)
st.sidebar.markdown('### Calculo Score Sentinel-2')
# Upload Arquivo csv 
uploaded_files = st.sidebar.file_uploader("Upload Planilha dados Sentinel 📥")


# In[78]:


tabela = pd.read_excel(uploaded_files)
tabela_drop = tabela.drop_duplicates(subset='DATA')
tabela_drop.head()


# In[58]:


ordered_dataframe = tabela.sort_values(by=["DATA"])
means_array = np.array(ordered_dataframe['NDVI'].array, dtype="float")
peak_vals = [means_array[peak] for peak in find_peaks(means_array)[0]]
valor_p90 = np.percentile(peak_vals, 90, method="midpoint")
valor_p90 = round(valor_p90,4)
print(valor_p90)


# In[ ]:


st.metric(label="O valor do Score é:", value= valor_p90)


# In[ ]:




