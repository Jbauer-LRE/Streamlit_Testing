#### imports
import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")

import os
from flopy.utils.zonbud import ZoneBudget
import numpy as np
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder




import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.cla()


st.write("Program active")


##################set up program and define inputs

## bring in gmd file
gmds=pd.read_csv("Model_Grid_RCL_GMDs.csv")
##count by each gmd
counts=(gmds['DisName'].value_counts())

countsx=(gmds.groupby('DisName')['Sort'].nunique())
countsx=pd.DataFrame(countsx)
countsx=countsx.reset_index()
countsx=countsx.rename(columns={"Sort": "number", })

#st.write((countsx))

    
## pumping/change file

st.write("Reading in blank input sheet")
q_df_in=pd.read_csv("InputSheet.csv")
q_df_in=q_df_in[0:120]
q_df_in.Month=datetime_series = pd.Series( pd.date_range("2013-01-01", periods=120, freq="M"))



with st.form('example form') as f:
    st.header('INPUT SHEET')
    response = AgGrid(q_df_in, editable=True, fit_columns_on_grid_load=True)
    st.form_submit_button()
    
q_df_in.Month=datetime_series = pd.Series( pd.date_range("2013-01-01", periods=120, freq="M"))


#st.write("hard check on what your inputs were:")
#st.write(response['data'])

q_df=response['data']

st.cache(allow_output_mutation=True)
# st.write("simple input")

q_df_x=pd.melt(q_df,id_vars=['Sp',  'Yr', 'Len', 'TS', 'One', 'Tr',   'Month'],value_vars=['Aberdeen-American Falls','Big Lost River','Bingham','Bonneville-Jefferson','Carey Valley', 'Henrys Fork',  'Jefferson', 'Madison', 'Magic Valley',  'North Snake',  'Raft River', ])
q_df_x = q_df.rename(columns={'variable': 'DisName'})

# #make well file
# #format=layer,row,column,q_yr



## write modflow well file

st.write("Constructing well file, currently configured not to account for any pumping after March 2023")
with open('well_slate.txt', 'w') as f:
    ## beginning junk
    f.writelines(str('      8386        50 '))
    f.writelines('\n')

    ## for each stress period
    for sp in range(0,120):  ### 6= number of stress periods
        print ("sp"+str(sp))
        
        ###write first line of well file
        
        #f.write(str('      8386        0')+    ("   #sp"+str(sp)))
        #f.write('\n')
        
        
        ##construct well file
        
        gmd_q=gmds
        gmd_q=gmd_q.merge(countsx)
        gmd_q['TS']=sp+1
        #q_df1=q_df[::600+sp]
        q_df_x=pd.melt(q_df.iloc[[sp]],id_vars=['Sp',  'Yr', 'Len', 'TS', 'One', 'Tr',   'Month'],value_vars=['Aberdeen-American Falls','Big Lost River','Bingham','Bonneville-Jefferson','Carey Valley', 'Henrys Fork',  'Jefferson', 'Madison', 'Magic Valley',  'North Snake',  'Raft River'])
        q_df_x = q_df_x.rename(columns={'variable': 'DisName'})
        gmd_q1=pd.merge(gmd_q,q_df_x,  on ='DisName',             how ='inner')
        gmd_q1['layer']=1
        gmd_q1.value=-gmd_q1.value/gmd_q1.number
        gmd_q1.value=gmd_q1.value/gmd_q1.Len
        
        if gmd_q1.value.sum()==0:
            f.writelines(str('      0       0 '))
            print ("tesx1")
            f.writelines('\n')
            
        else:
            chunk= gmd_q1[["layer","ROW_ID", "COL_ID","value", "Month"]]
            f.writelines(str('      8386        0 '))
            f.writelines('\n')
            print ("x")
            chunk.to_csv(f,index=False,header=False, sep=" ", lineterminator='\n' )

        
st.write("... Modflow Well File Creation Complete")
        

        
############ old code for running district-by-district
        
