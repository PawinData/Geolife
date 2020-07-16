import numpy as np
import re
import folium
from collections import deque
from geopy.distance import geodesic

# .plt files --> numpy arrays with binary entries
def get_plt(filename):
    raw = np.genfromtxt(filename, delimiter=",", skip_header=6, dtype=['f8,f8,i8,f8,f8,S10,S8'])
    data = np.array([list(thing[0]) for thing in raw])
    return data[:,[-2,-1,0,1]]
	


# input: date as a string
# output: the kth since 2007-01-01
calendar = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
def to_days(date):
    year = re.findall('^(20[0-9]+)-[0-9]+', date)
    year = int(year[0])
    month = re.findall('^20[0-9]+-([0-9]+)-', date)
    month = int(month[0])
    day = re.findall('^20[0-9]+-[0-9]+-([0-9]+)', date)
    day = int(day[0])
    count = 365*(year-2007) + day
    for m in range(1,month):
        count += calendar[m]
    if year==2008 and month>2:
        count += 1
    return count


# inputs: date as a string, timestamp as bytes
# output: the number of seconds since 2007-01-01 00:00:00
def to_time(date, timestamp):
    if not type(date)==str:
        date = date.decode()
    if not type(timestamp)==str:
        timestamp = timestamp.decode() # bytes --> string 
    hour = re.findall('([0-9]+):[0-9]+:[0-9]+', timestamp)
    hour = int(hour[0])
    minute = re.findall('[0-9]+:([0-9]+):[0-9]+', timestamp)
    minute = int(minute[0])
    second = re.findall('[0-9]+:[0-9]+:([0-9]+)', timestamp)
    second = int(second[0])
    total = 60*60*24*(to_days(date)-1) + 60*60*hour + 60*minute + second
    return total
    
    
  
  
# find the averages of a list of coordinates  
def centroid(list_of_coords):    
    lat = np.mean([a for a,b in list_of_coords])
    lng = np.mean([b for a,b in list_of_coords])
    return (lat,lng)
    


# compute auto-correlation function of time lags
def ACF(time_series):
    x = deque(time_series - np.mean(time_series))
    acf = [0] * len(time_series)
    for tau in range(len(acf)):
        y = x.copy()
        y.rotate(tau+1)
        acf[tau] = np.mean([u*v for u,v in zip(x,y)])  
    return acf
    
    
    
def draw_scope(Map, df, Message, Color):
    center = (np.mean(df.Latitude), np.mean(df.Longitude))
    folium.Circle(location = list(center),
                  radius = max([geodesic(center,(a,b)).meters for a,b in zip(df.Latitude,df.Longitude)]),
                  popup = Message, color = Color,
                  fill = True, fill_color = Color
                 ).add_to(Map)