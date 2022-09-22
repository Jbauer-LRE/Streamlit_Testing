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


df = pd.DataFrame(
   np.random.randn(50, 20),
   columns=('col %d' % i for i in range(20)))

st.dataframe(df)  # Same as st.write(df)

print (df)