# # #         # for ind in gmds.index[0:8386]:
# # #         #     #print(str(1),gmds['ROW_ID'][ind],gmds['COL_ID'][ind],str("#"),gmds['DisName__1'][ind])
# # #         #     dist=gmds['DisName__1'][ind]
# # #         #     y=q_df[dist].iloc[sp]
# # #         #     toprint=(1,gmds['ROW_ID'][ind],gmds['COL_ID'][ind],(y),'#',gmds['DisName__1'][ind])
        
        
# # #         #     line = (' '.join(str(x) for x in toprint))
# # #         #     f.writelines(str(line))
# # # #         #     f.writelines('\n')

# # ##  Run Modflow
st.write("Running MODFLOW. This may take a few a couple minutes")

exe = "mfusg.exe "
mf_nam =  "GMD_eval.nam"


# ###
os.system( exe + mf_nam)  #uncomment to make modflow run


##important note- this is run with an output control file (OCL) that has been modified to spit out the results for ALL time steps within ALL stress periods


st.write("Computing budget for each reach")
###read in the zones file
zones=np.loadtxt("zone_array.txt")
zones = zones.astype(int)


##run zonebudget
zb = ZoneBudget('Conservation.bud', zones )

##record all results
zb.to_csv('zonebudtest.csv')

zb_df=pd.read_csv('zonebudtest.csv')

###slice dataframe to get the "RIVER_LEAKAGE_IN" values because we are using pumping, which is negative and pulls water IN from the river (out of the river heheh)
riv_df=zb_df.iloc[3::28, :]
riv_df['time_increment']=riv_df.totim.diff(periods=1)
riv_df.time_increment.iloc[0]=15

riv_df[['ZONE_1','ZONE_2','ZONE_3','ZONE_4','ZONE_5','ZONE_6','ZONE_7']]=riv_df[['ZONE_1','ZONE_2','ZONE_3','ZONE_4','ZONE_5','ZONE_6','ZONE_7']].multiply(riv_df["time_increment"], axis="index",)
riv_df.to_csv("riv_df.csv")
# # ##results for just the zone 4 dataframe
#riv_df=riv_df[['totim','time_increment','time_step','stress_period','ZONE_4']]

# riv_df4['Z4_riv_vol']=riv_df4.time_increment*riv_df4.ZONE_4
# ### no need to conver to AF riv_df4['Z4_riv_vol_af']=riv_df4.Z4_riv_vol


# ###sum for each STRESS PERIOD
agg=pd.pivot_table(riv_df,index='stress_period',values=['ZONE_1','ZONE_2','ZONE_3','ZONE_4','ZONE_5','ZONE_6','ZONE_7'],aggfunc=np.sum)
agg= pd.DataFrame(agg.to_records())

agg.columns=['SP','All_Other','Milner_to_King_Hill_Downstream','Neeley_Minidoka','nr_Blackfoot_Neeley','Shelley_nr_Blackfoot','Heise_Shelley','Ashton_Rexburg', ]


# # ##save aggregated af file
agg.to_csv("aggregated_AllZones"+".csv")


# # on to the next district
# (q_df[str(gmd)])=0

st.write("Run Complete")
st.write("Note that General Head Boundary Cells are not included")

agg['Calendar_Mo']= q_df['Month']
st.write(agg)

print ("hello!")


fig, ax = plt.subplots(figsize=(10,4),tight_layout=True)
ax.scatter(agg.Calendar_Mo,agg.nr_Blackfoot_Neeley)
ax.set_xlabel("Month",fontsize=12)
ax.set_ylabel("Accretions (af)",fontsize=12)

ax.set_ylim(0,agg.nr_Blackfoot_Neeley.max()+10)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.xaxis.set_minor_locator(mdates.MonthLocator())

ax.set_title("Accretions to the Nr Blackfoot to Neeley Reach",fontsize=12)
ax.grid()

st.pyplot(fig)


plt.show()
plt.cla()






#st.bar_chart()
# ###if you need to look at the list file- this code does it
# mf_list = fp.utils.MfListBudget("NewOUT.lst")
# incremental, cumulative = mf_list.get_budget()
# df_inc, df_cumulative = mf_list.get_dataframes()

