import re
import socket
import time
from astropy.time import Time
from astropy.coordinates import TEME, ITRS, CartesianDifferential, CartesianRepresentation, EarthLocation, AltAz, Angle
from astropy import units as u
from sgp4.api import Satrec
from sgp4.api import SGP4_ERRORS

def MakeKML(FileName, Lat, Lon, Alt, Hdg, Tilt, Range, url):
	with open(FileName, "w") as f:
		print('<?xml version="1.0" encoding="UTF-8"?>', file=f)
		print('<kml xmlns="http://www.opengis.net/kml/2.2">', file=f)
		print('  <Folder>', file=f)
		print('    <name>HackASatCompetition</name>', file=f)
		print('    <visibility>1</visibility>', file=f)
		print('    <open>1</open>', file=f)
		print('    <description>HackASatComp1</description>', file=f)
		print('    <NetworkLink>', file=f)
		print('      <name>View Centered Placemark</name>', file=f)
		print('      <visibility>1</visibility>', file=f)
		print('      <open>1</open>', file=f)
		print('      <description>This is where the satellite was located when we saw it.</description>', file=f)
		print('      <refreshVisibility>1</refreshVisibility>', file=f)
		print('      <flyToView>0</flyToView>', file=f)
		print('      <LookAt id="ID">', file=f)
		print('        <!-- specific to LookAt -->', file=f)
		print('        <longitude>', Lon, '</longitude>', file=f)
		print('        <latitude>', Lat, '</latitude>', file=f)
		print('        <altitude>', Alt, '</altitude>', file=f)
		print('        <heading>', Hdg, '</heading>', file=f)
		print('        <tilt>', Tilt, '</tilt>', file=f)
		print('        <range>', Range, '</range>', file=f)
		print('        <altitudeMode>clampToGround</altitudeMode>', file=f)
		print('      </LookAt>', file=f)
		print('      <Link>', file=f)
		print('        <href>', url, '</href>', file=f)
		print('        <refreshInterval>1</refreshInterval>', file=f)
		print('        <viewRefreshMode>onStop</viewRefreshMode>', file=f)
		print('        <viewRefreshTime>1</viewRefreshTime>', file=f)
		print('        <viewFormat>BBOX=[bboxWest],[bboxSouth],[bboxEast],[bboxNorth];CAMERA=[lookatLon],[lookatLat],[lookatRange],[lookatTilt],[lookatHeading];VIEW=[horizFov],[vertFov],[horizPixels],[vertPixels],[terrainEnabled]</viewFormat>', file=f)
		print('      </Link>', file=f)
		print('    </NetworkLink>', file=f)
		print('  </Folder>', file=f)
		print('</kml>', file=f)
	return 0

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
socket.sendall(ticket)

# challenge info
time.sleep(1)
rec = socket.recv(32768)
r = rec.decode('ascii')

# grab the tle and url info
lines = re.findall('(.*)\n', r)
s = lines[5]
t = lines[6]
url = re.findall(url_regex, lines[8])[0][0]

satellite = Satrec.twoline2rv(s, t)

# Epoch March 26th, 2020, at 21:52:56
t = Time('2020-03-26T21:52:56.0', format='isot', scale='utc')
error_code, teme_p, teme_v = satellite.sgp4(t.jd1, t.jd2)  # in km and km/s

if error_code != 0:
	raise RuntimeError(SGP4_ERRORS[error_code])

# Convert SGP4 TEME to Astropy native TEME
teme_p = CartesianRepresentation(teme_p*u.km)
teme_v = CartesianDifferential(teme_v*u.km/u.s)
teme = TEME(teme_p.with_differentials(teme_v), obstime=t)

'''
itrs = teme.transform_to(ITRS(obstime=t))  
location = itrs.earth_location  
print(location.geodetic)
'''

# Lat/Lon/Alt of the Washington Monumnet
monumentLat = 38.889484
monumentLon = -77.035278
monumnetAlt = 169			# meters

# get the locations into similar coordinate system objects
#satellilteEarthLocation = ?.from_geocentric(xSat,ySat,zSat)
monumentEarthLocation = EarthLocation.from_geodetic(monumentLon,monumentLat,monumnetAlt)

aa = teme.transform_to(AltAz(obstime=t, location=monumentEarthLocation))
print('Altitude: ', aa.alt.degree)
print('Azimuth: ', aa.az.degree)

# Range is hyp of ground distance and sat geodetic altitude-monument altitude

# file, lat, lon, alt, heading, tilt, range, url
MakeKML('outFile.kml', monumentLat, monumentLon, monumnetAlt, aa.az.degree-180.0, 90.0-aa.alt.degree, 609374.8, url)
