# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 16:05:49 2022

@author: jbauer
"""

import streamlit as st
import pandas as pd
#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt


st.write ("hello joel")
st.write ("hi dave")

data= pd.read_csv('data.csv', index_col=0) 
