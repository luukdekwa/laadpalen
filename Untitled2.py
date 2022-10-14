#!/usr/bin/env python
# coding: utf-8

# In[100]:


#pip install streamlit
#pip install streamlit-folium
import requests 
import pandas as pd 
import json
import numpy as np
import folium
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from urllib.request import urlopen
import json
import streamlit as st
import folium
from folium import plugins
import streamlit_folium as st_folium
from streamlit_folium import folium_static




# In[2]:
InputHoeveelheid = st.slider('Selecteer hoeveelheid data in te laden', min_value=100, max_value=5000, value=500, step=100)

key = '5bab249f-923c-4cef-88b5-6ddab219f0cd'
results = InputHoeveelheid


url = f'https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults={results}&compact=true&verbose=false?key={key}'


# In[3]:


response = requests.get(url=url)


# In[4]:


#response.status_code


# In[5]:


data = json.loads(response.text)


# In[6]:


#data


# In[7]:


df = pd.DataFrame(data)


# In[8]:


df.sort_values(by='ID')
#df


# In[9]:


adres_df = pd.DataFrame.from_records(df.AddressInfo.dropna().tolist())


# In[10]:


adres_df.sort_values(by='ID')


# In[11]:


#df_2 = pd.concat([df, adres_df], axis=1)
#df_2


# In[12]:


columns = ['AddressLine1', 
           'Town', 
           'StateOrProvince', 
           'Postcode',  
           'Latitude', 
           'Longitude', 
           'OperatorID', 
           'UsageCost', 
           'UsageTypeID', 
           'NumberOfPoints']

#df_2 = df_2[columns]


# In[13]:


#df_3 = df_2[['OperatorID', 'UsageCost', 'UsageTypeID']]

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#    print(df_3)


# In[14]:


df['UsageCost'].isna().sum()


# In[15]:


df_connections = pd.DataFrame.from_records(df.Connections.dropna().tolist())


# In[16]:


#df_connections


# In[17]:


df_connections_2 = pd.DataFrame.from_records(df_connections.iloc[:, 0].dropna().tolist())


# In[18]:


#df_connections_2


# In[19]:


df_connections_3 = pd.DataFrame.from_records(df_connections.iloc[:, 1].dropna().tolist())


# In[20]:


df_connections_3['PowerKW'].isna().sum()


# In[21]:


#df_connections_3


# In[22]:


df2 = pd.read_csv('postcodes_20190622_1.csv')
df3 = pd.read_csv('postcodes_20190622_2.csv')
df4 = pd.read_csv('postcodes_20190622_3.csv')
df5 = pd.read_csv('postcodes_20190622_4.csv')
df6 = pd.read_csv('postcodes_20190613.csv')


# In[23]:


#df2


# In[24]:


df_postcodes = pd.concat([df2,df3,df4,df5,df6])
#df_postcodes



# In[ ]:





# In[25]:


#adres_df['Provincie'] = adres_df.loc[adres_df['Postcode'] == df_postcodes['postal_code']]
df = pd.merge(adres_df, df_postcodes, how='left', left_on='Postcode',right_on='postal_code')

#df
#for Provincie in 
#adres_df


# In[26]:


df = df[['ID','Postcode','Latitude','Longitude','street','province']]
#df


# In[27]:


adres_df.info()


# In[28]:


#adres_df['Postcode'][0]
#adres_df['Postcode'] = adres_df['Postcode'].str.strip()
adres_df['Postcode'] = adres_df['Postcode'].str.replace(" ", "")
#adres_df


# In[29]:


adres_df['Postcode'] = adres_df['Postcode'].astype(str)
adres_df.info()
adres_df['Postcode'] = adres_df['Postcode'].replace(" ", "")


# In[30]:


#adres_df


# In[51]:


provincie = df_postcodes.loc[df_postcodes['postal_code'] == adres_df['Postcode'][0]]
provincie['province'].iloc[0]


# In[72]:


adres_df['Provincie'] = ""
adres_df['Stad'] = ""
for i in range(len(adres_df)):
    try:
        provincie = df_postcodes.loc[df_postcodes['postal_code'] == adres_df['Postcode'][i]]
        adres_df['Provincie'][i] = provincie['province'].iloc[0]
    except:
        adres_df['Provincie'][i] = np.nan
        
for i in range(len(adres_df)):
    try:
        provincie = df_postcodes.loc[df_postcodes['city'] == adres_df['Town'][i]]
        adres_df['Stad'][i] = provincie['province'].iloc[0]
    except:
        adres_df['Stad'][i] = np.nan
        
#adres_df


# In[53]:


adres_df['Provincie'].isna().sum()


# In[54]:


df = adres_df[['ID','Postcode','Latitude','Longitude','StateOrProvince']]
#df


# In[35]:


#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also    
#    print(adres_df)


# In[73]:


