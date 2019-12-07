#!/usr/bin/env python
# coding: utf-8

# # WeatherPy
# ----

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import requests
import time

# Import API key
from api_keys import api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_df = "cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)


# ## Generate Cities List

# In[2]:


# Create your list for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for every_element in lat_lngs:
    city = citipy.nearest_city(every_element[0], every_element[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)


# In[3]:


#code verification it worked correctly
len(lats)


# In[4]:


#lats
#lngs
lat_lngs


# In[5]:


#cities


# ### Perform API Calls
# * Perform a weather check on each city using a series of successive API calls.
# * Include a print log of each city as it'sbeing processed (with the city number and city name).
# 

# In[6]:


#for i, city in enumerate(cities):
    #print(i, cities)


# In[7]:


#initial URL we will create our final city list from
url = "https://api.openweathermap.org/data/2.5/weather?units=Imperial&APPID=" + api_key
#?q=London,uk&appid=YOUR_API_KEY
city_data = []

#perform their desired print to logger
print("Beginning Data Retrieval")
print("--------------------------")

record_count = 1
set_count =1

for i, city in enumerate(cities):
    if(i % 50 == 0 and i >=50):
        set_count  = set_count + 1
        record_count = 0 
        
    city_url= url + "&q="+city
    
    print("Processing Record"+str(record_count) + "of Set" + str(set_count)+ "|" + city)
    #print(f"Processing Record {record_count} of set {set_count}|{city}")      
    print (city_url)
   
    try:
        city_weather = requests.get(city_url).json()
        #retrieving the data and parsing the json
        #parse out the data you need from the JSON
        city_latitude = city_weather['coord']['lat']
        city_long = city_weather['coord']['lon']
        city_tempMax = city_weather['main']['temp_max']
        city_wind = city_weather['wind']['speed']
        city_humidity = city_weather['main']['humidity']
        city_date = city_weather['dt']
        city_country = city_weather['sys']['country']
        city_cloudiness = city_weather['clouds']['all']
          
        city_data.append({"City": city,
                    "Cloudiness": city_cloudiness,
                      "Country": city_country,
                      "Date" : city_date  ,
                      "Humidity": city_humidity ,
                      "Lat": city_latitude,
                      "Longitude": city_long ,
                      "Max Temp": city_tempMax ,
                      "Wind Speed (mph)": city_wind}
                        )
    except:
        print("City not found. Skipping...")
        pass

#Show your data loading is complete
print("-----------------------")
print("Data Retrieval Complete")
print("-----------------------")
          
    


# In[8]:


#let it begin! convert the json to a panda df and preview
city_data_pd= pd.DataFrame(city_data)
city_data_pd.head()


# In[9]:


#reorganize columns into a meaningful order
city_data_pd = city_data_pd[["City","Country","Date","Lat","Max Temp","Humidity",
                             "Cloudiness","Wind Speed (mph)"]]
#city_data_pd.head()


# ### Convert Raw Data to DataFrame
# * Export the city data into a .csv.
# * Display the DataFrame

# In[10]:


#Check record count
city_data_pd.count()


# In[11]:


#display final df
city_data_pd.head()


# In[12]:


#export to csv
city_data_pd.to_csv(output_df, index_label="city_ID")


# In[13]:


#extract data for plots
lats= city_data_pd['Lat']
temp= city_data_pd['Max Temp']
humidity= city_data_pd['Humidity']
cloudiness= city_data_pd['Cloudiness']
wind= city_data_pd['Wind Speed (mph)']


# ### Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.

# #### Latitude vs. Temperature Plot

# In[47]:


#Building mpl scatter plot for Lat v Temp
plt.scatter(lats, temp, c=temp, cmap="Reds", alpha=0.8)

#other graph properties
plt.title(f"City Latitide vs. Max Temperature ({time.strftime('%x')})")
plt.grid(True)
plt.xlabel("Latitude")
plt.ylabel("Max Temp (°F)")
plt.savefig("LatvTemp.png")
plt.show()


# #### Latitude vs. Humidity Plot

# In[34]:


#Building mpl scatter plot for Lat v Humidity
plt.scatter(lats, humidity, c=humidity, cmap="viridis")

#other graph properties
plt.title(f"City Latitide vs. Humidity ({time.strftime('%x')})")
plt.grid(True)
plt.xlabel("Latitude")
plt.ylabel("Humidity (%)")
plt.savefig("LatvHumid.png")
plt.show()


# #### Latitude vs. Cloudiness Plot

# In[39]:


#Building mpl scatter plot for Lat v Cloudiness
plt.scatter(lats, cloudiness, c=cloudiness, cmap="winter")

#other graph properties
plt.title(f"City Latitide vs. Cloudiness ({time.strftime('%x')})")
plt.grid(True)
plt.xlabel("Latitude")
plt.ylabel("Cloudiness (%)")
plt.savefig("LatvCloudiness.png")
plt.show()


# #### Latitude vs. Wind Speed Plot

# In[42]:


#Building mpl scatter plot for Lat v Wind Speed
plt.scatter(lats, wind, c=wind, cmap="jet")

#other graph properties
plt.title(f"City Latitide vs. Wind Speed(mph) ({time.strftime('%x')})")
plt.grid(True)
plt.xlabel("Latitude")
plt.ylabel("Wind Speed (mph)")
plt.savefig("LatvWind.png")
plt.show()


# ####Observations:
# 1: Temperatures do seem to be higher within 20 degrees of the the equator. 
# 2: There does not seem to be a direct coorelation between lattitude and cloudiness or humidity.
# 3: Although there doesn't seem to be a coorelation of wind speed getting closer to the equator, there does appear to be a drastic increase of windspeeds the farther you go from the middle latitudes. 
# 
