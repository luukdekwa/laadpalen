import requests 
import pandas as pd 
import json
import numpy as np
import folium
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from urllib.request import urlopen
import json
import streamlit as st
import folium
from folium import plugins


laadpaal = pd.read_csv('laadpaaldata.csv',index_col=0)
laadpaal_2 = laadpaal
laadpaal_2['ChargeTime'] = np.where(laadpaal['ChargeTime'] > 10, 10, laadpaal['ChargeTime'])
laadpaal_2['ChargeTime'] = np.where(laadpaal['ChargeTime'] < 0, 0, laadpaal['ChargeTime'])
laadpaal_2['ChargeTime'] =laadpaal['ChargeTime'].round(0)
laadpaal_2['ChargeTime'] = laadpaal_2['ChargeTime'].astype(int)
laadpaal_2 = laadpaal_2.sort_values('ChargeTime').reset_index(drop=True)

#fig = plt.figure(figsize=(12,12))
#ax1 = fig.add_subplot(111)
#ax2 = ax1.twinx()
#laadpaal_2.plot(x='ChargeTime')
fig = px.histogram(laadpaal_2, x="ChargeTime")

fig.update_layout(
    title="Laad duur  ",
    xaxis_title="Aantal uur",
    yaxis_title="Aantal keer geladen")
fig.add_annotation(x=2.34, y=2962,
            text="Mediaan: 2,34 uur",
            showarrow=True,
            arrowhead=1)
fig.add_trace(go.Scatter(
    x=[2.34,2.34],
    y=[0,2962],
    mode="lines+text",
    name="Lines and Text",
    text=["", ""],
    textposition="bottom center"))

fig.show()