adres_df['Provincie'].fillna(adres_df['StateOrProvince'], inplace=True)
adres_df['Provincie'].fillna(adres_df['Stad'], inplace=True)
#adres_df


# In[74]:


adres_df['Provincie'].isna().sum()


# In[66]:


adres_df['Provincie'].isna()


# In[67]:


with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also    
    print(adres_df['Provincie'].isna())


# In[40]:


df_5 = pd.read_csv('laadpaaldata.csv')
#df_5


# In[41]:


#df_5.describe()


# In[42]:


#adres_df


# In[83]:


def add_categorical_legend(folium_map, title, colors, labels):
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))
    
    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """

    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map


# In[85]:


def color_producer(Provincie):
    if Provincie == 'Noord-Holland':
        return 'goldenrod'
    elif Provincie == 'Zuid-Holland':
        return 'lightsalmon'
    elif Provincie == 'Utrecht':
        return 'gray'
    elif Provincie == 'Noord-Brabant':
        return 'steelblue'
    elif Provincie == 'Gelderland':
        return 'rebeccapurple'
    elif Provincie == 'Overijssel':
        return 'orange'
    elif Provincie == 'Zeeland':
        return 'green'
    elif Provincie == 'Groningen':
        return 'purple'
    elif Provincie == 'Flevoland':
        return 'pink'
    elif Provincie == 'Friesland':
        return 'red'
    elif Provincie == 'Limburg':
        return 'yellow'
    elif Provincie == 'Drenthe':
        return 'olive'
    else:
        return 'green'


# In[ ]:





# In[68]:


#adres_df['Provincie'].value_counts()


# In[81]:
InputLand = st.sidebar.selectbox("Selecteer de Provincie", (['Noord-Holland','Zuid-Holland','Utrecht','Noord-Brabant','Gelderland','Overijssel','Zeeland','Groningen','Flevoland','Friesland','Limburg','Drenthe']))


adres_df1 = adres_df[adres_df['Provincie'] == InputLand]
#adres_df1








# In[97]:


m = folium.Map(location=[52.0893191, 5.1101691], zoom_start=7)



for index, meetpunt in adres_df1.iterrows():        
    location = [meetpunt['Latitude'], meetpunt['Longitude']]    
    popup = popup = '<strong>' + 'ID: '+ str(meetpunt['ID']) +' Adres: ' + str(meetpunt['AddressLine1']) + ' Stad: ' + str(meetpunt['Town']) + ' Provincie: ' + str(meetpunt['StateOrProvince']) + ' Postcode: '+ str(meetpunt['Postcode']) + '</strong>'
    color=color_producer(meetpunt.Provincie)
    marker = folium.CircleMarker(location = location, popup = popup, radius=5, color=color).add_to(m)

add_categorical_legend(m, 'Provincies',
                        colors = ['goldenrod', 'lightsalmon', 'gray', 'steelblue','rebeccapurple','orange','green','purple','pink','red','yellow','olive'],
                        labels = ['Noord-Holland', 'Zuid-Holland','Utrecht' ,'Noord-Brabant', 'Gelderland', 'Overijssel','Zeeland','Groningen','Flevoland','Friesland','Limburg','Drenthe'])
    
folium_static(m)

#'ID: '+row_values['ID']+' Adres: 'row_values['AddressLine1']+' Stad: '+row_values['Town'] + ' Provincie: '+row_values['StateOrProvince']+' Postcode: '+row_values['Postcode']


# In[ ]:





#GEDEELTE THOMAS
laadpaal = pd.read_csv('laadpaaldata.csv',index_col=0)
laadpaal_2 = laadpaal
laadpaal_2['ChargeTime'] = np.where(laadpaal['ChargeTime'] > 10, 10, laadpaal['ChargeTime'])
laadpaal_2['ChargeTime'] = np.where(laadpaal['ChargeTime'] < 0, 0, laadpaal['ChargeTime'])
laadpaal_2['ChargeTime'] =laadpaal['ChargeTime'].round(0)
laadpaal_2['ChargeTime'] = laadpaal_2['ChargeTime'].astype(int)
laadpaal_2 = laadpaal_2.sort_values('ChargeTime').reset_index(drop=True)



fig = px.histogram(laadpaal_2, x="ChargeTime")

fig.update_layout(
    title="Laad duur  ",
    xaxis_title="Aantal uur",
    yaxis_title="Aantal keer geladen",
    showlegend=False)
fig.add_annotation(x=2.34, y=2962,
            text="Mediaan: 2,34 uur",
            showarrow=True,
            arrowhead=1)
fig.add_trace(go.Scatter(
    x=[2.34,2.34],
    y=[0,2962],
    mode="lines+text",
    text=["", ""],
    textposition="bottom center"))

st.plotly_chart(fig)



#GEDEELTE LUUK
url = 'https://opendata.rdw.nl/resource/w4rt-e856.json'
url2 = 'https://opendata.rdw.nl/resource/8ys7-d773.json'

response = requests.get(url=url)
data = json.loads(response.text)

response2 = requests.get(url=url2)
data2 = json.loads(response2.text)

df_elek = pd.DataFrame(data)
df_brandstof = pd.DataFrame(data2)

#Te zwaar voor laptop, overigens kan dit niet worden ingeladen in github

#df_elek_2 = pd.read_csv('elektrischeVoertuigen.csv')
#df_brandstof_2 = pd.read_csv('Open_Data_RDW__Gekentekende_voertuigen_brandstof.csv')

auto_df = df_elek[['merk', 'catalogusprijs', 'bruto_bpm', 'datum_tenaamstelling']]

auto_df['jaar'] = auto_df['datum_tenaamstelling'].str[:-4]
auto_df = auto_df.sort_values('jaar')
auto_df['jaar'] = auto_df['jaar'].astype(float)
auto_df['jaar'] = auto_df['jaar'].astype(int)
auto_df['jaar'] = np.where(auto_df['jaar'] < 2010, 2010, auto_df['jaar'])
auto_per_jaar = auto_df['jaar'].value_counts().rename_axis('jaar').reset_index(name='counts')

auto_per_jaar = auto_per_jaar.sort_values('jaar')
auto_per_jaar['cum'] = auto_per_jaar['counts'].cumsum()

angle = np.rad2deg(np.arctan2(auto_per_jaar.loc[auto_per_jaar.index[-1], "counts"] - auto_per_jaar.loc[auto_per_jaar.index[0], "counts"],
                              auto_per_jaar.loc[auto_per_jaar.index[-1], "jaar"] - auto_per_jaar.loc[auto_per_jaar.index[0], "jaar"]))


fig, ax = plt.subplots()


ax.plot(auto_per_jaar['jaar'], auto_per_jaar['counts'], color='blue', marker='o')
plt.title('Hoeveelheid elektrische autos per jaar', fontsize=14)
plt.xlabel('Jaar', fontsize=14)
plt.ylabel('Elektrische autos', fontsize=14)
plt.grid(True)
plt.show()

st.pyplot(fig=fig)

fig, ax = plt.subplots()


ax.bar(auto_per_jaar['jaar'], auto_per_jaar['counts'], width = 0.4)
ax.plot(auto_per_jaar['jaar'] , auto_per_jaar['cum'], c='red')

bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
ax.text(2014, 950, 'Richting coefficient = ' + str(angle), ha="center", va="center", size=10,
        bbox=bbox_props)
plt.title('Hoeveelheid elektrische autos per jaar', fontsize=14)
plt.xlabel('Jaar', fontsize=14)
plt.ylabel('Elektrische autos', fontsize=14)
plt.show()
st.pyplot(fig=fig)


auto_per_jaar.loc[auto_per_jaar.index[-1], "counts"] - auto_per_jaar.loc[auto_per_jaar.index[0], "counts"]

auto_df['merk'].value_counts()

name_mapping = {'N.S.U.': 'VOLKSWAGEN',
               'SMART': 'MERCEDES-BENZ',
               'TESLA MOTORS': 'TESLA',
               'FORD-CNG-TECHNIK': 'FORD',
               'MICRO COMPACT CAR SMART': 'MERCEDES-BENZ',
               'ROVER': 'LAND-ROVER',
               'BMW I': 'BMW'}

auto_df['merk'] = auto_df['merk'].replace(name_mapping)
auto_per_merk = auto_df['merk'].value_counts().rename_axis('merk').reset_index(name='counts')
auto_per_merk = auto_per_merk.loc[auto_per_merk['counts'] > 10]

fig, ax = plt.subplots()

ax.bar(auto_per_merk['merk'], auto_per_merk['counts'])
plt.title("Hoeveelheid auto's per merk")
plt.xlabel("Merk")
plt.ylabel("Aantal")
plt.xticks(rotation=45)
plt.show()
st.pyplot(fig=fig)

autos_per_brandstof = df_brandstof['brandstof_omschrijving'].value_counts().rename_axis('brandstof').reset_index(name='counts')

autos_per_brandstof['cum'] = autos_per_brandstof['counts'].cumsum()

autos_per_brandstof.cum.iloc[-1]

fig, ax = plt.subplots()

percentage = []
 
for i in range(autos_per_brandstof.shape[0]):
    pct = (autos_per_brandstof.counts[i] / autos_per_brandstof.cum.iloc[-1]) * 100
    percentage.append(round(pct, 2))


# display percentage
print(percentage)
 
# display data
autos_per_brandstof['Percentage'] = percentage

ax.bar(autos_per_brandstof['brandstof'], autos_per_brandstof['Percentage'])
plt.title("Aantal auto's per brandstof")
plt.xlabel("Brandstof")
plt.ylabel("Aantal")
plt.xticks(rotation=45)
plt.show()
st.pyplot(fig=fig)