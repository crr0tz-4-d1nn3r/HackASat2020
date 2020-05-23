import sys
import socket
import time
import re
from skyfield.api import EarthSatellite, Topos, load


# connection info
host = 'watch.satellitesabove.me'
port = 5011
ticket = b'ticket{uniform56510charlie:GFpuJLLrLf1wn23xNe5l5mFY3ZjVuptBXYLtIDZ9Dw4w20t62ePzl0sjF2vwqR2b3A}\n'

# regex for finding stuff
url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

# connect
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((host,port))

# ticket info
rec = socket.recv(1024)
r = rec.decode('ascii')
print(r)
socket.sendall(ticket)

# challenge info
time.sleep(1)
rec = socket.recv(32768)
r = rec.decode('ascii')
print(r)

# grab the tle and url info
lines = re.findall('(.*)\n', r)
line1 = lines[5]
line2 = lines[6]
url = re.findall(url_regex, lines[8])[0][0]


# set up sat object using tle
ts = load.timescale()
satellite = EarthSatellite(line1, line2, 'NAVSTAR 65 (USA 213)', ts)

# get position at given time - date time is in lines[1] but not worth parsing - not changing
t = ts.utc(2020,3,26,21,52,56)
geo = satellite.at(t)
pt = geo.subpoint()
lat = pt.latitude.degrees
lon = pt.longitude.degrees
elev = pt.elevation.m
head = 28.45  
## Heading is from subtracting two points - did it somewhere else, prob not correct
### these are earth centric coordinatees and we may need something else 

# need angle and distance from monument to sat
WashMon = Topos(latitude_degrees=38.8894838, longitude_degrees=-77.0352791, elevation_m=10)
difference = satellite - WashMon
topocentric = difference.at(t)
tilt, az, distance = topocentric.altaz()
tilt = 90 - tilt.degrees


print('url:' + url)
print('lat:' + str(lat))
print('lon:' + str(lon))
print('alt:' + str(elev))
print('head:' + str(head))
print('tilt:' + str(tilt))
print('range:' + str(distance.m))


# Read in the file
with open('example.kml', 'r') as file :
  filedata = file.read()

# Replace the target string
lonS = '<longitude>'+str(WashMon.longitude.degrees)+'</longitude>'
latS = '<latitude>'+str(WashMon.latitude.degrees)+'</latitude>'
altS = '<altitude>' + str(elev) +'</altitude>'
headS = '<heading>'+str(head)+'</heading>'
tiltS = '<tilt>'+str(tilt)+'</tilt>'
rangeS = '<range>'+str(distance.m)+'</range>'
hrefS = '<href>'+url+'</href>'

filedata = filedata.replace('<longitude>0</longitude>', lonS)
filedata = filedata.replace('<latitude>0</latitude>', latS)
filedata = filedata.replace('<altitude>0</altitude>', altS)
filedata = filedata.replace('<heading>0</heading>', headS)
filedata = filedata.replace('<tilt>0</tilt>',tiltS)
filedata = filedata.replace('<range>0</range>',rangeS)
filedata = filedata.replace('<href>http://FILL ME IN:FILL ME IN/cgi-bin/HSCKML.py</href>', hrefS)

# Write the file out again
with open('filled.kml', 'w') as file:
  file.write(filedata)


