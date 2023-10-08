#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#sources
#https://www.educative.io/answers/how-to-use-curl-in-python
#https://pypi.org/project/sgp4/#:~:text=Project%20description%201%20Usage%20You%20will%20probably%20first,8%20Providing%20your%20own%20elements%20...%20More%20items


# In[ ]:


pip install sgp4 pycurl


# In[ ]:


from sgp4.api import accelerated
from sgp4.api import Satrec
import linecache
from io import StringIO    
import pycurl
from io import BytesIO
import tempfile 
import linecache
import csv


# In[ ]:


# Create a new cURL object
curl = pycurl.Curl()

# Set the URL to fetch
curl.setopt(curl.URL, 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle')

# Create a BytesIO object to store the response
buffer = BytesIO()
curl.setopt(curl.WRITEDATA, buffer)

# Perform the request
curl.perform()

# Get the response body
response = buffer.getvalue()


with open('tele_data.txt', 'w') as f:
    f.write(response.decode('utf-8'))

# Close the cURL object
curl.close()


# In[ ]:


with open( "tele_data.txt", 'r') as r, open( 'tele_data_updated.txt', 'w') as o: 
      
    for line in r: 
        #strip() function 
        if line.strip(): 
            o.write(line) 
  
f = open("tele_data_updated.txt", "r") 


# In[ ]:


with open('tele_data_updated.txt', 'r') as fp:
    lines = len(fp.readlines())
    


# In[ ]:


max_num_sats = int(lines/3)
print(max_num_sats)


# In[ ]:


def sat_name(sat_num):
        name_location = 1 + 3*(sat_num-1)
        name = linecache.getline('tele_data_updated.txt', name_location)
        name = name.strip()
        return name


# In[ ]:


def locate_tle(sat_num):
        name_location = 1 + 3*(sat_num-1)
        #print(name_location)
        s = linecache.getline('tele_data_updated.txt', name_location+1)
        t = linecache.getline('tele_data_updated.txt', name_location+2)
        s = s.strip()
        t = t.strip()
        return s, t


# In[ ]:


def sat_xyz(s,t):
    satellite = Satrec.twoline2rv(s, t)

    jd, fr = 2460224, 0.5
    e, r, v = satellite.sgp4(jd, fr)
    return r


# In[ ]:


with open('sat_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for x in range(1,max_num_sats):
        name = sat_name(x)
        s=locate_tle(x)[0]
        t=locate_tle(x)[1]
        x_pos, y_pos, z_pos = sat_xyz(s,t)
        writer.writerow([name, x_pos, y_pos, z_pos])
    file.close()

