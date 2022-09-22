"""
Created on Fri Aug 26 16:05:49 2022

@author: jbauer
"""

import streamlit as st
import pandas as pd
import numpy as np
#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt


st.write ("hello joel")
st.write ("hi dave")





#####

# bal_df=st.dataframe(pd.DataFrame({
#     'GMD': ["American Falls- Aberdeen","Bingham","Bonneville-Jefferson","Jefferson-Clark"],
#     'Balance': [1000, 0, 500, 10]
# }))


# urf_df=st.dataframe(pd.DataFrame({
#     'GMD': ["American Falls- Aberdeen","Bingham","Bonneville-Jefferson","Jefferson-Clark"],
#     'URF': [10, 60, 20, 10]
# }))



bal_df=(pd.DataFrame({
     'GMD': ["American Falls- Aberdeen","Bingham","Bonneville-Jefferson","Jefferson-Clark"],
     'Balance1': [1000, 0, 500, 10],
     'Balance2': [1000, 0, 500, 10],
     'Balance3': [0, 100, 500, 10],
     'Balance4': [0, 0, 500, 10],
     'Balance5': [1000, 0, 500, 10],
     'Balance6': [50, 0, 500, 10],
     'Balance7': [50, 0, 500, 10],
     'Balance8': [50, 0, 500, 10],


 }))
st.write(bal_df)
bal_df=bal_df.T
bal_arr=np.array(bal_df.iloc[1:9])



urf_df=(pd.DataFrame({
    'GMD': ["American Falls- Aberdeen","Bingham","Bonneville-Jefferson","Jefferson-Clark"],
    'URF1': [10, 0, 0, 10,],
    'URF2': [60 ,10, 0, 10],
    'URF3': [20, 20, 10, 10],
    'URF4': [10, 60, 50, 10],
    'URF5': [0,  10, 10, 30,],
    'URF6': [0,   0, 10, 10],
    'URF7': [0,  0, 10, 10],
    'URF8': [0, 0, 10, 10],
       
}))
stf.write(urf_df)

urf_arr=urf_df.iloc[0:10,1:9]
urf_arr=np.array(urf_arr)

result=bal_arr*urf_arr.T
result=pd.DataFrame(result)
st.dataframe(result)

# # reaches=["Milner to King Hill","Neeley-Minidoka","nr Blackfoot-Neeley","shelly-nr Blackfoot","Heise-Shelly","Ashton-Rexburg"]


st.markdown("## Party time!")
st.write("Yay! You're done with this tutorial of Streamlit. Click below to celebrate.")
btn = st.button("Celebrate!")
if btn:
    st.balloons()
